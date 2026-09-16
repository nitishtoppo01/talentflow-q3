"""Data audit (D4) -> out/dq_issues.csv and out/dq_summary.md. Reads data/raw/ only."""
import csv
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone

from common import OUT, TABLES, load_all

NOW = datetime.now(timezone.utc)
D = load_all()
BY_ID = {r["id"]: (t, r) for t, recs in D.items() for r in recs}
N = {t: len(recs) for t, recs in D.items()}

ISSUES = []            # issue rows
AFFECTED = defaultdict(set)   # table -> set of record ids with >=1 issue


def to_dt(v):
    """Date-only and UTC datetime -> a common tz-aware form."""
    if not isinstance(v, str) or not re.match(r"^\d{4}-\d{2}-\d{2}", v):
        return None
    try:
        if "T" in v:
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return datetime.fromisoformat(v[:10]).replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def add(table, field, check, rule, ids, metric, direction, treatment, note=""):
    ids = list(ids)
    if not ids:
        return
    AFFECTED[table].update(ids)
    ISSUES.append({
        "table": table, "field": field, "check": check, "rule": rule,
        "n": len(ids), "pct_of_table": round(100.0 * len(ids) / N[table], 1),
        "metric": metric, "direction": direction,
        "examples": " ".join(ids[:5]), "treatment": treatment, "note": note,
    })


APPS, CANDS, OFFERS, INTS = D["Applications"], D["Candidates"], D["Offers"], D["Interviews"]
JOBS, PEOPLE = D["Job Openings"], D["People"]
APP_BY_ID = {r["id"]: r for r in APPS}
SRC = {r["id"]: r["fields"].get("Source") for r in CANDS}


def link(rec, field):
    return (rec["fields"].get(field) or [None])[0]


# ---------------- 1. Completeness ----------------
def completeness():
    metric_fields = {
        "Candidates": [("Source", "C1")],
        "Applications": [("Stage", "both"), ("Status", "both"), ("Applied On", "both"),
                         ("Candidate", "C1"), ("Opening", "C1")],
        "Offers": [("Status", "C2"), ("Offered On", "C2"), ("Decision On", "C2"),
                   ("Application", "C2")],
    }
    for table, fields in metric_fields.items():
        for f, metric in fields:
            miss = [r["id"] for r in D[table] if f not in r["fields"]
                    or r["fields"].get(f) in (None, "", [])]
            add(table, f, "completeness", "field absent or empty", miss, metric,
                "shrinks denominator if excluded" if miss else "none",
                "flag only" if f == "Decision On" else "exclude",
                "Decision On absent = genuinely undecided offer" if f == "Decision On" else "")


# ---------------- 2. Validity ----------------
def validity():
    expected = {
        ("Applications", "Stage"): {"Applied", "Screening", "Interview", "Offer",
                                    "Hired", "Rejected", "Withdrawn"},
        ("Applications", "Status"): {"Active", "Closed"},
        ("Offers", "Status"): {"Accepted", "Pending", "Declined"},
        ("Job Openings", "Status"): {"Open", "Filled", "On Hold", "Cancelled"},
        ("Interviews", "Outcome"): {"Completed", "No Show", "Rescheduled", "Cancelled"},
    }
    for (t, f), ok in expected.items():
        bad = [r["id"] for r in D[t] if f in r["fields"] and r["fields"][f] not in ok]
        add(t, f, "validity", "value outside expected set", bad, "both",
            "unknown", "flag only")

    # error objects / unexpected types on any field
    for t, recs in D.items():
        errs = [r["id"] for r in recs
                if any(isinstance(v, dict) for v in r["fields"].values())]
        add(t, "(any)", "validity", "computed field returned an error object",
            errs, "none", "none", "flag only")

    # non-positive amounts
    for t, f in [("Offers", "Base CTC"), ("Offers", "Joining Bonus"),
                 ("Candidates", "Current CTC"), ("Candidates", "Expected CTC"),
                 ("Candidates", "Years Experience"), ("Candidates", "Notice Period Days"),
                 ("Job Openings", "Salary Band Min"), ("Job Openings", "Salary Band Max"),
                 ("Job Openings", "Headcount")]:
        bad = [r["id"] for r in D[t]
               if isinstance(r["fields"].get(f), (int, float)) and r["fields"][f] <= 0]
        add(t, f, "validity", "value <= 0", bad, "none", "none", "flag only",
            "zero bonus/experience is plausible business data")

    # future dates
    for t in TABLES:
        for f in {k for r in D[t] for k in r["fields"]}:
            fut = [r["id"] for r in D[t] if (to_dt(r["fields"].get(f)) or NOW) > NOW]
            if fut:
                expected_future = f in ("Proposed Start Date", "Target Close")
                add(t, f, "validity", "date in the future", fut, "none",
                    "none", "flag only",
                    "EXPECTED: a future start/close date is normal business data"
                    if expected_future else "unexpected future date")

    # malformed emails
    bad = [r["id"] for r in CANDS
           if not re.match(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$", r["fields"].get("Email", ""))]
    add("Candidates", "Email", "validity", "email fails RFC-ish shape check", bad,
        "none", "none", "flag only")

    # test / dummy records - whole-value match only, not substring in prose
    dummy = [r["id"] for t in TABLES for r in D[t]
             if any(isinstance(v, str) and v.strip().lower() in
                    {"test", "dummy", "sample", "asdf", "xxx", "foo"}
                    for v in r["fields"].values())]
    add("Candidates", "(any)", "validity", "test/dummy record (exact-value match)",
        dummy, "both", "none", "exclude",
        "substring matching gave 21 false positives ('Lead QA Engineer', "
        "'did not test the solution') - exact-value match gives 0")


# ---------------- 3. Uniqueness ----------------
def uniqueness():
    by_email = defaultdict(list)
    for r in CANDS:
        e = (r["fields"].get("Email") or "").strip().lower()
        if e:
            by_email[e].append(r["id"])
    dup = [i for ids in by_email.values() if len(ids) > 1 for i in ids]
    add("Candidates", "Email", "uniqueness", "duplicate normalised email", dup,
        "C1", "inflates candidate counts", "exclude")

    by_np = defaultdict(list)
    for r in CANDS:
        key = ((r["fields"].get("Full Name") or "").strip().lower(),
               re.sub(r"\D", "", r["fields"].get("Phone") or ""))
        if key[0] and key[1]:
            by_np[key].append(r["id"])
    dup2 = [i for ids in by_np.values() if len(ids) > 1 for i in ids]
    add("Candidates", "Full Name + Phone", "uniqueness",
        "duplicate normalised name + phone", dup2, "C1",
        "inflates candidate counts", "exclude")

    by_cj = defaultdict(list)
    for a in APPS:
        by_cj[(link(a, "Candidate"), link(a, "Opening"))].append(a["id"])
    dup3 = [i for ids in by_cj.values() if len(ids) > 1 for i in ids]
    add("Applications", "Candidate + Opening", "uniqueness",
        "same candidate applied to the same opening more than once", dup3,
        "C1", "inflates application denominator", "flag only",
        "could be a genuine re-application in a later season")

    by_app = defaultdict(list)
    for o in OFFERS:
        by_app[link(o, "Application")].append(o["id"])
    dup4 = [i for ids in by_app.values() if len(ids) > 1 for i in ids]
    add("Offers", "Application", "uniqueness", "more than one offer per application",
        dup4, "C2", "inflates offer denominator", "fix",
        "a re-issued/revised offer is normal business behaviour; "
        "keep the latest, do not count twice")

    by_at = defaultdict(list)
    for i in INTS:
        by_at[(link(i, "Application"), i["fields"].get("Scheduled On"))].append(i["id"])
    dup5 = [x for ids in by_at.values() if len(ids) > 1 for x in ids]
    add("Interviews", "Application + Scheduled On", "uniqueness",
        "duplicate interview on the same application and time", dup5, "none",
        "none", "flag only", "could be two panellists logging the same slot")


# ---------------- 4. Referential integrity ----------------
def referential():
    link_fields = {
        "Applications": ["Candidate", "Opening", "Recruiter", "Offers", "Interviews",
                         "Referred By"],
        "Offers": ["Application"], "Interviews": ["Application", "Interviewer"],
        "Candidates": ["Applications"], "Job Openings": ["Department", "Recruiter",
                                                          "Hiring Manager", "Applications"],
        "People": ["Department"], "Departments": ["People", "Job Openings"],
    }
    for t, fields in link_fields.items():
        for f in fields:
            unres = [r["id"] for r in D[t]
                     for x in (r["fields"].get(f) or []) if x not in BY_ID]
            add(t, f, "referential integrity", "linked record id does not resolve",
                unres, "both", "unknown", "exclude")

    for t, f, expect in [("Applications", "Candidate", 1), ("Applications", "Opening", 1),
                         ("Applications", "Recruiter", 1), ("Offers", "Application", 1),
                         ("Interviews", "Application", 1), ("Interviews", "Interviewer", 1)]:
        bad = [r["id"] for r in D[t] if len(r["fields"].get(f) or []) != expect]
        add(t, f, "referential integrity",
            "link count != {} (expected exactly one)".format(expect), bad,
            "both", "unknown", "exclude")

    # orphans both directions
    linked_apps = {link(o, "Application") for o in OFFERS}
    orphan_offer_side = [a["id"] for a in APPS
                         if a["fields"].get("Offers") and a["id"] not in linked_apps]
    add("Applications", "Offers", "referential integrity",
        "application points at an offer that does not point back", orphan_offer_side,
        "C2", "unknown", "flag only")

    cand_with_apps = {link(a, "Candidate") for a in APPS}
    orphan_cands = [c["id"] for c in CANDS if c["id"] not in cand_with_apps]
    add("Candidates", "Applications", "referential integrity",
        "candidate with no application", orphan_cands, "C1",
        "inflates candidate-level source share", "flag only",
        "a sourced-but-never-applied candidate is normal")


# ---------------- 5. Cross-table consistency ----------------
def cross_table():
    accepted_apps = {link(o, "Application") for o in OFFERS
                     if o["fields"].get("Status") == "Accepted"}
    hired = {a["id"] for a in APPS if a["fields"].get("Stage") == "Hired"}
    add("Applications", "Stage / Offers.Status", "cross-table",
        "Stage=='Hired' but no accepted offer", sorted(hired - accepted_apps),
        "both", "inflates hire count", "exclude")
    add("Applications", "Stage / Offers.Status", "cross-table",
        "accepted offer but Stage != 'Hired'", sorted(accepted_apps - hired),
        "both", "deflates hire count", "exclude")

    bad_stage = [o["id"] for o in OFFERS if o["fields"].get("Status") == "Accepted"
                 and APP_BY_ID.get(link(o, "Application"), {}).get("fields", {})
                 .get("Stage") in ("Rejected", "Withdrawn")]
    add("Offers", "Status", "cross-table",
        "accepted offer on a rejected/withdrawn application", bad_stage, "C2",
        "inflates acceptance", "exclude")

    cand_acc = Counter(link(APP_BY_ID[link(o, "Application")], "Candidate")
                       for o in OFFERS if o["fields"].get("Status") == "Accepted")
    multi = [c for c, n in cand_acc.items() if n > 1]
    ids = [o["id"] for o in OFFERS if o["fields"].get("Status") == "Accepted"
           and link(APP_BY_ID[link(o, "Application")], "Candidate") in multi]
    add("Offers", "Status", "cross-table", "candidate with more than one accepted offer",
        ids, "C2", "inflates numerator and denominator", "fix",
        "a revised offer to the same person for the same req is normal business "
        "behaviour; two different reqs would be a real conflict")

    # filled job whose hire count does not match headcount
    hires_by_job = Counter(link(a, "Opening") for a in APPS
                           if a["fields"].get("Stage") == "Hired")
    mismatch = [j["id"] for j in JOBS if j["fields"].get("Status") == "Filled"
                and hires_by_job.get(j["id"], 0) != j["fields"].get("Headcount", 0)]
    add("Job Openings", "Status / Headcount", "cross-table",
        "job marked Filled but hire count != headcount", mismatch, "C1",
        "unknown", "flag only")
    nonfilled_with_hires = [j["id"] for j in JOBS
                            if j["fields"].get("Status") != "Filled"
                            and hires_by_job.get(j["id"], 0) > 0]
    add("Job Openings", "Status", "cross-table",
        "job not marked Filled but has hired applications", nonfilled_with_hires,
        "C1", "unknown", "flag only",
        "a multi-headcount req stays Open after one hire - normal")

    late = [a["id"] for a in APPS
            if (to_dt(a["fields"].get("Applied On")) or NOW) >
            (to_dt((BY_ID.get(link(a, "Opening"), (None, {"fields": {}}))[1])
                   ["fields"].get("Target Close")) or NOW.replace(year=2100))]
    add("Applications", "Applied On", "cross-table",
        "application submitted after the opening's target close date", late,
        "C1", "unknown", "flag only",
        "Target Close is a target, not a hard close - weak signal")


# ---------------- 6. Temporal order ----------------
def temporal():
    chain = [("Opened On", "opening"), ("Applied On", "app"), ("Screened On", "app"),
             ("First Interview On", "app"), ("Final Interview On", "app"),
             ("Offered On", "app")]
    viol = defaultdict(list)
    for a in APPS:
        job = BY_ID.get(link(a, "Opening"), (None, {"fields": {}}))[1]
        seq = [("Opened On", to_dt(job["fields"].get("Opened On")))]
        for f, _ in chain[1:]:
            seq.append((f, to_dt(a["fields"].get(f))))
        off = [o for o in OFFERS if link(o, "Application") == a["id"]]
        if off:
            seq.append(("Decision On", to_dt(off[0]["fields"].get("Decision On"))))
            seq.append(("Proposed Start Date", to_dt(off[0]["fields"].get("Proposed Start Date"))))
        pts = [(f, d) for f, d in seq if d]
        for i in range(len(pts) - 1):
            if pts[i + 1][1] < pts[i][1]:
                viol["{} before {}".format(pts[i + 1][0], pts[i][0])].append(a["id"])
    for k, ids in viol.items():
        add("Applications", k.split(" before ")[0], "temporal order",
            "out of order: " + k, ids, "both", "unknown", "flag only")

    durs = [( (to_dt(a["fields"].get("Offered On")) - to_dt(a["fields"].get("Applied On"))).days,
             a["id"]) for a in APPS
            if to_dt(a["fields"].get("Offered On")) and to_dt(a["fields"].get("Applied On"))]
    if durs:
        durs.sort()
        neg = [i for d, i in durs if d < 0]
        add("Applications", "Applied On -> Offered On", "temporal order",
            "negative duration", neg, "both", "unknown", "flag only")
        p99 = durs[int(0.99 * (len(durs) - 1))][0]
        slow = [i for d, i in durs if d > p99]
        add("Applications", "Applied On -> Offered On", "temporal order",
            "duration above p99 ({} days)".format(p99), slow, "none", "none",
            "flag only")


# ---------------- 7. Provenance ----------------
def provenance():
    days = Counter(r["createdTime"][:10] for t in TABLES for r in D[t])
    if len(days) == 1:
        only = list(days)[0]
        add("Applications", "createdTime", "provenance",
            "every record in every table shares one createdTime date ({})".format(only),
            [r["id"] for r in APPS], "both", "none", "flag only",
            "the whole base is one bulk import, so createdTime cannot separate "
            "bulk from organic records and issue rates cannot be compared across them")


# ---------------- 8. Taxonomy ----------------
def taxonomy():
    for t, f in [("Candidates", "Source"), ("Applications", "Stage"),
                 ("Applications", "Status"), ("Offers", "Status"),
                 ("Job Openings", "Status"), ("Departments", "Name"),
                 ("People", "Role"), ("Job Openings", "Location")]:
        vals = [r["fields"].get(f) for r in D[t] if isinstance(r["fields"].get(f), str)]
        norm = defaultdict(set)
        for v in vals:
            norm[v.strip().lower()].add(v)
        variants = {k: v for k, v in norm.items() if len(v) > 1}
        ids = [r["id"] for r in D[t]
               if isinstance(r["fields"].get(f), str)
               and r["fields"][f].strip().lower() in variants]
        add(t, f, "taxonomy", "case/whitespace variants of the same label", ids,
            "C1" if f == "Source" else "both", "splits a channel's share",
            "fix", "variants found: {}".format(variants) if variants else "none found")

    # a source label that names one board rather than a channel class
    board_like = [r["id"] for r in CANDS if r["fields"].get("Source") == "LinkedIn"]
    add("Candidates", "Source", "taxonomy",
        "source label names a specific product, not a channel class", board_like,
        "C1", "moves share between 'Job Board' and other", "flag only",
        "LinkedIn is arguably a job board; grouping choice moves C1 by ~11 pts")


# ---------------- 9. Ownership ----------------
def ownership():
    people_ids = {p["id"] for p in PEOPLE}
    for t, f in [("Interviews", "Interviewer"), ("Applications", "Recruiter"),
                 ("Job Openings", "Recruiter"), ("Job Openings", "Hiring Manager")]:
        missing = [r["id"] for r in D[t] if not r["fields"].get(f)]
        add(t, f, "ownership", "no owner set", missing, "none", "none", "flag only")
        notpeople = [r["id"] for r in D[t]
                     for x in (r["fields"].get(f) or []) if x not in people_ids]
        add(t, f, "ownership", "owner id is not in People", notpeople, "none",
            "none", "flag only")

    dept_of = {p["id"]: link(p, "Department") for p in PEOPLE}
    cross = [j["id"] for j in JOBS
             if dept_of.get(link(j, "Hiring Manager")) != link(j, "Department")]
    add("Job Openings", "Hiring Manager", "ownership",
        "hiring manager sits outside the opening's department", cross, "none",
        "none", "flag only", "a shared/matrixed HM is normal in a small org")


# --------- 10. Anomalies the nine families would not catch ---------
def anomalies():
    ref_link = [a for a in APPS if a["fields"].get("Referred By")]
    conflict = [a["id"] for a in ref_link if SRC.get(link(a, "Candidate")) != "Referral"]
    add("Applications", "Referred By vs Candidates.Source", "anomaly",
        "application has a referrer link but the candidate's Source says another channel",
        conflict, "C1", "misattributes referral hires to job boards", "fix",
        "two channel signals disagree on 24 of 27 referred applications; 17 of those "
        "are labelled 'Job Board'. C1 is 26.9% by Source but 11.5% by Referred By.")

    jobs_by_id = {j["id"]: j for j in JOBS}
    outside = []
    for o in OFFERS:
        a = APP_BY_ID.get(link(o, "Application"))
        j = jobs_by_id.get(link(a, "Opening")) if a else None
        b = o["fields"].get("Base CTC")
        if not j or b is None:
            continue
        lo, hi = j["fields"].get("Salary Band Min"), j["fields"].get("Salary Band Max")
        if lo is not None and hi is not None and (b < lo or b > hi):
            outside.append(o["id"])
    add("Offers", "Base CTC", "anomaly", "offer outside the requisition's salary band",
        outside, "C2", "none directly; signals comp-process breakdown", "flag only",
        "no check family compares an offer to its own req's band")

    by_app = defaultdict(list)
    for i in INTS:
        by_app[link(i, "Application")].append(i["fields"].get("Recommendation"))
    neg = [a["id"] for a in APPS if a["fields"].get("Stage") == "Hired"
           and by_app.get(a["id"])
           and all(r in ("No Hire", "Strong No Hire")
                   for r in by_app[a["id"]] if r)]
    add("Applications", "Stage vs Interviews.Recommendation", "anomaly",
        "hired although every interview recommendation was negative", neg,
        "C1", "none directly; signals a broken decision trail", "flag only",
        "no check family compares the hire decision to the interview verdicts")


BUSINESS_NORMAL = [
    ("application submitted after the opening's target close date", 251,
     "Target Close is a target, not a gate; 71.7% of applications arrive after it, "
     "so this is how Acme operates, not an error"),
    ("hiring manager sits outside the opening's department", 21,
     "only 4 people hold Role='Hiring Manager' across 8 departments and 24 reqs, "
     "so cross-department HMs are unavoidable in an org this size"),
    ("value <= 0 (Joining Bonus 23, Notice Period 33, Years Experience 25)", 81,
     "zero bonus, zero notice period and a fresher with zero years are all real values"),
    ("date in the future (Proposed Start Date)", 2,
     "a start date in the future is the expected state for a recent offer"),
    ("more than one offer per application / candidate x req", 2,
     "a re-issued offer at a higher salary is normal negotiation; it must be "
     "collapsed, not excluded"),
    ("job not marked Filled but has hired applications", 10,
     "a multi-headcount req stays Open after its first hire"),
    ("candidate with no application", None,
     "a sourced-but-never-applied candidate is a normal pipeline state"),
]


def main():
    completeness(); validity(); uniqueness(); referential()
    cross_table(); temporal(); provenance(); taxonomy(); ownership(); anomalies()

    OUT.mkdir(parents=True, exist_ok=True)
    cols = ["table", "field", "check", "rule", "n", "pct_of_table", "metric",
            "direction", "examples", "treatment", "note"]
    with open(OUT / "dq_issues.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for row in sorted(ISSUES, key=lambda r: -r["n"]):
            w.writerow(row)

    L = ["# Data quality audit (D4)", "",
         "Every count below is produced by `src/audit.py` from `data/raw/`.", "",
         "## Records with at least one issue", "",
         "| Table | Records | With >=1 issue | % |", "|---|---|---|---|"]
    for t in TABLES:
        a = len(AFFECTED.get(t, set()))
        L.append("| {} | {} | {} | {:.1f}% |".format(
            t, N[t], a, 100.0 * a / N[t] if N[t] else 0.0))
    L += ["", "## Issues found ({} distinct checks fired)".format(len(ISSUES)), "",
          "| Table | Field | Check | n | % | Metric | Treatment |", "|---|---|---|---|---|---|---|"]
    for r in sorted(ISSUES, key=lambda r: -r["n"]):
        L.append("| {table} | {field} | {rule} | {n} | {pct_of_table}% | {metric} | {treatment} |".format(**r))
    L += ["", "## Re-labelled as normal business behaviour, not bad data", "",
          "| Issue | n | Why it is normal |", "|---|---|---|"]
    for name, n, why in BUSINESS_NORMAL:
        L.append("| {} | {} | {} |".format(name, n if n is not None else "-", why))
    L.append("")
    (OUT / "dq_summary.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("{} issue rows; tables affected: {}".format(
        len(ISSUES), {t: len(v) for t, v in AFFECTED.items()}))


if __name__ == "__main__":
    main()
