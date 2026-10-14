"""Run all three self-contained native Jac files, then summarize evidence."""
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(REPO / 'jac'))
env.setdefault('XDG_CACHE_HOME', '/tmp/graph-frontend-comparison-cache')
reports = {}
for case in ('linear', 'residual', 'cond'):
    subprocess.run([sys.executable, '-m', 'jaclang', 'run', '--backend', 'python',
                    str(HERE / ('native_' + case + '.jac'))], env=env, cwd=REPO, check=True)
    reports[case] = json.loads((HERE / ('validation_native_' + case + '.json')).read_text())
(HERE / 'validation_native.json').write_text(json.dumps(dict(status='passed', cases=reports), indent=2) + '\n')
print('PASS: all native Jac programs, actual CPU parity, selected traces/counts')
