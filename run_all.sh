#!/usr/bin/env bash
# Regenerate every number from a fresh clone + .env.
set -euo pipefail
cd "$(dirname "$0")"

PY=.venv/bin/python
if [ ! -x "$PY" ]; then
  echo "== creating venv =="
  python3 -m venv .venv
fi
.venv/bin/pip install --quiet -r requirements.txt

run_step () {   # run_step <label> <script>
  if [ -f "$2" ]; then
    echo "== $1 =="
    $PY "$2"
  else
    echo "== $1 == (not built yet: $2)"
  fi
}

echo "== pull =="
$PY src/pull.py
$PY src/verify_pull.py

run_step profile   src/profile.py
run_step reproduce src/reproduce.py
run_step audit     src/audit.py
run_step waterfall src/waterfall.py
run_step crosscheck src/crosscheck.py
run_step metrics src/metrics.py

if [ -d tests ]; then
  echo "== tests =="
  .venv/bin/python -m pytest -q tests
else
  echo "== tests == (not built yet: tests/)"
fi
