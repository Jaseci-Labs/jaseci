"""Measure what CPython's cyclic garbage collector costs one native build session.

Run with the checkout's pinned CPython against a checkout's compiler source:

    jac/.python-build/cpython/linux-x86_64/python/install/bin/python3.14 -I \
        scripts/native_session_gc_probe.py "$PWD/jac" diamond
    ... "$PWD/jac" kernel-root jaclang.compiler.types.enum_utils 440

`diamond` plans the five-module link diamond of
jac/tests/compiler/backends/native/fixtures/link_diamond (a fresh copy, so every
unit lowers) and links it. `kernel-root MODULE STEPS` runs one session with the
kernel's options over a single kernel module and stops after STEPS progress
steps or when RSS reaches GC_PROBE_RSS_CAP_MB (default 9000), so it never plans
the whole kernel. GC_PROBE_THRESHOLDS="a,b,c" sets the collector's thresholds
first. The report gives collections and pause time per generation, the share of
wall time spent collecting, peak RSS of the measured region and the collector
state after the session, which must equal the state before it.
"""

import gc
import os
import shutil
import sys
import tempfile
import time

root = sys.argv[1]
mode = sys.argv[2]
sys.path.insert(0, root)
import _jac_finder  # noqa: E402

_jac_finder.update_handoff(compiler_source="")
_jac_finder.install()

from jaclang.compiler.backends.native.link_plan import (  # noqa: E402
    ArtifactKind,
    build_link_plan,
    link_artifact,
)
from jaclang.compiler.driver.compile_options import CompileOptions  # noqa: E402
from jaclang.compiler.driver.program import JacProgram  # noqa: E402

if os.environ.get("GC_PROBE_THRESHOLDS"):
    gc.set_threshold(*[int(x) for x in os.environ["GC_PROBE_THRESHOLDS"].split(",")])

stats = {g: [0, 0.0, 0.0, 0] for g in range(3)}
started = [0.0]
origin = [0.0]
stalls: list[tuple[float, int, float]] = []


def on_gc(phase: str, info: dict) -> None:
    if phase == "start":
        started[0] = time.perf_counter()
        return
    pause = time.perf_counter() - started[0]
    row = stats[info["generation"]]
    row[0] += 1
    row[1] += pause
    row[2] = max(row[2], pause)
    row[3] += info.get("collected", 0)
    if pause > 0.5:
        stalls.append((round(started[0] - origin[0], 1), info["generation"], round(pause, 2)))


def status_mb(key: str) -> int:
    with open("/proc/self/status") as f:
        for line in f:
            if line.startswith(key):
                return int(line.split()[1]) // 1024
    return -1


def state() -> tuple:
    return (gc.isenabled(), gc.get_threshold(), gc.get_freeze_count())


class Enough(BaseException):
    pass


if os.environ.get("GC_PROBE_TRACE"):
    from jaclang.compiler.driver import nativecache

    heap_type = getattr(nativecache, "SessionHeap", None)
    if heap_type is not None:
        plain_settle = heap_type.settle

        def traced_settle(self):
            spent = plain_settle(self)
            print(f"  settle at {time.perf_counter() - origin[0]:.1f}s took {spent:.2f}s", flush=True)
            return spent

        heap_type.settle = traced_settle

before = state()
try:
    with open("/proc/self/clear_refs", "w") as f:
        f.write("5")
except OSError:
    pass
gc.callbacks.append(on_gc)
origin[0] = time.perf_counter()
units = 0
if mode == "diamond":
    fixtures = os.path.join(root, "tests/compiler/backends/native/fixtures/link_diamond")
    work = tempfile.mkdtemp(prefix="gc-probe-diamond-")
    for name in ("base.jac", "left.jac", "right.jac", "extra.jac", "top.jac"):
        shutil.copy(os.path.join(fixtures, name), os.path.join(work, name))
    opts = CompileOptions(
        aot_mode=True, default_codespace="native", skip_native_engine=True, no_ir_cache=True
    )
    prog = JacProgram()
    prog.options = opts
    plan = build_link_plan(prog, [os.path.join(work, "top.jac")], opts)
    link_artifact(plan, os.path.join(work, "top.so"), ArtifactKind.SHARED)
    units = prog.analysis.cache_events.get("native_unit_lower", 0)
elif mode == "kernel-root":
    import importlib.util

    from jaclang.compiler.backends.native.kernel_resolve import kernel_options

    path = importlib.util.find_spec(sys.argv[3]).origin
    limit = int(sys.argv[4])
    cap = int(os.environ.get("GC_PROBE_RSS_CAP_MB", "9000"))
    opts = kernel_options()
    opts.no_ir_cache = True
    prog = JacProgram()
    steps = [0]

    def progress(line: str) -> None:
        steps[0] += 1
        rss = status_mb("VmRSS:")
        print(f"{time.perf_counter() - origin[0]:8.1f}s rss={rss}MB {line}", flush=True)
        if steps[0] >= limit or rss >= cap:
            raise Enough()

    prog.native_units().progress = progress
    try:
        build_link_plan(prog, [path], opts, native_unit=True)
    except Enough:
        pass
    units = prog.analysis.cache_events.get("native_unit_lower", 0)
else:
    raise SystemExit(f"unknown mode {mode!r}")
wall = time.perf_counter() - origin[0]
gc.callbacks.remove(on_gc)

total = sum(row[1] for row in stats.values())
print(f"mode={mode} lowered={units} wall={wall:.1f}s peak_rss={status_mb('VmHWM:')}MB")
for g in range(3):
    count, pause, worst, collected = stats[g]
    print(f"  gen{g}: collections={count} pause={pause:.2f}s max={worst:.2f}s collected={collected}")
print(f"  gc pause total={total:.2f}s ({100 * total / wall:.1f}% of wall)")
print(f"  collections over 0.5s (t, gen, s): {stalls}")
print(prog.native_units().phase_summary())
print(f"  collector before={before} after={state()} {'restored' if state() == before else 'CHANGED'}")
