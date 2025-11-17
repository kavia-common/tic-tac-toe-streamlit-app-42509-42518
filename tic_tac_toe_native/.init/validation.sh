#!/usr/bin/env bash
set -euo pipefail
# Validation: start, probe, stop (deterministic pidfile & PGID termination)
WS="/home/kavia/workspace/code-generation/tic-tac-toe-streamlit-app-42509-42518/tic_tac_toe_native"
. /opt/venv/bin/activate
cd "$WS"
export PORT=${PORT:-8501}
PIDFILE=/tmp/tictactoe.pid
LOG=/tmp/tictactoe_streamlit.log
# start monitored wrapper that writes pidfile; use setsid to create new pg
bash -lc "setsid bash -c 'exec >\"${LOG}\" 2>&1; /opt/venv/bin/streamlit run \"$WS/app.py\" --server.enableCORS=false --server.headless=true --server.port=\"$PORT\"' & echo $! > \"${PIDFILE}\"'" >/dev/null || true
# wait for pidfile (conservative)
for i in {1..20}; do [ -f "$PIDFILE" ] && break || sleep 0.2; done
if [ ! -f "$PIDFILE" ]; then echo "Validation ERROR: Failed to create pidfile" >&2; exit 2; fi
bg_pid=$(cat "$PIDFILE" 2>/dev/null || true)
if [ -z "$bg_pid" ]; then echo "Validation ERROR: pidfile empty" >&2; rm -f "$PIDFILE" || true; exit 2; fi
# get PGID reliably
PGID=$(ps -o pgid= -p "$bg_pid" 2>/dev/null | tr -d ' ' || true)
if [ -z "$PGID" ]; then PGID=$bg_pid; fi
# wait up to ~30s for server to respond
ok=1
for i in {1..60}; do
  if command -v curl >/dev/null 2>&1 && curl -sSf "http://127.0.0.1:${PORT}/" >/dev/null 2>&1; then ok=0; break; else sleep 0.5; fi
done
if [ $ok -ne 0 ]; then
  echo "Validation failed: no response on port $PORT (see $LOG)" >&2
  echo "--- last 200 lines of log ($LOG) ---" >&2
  tail -n 200 "$LOG" || true
  echo "--- process list (ps -o pid,ppid,pgid,cmd) ---" >&2
  ps -o pid,ppid,pgid,cmd -p "$bg_pid" 2>/dev/null || ps -o pid,ppid,pgid,cmd -g "$PGID" 2>/dev/null || true
  # attempt clean termination
  kill -TERM -"$PGID" >/dev/null 2>&1 || pkill -f '/opt/venv/bin/streamlit' >/dev/null 2>&1 || kill -TERM "$bg_pid" >/dev/null 2>&1 || true
  sleep 0.5
  rm -f "$PIDFILE" || true
  exit 3
fi
echo "VALIDATION_OK: http://127.0.0.1:${PORT}/ is responding"
# terminate process group cleanly, wait for exit
kill -TERM -"$PGID" >/dev/null 2>&1 || pkill -f '/opt/venv/bin/streamlit' >/dev/null 2>&1 || kill -TERM "$bg_pid" >/dev/null 2>&1 || true
for j in {1..10}; do
  if kill -0 "$bg_pid" >/dev/null 2>&1; then sleep 0.5; else break; fi
done
if kill -0 "$bg_pid" >/dev/null 2>&1; then
  kill -KILL "$bg_pid" >/dev/null 2>&1 || true
fi
rm -f "$PIDFILE" || true
exit 0
