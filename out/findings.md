# Findings

Generated from `out/findings.csv`. Every value is produced by the named script.

| Claim | Metric | Value | Method | Confidence | n | Script |
|---|---|---|---|---|---|---|
| C1 | Job-board hire yield (hires / applications) | **3.4% [CI 1.7-6.6]** | cleaned applications; only the literal label 'Job Board'. LinkedIn (31 candidates) is reported separately because it is a specific product and counting it moves C1 by +13 pts; Career Site is owned inbound, not a board. | High | 234 | `src/metrics.py` |
| C1 | Referral hire yield | **30.0% [CI 10.8-60.3]** | cleaned applications | Low (n<30) | 10 | `src/metrics.py` |
| C1 | Job-board share of hires (raw) | **26.9%** | Stage=='Hired', strict 'Job Board', no cleaning | Low (n<30) | 26 | `src/metrics.py` |
| C1 | Job-board share of hires (cleaned) | **34.8%** | Stage 3 cleaning rules applied | Low (n<30) | 23 | `src/metrics.py` |
| C1 | Job-board share of applications | **67.8%** | cleaned applications | High | 345 | `src/metrics.py` |
| C1 | Screening load per job-board hire | **29 applications** | cleaned apps / cleaned hires | Medium | 234 | `src/metrics.py` |
| C2 | Offer acceptance rate (cleaned) | **82.1% [CI 64.4-92.1]** | collapse re-issued offers; exclude two-req conflict; exclude offers with no decision; exclude contradictory Pending | Low (n<30) | 28 | `src/metrics.py` |
| C2 | Offer acceptance rate (raw) | **72.2%** | accepted / all offers incl. Pending | Low (n<30) | 36 | `src/metrics.py` |
| C2 | Offer acceptance, unresolved-record range | **69.7% - 84.8%** | D3 spec (src/acceptance.py): lower = all 5 unresolved count as declined, upper = all accepted | Low | 33 | `src/metrics.py` |
| C2 | Genuine declines | **5** | Status=='Declined' after cleaning; counts not a rate because n<30 | Low (n<30) | 28 | `src/metrics.py` |
| D2 | Source-signal conflict (Referred By vs Candidates.Source) | **24 of 27 referred applications** | audit anomaly 1 | High | 27 | `src/metrics.py` |
| D2 | Offers blocked from a trustworthy rate | **7 of 36** | contradictory Pending (4) + open (1) + conflict (2) | High | 36 | `src/metrics.py` |
| D2 | Duplicate candidate records | **12 of 300 (4.0%)** | normalised name+phone | High | 300 | `src/metrics.py` |
| D2 | Offers outside the req salary band | **7 of 36 (19.4%)** | Base CTC vs Salary Band Min/Max | High | 36 | `src/metrics.py` |
| D2 | Hires with all-negative interview recommendations | **8 of 26 (30.8%)** | all Recommendation in No Hire/Strong No Hire | High | 26 | `src/metrics.py` |
