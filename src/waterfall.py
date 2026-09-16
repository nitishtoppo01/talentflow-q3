"""Cleaning waterfall for C1 and C2 -> out/waterfall.md. Reads data/raw/ only."""
import re
from collections import Counter, defaultdict

from common import OUT, load_all

D = load_all()
APPS, CANDS, OFFERS = D["Applications"], D["Candidates"], D["Offers"]
APP = {r["id"]: r for r in APPS}
CAND = {r["id"]: r for r in CANDS}
SRC = {r["id"]: r["fields"].get("Source") for r in CANDS}


def L(r, f):
    return (r["fields"].get(f) or [None])[0]


def c1_value(apps, jb_labels, cand_alias=None):
    """Job-board share of hires over a given application pool."""
    cand_alias = cand_alias or {}
    hires = [a for a in apps if a["fields"].get("Stage") == "Hired"]
    if not hires:
        return 0, 0, 0.0
    num = sum(1 for a in hires
              if SRC.get(cand_alias.get(L(a, "Candidate"), L(a, "Candidate"))) in jb_labels)
    return num, len(hires), 100.0 * num / len(hires)


def c1_waterfall():
    steps = []
    jb = {"Job Board"}

    n, d, p = c1_value(APPS, jb)
    steps.append(("0. Raw - every application, strict 'Job Board' label", n, d, p,
                  "the VP's number"))

    # 1. collapse duplicate candidates on normalised name + phone
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
    n, d, p = c1_value(APPS, jb, alias)
    steps.append(("1. + collapse duplicate candidates (name+phone, {} records)".format(
        len(alias)), n, d, p, "same source label, so no movement expected"))

    # 2. collapse duplicate applications (same candidate x opening) - keep earliest
    seen, deduped = set(), []
    for a in sorted(APPS, key=lambda a: a["fields"].get("Applied On", "")):
        key = (alias.get(L(a, "Candidate"), L(a, "Candidate")), L(a, "Opening"))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(a)
    n, d, p = c1_value(deduped, jb, alias)
    steps.append(("2. + collapse duplicate applications (same candidate x opening)",
                  n, d, p, "{} applications dropped".format(len(APPS) - len(deduped))))

    # 3. drop the cross-req double-accept conflict
    acc_by_cand = Counter(L(APP[L(o, "Application")], "Candidate")
                          for o in OFFERS if o["fields"].get("Status") == "Accepted")
    conflict_reqs = set()
    for c, k in acc_by_cand.items():
        if k > 1:
            reqs = {L(APP[L(o, "Application")], "Opening") for o in OFFERS
                    if o["fields"].get("Status") == "Accepted"
                    and L(APP[L(o, "Application")], "Candidate") == c}
            if len(reqs) > 1:
                conflict_reqs.add(c)
    step3 = [a for a in deduped if L(a, "Candidate") not in conflict_reqs]
    n, d, p = c1_value(step3, jb, alias)
    steps.append(("3. + exclude the candidate accepted on two different reqs",
                  n, d, p, "unresolvable conflict, {} applications dropped".format(
                      len(deduped) - len(step3))))

    # 4. regroup: LinkedIn counted as a job board
    n2, d2, p2 = c1_value(step3, {"Job Board", "LinkedIn"}, alias)
    steps.append(("4. ALT grouping: count LinkedIn as a job board too", n2, d2, p2,
                  "a grouping choice, not a cleaning rule"))
    return steps


def c2_waterfall():
    steps = []
    offers = list(OFFERS)

    def rate(os_, note=""):
        a = sum(1 for o in os_ if o["fields"].get("Status") == "Accepted")
        return a, len(os_), (100.0 * a / len(os_) if os_ else 0.0), note

    steps.append(("0. Raw - accepted / all offers incl. Pending",) + rate(offers))

    # 1. collapse re-issued offers: same candidate x opening, keep latest Offered On
    groups = defaultdict(list)
    for o in offers:
        a = APP[L(o, "Application")]
        groups[(L(a, "Candidate"), L(a, "Opening"))].append(o)
    collapsed = [sorted(v, key=lambda o: o["fields"].get("Offered On", ""))[-1]
                 for v in groups.values()]
    steps.append(("1. + collapse re-issued offers (same candidate x req, keep latest)",)
                 + rate(collapsed, "NORMAL BUSINESS BEHAVIOUR, not bad data"))

    # 2. exclude the cross-req double-accept conflict
    acc_by_cand = defaultdict(set)
    for o in collapsed:
        if o["fields"].get("Status") == "Accepted":
            a = APP[L(o, "Application")]
            acc_by_cand[L(a, "Candidate")].add(L(a, "Opening"))
    conflicted = {c for c, reqs in acc_by_cand.items() if len(reqs) > 1}
    step2 = [o for o in collapsed
             if L(APP[L(o, "Application")], "Candidate") not in conflicted]
    steps.append(("2. + exclude candidate accepted on two different reqs",)
                 + rate(step2, "GENUINE CONFLICT - one person cannot take two jobs"))

    # 3. exclude genuinely open offers (Pending with no Decision On)
    step3 = [o for o in step2 if not (o["fields"].get("Status") == "Pending"
                                      and not o["fields"].get("Decision On"))]
    steps.append(("3. + exclude offers still genuinely open (Pending, no Decision On)",)
                 + rate(step3, "maturity rule: an undecided offer is not yet a failure"))

    # 4. exclude contradictory Pending (status Pending but a Decision On exists)
    step4 = [o for o in step3 if not (o["fields"].get("Status") == "Pending"
                                      and o["fields"].get("Decision On"))]
    steps.append(("4. + exclude contradictory Pending (status Pending, decision dated)",)
                 + rate(step4, "STATUS CONFLICT - cannot be classified either way"))

    # 5. range on the unresolved contradictory records
    unres = [o for o in step3 if o["fields"].get("Status") == "Pending"
             and o["fields"].get("Decision On")]
    a4, d4, _, _ = rate(step4)
    lo = 100.0 * a4 / (d4 + len(unres)) if d4 + len(unres) else 0.0
    hi = 100.0 * (a4 + len(unres)) / (d4 + len(unres)) if d4 + len(unres) else 0.0
    steps.append(("5. RANGE over the {} unresolved records".format(len(unres)),
                  a4, d4 + len(unres), None,
                  "lower {:.1f}% (all declined) .. upper {:.1f}% (all accepted)".format(lo, hi)))
    return steps


def main():
    L_ = ["# Cleaning waterfall", "",
          "Each row applies the rule above it as well. Produced by `src/waterfall.py`.", ""]

    L_ += ["## C1 - job-board share of hires", "",
           "| Step | Job-board hires | Total hires | Value | Note |", "|---|---|---|---|---|"]
    c1 = c1_waterfall()
    for s, n, d, p, note in c1:
        L_.append("| {} | {} | {} | {:.1f}% | {} |".format(s, n, d, p, note))
    raw = c1[0][3]
    moves = [(abs(p - raw), s) for s, n, d, p, _ in c1[1:]]
    L_ += ["", "**Largest mover:** {} ({:+.1f} pts from raw).".format(
        max(moves)[1], max(moves)[0]), ""]

    L_ += ["## C2 - offer acceptance", "",
           "| Step | Accepted | Denominator | Value | Note |", "|---|---|---|---|---|"]
    c2 = c2_waterfall()
    for s, a, d, p, note in c2:
        L_.append("| {} | {} | {} | {} | {} |".format(
            s, a, d, "{:.1f}%".format(p) if p is not None else "range", note))
    raw2 = c2[0][3]
    moves2 = [(abs(p - raw2), s) for s, a, d, p, _ in c2[1:] if p is not None]
    L_ += ["", "**Largest mover:** {} ({:+.1f} pts from raw).".format(
        max(moves2)[1], max(moves2)[0]), ""]

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "waterfall.md").write_text("\n".join(L_) + "\n", encoding="utf-8")
    print("\n".join(L_))


if __name__ == "__main__":
    main()
