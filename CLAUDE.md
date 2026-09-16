# TalentFlow Q3 roadmap exercise — standing rules

## Context
- I am the PM for TalentFlow (a recruiting-ops product). Acme is our largest design partner.
- Data: Acme's Airtable base appYePRAI75PMbQNQ. It is read-only; writes return 403 by design.
  Tables: Departments, People, Job Openings, Candidates, Applications, Interviews, Offers, Findings.
- Budget: 6 engineer-weeks next quarter. This exercise has a hard 2-hour cap.
- The VP People's two claims are hypotheses to test, not requirements:
  C1: job boards are the biggest channel by a wide margin and bring 26.9% of hires, so job-board integration should move up.
  C2: offer acceptance is around 72% and needs to move.

## Data access
- Read the token from AIRTABLE_TOKEN in .env. Never print, log, echo or hard-code it.
- Pull each table once into data/raw/. Paginate with `offset` (pageSize=100). Send at most 4 requests per second.
  On HTTP 429, wait 35 seconds and retry. URL-encode table names ("Job Openings").
- After the pull, all analysis reads data/raw/ only. Make no further API calls.
- .env and data/ are git-ignored because the cache contains candidate PII.

## Airtable gotchas
- API responses leave out empty fields and unchecked checkboxes. Build each table's columns
  from the union of keys across records. Treat an absent checkbox as false and any other absent field as missing.
- Linked-record fields are arrays of record IDs, even when there is only one link.
  Check that every ID resolves and check how many links each record has.
- Computed fields (formula, rollup, lookup) can return error objects or arrays. Check value types.
- Date-only fields and UTC datetime fields must be converted to a common form before comparing them across tables.

## Analysis rules
- Never invent a number. Every number comes from a script in src/ and is written to out/.
- For every rate, report numerator, denominator, n and a Wilson 95% CI. If n < 30, report counts instead of a rate.
- Treat a difference as actionable only if the CIs don't overlap (a conservative test). Otherwise say it is too small to act on.
- Report every headline number both raw and cleaned, and name each cleaning rule applied.
- For every data-quality issue, give n, % of the table, and 3–5 example record IDs.
- Tag each statement as [Fact] (from data), [Inference] or [Assumption].
- Confidence levels:
  High = CI half-width ≤ 5 pts and the value moves ≤ 2 pts across cleaning rules.
  Medium = the direction holds but the size of the effect changes.
  Low = the decision could flip, or n < 30.
- Correlation is not causation. Say so where it matters.

## Output rules
- Prefer tables to prose. Write in an executive tone with no filler.
- Deliverables: docs/submission.md (D5 memo, then D1, D2, D3, D4) and out/findings.csv.
- `bash run_all.sh` must regenerate every number from a fresh clone plus .env.
- At the end of each stage, stop and wait for my review.
