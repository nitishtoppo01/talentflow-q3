"""Prove the pull is complete. Reads only what is on disk - never calls the API."""
import csv
import json
import pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "data" / "raw"
LOG_PATH = ROOT / "data" / "pull_log.csv"
MANIFEST_PATH = ROOT / "data" / "manifest.json"
OUT_PATH = ROOT / "out" / "pull_verification.md"


def slug(table):
    return table.lower().replace(" ", "_")


def main():
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    rows = list(csv.DictReader(LOG_PATH.open(encoding="utf-8")))

    lines = ["# Pull verification", ""]
    lines.append("Pulled at (UTC): {}".format(manifest["pulled_at_utc"]))
    lines.append("")
    lines.append(
        "| Table | Records in file | Pages (200s) | Log sum = file count | "
        "Final page had offset | IDs unique | 429s | 429s retried |"
    )
    lines.append("|---|---|---|---|---|---|---|---|")

    all_ok = True
    for table in manifest["tables"]:
        records = json.loads((RAW_DIR / "{}.json".format(slug(table))).read_text(encoding="utf-8"))
        table_rows = [r for r in rows if r["table"] == table]
        ok_rows = [r for r in table_rows if r["http_status"] == "200"]
        throttled = [r for r in table_rows if r["http_status"] == "429"]

        log_sum = sum(int(r["records"]) for r in ok_rows)
        final_offset = ok_rows[-1]["had_offset"] if ok_rows else "?"
        ids = [r["id"] for r in records]
        dupes = [i for i, n in Counter(ids).items() if n > 1]

        # Every 429 must be followed by another attempt at the same page.
        retried = all(
            any(
                o["page"] == t["page"] and table_rows.index(o) > table_rows.index(t)
                for o in table_rows
            )
            for t in throttled
        )

        checks = (
            log_sum == len(records)
            and final_offset == "no"
            and not dupes
            and (retried or not throttled)
        )
        all_ok = all_ok and checks
        lines.append(
            "| {} | {} | {} | {} | {} | {} | {} | {} |".format(
                table,
                len(records),
                len(ok_rows),
                "PASS" if log_sum == len(records) else "FAIL ({})".format(log_sum),
                "FAIL" if final_offset != "no" else "no - PASS",
                "PASS" if not dupes else "FAIL ({} dupes)".format(len(dupes)),
                len(throttled),
                "n/a" if not throttled else ("PASS" if retried else "FAIL"),
            )
        )

    lines.append("")
    lines.append("Overall: {}".format("PASS" if all_ok else "FAIL"))
    lines.append("")
    lines.append("Totals: {} records, {} requests, {} retries.".format(
        manifest["totals"]["records"],
        manifest["totals"]["requests"],
        manifest["totals"]["retries_429"],
    ))
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
