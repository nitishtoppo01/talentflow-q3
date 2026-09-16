"""Assemble docs/submission.md (D5,D1,D2,D3,D4), write out/findings.md, verify numbers."""
import csv
import pathlib
import re

from common import OUT, ROOT

DOCS = ROOT / "docs"
PARTS = DOCS / "parts"


def demote(text):
    """An included file's H1 becomes an H2 so each deliverable keeps a single H1."""
    return re.sub(r"^# ", "## ", text, flags=re.M)


def read(p):
    return pathlib.Path(p).read_text(encoding="utf-8").rstrip() + "\n"


def findings_md():
    rows = list(csv.DictReader((OUT / "findings.csv").open(encoding="utf-8")))
    L = ["# Findings", "",
         "Generated from `out/findings.csv`. Every value is produced by the named script.",
         "", "| Claim | Metric | Value | Method | Confidence | n | Script |",
         "|---|---|---|---|---|---|---|"]
    for r in rows:
        L.append("| {claim} | {metric} | **{value}** | {method} | {confidence} | {n} | `{script}` |"
                 .format(**r))
    L.append("")
    (OUT / "findings.md").write_text("\n".join(L), encoding="utf-8")
    return rows


def audit_changed_section():
    return """
## How the audit changed D1 and D2

| | Before the audit | After | Did the verdict change? |
|---|---|---|---|
| C1 job-board share of hires | 26.9% | 34.8% | **No.** Cleaning moved the share *up* 7.9 pts; the verdict rests on hire yield (3.4%), which cleaning barely moved. |
| C1 grouping choice | 'Job Board' only | +LinkedIn = 47.8% | **No**, but it is the largest single mover (+20.9 pts) and it is a definition decision, not a data fix. |
| C2 acceptance | 72.2% | 82.1% (range 69.7-84.8%) | **Yes.** 4 contradictory `Pending` records move it 9.9 pts, and the range straddles "there is a problem" and "there is not". |
| D2 ordering | - | Source capture funded at 2.0 ew | **Yes.** The audit found 24 of 27 referred applications contradict their own channel label, which is the one argument that could overturn the C1 verdict - so it is funded as build 2. |

Three flagged issues were withdrawn after opening the records: 251 "applied after target
close" and 21 "hiring manager outside department" are how Acme operates, and 21 "test
records" were a substring-matching artifact ('Lead QA Engineer', "did not test the
solution") - the true count is 0.
"""


def check_numbers(rows):
    """Every %/number in the memo must appear somewhere in out/."""
    corpus = "\n".join(read(OUT / f) for f in
                       ("findings.csv", "metrics.md", "roadmap.md", "waterfall.md",
                        "dq_summary.md"))
    memo = read(PARTS / "d5.md")
    pat = re.compile(r"\d+(?:\.\d+)?%?")
    missing = []
    for tok in sorted(set(pat.findall(memo))):
        if len(tok.rstrip("%")) < 2:      # skip 1-digit list markers
            continue
        if tok in corpus or tok.rstrip("%") in corpus:
            continue
        missing.append(tok)
    return missing


def main():
    rows = findings_md()
    doc = [read(PARTS / "d5.md"), "\n---\n",
           "# D1 — Verdicts on the VP's claims\n",
           "**C1 verdict: do not bring job-board integration forward.** Deciding number: "
           "job-board hire yield 3.4% (Wilson 95% CI [1.7%, 6.6%], n=234) against 6.7% "
           "all-channel. Raw share 26.9%, cleaned 34.8%. Confidence High on the yield, "
           "Low on the share (n=23<30). The verdict holds at ±10% on the deciding number "
           "(3.1%-3.8%, still below referral's 10.8% CI floor).\n\n"
           "**C2 verdict: build something different — make the number trustworthy before "
           "moving it.** Deciding number: cleaned acceptance 82.1% (CI [64.4%, 92.1%], "
           "n=28), range 69.7%-84.8%. Confidence Low: n<30 and the range spans the "
           "decision.\n\n"
           "Differences whose CIs overlap (job board vs Agency, Career Site, LinkedIn "
           "individually) are **too small to act on**. Only the job-board/referral gap "
           "is claimed: [1.7, 6.6] vs [10.8, 60.3] do not overlap.\n",
           demote(read(OUT / "metrics.md")), "\n---\n",
           "# D2 — Q3 roadmap\n", demote(read(OUT / "roadmap.md")).replace("## D2 - Q3 roadmap\n", ""), "\n---\n",
           read(PARTS / "d3.md"), "\n---\n",
           "# D4 — Data audit\n", demote(read(OUT / "dq_summary.md")), "\n",
           demote(read(OUT / "waterfall.md")), audit_changed_section()]
    (DOCS / "submission.md").write_text("".join(doc), encoding="utf-8")

    missing = check_numbers(rows)
    print("out/findings.md: {} rows".format(len(rows)))
    print("docs/submission.md assembled, order D5 -> D1 -> D2 -> D3 -> D4")
    if missing:
        print("NUMBER CHECK - tokens in the memo not found in out/: {}".format(missing))
    else:
        print("NUMBER CHECK - every number in the memo traces to out/. No mismatches.")


if __name__ == "__main__":
    main()
