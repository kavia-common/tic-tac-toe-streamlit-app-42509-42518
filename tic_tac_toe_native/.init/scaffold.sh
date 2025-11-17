#!/usr/bin/env bash
set -euo pipefail
# Idempotent scaffold: create workspace, minimal app.py, safe entrypoint that activates /opt/venv
WS="/home/kavia/workspace/code-generation/tic-tac-toe-streamlit-app-42509-42518/tic_tac_toe_native"
mkdir -p "$WS" && cd "$WS"
# create minimal app.py if absent
if [ ! -f "$WS/app.py" ]; then
  cat >"$WS/app.py" <<'PY'
import streamlit as st
st.title('Tic Tac Toe - placeholder')
st.write('Placeholder app created by scaffold; will not overwrite existing app.py')
PY
fi
# create entrypoint only if missing
if [ ! -f "$WS/entrypoint.sh" ]; then
  cat >"$WS/entrypoint.sh" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
# WS must be provided by the environment; fallback to workspace path if not set
WS="${WS:-/home/kavia/workspace/code-generation/tic-tac-toe-streamlit-app-42509-42518/tic_tac_toe_native}"
# Activate deterministic venv if present
if [ -f "/opt/venv/bin/activate" ]; then
  # shellcheck disable=SC1090
  . /opt/venv/bin/activate
fi
APP="$WS/app.py"
export PORT="${PORT:-8501}"
# Exec streamlit from venv if available, otherwise rely on PATH
STREAMLIT_BIN="/opt/venv/bin/streamlit"
if [ -x "$STREAMLIT_BIN" ]; then
  exec "$STREAMLIT_BIN" run "$APP" --server.enableCORS=false --server.headless=true --server.port="$PORT"
else
  exec streamlit run "$APP" --server.enableCORS=false --server.headless=true --server.port="$PORT"
fi
SH
  chmod +x "$WS/entrypoint.sh"
  # chown entrypoint to invoking user if possible
  if [ -n "${SUDO_UID:-}" ]; then
    sudo chown "${SUDO_UID}:${SUDO_GID:-${SUDO_UID}}" "$WS/entrypoint.sh" || true
  fi
fi
