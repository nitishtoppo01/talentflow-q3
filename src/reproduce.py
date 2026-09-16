"""Try to reproduce the VP's 26.9% and ~72% under many definitions.

No judgement here - this only enumerates definition -> value.
"""
from collections import Counter

from common import OUT, load

APPS = load("Applications")
CANDS = load("Candidates")
OFFERS = load("Offers")

SRC = {r["id"]: r["fields"].get("Source") for r in CANDS}
APP_BY_ID = {r["id"]: r for r in APPS}

JOB_BOARD_SETS = {
    "strict: {'Job Board'}": {"Job Board"},
    "+LinkedIn": {"Job Board", "LinkedIn"},
    "+LinkedIn +Career Site": {"Job Board", "LinkedIn", "Career Site"},
    "all inbound (not Referral/Campus)": {"Job Board", "LinkedIn", "Career Site", "Agency"},
}


def app_source(app):
    link = app["fields"].get("Candidate") or []
    return SRC.get(link[0]) if link else None


def quarter(d):
    if not d:
        return None
    y, m = int(d[:4]), int(d[5:7])
    return "{}Q{}".format(y, (m - 1) // 3 + 1)


# ---------- hire definitions ----------
def hires_stage(apps):
    return [a for a in apps if a["fields"].get("Stage") == "Hired"]


def hires_accepted_offer(apps):
    accepted = {o["fields"]["Application"][0] for o in OFFERS
                if o["fields"].get("Status") == "Accepted"}
    return [a for a in apps if a["id"] in accepted]


def hires_any_offer(apps):
    offered = {o["fields"]["Application"][0] for o in OFFERS}
    return [a for a in apps if a["id"] in offered]


HIRE_DEFS = {
    "Applications.Stage == 'Hired'": hires_stage,
    "Offers.Status == 'Accepted'": hires_accepted_offer,
    "any linked Offer (offer extended)": hires_any_offer,
}


def c1_rows():
    rows = []
    windows = {"all time": None}
    qs = sorted({quarter(a["fields"].get("Applied On")) for a in APPS} - {None})
    for q in qs:
        windows["Applied On in " + q] = q

    for hname, hfn in HIRE_DEFS.items():
        for wname, w in windows.items():
            pool = APPS if w is None else [
                a for a in APPS if quarter(a["fields"].get("Applied On")) == w]
            hires = hfn(pool)
            if not hires:
                continue
            for label, jb in JOB_BOARD_SETS.items():
                for dedup in ("per application", "per candidate"):
                    if dedup == "per candidate":
                        seen, uniq = set(), []
                        for a in hires:
                            cid = (a["fields"].get("Candidate") or [None])[0]
                            if cid not in seen:
                                seen.add(cid)
                                uniq.append(a)
                        hh = uniq
                    else:
                        hh = hires
                    denom = len(hh)
                    num = sum(1 for a in hh if app_source(a) in jb)
                    if denom == 0:
                        continue
                    pct = 100.0 * num / denom
                    rows.append({
                        "hire_def": hname, "jb_labels": label, "dedup": dedup,
                        "window": wname, "num": num, "denom": denom, "pct": pct,
                    })
    return rows


# ---------- C2 ----------
def c2_rows():
    rows = []
    st = [o["fields"].get("Status") for o in OFFERS]
    counts = Counter(st)
    accepted = counts.get("Accepted", 0)

    denoms = {
        "all offers (incl. Pending)": len(OFFERS),
        "exclude Pending": len(OFFERS) - counts.get("Pending", 0),
        "Accepted + Declined only": counts.get("Accepted", 0) + counts.get("Declined", 0),
        "offers with a Decision On date": sum(
            1 for o in OFFERS if o["fields"].get("Decision On")),
    }
    for dname, d in denoms.items():
        if d:
            rows.append({"unit": "one row per offer", "denom_rule": dname,
                         "window": "all time", "num": accepted, "denom": d,
                         "pct": 100.0 * accepted / d})

    # one row per candidate x job (offer episode)
    episodes = {}
    for o in OFFERS:
        app = APP_BY_ID[o["fields"]["Application"][0]]
        key = ((app["fields"].get("Candidate") or [None])[0],
               (app["fields"].get("Opening") or [None])[0])
        episodes.setdefault(key, []).append(o)
    ep_status = []
    for key, os_ in episodes.items():
        sts = [o["fields"].get("Status") for o in os_]
        ep_status.append("Accepted" if "Accepted" in sts else sts[0])
    ec = Counter(ep_status)
    rows.append({"unit": "one row per candidate x job", "denom_rule": "all episodes",
                 "window": "all time", "num": ec.get("Accepted", 0),
                 "denom": len(ep_status),
                 "pct": 100.0 * ec.get("Accepted", 0) / len(ep_status)})

    # by quarter of Offered On and of Decision On
    for datefield in ("Offered On", "Decision On"):
        qs = sorted({quarter(o["fields"].get(datefield)) for o in OFFERS} - {None})
        for q in qs:
            sub = [o for o in OFFERS if quarter(o["fields"].get(datefield)) == q]
            a = sum(1 for o in sub if o["fields"].get("Status") == "Accepted")
            rows.append({"unit": "one row per offer",
                         "denom_rule": "all offers, window on " + datefield,
                         "window": q, "num": a, "denom": len(sub),
                         "pct": 100.0 * a / len(sub)})
    return rows, counts


CANDIDATE_FIELDS = {
    "(a) hiring channel / source": [
        ("Candidates.Source", "300/300 present; 6 labels; candidate-level, not application-level"),
        ("Applications.Referred By", "27/350 present; link to People; application-level referral signal"),
        ("People.Referrals Made", "12/14 present; the same referral edge seen from the employee side"),
    ],
    "(b) 'a hire'": [
        ("Applications.Stage == 'Hired'", "26/350"),
        ("Offers.Status == 'Accepted'", "26/36 offers"),
        ("Applications.Status == 'Closed'", "245/350 - closed includes rejections, not a hire signal"),
        ("Job Openings.Status", "req-level fill signal, 24 rows"),
    ],
    "(c) offer status": [
        ("Offers.Status", "Accepted 26, Pending 5, Declined 5"),
        ("Offers.Decline Reason", "5/36 present"),
        ("Applications.Stage == 'Offer'", "10/350"),
    ],
    "(d) offer dates": [
        ("Offers.Offered On", "36/36, date-only"),
        ("Offers.Decision On", "35/36, date-only"),
        ("Offers.Proposed Start Date", "36/36, date-only, 2 in the future"),
        ("Applications.Offered On", "36/350, date-only, mirrors Offers.Offered On"),
    ],
}


def candidate_fields_section():
    L = ["## Fields that could define each concept (no choice made yet)", ""]
    for concept, items in CANDIDATE_FIELDS.items():
        L += ["**{}**".format(concept), "", "| Field | Note |", "|---|---|"]
        for f, note in items:
            L.append("| `{}` | {} |".format(f, note))
        L.append("")
    return L


def main():
    L = ["# Reproducing the VP's numbers", "",
         "Enumeration only - no judgement on which definition is right.", ""]

    L += candidate_fields_section()

    rows = c1_rows()
    L += ["## C1 - 'job boards bring 26.9% of hires'", "",
          "| Hire definition | 'Job board' labels | Dedup | Window | Hires from job board | Total hires | % | Matches 26.9%? |",
          "|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["hire_def"], r["window"], r["jb_labels"], r["dedup"])):
        hit = "**YES**" if abs(r["pct"] - 26.9) < 0.1 else ""
        L.append("| {} | {} | {} | {} | {} | {} | {:.1f}% | {} |".format(
            r["hire_def"], r["jb_labels"], r["dedup"], r["window"],
            r["num"], r["denom"], r["pct"], hit))
    L.append("")

    c2, counts = c2_rows()
    L += ["## C2 - 'offer acceptance is around 72%'", "",
          "Offers.Status counts: " + ", ".join(
              "`{}`={}".format(k, v) for k, v in counts.most_common()), "",
          "| Unit | Denominator rule | Window | Accepted | Denominator | % | Matches ~72%? |",
          "|---|---|---|---|---|---|---|"]
    for r in c2:
        hit = "**YES**" if abs(r["pct"] - 72.0) < 1.0 else ""
        L.append("| {} | {} | {} | {} | {} | {:.1f}% | {} |".format(
            r["unit"], r["denom_rule"], r["window"], r["num"], r["denom"],
            r["pct"], hit))
    L.append("")

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "reproduce.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    hits1 = [r for r in rows if abs(r["pct"] - 26.9) < 0.1]
    hits2 = [r for r in c2 if abs(r["pct"] - 72.0) < 1.0]
    print("C1 exact matches to 26.9%: {}".format(len(hits1)))
    for r in hits1:
        print("   {} | {} | {} | {} -> {}/{}".format(
            r["hire_def"], r["jb_labels"], r["dedup"], r["window"], r["num"], r["denom"]))
    print("C2 matches to ~72%: {}".format(len(hits2)))
    for r in hits2:
        print("   {} | {} | {} -> {}/{} = {:.1f}%".format(
            r["unit"], r["denom_rule"], r["window"], r["num"], r["denom"], r["pct"]))
    print("Wrote out/reproduce.md")


if __name__ == "__main__":
    main()
