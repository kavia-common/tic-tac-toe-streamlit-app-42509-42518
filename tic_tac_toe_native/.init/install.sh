#!/usr/bin/env bash
set -euo pipefail
WS="/home/kavia/workspace/code-generation/tic-tac-toe-streamlit-app-42509-42518/tic_tac_toe_native"
cd "$WS"
# ensure venv python exists
if [ ! -x "/opt/venv/bin/python" ]; then
  echo "/opt/venv python not found, run env-001 first" >&2
  exit 3
fi
# check system python availability
command -v python3 >/dev/null 2>&1 || { echo "python3 not available" >&2; exit 2; }
# check venv python version (major >=3)
PYVER=$(/opt/venv/bin/python -c 'import sys; print("%d.%d"%(sys.version_info[0],sys.version_info[1]))')
major=$(echo "$PYVER" | cut -d. -f1)
if [ "${major:-0}" -lt 3 ]; then echo "Unsupported python version: $PYVER" >&2; exit 4; fi
# ensure system deps sqlite3 and curl
need_apt=()
command -v sqlite3 >/dev/null 2>&1 || need_apt+=(sqlite3)
command -v curl >/dev/null 2>&1 || need_apt+=(curl)
if [ ${#need_apt[@]} -gt 0 ]; then
  DEBIAN_FRONTEND=noninteractive sudo apt-get update -q && DEBIAN_FRONTEND=noninteractive sudo apt-get install -y -qq "${need_apt[@]}"
fi
# upgrade pip inside venv
/opt/venv/bin/python -m pip install --upgrade --quiet pip >/dev/null
# install python deps into venv (prefer requirements.txt)
if [ -f "$WS/requirements.txt" ]; then
  /opt/venv/bin/python -m pip install --no-input -r "$WS/requirements.txt"
else
  /opt/venv/bin/python -m pip install --no-input "streamlit>=1.20,<2" pytest
fi
# validate installs by importing and printing versions
/opt/venv/bin/python - <<'PY'
import sys
try:
    import streamlit, pytest
    print('STREAMLIT', getattr(streamlit, '__version__', 'unknown'))
    print('PYTEST', getattr(pytest, '__version__', 'unknown'))
except Exception as e:
    print('Dependency import failed:', e, file=sys.stderr)
    sys.exit(5)
PY
