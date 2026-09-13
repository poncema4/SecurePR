#!/usr/bin/env bash
set -euo pipefail

if [[ -x ".venv/bin/python" ]]; then
  PYTHON=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON="python"
else
  echo "Python 3 is required but was not found." >&2
  exit 1
fi

"$PYTHON" -m pytest -q
"$PYTHON" -m compileall -q app tests
