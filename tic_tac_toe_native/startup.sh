#!/usr/bin/env bash
set -e
if [ ! -x /opt/venv/bin/python ]; then
  echo "/opt/venv python not found; ensure env-001 ran in the base image." >&2
  exit 1
fi
/opt/venv/bin/pip install -r /workspace/requirements.txt
exec /opt/venv/bin/streamlit run /workspace/app.py --server.port=${PORT:-8501} --server.address=0.0.0.0
