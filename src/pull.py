"""Pull all 8 Acme Airtable tables into data/raw/. See CLAUDE.md for the rules."""
import csv
import json
import os
import pathlib
import sys
import time
import urllib.parse
from datetime import datetime, timezone

import requests

BASE_ID = "appYePRAI75PMbQNQ"
TABLES = [
    "Departments",
    "People",
    "Job Openings",
    "Candidates",
    "Applications",
    "Interviews",
    "Offers",
    "Findings",
]
PAGE_SIZE = 100
MIN_INTERVAL = 0.25   # <= 4 requests/second
RETRY_WAIT = 35       # seconds to wait on HTTP 429
MAX_ATTEMPTS = 5

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
LOG_PATH = ROOT / "data" / "pull_log.csv"
MANIFEST_PATH = ROOT / "data" / "manifest.json"


def read_token():
    """Read AIRTABLE_TOKEN from .env. The value is never printed or logged."""
    env_path = ROOT / ".env"
    if not env_path.exists():
        sys.exit("ERROR: .env not found. Create it with AIRTABLE_TOKEN=<key>.")
    for line in env_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("AIRTABLE_TOKEN="):
            token = line.split("=", 1)[1].strip()
            if token:
                return token
    sys.exit("ERROR: AIRTABLE_TOKEN not set in .env.")


def slug(table):
    return table.lower().replace(" ", "_")


class Throttle:
    """Gate on request START times so a slow call cannot push us over 4/s."""

    def __init__(self, min_interval):
        self.min_interval = min_interval
        self.last_start = None

    def wait(self):
        if self.last_start is not None:
            elapsed = time.monotonic() - self.last_start
            if elapsed < self.min_interval:
                time.sleep(self.min_interval - elapsed)
        self.last_start = time.monotonic()


def pull_table(table, session, throttle, log_writer):
    """Fetch every page of one table. Returns (records, pages, requests, retries)."""
    url = "https://api.airtable.com/v0/{}/{}".format(
        BASE_ID, urllib.parse.quote(table, safe="")
    )
    records, offset, page = [], None, 0
    requests_made = retries = 0
    seen_offsets = set()

    while True:
        page += 1
        params = {"pageSize": PAGE_SIZE}
        if offset:
            params["offset"] = offset

        for attempt in range(1, MAX_ATTEMPTS + 1):
            throttle.wait()
            resp = session.get(url, params=params, timeout=30)
            requests_made += 1

            if resp.status_code == 429:
                # Log the throttled attempt, then wait and retry the same page.
                log_writer.writerow([table, page, 429, 0, ""])
                retries += 1
                if attempt == MAX_ATTEMPTS:
                    sys.exit(
                        "ERROR: {} page {} still 429 after {} attempts.".format(
                            table, page, MAX_ATTEMPTS
                        )
                    )
                time.sleep(RETRY_WAIT)
                continue

            if resp.status_code in (401, 403):
                sys.exit(
                    "ERROR: HTTP {} on {} - check the token in .env.".format(
                        resp.status_code, table
                    )
                )
            if resp.status_code != 200:
                sys.exit(
                    "ERROR: HTTP {} on {} page {}: {}".format(
                        resp.status_code, table, page, resp.text[:200]
                    )
                )
            break

        payload = resp.json()
        page_records = payload.get("records", [])
        records.extend(page_records)
        offset = payload.get("offset")
        log_writer.writerow(
            [table, page, 200, len(page_records), "yes" if offset else "no"]
        )

        if not offset:
            break
        if offset in seen_offsets:
            sys.exit("ERROR: {} returned a repeated offset - aborting.".format(table))
        seen_offsets.add(offset)

    return records, page, requests_made, retries


def main():
    token = read_token()
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"Authorization": "Bearer {}".format(token)})
    throttle = Throttle(MIN_INTERVAL)

    manifest = {
        "pulled_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "base_id": BASE_ID,
        "tables": {},
        "totals": {},
    }

    with open(LOG_PATH, "w", newline="", encoding="utf-8") as fh:
        log_writer = csv.writer(fh)
        log_writer.writerow(["table", "page", "http_status", "records", "had_offset"])

        for table in TABLES:
            records, pages, requests_made, retries = pull_table(
                table, session, throttle, log_writer
            )
            out_path = RAW_DIR / "{}.json".format(slug(table))
            out_path.write_text(
                json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8"
            )
            manifest["tables"][table] = {
                "file": "data/raw/{}.json".format(slug(table)),
                "record_count": len(records),
                "pages": pages,
                "requests": requests_made,
                "retries_429": retries,
            }
            print(
                "{:<14} {:>5} records  {:>2} pages  {:>2} requests  {} retries".format(
                    table, len(records), pages, requests_made, retries
                )
            )

    manifest["totals"] = {
        "records": sum(t["record_count"] for t in manifest["tables"].values()),
        "requests": sum(t["requests"] for t in manifest["tables"].values()),
        "retries_429": sum(t["retries_429"] for t in manifest["tables"].values()),
    }
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("\nWrote {} and {}".format(MANIFEST_PATH.name, LOG_PATH.name))


if __name__ == "__main__":
    main()
