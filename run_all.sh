#!/usr/bin/env bash
# Regenerate every number from a fresh clone + .env.
set -euo pipefail
cd "$(dirname "$0")"

PY=.venv/bin/python
if [ ! -x "$PY" ]; then
  # Pick an interpreter that is actually >= 3.10. A bare `python3` is 3.9 on stock
  # macOS, and the pinned deps have no 3.9 build, so this must not be left to PATH.
  BOOT=""
  for c in python3.13 python3.12 python3.11 python3.10 python3; do
    if command -v "$c" >/dev/null 2>&1 && "$c" -c 'import sys; sys.exit(0 if sys.version_info[:2] >= (3,10) else 1)' 2>/dev/null; then
      BOOT="$c"; break
    fi
  done
  if [ -z "$BOOT" ]; then
    echo "ERROR: no Python 3.10+ found on PATH. Install one, e.g. brew install python@3.12" >&2
    exit 1
  fi
  echo "== creating venv with $($BOOT --version) =="
  "$BOOT" -m venv .venv
fi
.venv/bin/python -m pip install --quiet --upgrade pip
.venv/bin/python -m pip install --quiet -r requirements.txt

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
run_step metrics   src/metrics.py
run_step roadmap   src/roadmap.py
run_step report    src/report.py

if [ -d tests ]; then
  echo "== tests =="
  .venv/bin/python -m pytest -q tests
else
  echo "== tests == (not built yet: tests/)"
fi
