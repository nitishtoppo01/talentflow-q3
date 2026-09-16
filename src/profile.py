"""Profile every table -> out/profile.md. Reads data/raw/ only."""
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone

from common import OUT, TABLES, field_union, load_all, type_name

# Treat a field as categorical if it is all strings and has few distinct values.
CATEGORICAL_MAX_DISTINCT = 25
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}")
NOW = datetime.now(timezone.utc)


def parse_date(v):
    if not isinstance(v, str) or not DATE_RE.match(v):
        return None
    try:
        if "T" in v:
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        d = datetime.fromisoformat(v[:10])
        return d.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def main():
    data = load_all()
    # id -> table, so link targets can be resolved
    id_owner = {}
    for t, recs in data.items():
        for r in recs:
            id_owner[r["id"]] = t

    L = ["# Data profile", "", "Source: `data/raw/` only. No API calls.", ""]

    for table in TABLES:
        recs = data[table]
        n = len(recs)
        L += ["## {} (n={})".format(table, n), ""]
        if n == 0:
            L += ["_Table is empty. Airtable exposes no field names for a table with "
                  "zero records, so its schema is not observable from the API._", ""]
            continue

        fields = field_union(recs)
        L += ["| Field | % present | n present | Type(s) seen |", "|---|---|---|---|"]
        for f in fields:
            vals = [r["fields"][f] for r in recs if f in r["fields"]]
            types = sorted({type_name(v) for v in vals})
            L.append("| {} | {:.1f}% | {} | {} |".format(
                f, 100.0 * len(vals) / n, len(vals), ", ".join(types)))
        L.append("")

        # --- categorical values, quoted so case and whitespace are visible ---
        cat_lines = []
        for f in fields:
            vals = [r["fields"][f] for r in recs if f in r["fields"]]
            strs = [v for v in vals if isinstance(v, str)]
            if not strs or len(strs) != len(vals):
                continue
            distinct = Counter(strs)
            if len(distinct) > CATEGORICAL_MAX_DISTINCT:
                continue
            cat_lines.append("**{}** ({} distinct)".format(f, len(distinct)))
            cat_lines.append("")
            cat_lines.append("| Value (repr, so spaces/case are visible) | Count |")
            cat_lines.append("|---|---|")
            for v, c in distinct.most_common():
                cat_lines.append("| `{}` | {} |".format(repr(v), c))
            cat_lines.append("")
        if cat_lines:
            L += ["### Categorical fields — exact values", ""] + cat_lines

        # --- dates and numbers ---
        dn = []
        for f in fields:
            vals = [r["fields"][f] for r in recs if f in r["fields"]]
            dates = [parse_date(v) for v in vals]
            dates = [d for d in dates if d]
            if dates and len(dates) == len(vals):
                fut = sum(1 for d in dates if d > NOW)
                has_time = sum(1 for v in vals if isinstance(v, str) and "T" in v)
                dn.append("| {} | date | {} | {} | {} | — | {} |".format(
                    f, min(dates).date(), max(dates).date(), fut,
                    "datetime" if has_time else "date-only"))
                continue
            nums = [v for v in vals if isinstance(v, (int, float))
                    and not isinstance(v, bool)]
            if nums and len(nums) == len(vals):
                dn.append("| {} | number | {} | {} | — | {} | — |".format(
                    f, min(nums), max(nums), sum(1 for v in nums if v <= 0)))
        if dn:
            L += ["### Dates and numbers", "",
                  "| Field | Kind | Min | Max | Future dates | Values <= 0 | Format |",
                  "|---|---|---|---|---|---|---|"] + dn + [""]

        # --- link fields ---
        lk = []
        for f in fields:
            vals = [r["fields"].get(f) for r in recs]
            listy = [v for v in vals if isinstance(v, list)]
            if not listy:
                continue
            flat = [x for v in listy for x in v]
            if not flat or not all(isinstance(x, str) and x.startswith("rec") for x in flat):
                continue
            targets = Counter(id_owner.get(x, "UNRESOLVED") for x in flat)
            card = Counter(len(v) if isinstance(v, list) else 0 for v in vals)
            lk.append("| {} | {} | {} | {} | {} | {} |".format(
                f,
                ", ".join("{} ({})".format(k, v) for k, v in targets.most_common()),
                card.get(0, 0), card.get(1, 0),
                sum(c for k, c in card.items() if k > 1),
                targets.get("UNRESOLVED", 0)))
        if lk:
            L += ["### Link fields", "",
                  "| Field | Links to (n ids) | 0 links | 1 link | many links | unresolved ids |",
                  "|---|---|---|---|---|---|"] + lk + [""]

    # --- Findings table, first 20 rows ---
    findings = data["Findings"]
    L += ["## Findings table — first 20 rows", ""]
    if not findings:
        L += ["**The Findings table is empty (0 records).**", "",
              "No fields are observable and no rows exist, so it documents neither "
              "the 26.9% nor the ~72% claim.", ""]
    else:
        for r in findings[:20]:
            L.append("- `{}` {}".format(r["id"], json.dumps(r["fields"], ensure_ascii=False)))
        L.append("")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "profile.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("Wrote out/profile.md ({} lines)".format(len(L)))


if __name__ == "__main__":
    main()
