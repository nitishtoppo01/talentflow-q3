# Data profile

Source: `data/raw/` only. No API calls.

## Departments (n=8)

| Field | % present | n present | Type(s) seen |
|---|---|---|---|
| Location | 100.0% | 8 | str |
| Headcount Budget | 100.0% | 8 | int |
| Job Openings | 100.0% | 8 | list[str] |
| People | 100.0% | 8 | list[str] |
| Code | 100.0% | 8 | str |
| Name | 100.0% | 8 | str |

### Categorical fields — exact values

**Location** (4 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'Noida'` | 4 |
| `'Bengaluru'` | 2 |
| `'Remote'` | 1 |
| `'Mumbai'` | 1 |

**Code** (8 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'FIN'` | 1 |
| `'PRD'` | 1 |
| `'POP'` | 1 |
| `'DAT'` | 1 |
| `'CS'` | 1 |
| `'ENG'` | 1 |
| `'MKT'` | 1 |
| `'SLS'` | 1 |

**Name** (8 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'Finance'` | 1 |
| `'Product'` | 1 |
| `'People Operations'` | 1 |
| `'Data'` | 1 |
| `'Customer Support'` | 1 |
| `'Engineering'` | 1 |
| `'Marketing'` | 1 |
| `'Sales'` | 1 |

### Dates and numbers

| Field | Kind | Min | Max | Future dates | Values <= 0 | Format |
|---|---|---|---|---|---|---|
| Headcount Budget | number | 7 | 39 | — | 0 | — |

### Link fields

| Field | Links to (n ids) | 0 links | 1 link | many links | unresolved ids |
|---|---|---|---|---|---|
| Job Openings | Job Openings (24) | 0 | 0 | 8 | 0 |
| People | People (14) | 0 | 2 | 6 | 0 |

## People (n=14)

| Field | % present | n present | Type(s) seen |
|---|---|---|---|
| Reqs as Recruiter | 28.6% | 4 | list[str] |
| Role | 100.0% | 14 | str |
| Full Name | 100.0% | 14 | str |
| Work Email | 100.0% | 14 | str |
| Department | 100.0% | 14 | list[str] |
| Joined On | 100.0% | 14 | str |
| Applications as Recruiter | 28.6% | 4 | list[str] |
| Referrals Made | 85.7% | 12 | list[str] |
| Interviews | 42.9% | 6 | list[str] |
| Reqs as Hiring Manager | 28.6% | 4 | list[str] |

### Categorical fields — exact values

**Role** (3 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'Interviewer'` | 6 |
| `'Recruiter'` | 4 |
| `'Hiring Manager'` | 4 |

**Full Name** (14 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'Sunil Jain'` | 1 |
| `'Deepak Dubey'` | 1 |
| `'Arjun Kapoor'` | 1 |
| `'Chetan Pandey'` | 1 |
| `'Lakshmi Khanna'` | 1 |
| `'Aarav Desai'` | 1 |
| `'Harsh Kaur'` | 1 |
| `'Nikhil Sinha'` | 1 |
| `'Zoya Nair'` | 1 |
| `'Grace Chen'` | 1 |
| `'Kavya Sethi'` | 1 |
| `'Rohit Yadav'` | 1 |
| `'Daniel Ibrahim'` | 1 |
| `'Rakesh Sethi'` | 1 |

**Work Email** (14 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'sunil.jain@example.com'` | 1 |
| `'deepak.dubey@example.com'` | 1 |
| `'arjun.kapoor@example.com'` | 1 |
| `'chetan.pandey@example.com'` | 1 |
| `'lakshmi.khanna@example.com'` | 1 |
| `'aarav.desai@example.com'` | 1 |
| `'harsh.kaur@example.com'` | 1 |
| `'nikhil.sinha@example.com'` | 1 |
| `'zoya.nair@example.com'` | 1 |
| `'grace.chen@example.com'` | 1 |
| `'kavya.sethi@example.com'` | 1 |
| `'rohit.yadav@example.com'` | 1 |
| `'daniel.ibrahim@example.com'` | 1 |
| `'rakesh.sethi@example.com'` | 1 |

**Joined On** (14 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'2021-08-20'` | 1 |
| `'2023-12-09'` | 1 |
| `'2023-08-19'` | 1 |
| `'2025-01-13'` | 1 |
| `'2024-07-29'` | 1 |
| `'2023-04-17'` | 1 |
| `'2022-07-09'` | 1 |
| `'2025-06-08'` | 1 |
| `'2022-01-20'` | 1 |
| `'2023-09-19'` | 1 |
| `'2022-02-05'` | 1 |
| `'2023-02-21'` | 1 |
| `'2024-09-01'` | 1 |
| `'2022-03-15'` | 1 |

### Dates and numbers

| Field | Kind | Min | Max | Future dates | Values <= 0 | Format |
|---|---|---|---|---|---|---|
| Joined On | date | 2021-08-20 | 2025-06-08 | 0 | — | date-only |

### Link fields

| Field | Links to (n ids) | 0 links | 1 link | many links | unresolved ids |
|---|---|---|---|---|---|
| Reqs as Recruiter | Job Openings (24) | 10 | 0 | 4 | 0 |
| Department | Departments (14) | 0 | 14 | 0 | 0 |
| Applications as Recruiter | Applications (350) | 10 | 0 | 4 | 0 |
| Referrals Made | Applications (27) | 2 | 3 | 9 | 0 |
| Interviews | Interviews (160) | 8 | 0 | 6 | 0 |
| Reqs as Hiring Manager | Job Openings (24) | 10 | 0 | 4 | 0 |

## Job Openings (n=24)

| Field | % present | n present | Type(s) seen |
|---|---|---|---|
| Target Close | 100.0% | 24 | str |
| Employment Type | 100.0% | 24 | str |
| Recruiter | 100.0% | 24 | list[str] |
| Opened On | 100.0% | 24 | str |
| Applications | 100.0% | 24 | list[str] |
| Salary Band Max | 100.0% | 24 | int |
| Hiring Manager | 100.0% | 24 | list[str] |
| Salary Band Min | 100.0% | 24 | int |
| Location | 100.0% | 24 | str |
| Status | 100.0% | 24 | str |
| Level | 100.0% | 24 | str |
| Department | 100.0% | 24 | list[str] |
| Headcount | 100.0% | 24 | int |
| Req ID | 100.0% | 24 | str |
| Title | 100.0% | 24 | str |

### Categorical fields — exact values

**Target Close** (24 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'2025-08-10'` | 1 |
| `'2025-12-06'` | 1 |
| `'2026-01-25'` | 1 |
| `'2025-09-22'` | 1 |
| `'2025-07-23'` | 1 |
| `'2026-05-22'` | 1 |
| `'2025-07-17'` | 1 |
| `'2026-01-08'` | 1 |
| `'2026-04-07'` | 1 |
| `'2026-04-25'` | 1 |
| `'2026-01-02'` | 1 |
| `'2025-07-01'` | 1 |
| `'2025-09-27'` | 1 |
| `'2026-05-06'` | 1 |
| `'2026-01-16'` | 1 |
| `'2026-08-03'` | 1 |
| `'2025-08-04'` | 1 |
| `'2026-04-14'` | 1 |
| `'2026-09-04'` | 1 |
| `'2026-07-01'` | 1 |
| `'2026-02-26'` | 1 |
| `'2026-02-03'` | 1 |
| `'2025-07-29'` | 1 |
| `'2025-07-06'` | 1 |

**Employment Type** (2 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'Full-time'` | 20 |
| `'Contract'` | 4 |

**Opened On** (24 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'2025-05-20'` | 1 |
| `'2025-10-30'` | 1 |
| `'2025-11-27'` | 1 |
| `'2025-07-23'` | 1 |
| `'2025-05-09'` | 1 |
| `'2026-03-26'` | 1 |
| `'2025-05-05'` | 1 |
| `'2025-09-24'` | 1 |
| `'2026-02-23'` | 1 |
| `'2026-03-03'` | 1 |
| `'2025-10-13'` | 1 |
| `'2025-05-03'` | 1 |
| `'2025-08-03'` | 1 |
| `'2026-04-01'` | 1 |
| `'2025-10-25'` | 1 |
| `'2026-04-09'` | 1 |
| `'2025-05-26'` | 1 |
| `'2026-02-27'` | 1 |
| `'2026-05-14'` | 1 |
| `'2026-03-31'` | 1 |
| `'2025-12-19'` | 1 |
| `'2025-12-24'` | 1 |
| `'2025-06-28'` | 1 |
| `'2025-03-19'` | 1 |

**Location** (4 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'Mumbai'` | 8 |
| `'Bengaluru'` | 7 |
| `'Noida'` | 5 |
| `'Remote'` | 4 |

**Status** (4 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'Open'` | 11 |
| `'Filled'` | 8 |
| `'On Hold'` | 3 |
| `'Cancelled'` | 2 |

**Level** (4 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'Senior'` | 8 |
| `'Junior'` | 8 |
| `'Mid'` | 5 |
| `'Lead'` | 3 |

**Req ID** (24 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'REQ-2025-013'` | 1 |
| `'REQ-2025-005'` | 1 |
| `'REQ-2025-004'` | 1 |
| `'REQ-2025-015'` | 1 |
| `'REQ-2025-024'` | 1 |
| `'REQ-2026-022'` | 1 |
| `'REQ-2025-020'` | 1 |
| `'REQ-2025-007'` | 1 |
| `'REQ-2026-017'` | 1 |
| `'REQ-2026-008'` | 1 |
| `'REQ-2025-001'` | 1 |
| `'REQ-2025-012'` | 1 |
| `'REQ-2025-003'` | 1 |
| `'REQ-2026-002'` | 1 |
| `'REQ-2025-016'` | 1 |
| `'REQ-2026-011'` | 1 |
| `'REQ-2025-018'` | 1 |
| `'REQ-2026-006'` | 1 |
| `'REQ-2026-021'` | 1 |
| `'REQ-2026-014'` | 1 |
| `'REQ-2025-010'` | 1 |
| `'REQ-2025-019'` | 1 |
| `'REQ-2025-009'` | 1 |
| `'REQ-2025-023'` | 1 |

**Title** (21 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'Junior Content Marketer'` | 2 |
| `'HR Generalist'` | 2 |
| `'Enterprise AE'` | 2 |
| `'Finance Manager'` | 1 |
| `'Financial Analyst'` | 1 |
| `'Junior Associate Product Manager'` | 1 |
| `'Data Engineer'` | 1 |
| `'Brand Manager'` | 1 |
| `'Associate Product Manager'` | 1 |
| `'Lead QA Engineer'` | 1 |
| `'Junior Data Analyst'` | 1 |
| `'Junior QA Engineer'` | 1 |
| `'Lead Support Specialist'` | 1 |
| `'Data Analyst'` | 1 |
| `'Junior Technical Support Engineer'` | 1 |
| `'Sales Development Rep'` | 1 |
| `'Lead HR Generalist'` | 1 |
| `'Junior Accountant'` | 1 |
| `'Support Specialist'` | 1 |
| `'Backend Engineer'` | 1 |
| `'Junior Product Designer'` | 1 |

### Dates and numbers

| Field | Kind | Min | Max | Future dates | Values <= 0 | Format |
|---|---|---|---|---|---|---|
| Target Close | date | 2025-07-01 | 2026-09-04 | 0 | — | date-only |
| Opened On | date | 2025-03-19 | 2026-05-14 | 0 | — | date-only |
| Salary Band Max | number | 800000 | 4500000 | — | 0 | — |
| Salary Band Min | number | 400000 | 2800000 | — | 0 | — |
| Headcount | number | 1 | 3 | — | 0 | — |

### Link fields

| Field | Links to (n ids) | 0 links | 1 link | many links | unresolved ids |
|---|---|---|---|---|---|
| Recruiter | People (24) | 0 | 24 | 0 | 0 |
| Applications | Applications (350) | 0 | 0 | 24 | 0 |
| Hiring Manager | People (24) | 0 | 24 | 0 | 0 |
| Department | Departments (24) | 0 | 24 | 0 | 0 |

## Candidates (n=300)

| Field | % present | n present | Type(s) seen |
|---|---|---|---|
| Full Name | 100.0% | 300 | str |
| Phone | 100.0% | 300 | str |
| Expected CTC | 100.0% | 300 | int |
| Created On | 100.0% | 300 | str |
| Candidate ID | 100.0% | 300 | str |
| Notice Period Days | 100.0% | 300 | int |
| Current CTC | 100.0% | 300 | int |
| City | 100.0% | 300 | str |
| Email | 100.0% | 300 | str |
| Current Company | 100.0% | 300 | str |
| Notes | 79.0% | 237 | str |
| Years Experience | 100.0% | 300 | float, int |
| Source | 100.0% | 300 | str |
| Applications | 100.0% | 300 | list[str] |

### Categorical fields — exact values

**City** (7 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'Pune'` | 53 |
| `'Remote'` | 43 |
| `'Mumbai'` | 43 |
| `'Hyderabad'` | 42 |
| `'Chennai'` | 40 |
| `'Bengaluru'` | 40 |
| `'Noida'` | 39 |

**Current Company** (18 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'Basalt Energy'` | 31 |
| `'Marigold Foods'` | 21 |
| `'Meridian Health'` | 21 |
| `'Parable Systems'` | 21 |
| `'Silverpine Analytics'` | 19 |
| `'Arcadia Retail'` | 18 |
| `'Zenlytics'` | 18 |
| `'Bluestone Labs'` | 18 |
| `'Harbourline'` | 18 |
| `'Copperfield Bank'` | 15 |
| `'Kettle & Co'` | 15 |
| `'Quillion'` | 15 |
| `'Vantage Mobility'` | 14 |
| `'Larkspur Software'` | 13 |
| `'Redthread'` | 13 |
| `'Northwind Telecom'` | 12 |
| `'Tidewater Logistics'` | 9 |
| `'Foxglove Media'` | 9 |

**Notes** (7 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'Referred internally. Available for a call after 6pm.'` | 38 |
| `'Reached out again after an earlier rejection.'` | 37 |
| `'Strong portfolio, thin on formal experience.'` | 35 |
| `'Currently on a notice period; flexible on start date.'` | 35 |
| `'Sourced from a conference list. Responsive over email.'` | 34 |
| `'Applied to two openings; consolidated onto the more senior one.'` | 33 |
| `'Asked about remote policy in the first call.'` | 25 |

**Source** (6 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'Job Board'` | 191 |
| `'Agency'` | 35 |
| `'LinkedIn'` | 31 |
| `'Career Site'` | 31 |
| `'Referral'` | 8 |
| `'Campus'` | 4 |

### Dates and numbers

| Field | Kind | Min | Max | Future dates | Values <= 0 | Format |
|---|---|---|---|---|---|---|
| Expected CTC | number | 286858 | 5310000 | — | 0 | — |
| Created On | date | 2025-03-01 | 2026-08-30 | 0 | — | date-only |
| Notice Period Days | number | 0 | 90 | — | 33 | — |
| Current CTC | number | 300000 | 4510000 | — | 0 | — |
| Years Experience | number | 0 | 17.1 | — | 25 | — |

### Link fields

| Field | Links to (n ids) | 0 links | 1 link | many links | unresolved ids |
|---|---|---|---|---|---|
| Applications | Applications (350) | 0 | 250 | 50 | 0 |

## Applications (n=350)

| Field | % present | n present | Type(s) seen |
|---|---|---|---|
| Recruiter | 100.0% | 350 | list[str] |
| Applied On | 100.0% | 350 | str |
| Candidate | 100.0% | 350 | list[str] |
| Closed On | 70.0% | 245 | str |
| Rejection Reason | 62.3% | 218 | str |
| Application ID | 100.0% | 350 | str |
| Screened On | 79.7% | 279 | str |
| Opening | 100.0% | 350 | list[str] |
| Stage | 100.0% | 350 | str |
| Status | 100.0% | 350 | str |
| Interviews | 40.9% | 143 | list[str] |
| First Interview On | 40.9% | 143 | str |
| Final Interview On | 14.3% | 50 | str |
| Offers | 10.3% | 36 | list[str] |
| Offered On | 10.3% | 36 | str |
| Referred By | 7.7% | 27 | list[str] |

### Categorical fields — exact values

**Rejection Reason** (7 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'Skills Mismatch'` | 49 |
| `'Culture Fit'` | 47 |
| `'Better Candidate'` | 45 |
| `'Comp Expectation'` | 26 |
| `'Position Cancelled'` | 18 |
| `'No Show'` | 18 |
| `'Withdrew'` | 15 |

**Stage** (7 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'Rejected'` | 200 |
| `'Applied'` | 45 |
| `'Screening'` | 32 |
| `'Hired'` | 26 |
| `'Interview'` | 23 |
| `'Withdrawn'` | 14 |
| `'Offer'` | 10 |

**Status** (2 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'Closed'` | 245 |
| `'Active'` | 105 |

### Dates and numbers

| Field | Kind | Min | Max | Future dates | Values <= 0 | Format |
|---|---|---|---|---|---|---|
| Applied On | date | 2025-05-06 | 2026-08-27 | 0 | — | date-only |
| Closed On | date | 2025-05-20 | 2026-08-17 | 0 | — | date-only |
| Screened On | date | 2025-05-08 | 2026-08-13 | 0 | — | date-only |
| First Interview On | date | 2025-08-29 | 2026-08-06 | 0 | — | date-only |
| Final Interview On | date | 2025-09-11 | 2026-08-02 | 0 | — | date-only |
| Offered On | date | 2025-10-14 | 2026-08-07 | 0 | — | date-only |

### Link fields

| Field | Links to (n ids) | 0 links | 1 link | many links | unresolved ids |
|---|---|---|---|---|---|
| Recruiter | People (350) | 0 | 350 | 0 | 0 |
| Candidate | Candidates (350) | 0 | 350 | 0 | 0 |
| Opening | Job Openings (350) | 0 | 350 | 0 | 0 |
| Interviews | Interviews (160) | 207 | 126 | 17 | 0 |
| Offers | Offers (36) | 314 | 36 | 0 | 0 |
| Referred By | People (27) | 323 | 27 | 0 | 0 |

## Interviews (n=160)

| Field | % present | n present | Type(s) seen |
|---|---|---|---|
| Application | 100.0% | 160 | list[str] |
| Scheduled On | 100.0% | 160 | str |
| Interview ID | 100.0% | 160 | str |
| Interviewer | 100.0% | 160 | list[str] |
| Round | 100.0% | 160 | str |
| Score | 88.8% | 142 | float, int |
| Recommendation | 88.8% | 142 | str |
| Outcome | 100.0% | 160 | str |
| Feedback | 88.8% | 142 | str |
| Completed On | 88.8% | 142 | str |

### Categorical fields — exact values

**Round** (5 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'Screen'` | 74 |
| `'Technical 1'` | 69 |
| `'Bar Raiser'` | 7 |
| `'Hiring Manager'` | 7 |
| `'Technical 2'` | 3 |

**Recommendation** (4 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'No Hire'` | 48 |
| `'Strong No Hire'` | 39 |
| `'Hire'` | 34 |
| `'Strong Hire'` | 21 |

**Outcome** (4 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'Completed'` | 138 |
| `'No Show'` | 10 |
| `'Cancelled'` | 7 |
| `'Rescheduled'` | 5 |

**Feedback** (12 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'Not convinced. Did not meet the bar for this level.'` | 28 |
| `'Missed the main edge case and did not test the solution.'` | 19 |
| `'Solid fundamentals. Needed a hint on the follow-up but recovered well.'` | 16 |
| `'Struggled with the core problem. Could not explain their own prior work.'` | 15 |
| `'Answers stayed surface level even after probing.'` | 13 |
| `'Could not complete the exercise. Defensive when given a hint.'` | 10 |
| `'Reasonable answers throughout. No red flags.'` | 10 |
| `'Good practical experience. Some gaps in scale but coachable.'` | 8 |
| `'Excellent depth on system design. Explained trade-offs without prompting.'` | 7 |
| `'Clear communicator, solved the problem two ways and compared them.'` | 6 |
| `'Strongest candidate in this loop. Would hire on the spot.'` | 6 |
| `'Significant gaps against the level. Not close on the fundamentals.'` | 4 |

### Dates and numbers

| Field | Kind | Min | Max | Future dates | Values <= 0 | Format |
|---|---|---|---|---|---|---|
| Scheduled On | date | 2025-08-10 | 2026-08-06 | 0 | — | date-only |
| Score | number | 1 | 5 | — | 0 | — |
| Completed On | date | 2025-08-10 | 2026-07-30 | 0 | — | date-only |

### Link fields

| Field | Links to (n ids) | 0 links | 1 link | many links | unresolved ids |
|---|---|---|---|---|---|
| Application | Applications (160) | 0 | 160 | 0 | 0 |
| Interviewer | People (160) | 0 | 160 | 0 | 0 |

## Offers (n=36)

| Field | % present | n present | Type(s) seen |
|---|---|---|---|
| Joining Bonus | 100.0% | 36 | int |
| Proposed Start Date | 100.0% | 36 | str |
| Application | 100.0% | 36 | list[str] |
| Base CTC | 100.0% | 36 | int |
| Offer ID | 100.0% | 36 | str |
| Status | 100.0% | 36 | str |
| Offered On | 100.0% | 36 | str |
| Decision On | 97.2% | 35 | str |
| Decline Reason | 13.9% | 5 | str |

### Categorical fields — exact values

**Status** (3 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'Accepted'` | 26 |
| `'Pending'` | 5 |
| `'Declined'` | 5 |

**Decline Reason** (3 distinct)

| Value (repr, so spaces/case are visible) | Count |
|---|---|
| `'Counter Offer'` | 3 |
| `'Location'` | 1 |
| `'Compensation'` | 1 |

### Dates and numbers

| Field | Kind | Min | Max | Future dates | Values <= 0 | Format |
|---|---|---|---|---|---|---|
| Joining Bonus | number | 0 | 100000 | — | 23 | — |
| Proposed Start Date | date | 2025-11-07 | 2026-10-01 | 2 | — | date-only |
| Base CTC | number | 440000 | 4180000 | — | 0 | — |
| Offered On | date | 2025-10-14 | 2026-08-07 | 0 | — | date-only |
| Decision On | date | 2025-10-17 | 2026-08-20 | 0 | — | date-only |

### Link fields

| Field | Links to (n ids) | 0 links | 1 link | many links | unresolved ids |
|---|---|---|---|---|---|
| Application | Applications (36) | 0 | 36 | 0 | 0 |

## Findings (n=0)

_Table is empty. Airtable exposes no field names for a table with zero records, so its schema is not observable from the API._

## Findings table — first 20 rows

**The Findings table is empty (0 records).**

No fields are observable and no rows exist, so it documents neither the 26.9% nor the ~72% claim.

