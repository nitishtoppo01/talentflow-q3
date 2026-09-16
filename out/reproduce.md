# Reproducing the VP's numbers

Enumeration only - no judgement on which definition is right.

## Fields that could define each concept (no choice made yet)

**(a) hiring channel / source**

| Field | Note |
|---|---|
| `Candidates.Source` | 300/300 present; 6 labels; candidate-level, not application-level |
| `Applications.Referred By` | 27/350 present; link to People; application-level referral signal |
| `People.Referrals Made` | 12/14 present; the same referral edge seen from the employee side |

**(b) 'a hire'**

| Field | Note |
|---|---|
| `Applications.Stage == 'Hired'` | 26/350 |
| `Offers.Status == 'Accepted'` | 26/36 offers |
| `Applications.Status == 'Closed'` | 245/350 - closed includes rejections, not a hire signal |
| `Job Openings.Status` | req-level fill signal, 24 rows |

**(c) offer status**

| Field | Note |
|---|---|
| `Offers.Status` | Accepted 26, Pending 5, Declined 5 |
| `Offers.Decline Reason` | 5/36 present |
| `Applications.Stage == 'Offer'` | 10/350 |

**(d) offer dates**

| Field | Note |
|---|---|
| `Offers.Offered On` | 36/36, date-only |
| `Offers.Decision On` | 35/36, date-only |
| `Offers.Proposed Start Date` | 36/36, date-only, 2 in the future |
| `Applications.Offered On` | 36/350, date-only, mirrors Offers.Offered On |

## C1 - 'job boards bring 26.9% of hires'

| Hire definition | 'Job board' labels | Dedup | Window | Hires from job board | Total hires | % | Matches 26.9%? |
|---|---|---|---|---|---|---|---|
| Applications.Stage == 'Hired' | +LinkedIn | per application | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| Applications.Stage == 'Hired' | +LinkedIn | per candidate | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| Applications.Stage == 'Hired' | +LinkedIn +Career Site | per application | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| Applications.Stage == 'Hired' | +LinkedIn +Career Site | per candidate | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| Applications.Stage == 'Hired' | all inbound (not Referral/Campus) | per application | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| Applications.Stage == 'Hired' | all inbound (not Referral/Campus) | per candidate | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| Applications.Stage == 'Hired' | strict: {'Job Board'} | per application | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| Applications.Stage == 'Hired' | strict: {'Job Board'} | per candidate | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| Applications.Stage == 'Hired' | +LinkedIn | per application | Applied On in 2025Q4 | 3 | 6 | 50.0% |  |
| Applications.Stage == 'Hired' | +LinkedIn | per candidate | Applied On in 2025Q4 | 3 | 6 | 50.0% |  |
| Applications.Stage == 'Hired' | +LinkedIn +Career Site | per application | Applied On in 2025Q4 | 4 | 6 | 66.7% |  |
| Applications.Stage == 'Hired' | +LinkedIn +Career Site | per candidate | Applied On in 2025Q4 | 4 | 6 | 66.7% |  |
| Applications.Stage == 'Hired' | all inbound (not Referral/Campus) | per application | Applied On in 2025Q4 | 4 | 6 | 66.7% |  |
| Applications.Stage == 'Hired' | all inbound (not Referral/Campus) | per candidate | Applied On in 2025Q4 | 4 | 6 | 66.7% |  |
| Applications.Stage == 'Hired' | strict: {'Job Board'} | per application | Applied On in 2025Q4 | 3 | 6 | 50.0% |  |
| Applications.Stage == 'Hired' | strict: {'Job Board'} | per candidate | Applied On in 2025Q4 | 3 | 6 | 50.0% |  |
| Applications.Stage == 'Hired' | +LinkedIn | per application | Applied On in 2026Q1 | 0 | 4 | 0.0% |  |
| Applications.Stage == 'Hired' | +LinkedIn | per candidate | Applied On in 2026Q1 | 0 | 4 | 0.0% |  |
| Applications.Stage == 'Hired' | +LinkedIn +Career Site | per application | Applied On in 2026Q1 | 1 | 4 | 25.0% |  |
| Applications.Stage == 'Hired' | +LinkedIn +Career Site | per candidate | Applied On in 2026Q1 | 1 | 4 | 25.0% |  |
| Applications.Stage == 'Hired' | all inbound (not Referral/Campus) | per application | Applied On in 2026Q1 | 2 | 4 | 50.0% |  |
| Applications.Stage == 'Hired' | all inbound (not Referral/Campus) | per candidate | Applied On in 2026Q1 | 2 | 4 | 50.0% |  |
| Applications.Stage == 'Hired' | strict: {'Job Board'} | per application | Applied On in 2026Q1 | 0 | 4 | 0.0% |  |
| Applications.Stage == 'Hired' | strict: {'Job Board'} | per candidate | Applied On in 2026Q1 | 0 | 4 | 0.0% |  |
| Applications.Stage == 'Hired' | +LinkedIn | per application | Applied On in 2026Q2 | 5 | 14 | 35.7% |  |
| Applications.Stage == 'Hired' | +LinkedIn | per candidate | Applied On in 2026Q2 | 5 | 14 | 35.7% |  |
| Applications.Stage == 'Hired' | +LinkedIn +Career Site | per application | Applied On in 2026Q2 | 8 | 14 | 57.1% |  |
| Applications.Stage == 'Hired' | +LinkedIn +Career Site | per candidate | Applied On in 2026Q2 | 8 | 14 | 57.1% |  |
| Applications.Stage == 'Hired' | all inbound (not Referral/Campus) | per application | Applied On in 2026Q2 | 11 | 14 | 78.6% |  |
| Applications.Stage == 'Hired' | all inbound (not Referral/Campus) | per candidate | Applied On in 2026Q2 | 11 | 14 | 78.6% |  |
| Applications.Stage == 'Hired' | strict: {'Job Board'} | per application | Applied On in 2026Q2 | 2 | 14 | 14.3% |  |
| Applications.Stage == 'Hired' | strict: {'Job Board'} | per candidate | Applied On in 2026Q2 | 2 | 14 | 14.3% |  |
| Applications.Stage == 'Hired' | +LinkedIn | per application | all time | 10 | 26 | 38.5% |  |
| Applications.Stage == 'Hired' | +LinkedIn | per candidate | all time | 10 | 24 | 41.7% |  |
| Applications.Stage == 'Hired' | +LinkedIn +Career Site | per application | all time | 15 | 26 | 57.7% |  |
| Applications.Stage == 'Hired' | +LinkedIn +Career Site | per candidate | all time | 15 | 24 | 62.5% |  |
| Applications.Stage == 'Hired' | all inbound (not Referral/Campus) | per application | all time | 19 | 26 | 73.1% |  |
| Applications.Stage == 'Hired' | all inbound (not Referral/Campus) | per candidate | all time | 19 | 24 | 79.2% |  |
| Applications.Stage == 'Hired' | strict: {'Job Board'} | per application | all time | 7 | 26 | 26.9% | **YES** |
| Applications.Stage == 'Hired' | strict: {'Job Board'} | per candidate | all time | 7 | 24 | 29.2% |  |
| Offers.Status == 'Accepted' | +LinkedIn | per application | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| Offers.Status == 'Accepted' | +LinkedIn | per candidate | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| Offers.Status == 'Accepted' | +LinkedIn +Career Site | per application | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| Offers.Status == 'Accepted' | +LinkedIn +Career Site | per candidate | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| Offers.Status == 'Accepted' | all inbound (not Referral/Campus) | per application | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| Offers.Status == 'Accepted' | all inbound (not Referral/Campus) | per candidate | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| Offers.Status == 'Accepted' | strict: {'Job Board'} | per application | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| Offers.Status == 'Accepted' | strict: {'Job Board'} | per candidate | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| Offers.Status == 'Accepted' | +LinkedIn | per application | Applied On in 2025Q4 | 3 | 6 | 50.0% |  |
| Offers.Status == 'Accepted' | +LinkedIn | per candidate | Applied On in 2025Q4 | 3 | 6 | 50.0% |  |
| Offers.Status == 'Accepted' | +LinkedIn +Career Site | per application | Applied On in 2025Q4 | 4 | 6 | 66.7% |  |
| Offers.Status == 'Accepted' | +LinkedIn +Career Site | per candidate | Applied On in 2025Q4 | 4 | 6 | 66.7% |  |
| Offers.Status == 'Accepted' | all inbound (not Referral/Campus) | per application | Applied On in 2025Q4 | 4 | 6 | 66.7% |  |
| Offers.Status == 'Accepted' | all inbound (not Referral/Campus) | per candidate | Applied On in 2025Q4 | 4 | 6 | 66.7% |  |
| Offers.Status == 'Accepted' | strict: {'Job Board'} | per application | Applied On in 2025Q4 | 3 | 6 | 50.0% |  |
| Offers.Status == 'Accepted' | strict: {'Job Board'} | per candidate | Applied On in 2025Q4 | 3 | 6 | 50.0% |  |
| Offers.Status == 'Accepted' | +LinkedIn | per application | Applied On in 2026Q1 | 0 | 4 | 0.0% |  |
| Offers.Status == 'Accepted' | +LinkedIn | per candidate | Applied On in 2026Q1 | 0 | 4 | 0.0% |  |
| Offers.Status == 'Accepted' | +LinkedIn +Career Site | per application | Applied On in 2026Q1 | 1 | 4 | 25.0% |  |
| Offers.Status == 'Accepted' | +LinkedIn +Career Site | per candidate | Applied On in 2026Q1 | 1 | 4 | 25.0% |  |
| Offers.Status == 'Accepted' | all inbound (not Referral/Campus) | per application | Applied On in 2026Q1 | 2 | 4 | 50.0% |  |
| Offers.Status == 'Accepted' | all inbound (not Referral/Campus) | per candidate | Applied On in 2026Q1 | 2 | 4 | 50.0% |  |
| Offers.Status == 'Accepted' | strict: {'Job Board'} | per application | Applied On in 2026Q1 | 0 | 4 | 0.0% |  |
| Offers.Status == 'Accepted' | strict: {'Job Board'} | per candidate | Applied On in 2026Q1 | 0 | 4 | 0.0% |  |
| Offers.Status == 'Accepted' | +LinkedIn | per application | Applied On in 2026Q2 | 5 | 14 | 35.7% |  |
| Offers.Status == 'Accepted' | +LinkedIn | per candidate | Applied On in 2026Q2 | 5 | 14 | 35.7% |  |
| Offers.Status == 'Accepted' | +LinkedIn +Career Site | per application | Applied On in 2026Q2 | 8 | 14 | 57.1% |  |
| Offers.Status == 'Accepted' | +LinkedIn +Career Site | per candidate | Applied On in 2026Q2 | 8 | 14 | 57.1% |  |
| Offers.Status == 'Accepted' | all inbound (not Referral/Campus) | per application | Applied On in 2026Q2 | 11 | 14 | 78.6% |  |
| Offers.Status == 'Accepted' | all inbound (not Referral/Campus) | per candidate | Applied On in 2026Q2 | 11 | 14 | 78.6% |  |
| Offers.Status == 'Accepted' | strict: {'Job Board'} | per application | Applied On in 2026Q2 | 2 | 14 | 14.3% |  |
| Offers.Status == 'Accepted' | strict: {'Job Board'} | per candidate | Applied On in 2026Q2 | 2 | 14 | 14.3% |  |
| Offers.Status == 'Accepted' | +LinkedIn | per application | all time | 10 | 26 | 38.5% |  |
| Offers.Status == 'Accepted' | +LinkedIn | per candidate | all time | 10 | 24 | 41.7% |  |
| Offers.Status == 'Accepted' | +LinkedIn +Career Site | per application | all time | 15 | 26 | 57.7% |  |
| Offers.Status == 'Accepted' | +LinkedIn +Career Site | per candidate | all time | 15 | 24 | 62.5% |  |
| Offers.Status == 'Accepted' | all inbound (not Referral/Campus) | per application | all time | 19 | 26 | 73.1% |  |
| Offers.Status == 'Accepted' | all inbound (not Referral/Campus) | per candidate | all time | 19 | 24 | 79.2% |  |
| Offers.Status == 'Accepted' | strict: {'Job Board'} | per application | all time | 7 | 26 | 26.9% | **YES** |
| Offers.Status == 'Accepted' | strict: {'Job Board'} | per candidate | all time | 7 | 24 | 29.2% |  |
| any linked Offer (offer extended) | +LinkedIn | per application | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| any linked Offer (offer extended) | +LinkedIn | per candidate | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| any linked Offer (offer extended) | +LinkedIn +Career Site | per application | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| any linked Offer (offer extended) | +LinkedIn +Career Site | per candidate | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| any linked Offer (offer extended) | all inbound (not Referral/Campus) | per application | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| any linked Offer (offer extended) | all inbound (not Referral/Campus) | per candidate | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| any linked Offer (offer extended) | strict: {'Job Board'} | per application | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| any linked Offer (offer extended) | strict: {'Job Board'} | per candidate | Applied On in 2025Q3 | 2 | 2 | 100.0% |  |
| any linked Offer (offer extended) | +LinkedIn | per application | Applied On in 2025Q4 | 4 | 7 | 57.1% |  |
| any linked Offer (offer extended) | +LinkedIn | per candidate | Applied On in 2025Q4 | 4 | 7 | 57.1% |  |
| any linked Offer (offer extended) | +LinkedIn +Career Site | per application | Applied On in 2025Q4 | 5 | 7 | 71.4% |  |
| any linked Offer (offer extended) | +LinkedIn +Career Site | per candidate | Applied On in 2025Q4 | 5 | 7 | 71.4% |  |
| any linked Offer (offer extended) | all inbound (not Referral/Campus) | per application | Applied On in 2025Q4 | 5 | 7 | 71.4% |  |
| any linked Offer (offer extended) | all inbound (not Referral/Campus) | per candidate | Applied On in 2025Q4 | 5 | 7 | 71.4% |  |
| any linked Offer (offer extended) | strict: {'Job Board'} | per application | Applied On in 2025Q4 | 3 | 7 | 42.9% |  |
| any linked Offer (offer extended) | strict: {'Job Board'} | per candidate | Applied On in 2025Q4 | 3 | 7 | 42.9% |  |
| any linked Offer (offer extended) | +LinkedIn | per application | Applied On in 2026Q1 | 3 | 7 | 42.9% |  |
| any linked Offer (offer extended) | +LinkedIn | per candidate | Applied On in 2026Q1 | 3 | 7 | 42.9% |  |
| any linked Offer (offer extended) | +LinkedIn +Career Site | per application | Applied On in 2026Q1 | 4 | 7 | 57.1% |  |
| any linked Offer (offer extended) | +LinkedIn +Career Site | per candidate | Applied On in 2026Q1 | 4 | 7 | 57.1% |  |
| any linked Offer (offer extended) | all inbound (not Referral/Campus) | per application | Applied On in 2026Q1 | 5 | 7 | 71.4% |  |
| any linked Offer (offer extended) | all inbound (not Referral/Campus) | per candidate | Applied On in 2026Q1 | 5 | 7 | 71.4% |  |
| any linked Offer (offer extended) | strict: {'Job Board'} | per application | Applied On in 2026Q1 | 3 | 7 | 42.9% |  |
| any linked Offer (offer extended) | strict: {'Job Board'} | per candidate | Applied On in 2026Q1 | 3 | 7 | 42.9% |  |
| any linked Offer (offer extended) | +LinkedIn | per application | Applied On in 2026Q2 | 8 | 19 | 42.1% |  |
| any linked Offer (offer extended) | +LinkedIn | per candidate | Applied On in 2026Q2 | 8 | 19 | 42.1% |  |
| any linked Offer (offer extended) | +LinkedIn +Career Site | per application | Applied On in 2026Q2 | 11 | 19 | 57.9% |  |
| any linked Offer (offer extended) | +LinkedIn +Career Site | per candidate | Applied On in 2026Q2 | 11 | 19 | 57.9% |  |
| any linked Offer (offer extended) | all inbound (not Referral/Campus) | per application | Applied On in 2026Q2 | 16 | 19 | 84.2% |  |
| any linked Offer (offer extended) | all inbound (not Referral/Campus) | per candidate | Applied On in 2026Q2 | 16 | 19 | 84.2% |  |
| any linked Offer (offer extended) | strict: {'Job Board'} | per application | Applied On in 2026Q2 | 4 | 19 | 21.1% |  |
| any linked Offer (offer extended) | strict: {'Job Board'} | per candidate | Applied On in 2026Q2 | 4 | 19 | 21.1% |  |
| any linked Offer (offer extended) | +LinkedIn | per application | Applied On in 2026Q3 | 1 | 1 | 100.0% |  |
| any linked Offer (offer extended) | +LinkedIn | per candidate | Applied On in 2026Q3 | 1 | 1 | 100.0% |  |
| any linked Offer (offer extended) | +LinkedIn +Career Site | per application | Applied On in 2026Q3 | 1 | 1 | 100.0% |  |
| any linked Offer (offer extended) | +LinkedIn +Career Site | per candidate | Applied On in 2026Q3 | 1 | 1 | 100.0% |  |
| any linked Offer (offer extended) | all inbound (not Referral/Campus) | per application | Applied On in 2026Q3 | 1 | 1 | 100.0% |  |
| any linked Offer (offer extended) | all inbound (not Referral/Campus) | per candidate | Applied On in 2026Q3 | 1 | 1 | 100.0% |  |
| any linked Offer (offer extended) | strict: {'Job Board'} | per application | Applied On in 2026Q3 | 1 | 1 | 100.0% |  |
| any linked Offer (offer extended) | strict: {'Job Board'} | per candidate | Applied On in 2026Q3 | 1 | 1 | 100.0% |  |
| any linked Offer (offer extended) | +LinkedIn | per application | all time | 18 | 36 | 50.0% |  |
| any linked Offer (offer extended) | +LinkedIn | per candidate | all time | 16 | 32 | 50.0% |  |
| any linked Offer (offer extended) | +LinkedIn +Career Site | per application | all time | 23 | 36 | 63.9% |  |
| any linked Offer (offer extended) | +LinkedIn +Career Site | per candidate | all time | 21 | 32 | 65.6% |  |
| any linked Offer (offer extended) | all inbound (not Referral/Campus) | per application | all time | 29 | 36 | 80.6% |  |
| any linked Offer (offer extended) | all inbound (not Referral/Campus) | per candidate | all time | 27 | 32 | 84.4% |  |
| any linked Offer (offer extended) | strict: {'Job Board'} | per application | all time | 13 | 36 | 36.1% |  |
| any linked Offer (offer extended) | strict: {'Job Board'} | per candidate | all time | 11 | 32 | 34.4% |  |

## C2 - 'offer acceptance is around 72%'

Offers.Status counts: `Accepted`=26, `Pending`=5, `Declined`=5

| Unit | Denominator rule | Window | Accepted | Denominator | % | Matches ~72%? |
|---|---|---|---|---|---|---|
| one row per offer | all offers (incl. Pending) | all time | 26 | 36 | 72.2% | **YES** |
| one row per offer | exclude Pending | all time | 26 | 31 | 83.9% |  |
| one row per offer | Accepted + Declined only | all time | 26 | 31 | 83.9% |  |
| one row per offer | offers with a Decision On date | all time | 26 | 35 | 74.3% |  |
| one row per candidate x job | all episodes | all time | 25 | 35 | 71.4% | **YES** |
| one row per offer | all offers, window on Offered On | 2025Q4 | 7 | 8 | 87.5% |  |
| one row per offer | all offers, window on Offered On | 2026Q1 | 5 | 6 | 83.3% |  |
| one row per offer | all offers, window on Offered On | 2026Q2 | 8 | 14 | 57.1% |  |
| one row per offer | all offers, window on Offered On | 2026Q3 | 6 | 8 | 75.0% |  |
| one row per offer | all offers, window on Decision On | 2025Q4 | 6 | 6 | 100.0% |  |
| one row per offer | all offers, window on Decision On | 2026Q1 | 6 | 8 | 75.0% |  |
| one row per offer | all offers, window on Decision On | 2026Q2 | 8 | 12 | 66.7% |  |
| one row per offer | all offers, window on Decision On | 2026Q3 | 6 | 9 | 66.7% |  |

