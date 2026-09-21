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


def best_of_sqrt(n: int) -> tuple[float, float] {
    res = bench_sqrt(n);
    t: float = res[0];
    i: int = 0;
    while i < 2 {
        res = bench_sqrt(n);
        if res[0] < t {
            t = res[0];
        }
        i += 1;
    }
    return (t, res[1]);
}


def best_of_struct(n: int) -> tuple[float, int] {
    res = bench_struct(n);
    t: float = res[0];
    i: int = 0;
    while i < 2 {
        res = bench_struct(n);
        if res[0] < t {
            t = res[0];
        }
        i += 1;
    }
    return (t, res[1]);
}


def best_of_binascii(n: int) -> tuple[float, int] {
    res = bench_binascii(n);
    t: float = res[0];
    i: int = 0;
    while i < 2 {
        res = bench_binascii(n);
        if res[0] < t {
            t = res[0];
        }
        i += 1;
    }
    return (t, res[1]);
}


def best_of_array(n: int) -> tuple[float, int] {
    res = bench_array(n);
    t: float = res[0];
    i: int = 0;
    while i < 2 {
        res = bench_array(n);
        if res[0] < t {
            t = res[0];
        }
        i += 1;
    }
    return (t, res[1]);
}


def best_of_mmap(n: int) -> tuple[float, int] {
    res = bench_mmap(n);
    t: float = res[0];
    i: int = 0;
    while i < 2 {
        res = bench_mmap(n);
        if res[0] < t {
            t = res[0];
        }
        i += 1;
    }
    return (t, res[1]);
}


glob scale: int = 1;

with entry {
    res = best_of_sqrt(2000000 * scale);
    emit_row("math.sqrt loop    ", res[0], 2000000 * scale, res[1]);
    res2 = best_of_struct(200000 * scale);
    emit_row("struct pack/unpack", res2[0], 200000 * scale, res2[1]);
    res3 = best_of_binascii(50000 * scale);
    emit_row("binascii hexlify  ", res3[0], 50000 * scale, res3[1]);
    res4 = best_of_array(300000 * scale);
    emit_row("array append/get  ", res4[0], 300000 * scale, res4[1]);
    res5 = best_of_mmap(200000 * scale);
    emit_row("mmap set/get byte ", res5[0], 200000 * scale, res5[1]);
}
