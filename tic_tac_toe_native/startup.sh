#!/usr/bin/env bash
# Robust startup script for native container runtime
# - Ensures /opt/venv exists (provided by env-001)
# - Installs requirements from /workspace/requirements.txt
# - Starts Streamlit from /opt/venv
set -euo pipefail

VENV_PY="/opt/venv/bin/python"
VENV_PIP="/opt/venv/bin/pip"
VENV_STREAMLIT="/opt/venv/bin/streamlit"

# Verify virtual environment provided by env-001
if [ ! -x "${VENV_PY}" ] || [ ! -x "${VENV_PIP}" ]; then
  echo "[startup] /opt/venv python/pip not found. Ensure 'env-001' pre-run hook executed." >&2
  exit 1
fi

REQ_FILE="/workspace/requirements.txt"
APP_ENTRY="/workspace/app.py"

# If app entrypoint actually resides in container folder, align APP_ENTRY
if [ -f "/workspace/tic-tac-toe-streamlit-app-42509-42518/tic_tac_toe_native/app.py" ]; then
  APP_ENTRY="/workspace/tic-tac-toe-streamlit-app-42509-42518/tic_tac_toe_native/app.py"
fi

# Install dependencies if requirements file exists
if [ -f "${REQ_FILE}" ]; then
  echo "[startup] Installing requirements from ${REQ_FILE} ..."
  "${VENV_PIP}" install -r "${REQ_FILE}"
else
  echo "[startup] WARNING: ${REQ_FILE} not found. Continuing without dependency installation." >&2
fi

# Start Streamlit
if [ ! -x "${VENV_STREAMLIT}" ]; then
  echo "[startup] streamlit not found in ${VENV_STREAMLIT}. Did requirements install succeed?" >&2
  exit 1
fi

echo "[startup] Starting Streamlit app at ${APP_ENTRY} ..."
exec "${VENV_STREAMLIT}" run "${APP_ENTRY}" --server.port="${PORT:-8501}" --server.address=0.0.0.0
