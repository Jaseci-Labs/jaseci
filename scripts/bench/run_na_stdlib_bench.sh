#!/usr/bin/env bash
# Native-stdlib benchmark: three sqrt lanes + per-module timings.
#
#   LANE 1  native Jac -> C `sqrt` directly (FFI `import from c`)
#   LANE 2  CPython loop -> `math.sqrt`
#   LANE 3  Jac on the sv backend -> CPython `math.sqrt` (the bridge)
#   then    per-module ops (struct/binascii/array/mmap) na vs sv vs CPython
#
# Usage:  scripts/bench/run_na_stdlib_bench.sh
set -euo pipefail
cd "$(dirname "$0")/../.."

echo "=== lane 1: native jac -> C sqrt directly ==="
jac run scripts/bench/na_sqrt_native.jac --native
echo
echo "=== lane 2: cpython loop -> math.sqrt ==="
python3 - <<'PY'
import math, time
n = 2000000
t0 = time.perf_counter()
acc = 0.0
for i in range(n):
    acc += math.sqrt(i + 0.5)
dt = time.perf_counter() - t0
print(f"cpython math.sqrt  n={n}   {dt*1000:.2f} ms   {dt*1e9/n:.1f} ns/call   acc={acc}")
PY
echo
echo "=== lane 3: jac sv backend -> cpython bridge (math.sqrt) ==="
jac run -b python scripts/bench/na_stdlib_bench.jac
echo
echo "=== per-module: cpython reference ==="
python3 scripts/bench/na_stdlib_bench.py
echo
echo "=== per-module: native jac (bundled na_stdlib / struct intercept) ==="
jac run -b native scripts/bench/na_stdlib_bench.jac
