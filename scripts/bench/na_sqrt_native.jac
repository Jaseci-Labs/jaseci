"""Native-only lane: Jac -> C `sqrt` via the FFI floor (`import from c`).

    jac run scripts/bench/na_sqrt_native.jac --native

Compare with:
    python3 scripts/bench/na_stdlib_bench.py        (CPython math.sqrt loop)
    jac run scripts/bench/na_stdlib_bench.jac       (sv lane: CPython bridge)
"""

import from c { def sqrt(x: f64) -> f64;  }
import time;


def bench_sqrt(n: int) -> tuple[float, float] {
    t0: float = time.perf_counter();
    acc: float = 0.0;
    i: int = 0;
    while i < n {
        fi: float = i;
        acc = acc + sqrt(fi + 0.5);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


glob n: int = 2000000;

with entry {
    # Warmup + best-of-3 measured rounds.
    (wt, wacc) = bench_sqrt(100000);
    res = bench_sqrt(n);
    dt: float = res[0];
    acc: float = res[1];
    i: int = 0;
    while i < 2 {
        res = bench_sqrt(n);
        if res[0] < dt {
            dt = res[0];
        }
        i += 1;
    }
    print(
        "na-direct-C sqrt   n=",
        n,
        "  ",
        dt * 1000.0,
        " ms  ",
        dt * 1000000000.0 / n,
        " ns/call  acc=",
        acc
    );
}
