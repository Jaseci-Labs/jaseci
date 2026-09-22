"""binascii bench split -- same workloads as na_stdlib_bench.jac.

Run: jac run -b {"native"|"python"} scripts/bench/na_bench_binascii.jac
"""

import time;
import binascii;


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


def bench_hexlify(n: int) -> tuple[float, int] {
    data = b"the quick brown fox jumps over the lazy dog";
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        h = binascii.hexlify(data);
        acc = acc + _bchk(h);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_b2a_hex(n: int) -> tuple[float, int] {
    data = b"the quick brown fox jumps over the lazy dog";
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        h = binascii.b2a_hex(data);
        acc = acc + _bchk(h);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_unhexlify(n: int) -> tuple[float, int] {
    data = b"the quick brown fox jumps over the lazy dog";
    h = binascii.hexlify(data);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        d = binascii.unhexlify(h);
        acc = acc + _bchk(d);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_a2b_hex(n: int) -> tuple[float, int] {
    data = b"the quick brown fox jumps over the lazy dog";
    h = binascii.b2a_hex(data);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        d = binascii.a2b_hex(h);
        acc = acc + _bchk(d);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_b2a_base64(n: int) -> tuple[float, int] {
    data = b"the quick brown fox jumps over the lazy dog";
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        e = binascii.b2a_base64(data);
        acc = acc + _bchk(e);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_a2b_base64(n: int) -> tuple[float, int] {
    data = b"the quick brown fox jumps over the lazy dog";
    e = binascii.b2a_base64(data);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        d = binascii.a2b_base64(e);
        acc = acc + _bchk(d);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_crc32(n: int) -> tuple[float, int] {
    data = b"the quick brown fox jumps over the lazy dog";
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        acc = acc + binascii.crc32(data);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_crc_hqx(n: int) -> tuple[float, int] {
    data = b"the quick brown fox jumps over the lazy dog";
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        acc = acc + binascii.crc_hqx(data, 0);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_b2a_uu(n: int) -> tuple[float, int] {
    data = b"the quick brown fox jumps over the lazy dog";
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        u = binascii.b2a_uu(data);
        acc = acc + _bchk(u);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_a2b_uu(n: int) -> tuple[float, int] {
    data = b"the quick brown fox jumps over the lazy dog";
    u = binascii.b2a_uu(data);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        d = binascii.a2b_uu(u);
        acc = acc + _bchk(d);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_a2b_qp(n: int) -> tuple[float, int] {
    data = b"the quick = brown\tfox \x01 jumps\n";
    q = binascii.b2a_qp(data);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        d = binascii.a2b_qp(q);
        acc = acc + _bchk(d);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_b2a_qp(n: int) -> tuple[float, int] {
    data = b"the quick = brown\tfox \x01 jumps\n";
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        q = binascii.b2a_qp(data);
        acc = acc + _bchk(q);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


# ---------- array ----------
with entry {
    emit_sec("binascii (43B payload)");
    res = pick(pick(bench_hexlify(50000), bench_hexlify(50000)), bench_hexlify(50000));
    emit_row("binascii.hexlify", res[0], 50000, res[1]);
    res = pick(pick(bench_b2a_hex(50000), bench_b2a_hex(50000)), bench_b2a_hex(50000));
    emit_row("binascii.b2a_hex", res[0], 50000, res[1]);
    res = pick(
        pick(bench_unhexlify(50000), bench_unhexlify(50000)), bench_unhexlify(50000)
    );
    emit_row("binascii.unhexlify", res[0], 50000, res[1]);
    res = pick(pick(bench_a2b_hex(50000), bench_a2b_hex(50000)), bench_a2b_hex(50000));
    emit_row("binascii.a2b_hex", res[0], 50000, res[1]);
    res = pick(
        pick(bench_b2a_base64(50000), bench_b2a_base64(50000)), bench_b2a_base64(50000)
    );
    emit_row("binascii.b2a_base64", res[0], 50000, res[1]);
    res = pick(
        pick(bench_a2b_base64(50000), bench_a2b_base64(50000)), bench_a2b_base64(50000)
    );
    emit_row("binascii.a2b_base64", res[0], 50000, res[1]);
    res = pick(pick(bench_crc32(100000), bench_crc32(100000)), bench_crc32(100000));
    emit_row("binascii.crc32", res[0], 100000, res[1]);
    res = pick(pick(bench_crc_hqx(50000), bench_crc_hqx(50000)), bench_crc_hqx(50000));
    emit_row("binascii.crc_hqx", res[0], 50000, res[1]);
    res = pick(pick(bench_b2a_uu(50000), bench_b2a_uu(50000)), bench_b2a_uu(50000));
    emit_row("binascii.b2a_uu", res[0], 50000, res[1]);
    res = pick(pick(bench_a2b_uu(50000), bench_a2b_uu(50000)), bench_a2b_uu(50000));
    emit_row("binascii.a2b_uu", res[0], 50000, res[1]);
    res = pick(pick(bench_a2b_qp(50000), bench_a2b_qp(50000)), bench_a2b_qp(50000));
    emit_row("binascii.a2b_qp", res[0], 50000, res[1]);
    res = pick(pick(bench_b2a_qp(50000), bench_b2a_qp(50000)), bench_b2a_qp(50000));
    emit_row("binascii.b2a_qp", res[0], 50000, res[1]);
}
