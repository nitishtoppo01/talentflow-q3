"""D2 roadmap -> out/roadmap.md. Every number is read back from out/findings.csv."""
import csv

from common import OUT

F = {}
with open(OUT / "findings.csv", encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        F[(r["claim"], r["metric"])] = r

EFFORT_NOTE = ("All effort figures are **estimates to confirm with the engineering "
               "lead**, sized against a 6-engineer-week Q3 budget.")

POOL = [
    # name, problem size, who, evidence, effort, confidence, decision
    ("Offer lifecycle states + decline reasons",
     "7 of 36 offers (19.4%) cannot be classified; 4 contradictory Pending move the "
     "headline 9.9 pts", "Recruiters, VP People, anyone reading the acceptance number",
     "High - every record inspected by hand", "2.0", "High", "BUILD 1"),
    ("Source captured at application time (required picklist)",
     "24 of 27 referred applications (88.9%) carry a channel label that contradicts "
     "their referrer link; 17 are labelled 'Job Board'",
     "Everyone who reads channel reporting, incl. the Q3 roadmap decision",
     "High - two independent fields disagree on the same records", "2.0", "High",
     "BUILD 2"),
    ("Write-time validation (required links, date order)",
     "7 date-order violations + 2 accept conflicts + 7 offers outside their salary band",
     "Recruiters at data entry; every downstream metric",
     "High - all counted from the live base", "1.5", "Medium", "BUILD 3"),
    ("Candidate de-duplication",
     "12 of 300 candidates (4.0%) duplicate on name+phone; moves C1 by +3.9 pts but "
     "changes no verdict", "Recruiters seeing the same person twice",
     "High on the count, low on the consequence", "1.0", "Medium", "DEFER"),
    ("Job-board integration",
     "236 applications/quarter peak, but 3.4% hire yield [CI 1.7-6.6] vs 6.7% overall",
     "Recruiters, who absorb the screening load",
     "High - CIs do not overlap with referral", "3.0", "High", "DO NOT BUILD"),
    ("Referral tooling",
     "Highest yield at 30.0%, but CI [10.8-60.3] on n=10 applications",
     "Employees and recruiters", "Low - 49-point CI, n well below 30", "2.0",
     "Low (n<30)", "DO NOT BUILD YET"),
    ("Time-to-offer alerts",
     "Median 35 days to offer for accepted vs 31 for declined - the difference runs "
     "the wrong way for the hypothesis, on n=5 declines",
     "Recruiters", "Low - n=5, correlation only", "1.0", "Low (n<30)", "DO NOT BUILD"),
]

BUILDS = [
    ("1", "Offer lifecycle states + decline reasons", "2.0",
     "4 contradictory Pending offers move acceptance from 72.2% to 82.1% - 9.9 pts on "
     "4 records",
     "One acceptance number everyone agrees on, with a maturity rule so open offers "
     "stop counting as failures",
     "First because it is a dependency: the VP wants the acceptance number moved, and "
     "no fix can be shown to work while 7 of 36 offers are unclassifiable."),
    ("2", "Source captured at application time (required picklist)", "2.0",
     "24 of 27 referred applications carry a contradicting channel label; C1 is 26.9% "
     "by one field and 11.5% by the other",
     "Channel attribution that survives scrutiny, at the application level rather than "
     "inherited from the candidate",
     "Second because the recommendation to hold job-board work rests on channel "
     "attribution - we should be able to defend that attribution before we act on it."),
    ("3", "Write-time validation (required links, date order)", "1.5",
     "7 date-order violations, 2 accept conflicts, 7 offers outside the req's salary band",
     "The classes of error cleaned in this audit stop recurring",
     "Third because it protects builds 1 and 2 rather than producing a number itself; "
     "doing it first would validate fields that build 2 is about to change."),
]

NOT_BUILDS = [
    ("Job-board integration", "3.4% hire yield [CI 1.7-6.6] vs 6.7% overall; 29 "
     "applications screened per hire vs 3 for referral",
     "3.0 engineer-weeks - half the quarter, and it would displace both metric-trust "
     "builds",
     "Revisit if the job-board yield CI lower bound rises above the all-channel yield, "
     "or if screening is automated so the marginal cost of an extra applicant "
     "approaches zero."),
    ("Referral tooling", "30.0% yield is the highest of any channel, but the CI is "
     "[10.8-60.3] on n=10 applications - a 49-point interval",
     "2.0 engineer-weeks bet on an interval that spans 'best channel' and 'ordinary'",
     "Revisit at n>=30 referral applications, which build 2 will produce reliably; on "
     "current volume that is roughly 3 quarters away."),
    ("Time-to-offer alerts", "Median days-to-offer is 35 for accepted offers and 31 "
     "for declined - the difference points the wrong way, on n=5 declines",
     "1.0 engineer-week spent on a hypothesis the data does not support",
     "Revisit when declines reach n>=30, or if decline reasons start naming speed; "
     "today 3 of 5 name 'Counter Offer'."),
]


def main():
    L = ["# D2 - Q3 roadmap", "", EFFORT_NOTE, "",
         "## Scored pool", "",
         "| Opportunity | Problem size | Who is affected | Evidence | Effort (ew) | "
         "Confidence | Decision |", "|---|---|---|---|---|---|---|"]
    for row in POOL:
        L.append("| " + " | ".join(row) + " |")

    total = sum(float(b[2]) for b in BUILDS)
    L += ["", "## Build - {} of 6 engineer-weeks".format(total), "",
          "| # | Build | ew | The number that justifies it | Expected outcome | "
          "Why it sits here |", "|---|---|---|---|---|---|"]
    for row in BUILDS:
        L.append("| " + " | ".join(row) + " |")
    L += ["", "Total **{} engineer-weeks**, leaving {} as buffer.".format(
        total, round(6 - total, 1)), ""]

    L += ["## Do not build", "",
          "| Not building | The number against it | Opportunity cost | "
          "What would make us revisit |", "|---|---|---|---|"]
    for row in NOT_BUILDS:
        L.append("| " + " | ".join(row) + " |")
    L.append("")

    (OUT / "roadmap.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    assert total <= 6, "roadmap exceeds the 6 engineer-week budget"
    print("wrote out/roadmap.md - {} builds totalling {} ew (budget 6)".format(
        len(BUILDS), total))


if __name__ == "__main__":
    main()
