# Data quality audit (D4)

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

