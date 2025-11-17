#!/usr/bin/env bash
set -euo pipefail
WS="/home/kavia/workspace/code-generation/tic-tac-toe-streamlit-app-42509-42518/tic_tac_toe_native"
. /opt/venv/bin/activate
cd "$WS"
cat >"$WS/test_smoke.py" <<'PY'
import os, subprocess, time, urllib.request, sys, signal
pidfile='/tmp/tictactoe.pid'
log='/tmp/tictactoe_test.log'
# Launch monitored wrapper: start entrypoint via setsid so it has its own PGID
wrapper = (
    "setsid bash -lc 'exec >%s 2>&1; "
    "WS=\"%s\"; . /opt/venv/bin/activate; "
    "bash "$WS/entrypoint.sh"' & echo $! > %s" % (log, os.environ.get('WS', '/tmp'), pidfile)
)
# Use subprocess to run wrapper in shell so pidfile is written by the wrapper
proc = subprocess.Popen(['bash','-lc', wrapper], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
try:
    out, err = proc.communicate(timeout=12)
except subprocess.TimeoutExpired:
    proc.kill()
    out, err = proc.communicate()
if proc.returncode not in (0, None):
    print('failed to start wrapper', file=sys.stderr)
    print('stdout:', out, 'stderr:', err, file=sys.stderr)
    raise SystemExit(2)
# wait for pidfile
for _ in range(40):
    if os.path.exists(pidfile): break
    time.sleep(0.25)
else:
    raise RuntimeError('pidfile not created')
with open(pidfile) as f: pid = int(f.read().strip())
# resolve PGID (fallback to pid if not available)
try:
    pgid = os.getpgid(pid)
except Exception:
    pgid = pid
port = int(os.environ.get('PORT','8501'))
url = f'http://127.0.0.1:{port}/'
# poll until responsive (total ~30s)
for _ in range(60):
    try:
        resp = urllib.request.urlopen(url, timeout=2)
        code = resp.getcode()
        if 200 <= code < 400:
            break
    except Exception:
        time.sleep(0.5)
else:
    # on failure, dump last 200 lines of log and pgrouplist
    tail = '(no log)'
    try:
        with open(log) as f: tail = ''.join(f.readlines()[-200:])
    except Exception:
        pass
    pgproc = '(ps failed)'
    try:
        pgproc = subprocess.check_output(['ps','-o','pid,pgid,cmd','-g',str(pgid)], text=True)
    except Exception:
        pass
    raise RuntimeError('server did not respond; tail of log:\n'+tail+'\nPGROUP:\n'+pgproc)
# terminate the whole process group reliably
try:
    os.killpg(pgid, signal.SIGTERM)
except Exception:
    try:
        os.kill(pid, signal.SIGTERM)
    except Exception:
        pass
# wait for termination
for _ in range(40):
    try:
        os.kill(pid, 0)
        time.sleep(0.25)
    except Exception:
        break
# cleanup
try:
    os.remove(pidfile)
except Exception:
    pass
PY

# run pytest using venv python/pytest
/opt/venv/bin/pytest -q "$WS/test_smoke.py"
