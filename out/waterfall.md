# Cleaning waterfall

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

