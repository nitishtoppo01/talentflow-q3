# D5 — Memo: Q3 recruiting-ops roadmap

**Decision.** Build offer-metric trust, application-time source capture and write-time
validation: 5.5 of our 6 engineer-weeks. Do not build job-board integration this quarter —
job-board hire yield is 3.4% against 6.7% all-channel. Tell the VP both her numbers are
arithmetically correct and neither supports the conclusion drawn from it.

**What's true.**

| Claim | VP's number | Cleaned | CI | Confidence |
|---|---|---|---|---|
| C1 job-board share of hires | 26.9% | 34.8% | — (n=23) | Low (n<30) |
| C1 **deciding number**: job-board hire yield | — | **3.4%** | [1.7, 6.6] | **High** (n=234) |
| C2 offer acceptance | 72.2% | **82.1%** | [64.4, 92.1] | Low (n=28<30) |

C1 reproduces exactly as 7 of 26 hires — and referral is also 26.9%, on 13 applications
instead of 236. Job boards need 29 applications per hire; referral needs 3. C2's honest
answer is a range, 69.7%–84.8%, because 5 offers cannot be classified.

**Q3 plan (5.5 of 6 engineer-weeks; estimates to confirm with the engineering lead).**

1. **Offer lifecycle states + decline reasons — 2.0 ew.** 4 contradictory `Pending` offers
   move the headline 9.9 points.
2. **Source captured at application time — 2.0 ew.** 24 of 27 referred applications carry a
   channel label that contradicts their own referrer link.
3. **Write-time validation — 1.5 ew.** 7 date-order violations and 7 offers outside their
   requisition's salary band.

**Not building.** Job-board integration (3.0 ew): 3.4% yield [1.7–6.6] vs 6.7% all-channel.
Referral tooling (2.0 ew): best yield at 30.0% but a 49-point CI [10.8–60.3] on n=10.
Time-to-offer alerts (1.0 ew): declined offers were *faster* (31 days vs 35), on n=5.

**Data risks.** Channel attribution — 24 of 27 referred applications (88.9%) contradict
their source label. Offer status — 7 of 36 offers (19.4%) cannot be classified. Decision
trail — 8 of 26 hires (30.8%) had every interview recommendation negative.

**Next.** (1) Which channel signal is true? If `Referred By` wins, referral share of hires
falls from 26.9% to 11.5% and referral tooling drops further down the list. (2) Are the 4
contradictory `Pending` offers accepted or declined? The answer moves C2 anywhere between
69.7% and 84.8%. (3) Why are 7 of 36 offers outside their salary band? If comp approval is
broken, that outranks build 3.

**Asks.** From Acme: one recruiter for two hours to adjudicate 7 offer records, and
confirmation that `Target Close` is not a gate — 251 applications (71.7%) arrive after it.
From our CEO: agreement to tell the VP "not yet, and here is the 2.0-engineer-week
experiment that could overturn it within one quarter", rather than "no".

---
# D1 — Verdicts on the VP's claims
**C1 verdict: do not bring job-board integration forward.** Deciding number: job-board hire yield 3.4% (Wilson 95% CI [1.7%, 6.6%], n=234) against 6.7% all-channel. Raw share 26.9%, cleaned 34.8%. Confidence High on the yield, Low on the share (n=23<30). The verdict holds at ±10% on the deciding number (3.1%-3.8%, still below referral's 10.8% CI floor).

**C2 verdict: build something different — make the number trustworthy before moving it.** Deciding number: cleaned acceptance 82.1% (CI [64.4%, 92.1%], n=28), range 69.7%-84.8%. Confidence Low: n<30 and the range spans the decision.

Differences whose CIs overlap (job board vs Agency, Career Site, LinkedIn individually) are **too small to act on**. Only the job-board/referral gap is claimed: [1.7, 6.6] vs [10.8, 60.3] do not overlap.
## D1 metrics

## Claim 1 - channels

**Job-board grouping rule:** only the literal label 'Job Board'. LinkedIn (31 candidates) is reported separately because it is a specific product and counting it moves C1 by +13 pts; Career Site is owned inbound, not a board.

| Channel | Apps | Share of apps | Hires | Share of hires | Hire yield | Wilson 95% CI on yield |
|---|---|---|---|---|---|---|
| Job Board | 234 | 67.8% | 8 | 34.8% | **3.4%** | [1.7%, 6.6%] |
| Agency | 35 | 10.1% | 4 | 17.4% | **11.4%** | [4.5%, 26.0%] |
| Career Site | 31 | 9.0% | 5 | 21.7% | **16.1%** | [7.1%, 32.6%] |
| LinkedIn | 31 | 9.0% | 3 | 13.0% | **9.7%** | [3.3%, 24.9%] |
| Referral | 10 | 2.9% | 3 | 13.0% | **30.0%** | [10.8%, 60.3%] |
| Campus | 4 | 1.2% | 0 | 0.0% | **0.0%** | [0.0%, 49.0%] |

### By quarter

| Quarter | JB apps | JB hires | JB yield | All hires | JB share of hires |
|---|---|---|---|---|---|
| 2025Q2 | 3 | 0 | 0.0% | 0 | - |
| 2025Q3 | 17 | 2 | 11.8% | 2 | 100.0% |
| 2025Q4 | 26 | 4 | 15.4% | 6 | 66.7% |
| 2026Q1 | 44 | 0 | 0.0% | 3 | 0.0% |
| 2026Q2 | 109 | 2 | 1.8% | 12 | 16.7% |
| 2026Q3 | 35 | 0 | 0.0% | 0 | - |

## Claim 2 - offer acceptance

Cleaned rate: **82.1%** (Wilson 95% CI [64.4%, 92.1%], n=28).
Unresolved-record range: **71.9% - 84.4%**.

### Gap decomposition from the VP's 72.2%

| Cause | Effect | Running value | Note |
|---|---|---|---|
| Raw (the VP's number) | 26/36 | 72.2% |  |
| Re-issued / duplicate offers | -1 offer | 71.4% | normal negotiation |
| Two-req accept conflict | -2 offers | 69.7% | genuine data conflict |
| Genuinely open (maturity rule) | -1 offer | 71.9% | not yet a failure |
| Contradictory Pending status | -4 offers | 82.1% | status hygiene |
| Genuine declines remaining | 5 offers | 82.1% | the only real candidate behaviour |

### By quarter

| Quarter (Offered On) | Offers | Accepted | Rate | n>=30? |
|---|---|---|---|---|
| 2025Q4 | 8 | 7 | 7/8 | no |
| 2026Q1 | 5 | 4 | 4/5 | no |
| 2026Q2 | 14 | 8 | 8/14 | no |
| 2026Q3 | 8 | 6 | 6/8 | no |

---
# D2 — Q3 roadmap

All effort figures are **estimates to confirm with the engineering lead**, sized against a 6-engineer-week Q3 budget.

## Scored pool

| Opportunity | Problem size | Who is affected | Evidence | Effort (ew) | Confidence | Decision |
|---|---|---|---|---|---|---|
| Offer lifecycle states + decline reasons | 7 of 36 offers (19.4%) cannot be classified; 4 contradictory Pending move the headline 9.9 pts | Recruiters, VP People, anyone reading the acceptance number | High - every record inspected by hand | 2.0 | High | BUILD 1 |
| Source captured at application time (required picklist) | 24 of 27 referred applications (88.9%) carry a channel label that contradicts their referrer link; 17 are labelled 'Job Board' | Everyone who reads channel reporting, incl. the Q3 roadmap decision | High - two independent fields disagree on the same records | 2.0 | High | BUILD 2 |
| Write-time validation (required links, date order) | 7 date-order violations + 2 accept conflicts + 7 offers outside their salary band | Recruiters at data entry; every downstream metric | High - all counted from the live base | 1.5 | Medium | BUILD 3 |
| Candidate de-duplication | 12 of 300 candidates (4.0%) duplicate on name+phone; moves C1 by +3.9 pts but changes no verdict | Recruiters seeing the same person twice | High on the count, low on the consequence | 1.0 | Medium | DEFER |
| Job-board integration | 236 applications/quarter peak, but 3.4% hire yield [CI 1.7-6.6] vs 6.7% overall | Recruiters, who absorb the screening load | High - CIs do not overlap with referral | 3.0 | High | DO NOT BUILD |
| Referral tooling | Highest yield at 30.0%, but CI [10.8-60.3] on n=10 applications | Employees and recruiters | Low - 49-point CI, n well below 30 | 2.0 | Low (n<30) | DO NOT BUILD YET |
| Time-to-offer alerts | Median 35 days to offer for accepted vs 31 for declined - the difference runs the wrong way for the hypothesis, on n=5 declines | Recruiters | Low - n=5, correlation only | 1.0 | Low (n<30) | DO NOT BUILD |

## Build - 5.5 of 6 engineer-weeks

| # | Build | ew | The number that justifies it | Expected outcome | Why it sits here |
|---|---|---|---|---|---|
| 1 | Offer lifecycle states + decline reasons | 2.0 | 4 contradictory Pending offers move acceptance from 72.2% to 82.1% - 9.9 pts on 4 records | One acceptance number everyone agrees on, with a maturity rule so open offers stop counting as failures | First because it is a dependency: the VP wants the acceptance number moved, and no fix can be shown to work while 7 of 36 offers are unclassifiable. |
| 2 | Source captured at application time (required picklist) | 2.0 | 24 of 27 referred applications carry a contradicting channel label; C1 is 26.9% by one field and 11.5% by the other | Channel attribution that survives scrutiny, at the application level rather than inherited from the candidate | Second because the recommendation to hold job-board work rests on channel attribution - we should be able to defend that attribution before we act on it. |
| 3 | Write-time validation (required links, date order) | 1.5 | 7 date-order violations, 2 accept conflicts, 7 offers outside the req's salary band | The classes of error cleaned in this audit stop recurring | Third because it protects builds 1 and 2 rather than producing a number itself; doing it first would validate fields that build 2 is about to change. |

Total **5.5 engineer-weeks**, leaving 0.5 as buffer.

## Do not build

| Not building | The number against it | Opportunity cost | What would make us revisit |
|---|---|---|---|
| Job-board integration | 3.4% hire yield [CI 1.7-6.6] vs 6.7% overall; 29 applications screened per hire vs 3 for referral | 3.0 engineer-weeks - half the quarter, and it would displace both metric-trust builds | Revisit if the job-board yield CI lower bound rises above the all-channel yield, or if screening is automated so the marginal cost of an extra applicant approaches zero. |
| Referral tooling | 30.0% yield is the highest of any channel, but the CI is [10.8-60.3] on n=10 applications - a 49-point interval | 2.0 engineer-weeks bet on an interval that spans 'best channel' and 'ordinary' | Revisit at n>=30 referral applications, which build 2 will produce reliably; on current volume that is roughly 3 quarters away. |
| Time-to-offer alerts | Median days-to-offer is 35 for accepted offers and 31 for declined - the difference points the wrong way, on n=5 declines | 1.0 engineer-week spent on a hypothesis the data does not support | Revisit when declines reach n>=30, or if decline reasons start naming speed; today 3 of 5 name 'Counter Offer'. |

---
# D3 — Offer acceptance rate: metric specification

Reference implementation: `src/acceptance.py`. Tests: `tests/test_acceptance.py` (26 tests).
**If this prose and the tests disagree, the tests decide.**

Written against Acme's real fields: `Offers.Status` (`Accepted` 26, `Pending` 5,
`Declined` 5), `Offers.Offered On`, `Offers.Decision On`, `Offers.Decline Reason`,
`Offers.Application`.

## 1. Definition

| Item | Rule |
|---|---|
| **Unit of analysis** | The **offer episode**: one candidate × one job opening. Not the raw offer row. Acme has a real case (OFF-00008 / OFF-00035 on REQ-2025-019) of two `Accepted` offers five months apart at ₹16.2L then ₹22.7L — one negotiation, one outcome. |
| **Winning offer in an episode** | Latest `Offered On`; ties broken by latest `Decision On`, then highest `Offer ID`. Deterministic, so two engineers get the same row. |
| **Numerator** | Episodes whose winning offer has `Status = 'Accepted'`. |
| **Denominator** | Episodes that are **resolved and eligible**: numerator, plus episodes whose winning offer is `Declined`, `Withdrawn` or `Expired`. Everything else is excluded, unresolved, or open — and each is reported separately. |

## 2. Time window

| Item | Rule |
|---|---|
| **Which date places an episode in a period** | `Offered On` (the date sent). |
| **Why** | The cohort a recruiting team can act on is the offers it *made* in a period; keying on decision date lets a slow candidate silently move a period that was already reported closed. The cost is that recent periods stay provisional, which the dashboard states explicitly. |
| **Default window** | Trailing 4 complete quarters, plus the current quarter shown separately and labelled provisional. |
| **Offers still open** | **Maturity rule, no restatement.** An episode with no decision and `Offered On` within **45 days** of the reporting date is `open`: excluded from both the point estimate and the range, and counted in the "open offers" guardrail. Past periods are never restated; the rate is recomputed live and carries a provisional flag until every episode in the window resolves. |
| **Stale offers** | No decision and older than 45 days is **not** open — it is `unresolved` (see §3). |

## 3. Edge cases — every one resolved, no TBD

| Edge case | In or out | How it is counted |
|---|---|---|
| Pending / unanswered, ≤45 days | **Excluded** | `open`. Not a failure yet. Triggers the provisional label. |
| Pending / unanswered, >45 days | **Excluded from the point estimate** | `unresolved`. Enters the **range** only. |
| Expired | **Included** | Counts as not accepted — the company let it lapse. *(No `Expired` value exists in Acme's data today; the rule is forward-compatible.)* |
| Rescinded by the company | **Excluded** | Not a candidate decision. Tracked in the rescind-rate guardrail so it cannot be used to flatter the number. |
| Withdrawn by the candidate | **Included** | Counts as not accepted. A withdrawal is a decline. |
| Revised / re-issued | **Included once** | The episode's winning offer decides; earlier versions are excluded as `re-issued offer superseded by a later version`. |
| Duplicate records | **Included once** | Same episode key collapses to one row by the same winning-offer rule. |
| Accepted, then reneged or no-show | **Included as accepted** | Acceptance measures the decision when it was made. Reneges belong to a separate start-rate metric. **Spec dependency: Acme has no renege field — one is required before start-rate can be built.** |
| Offer with no linked application or candidate | **Excluded** | Reason: `no linked application` / `no linked candidate`. 0 records today. |
| Decision dated before the offer was sent | **Excluded** | Invalid record. 0 records today. |
| Status `Pending` with a `Decision On` date | **Excluded from the point estimate** | `unresolved` — cannot be classified either way. **4 records today**, and they move the headline 9.9 points. |
| Accepted but the application is Rejected or Withdrawn | **Excluded** | Unresolvable conflict between two tables. 0 records today. |
| Internal candidates | **Included** | Counted like any other. **Spec dependency: no field distinguishes them today**; once one exists, report as a segment, never as an exclusion. |
| More than one accepted offer for one candidate — same opening | **Included once** | A revision. Collapsed by the episode rule. |
| More than one accepted offer for one candidate — different openings | **Excluded, all of that candidate's episodes** | One person cannot take two jobs. 1 candidate (candidate of OFF-00005 / OFF-00030), 2 episodes today. |
| Test records | **Excluded** | Exact-value match on `test, dummy, sample, asdf, xxx, foo` in any text field. **Never substring matching** — that flags `Lead QA Engineer` and the phrase "did not test the solution", giving 21 false positives and 0 true ones. |
| Timezone for period boundaries | **Asia/Kolkata (UTC+05:30)** | Every `Offers` date is date-only and every Acme location is Indian (Bengaluru, Mumbai, Noida, Remote), so period edges are IST calendar days. A UTC boundary would move a 31 March offer into Q2. |

## 4. Dashboard behaviour

| Rule | Implementation |
|---|---|
| Show `n` beside every rate | `payload["n"]` |
| Below minimum n, show counts | `MIN_N = 30`. Acme is at n=28, so the dashboard shows **"23/28"**, not "82.1%". |
| Excluded records by reason | `payload["excluded"]`, e.g. `{re-issued superseded: 1, accepted on two openings: 2}` |
| Range, not false precision | Lower = all unresolved count as declined; upper = all accepted. Acme today: **69.7% – 84.8%** |
| Provisional label | Set whenever any episode in the window is `open` |
| Guardrails shown alongside | Rescind rate (`0/36`), open offers older than 45 days (`1`), median days to decision (`11`). These exist so the headline cannot be improved just by redefining the denominator — narrowing the denominator raises the rate but shows up immediately in the exclusion counts and the rescind rate. |

## 5. The number this spec produces

| | |
|---|---|
| Accepted / denominator | **23 / 28** |
| Rate | **82.1%** (Wilson 95% CI [64.4%, 92.1%]) |
| Dashboard display | `23/28` — n is below 30 |
| Range over 5 unresolved | **69.7% – 84.8%** |
| Excluded | 1 superseded re-issue, 2 two-opening conflict |
| VP's stated figure | 72.2% (26/36, all Pending counted as failures) |

`src/metrics.py` asserts its own C2 number against `src/acceptance.py` and fails the
build if they diverge, so there is exactly one definition in the repo.

---
# D4 — Data audit
## Data quality audit (D4)

Every count below is produced by `src/audit.py` from `data/raw/`.

## Records with at least one issue

| Table | Records | With >=1 issue | % |
|---|---|---|---|
| Departments | 8 | 0 | 0.0% |
| People | 14 | 0 | 0.0% |
| Job Openings | 24 | 21 | 87.5% |
| Candidates | 300 | 95 | 31.7% |
| Applications | 350 | 350 | 100.0% |
| Interviews | 160 | 0 | 0.0% |
| Offers | 36 | 30 | 83.3% |
| Findings | 0 | 0 | 0.0% |

## Issues found (19 distinct checks fired)

| Table | Field | Check | n | % | Metric | Treatment |
|---|---|---|---|---|---|---|
| Applications | createdTime | every record in every table shares one createdTime date (2026-08-27) | 350 | 100.0% | both | flag only |
| Applications | Applied On | application submitted after the opening's target close date | 251 | 71.7% | C1 | flag only |
| Candidates | Notice Period Days | value <= 0 | 33 | 11.0% | none | flag only |
| Candidates | Source | source label names a specific product, not a channel class | 31 | 10.3% | C1 | flag only |
| Candidates | Years Experience | value <= 0 | 25 | 8.3% | none | flag only |
| Applications | Referred By vs Candidates.Source | application has a referrer link but the candidate's Source says another channel | 24 | 6.9% | C1 | fix |
| Offers | Joining Bonus | value <= 0 | 23 | 63.9% | none | flag only |
| Job Openings | Hiring Manager | hiring manager sits outside the opening's department | 21 | 87.5% | none | flag only |
| Candidates | Full Name + Phone | duplicate normalised name + phone | 12 | 4.0% | C1 | exclude |
| Job Openings | Status | job not marked Filled but has hired applications | 10 | 41.7% | C1 | flag only |
| Applications | Stage vs Interviews.Recommendation | hired although every interview recommendation was negative | 8 | 2.3% | C1 | flag only |
| Offers | Base CTC | offer outside the requisition's salary band | 7 | 19.4% | C2 | flag only |
| Applications | Candidate + Opening | same candidate applied to the same opening more than once | 6 | 1.7% | C1 | flag only |
| Offers | Status | candidate with more than one accepted offer | 4 | 11.1% | C2 | fix |
| Job Openings | Status / Headcount | job marked Filled but hire count != headcount | 4 | 16.7% | C1 | flag only |
| Applications | Proposed Start Date | out of order: Proposed Start Date before Decision On | 4 | 1.1% | both | flag only |
| Applications | Applied On | out of order: Applied On before Opened On | 3 | 0.9% | both | flag only |
| Offers | Proposed Start Date | date in the future | 2 | 5.6% | none | flag only |
| Offers | Decision On | field absent or empty | 1 | 2.8% | C2 | flag only |

## Re-labelled as normal business behaviour, not bad data

| Issue | n | Why it is normal |
|---|---|---|
| application submitted after the opening's target close date | 251 | Target Close is a target, not a gate; 71.7% of applications arrive after it, so this is how Acme operates, not an error |
| hiring manager sits outside the opening's department | 21 | only 4 people hold Role='Hiring Manager' across 8 departments and 24 reqs, so cross-department HMs are unavoidable in an org this size |
| value <= 0 (Joining Bonus 23, Notice Period 33, Years Experience 25) | 81 | zero bonus, zero notice period and a fresher with zero years are all real values |
| date in the future (Proposed Start Date) | 2 | a start date in the future is the expected state for a recent offer |
| more than one offer per application / candidate x req | 2 | a re-issued offer at a higher salary is normal negotiation; it must be collapsed, not excluded |
| job not marked Filled but has hired applications | 10 | a multi-headcount req stays Open after its first hire |
| candidate with no application | - | a sourced-but-never-applied candidate is a normal pipeline state |

## Cleaning waterfall

Each row applies the rule above it as well. Produced by `src/waterfall.py`.

## C1 - job-board share of hires

| Step | Job-board hires | Total hires | Value | Note |
|---|---|---|---|---|
| 0. Raw - every application, strict 'Job Board' label | 7 | 26 | 26.9% | the VP's number |
| 1. + collapse duplicate candidates (name+phone, 12 records) | 8 | 26 | 30.8% | same source label, so no movement expected |
| 2. + collapse duplicate applications (same candidate x opening) | 8 | 25 | 32.0% | 3 applications dropped |
| 3. + exclude the candidate accepted on two different reqs | 8 | 23 | 34.8% | unresolvable conflict, 2 applications dropped |
| 4. ALT grouping: count LinkedIn as a job board too | 11 | 23 | 47.8% | a grouping choice, not a cleaning rule |

**Largest mover:** 4. ALT grouping: count LinkedIn as a job board too (+20.9 pts from raw).

## C2 - offer acceptance

| Step | Accepted | Denominator | Value | Note |
|---|---|---|---|---|
| 0. Raw - accepted / all offers incl. Pending | 26 | 36 | 72.2% |  |
| 1. + collapse re-issued offers (same candidate x req, keep latest) | 25 | 35 | 71.4% | NORMAL BUSINESS BEHAVIOUR, not bad data |
| 2. + exclude candidate accepted on two different reqs | 23 | 33 | 69.7% | GENUINE CONFLICT - one person cannot take two jobs |
| 3. + exclude offers still genuinely open (Pending, no Decision On) | 23 | 32 | 71.9% | maturity rule: an undecided offer is not yet a failure |
| 4. + exclude contradictory Pending (status Pending, decision dated) | 23 | 28 | 82.1% | STATUS CONFLICT - cannot be classified either way |
| 5. RANGE over the 4 unresolved records | 23 | 32 | range | lower 71.9% (all declined) .. upper 84.4% (all accepted) |

**Largest mover:** 4. + exclude contradictory Pending (status Pending, decision dated) (+9.9 pts from raw).

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
