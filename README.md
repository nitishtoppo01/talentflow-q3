# TalentFlow Q3 roadmap exercise

Analysis of Acme's Airtable base (`appYePRAI75PMbQNQ`) to test two VP People claims
and set a 6-engineer-week Q3 roadmap.

- C1: job boards are the biggest channel and bring 26.9% of hires.
- C2: offer acceptance is around 72%.

Standing rules for the analysis are in `CLAUDE.md`.

## Timing

| | |
|---|---|
| Prep (tooling install, pre-flight) | from ~08:30 IST |
| **Exercise start** | **08:54 AM IST (2026-09-16T03:24:15Z)** |
| Exercise end | _to be filled at Stage 7_ |
| Total minutes | _to be filled at Stage 7_ |

## Reproduce

Requires Python 3.10+ (built and run on 3.12.14) and an Airtable token with read access
to the base.

```bash
git clone <repo> talentflow-q3
cd talentflow-q3
printf 'AIRTABLE_TOKEN=<your key>\n' > .env   # 82-char personal access token
bash run_all.sh
```

`run_all.sh` creates `.venv`, installs pinned deps, then runs
pull -> profile -> audit -> metrics -> tests. Stages not yet built are skipped with a
notice.

## Layout

| Path | What |
|---|---|
| `src/pull.py` | Pulls all 8 tables into `data/raw/` |
| `src/verify_pull.py` | Proves the pull is complete (pages, offsets, unique IDs) |
| `data/raw/*.json` | Cached records, verbatim from the API |
| `data/manifest.json` | Pull time (UTC), records per table, requests, retries |
| `data/pull_log.csv` | One row per HTTP request |
| `out/` | Every generated number |
| `docs/submission.md` | Deliverables, ordered D5 -> D1 -> D2 -> D3 -> D4 |

`.env`, `data/` and `.venv/` are git-ignored: the token is secret and the cache holds
candidate PII.
