"""Dual-lane stdlib benchmark -- same source, two backends.

    jac run scripts/bench/na_stdlib_bench.jac            # sv lane: Jac on
        # embedded CPython -- `import math` reaches CPython's math.sqrt
        # through the interop bridge; struct/binascii/array/mmap are the
        # CPython modules.
    jac run scripts/bench/na_stdlib_bench.jac --native   # na lane: the bundled
        # native modules (struct intercept, na_stdlib/*) directly.

Compare against `python3 scripts/bench/na_stdlib_bench.py` for the raw
CPython loop timings.
"""

import time;
import math;
import struct;
import binascii;
import array;
import mmap;


def bench_sqrt(n: int) -> tuple[float, float] {
    t0: float = time.perf_counter();
    acc: float = 0.0;
    i: int = 0;
    while i < n {
        fi: float = i;
        acc = acc + math.sqrt(fi + 0.5);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_struct(n: int) -> tuple[float, int] {
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        p = struct.pack("<iid", i, i * 2, 1.5);
        (a, b, c) = struct.unpack("<iid", p);
        ai: int = a;
        bi: int = b;
        acc = acc + ai + bi;
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_binascii(n: int) -> tuple[float, int] {
    data = b"the quick brown fox jumps over the lazy dog";
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        h = binascii.hexlify(data);
        acc = acc + len(binascii.unhexlify(h));
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_array(n: int) -> tuple[float, int] {
    a = array.array("i");
    t0: float = time.perf_counter();
    i: int = 0;
    while i < n {
        a.append(i);
        i = i + 1;
    }
    acc: int = 0;
    i = 0;
    while i < n {
        v: int = a.__getitem__(i);
        acc = acc + v;
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_mmap(n: int) -> tuple[float, int] {
    m = mmap.mmap(-1, 65536);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        off: int = (i * 7) % 60000;
        m.__setitem__(off, i & 255);
        gv: int = m.__getitem__(off);
        acc = acc + gv;
        i = i + 1;
    }
    t1: float = time.perf_counter();
    m.close();
    return (t1 - t0, acc);
}


def emit_row(name: str, dt: float, n: int, acc: any) {
    print(
        "  ",
        name,
        " n=",
        n,
        "  ",
        dt * 1000.0,
        " ms  ",
        dt * 1000000000.0 / n,
        " ns/op  acc=",
        acc
    );
}


# Mirrors na_stdlib_bench.py's generic best_of(fn, n, rounds=3): one warm-up
# candidate plus two repeats, keeping the fastest.
def best_of(fn: any, n: int) -> tuple[float, int] {
    best = fn(n);
    i: int = 0;
    while i < 2 {
        res = fn(n);
        if res[0] < best[0] {
            best = res;
        }
        i += 1;
    }
    return best;
}


with entry {
    res = best_of(bench_sqrt, 2000000);
    emit_row("math.sqrt loop    ", res[0], 2000000, res[1]);
    res = best_of(bench_struct, 200000);
    emit_row("struct pack/unpack", res[0], 200000, res[1]);
    res = best_of(bench_binascii, 50000);
    emit_row("binascii hexlify  ", res[0], 50000, res[1]);
    res = best_of(bench_array, 300000);
    emit_row("array append/get  ", res[0], 300000, res[1]);
    res = best_of(bench_mmap, 200000);
    emit_row("mmap set/get byte ", res[0], 200000, res[1]);
}
