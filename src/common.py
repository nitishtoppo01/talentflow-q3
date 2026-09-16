"""Shared loaders. Every stage after the pull reads data/raw/ only."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "out"

TABLES = [
    "Departments", "People", "Job Openings", "Candidates",
    "Applications", "Interviews", "Offers", "Findings",
]


def slug(table):
    return table.lower().replace(" ", "_")


def load(table):
    """Records for one table, verbatim as pulled."""
    return json.loads((RAW / "{}.json".format(slug(table))).read_text(encoding="utf-8"))


def load_all():
    return {t: load(t) for t in TABLES}


def field_union(records):
    """Ordered union of field keys across records (Airtable omits empty fields)."""
    seen = []
    for r in records:
        for k in r.get("fields", {}):
            if k not in seen:
                seen.append(k)
    return seen


def type_name(v):
    if isinstance(v, bool):
        return "bool"
    if isinstance(v, int):
        return "int"
    if isinstance(v, float):
        return "float"
    if isinstance(v, str):
        return "str"
    if isinstance(v, list):
        return "list[{}]".format(",".join(sorted({type_name(x) for x in v})) or "empty")
    if isinstance(v, dict):
        return "dict/ERROR_OBJECT" if "error" in v or "specialValue" in v else "dict"
    if v is None:
        return "null"
    return type(v).__name__
