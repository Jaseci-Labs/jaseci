"""struct bench split -- same workloads as na_stdlib_bench.jac.

Run: jac run -b {"native"|"python"} scripts/bench/na_bench_struct.jac
"""

import time;
import math;
import struct;


def _bchk(b: bytes) -> int {
    n: int = len(b);
    if n == 0 {
        return 0;
    }
    return n * 131 + b[0] * 17 + b[n - 1];
}


def emit_row(name: str, dt: float, n: int, acc: any) {
    print("ROW|", name, "|", n, "|", dt * 1000000000.0 / n, "|", acc);
}


def emit_sec(name: str) {
    print("SEC|", name);
}


# best-of-3 via literal calls (an `any`-typed callee cannot lower on na).
def pick(a: tuple[float, int], b: tuple[float, int]) -> tuple[float, int] {
    return a if a[0] < b[0] else b;
}


def pickf(a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float] {
    return a if a[0] < b[0] else b;
}


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


# ---------- struct ----------

def bench_struct_pack(n: int) -> tuple[float, int] {
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        p = struct.pack("<iid", i, i * 2, 1.5);
        acc = acc + len(p);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_struct_unpack(n: int) -> tuple[float, int] {
    p = struct.pack("<iid", 7, 14, 1.5);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        (a, b, c) = struct.unpack("<iid", p);
        ai: int = a;
        bi: int = b;
        acc = acc + ai + bi;
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_struct_pack_into(n: int) -> tuple[float, int] {
    buf = bytearray(16);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        struct.pack_into("<iid", buf, 0, i, i * 2, 1.5);
        acc = acc + buf[0];
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_struct_unpack_from(n: int) -> tuple[float, int] {
    buf = bytearray(32);
    struct.pack_into("<iid", buf, 8, 3, 6, 2.5);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        (a, b, c) = struct.unpack_from("<iid", buf, 8);
        ai: int = a;
        bi: int = b;
        acc = acc + ai + bi;
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_struct_calcsize(n: int) -> tuple[float, int] {
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        acc = acc + struct.calcsize("<iid");
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


# ---------- binascii ----------
with entry {
    resf = pickf(pickf(bench_sqrt(2000000), bench_sqrt(2000000)), bench_sqrt(2000000));
    emit_row("math.sqrt loop", resf[0], 2000000, resf[1]);
    emit_sec("struct");
    res = pick(
        pick(bench_struct_pack(200000), bench_struct_pack(200000)),
        bench_struct_pack(200000)
    );
    emit_row("struct.pack `<iid`", res[0], 200000, res[1]);
    res = pick(
        pick(bench_struct_unpack(200000), bench_struct_unpack(200000)),
        bench_struct_unpack(200000)
    );
    emit_row("struct.unpack `<iid`", res[0], 200000, res[1]);
    res = pick(
        pick(bench_struct_pack_into(200000), bench_struct_pack_into(200000)),
        bench_struct_pack_into(200000)
    );
    emit_row("struct.pack_into `<iid`", res[0], 200000, res[1]);
    res = pick(
        pick(bench_struct_unpack_from(200000), bench_struct_unpack_from(200000)),
        bench_struct_unpack_from(200000)
    );
    emit_row("struct.unpack_from `<iid`", res[0], 200000, res[1]);
    res = pick(
        pick(bench_struct_calcsize(500000), bench_struct_calcsize(500000)),
        bench_struct_calcsize(500000)
    );
    emit_row("struct.calcsize `<iid`", res[0], 500000, res[1]);
}
