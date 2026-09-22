"""na-only stdlib bench additions -- `jac run -b native` only.

These APIs have no attribute-equivalent on CPython's objects, so they
cannot live in the shared dual-lane source: `array.extend_array` /
`array.extend_bytes` (na's `extend` is `list[any]`-typed), and
`mmap.read_slice` / `mmap.size` (file-backed map needs a real fd, which
na opens through the bundled `_fd_native` floor). The CPython column in
the report runs the closest equivalent workload from
na_stdlib_extra.py (`a.extend(arr)`, `a.extend(bytes)`, `m[a:b]`,
`os.open` + `mmap.mmap(fd, 0).size()`).
"""

import time;
import array;
import mmap;
import from _fd_native { open_readonly }


def _bchk(b: bytes) -> int {
    n: int = len(b);
    if n == 0 {
        return 0;
    }
    return n * 131 + b[0] * 17 + b[n - 1];
}


def _mk_iarray(k: int) -> any {
    a = array.array("i");
    i: int = 0;
    while i < k {
        a.append(i);
        i += 1;
    }
    return a;
}


def bench_extend_array(n: int) -> tuple[float, int] {
    a = array.array("i");
    src = _mk_iarray(8);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        a.extend_array(src);
        acc = acc + a.__len__();
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_extend_bytes(n: int) -> tuple[float, int] {
    a = array.array("i");
    payload = b"\x01\x00\x00\x00\x02\x00\x00\x00";
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        a.extend_bytes(payload);
        acc = acc + a.__len__();
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_read_slice(n: int) -> tuple[float, int] {
    m = mmap.mmap(-1, 65536);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        d = m.read_slice(i * 7 % 60000, 64);
        acc = acc + _bchk(d);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    m.close();
    return (t1 - t0, acc);
}


def bench_resize_grow(n: int) -> tuple[float, int] {
    m = mmap.mmap(-1, 8192, mmap.MAP_PRIVATE, mmap.PROT_READ | mmap.PROT_WRITE);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        sz: int = 16384 if i % 2 == 0 else 8192;
        m.resize(sz);
        acc = acc + m.__len__();
        i = i + 1;
    }
    t1: float = time.perf_counter();
    m.close();
    return (t1 - t0, acc);
}


def bench_size(n: int) -> tuple[float, int] {
    fd: int = open_readonly("scripts/bench/na_stdlib_bench.py");
    m = mmap.mmap(fd, 0, access=mmap.ACCESS_READ);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        acc = acc + m.size();
        i = i + 1;
    }
    t1: float = time.perf_counter();
    m.close();
    return (t1 - t0, acc);
}


def emit_row(name: str, dt: float, n: int, acc: any) {
    print("ROW|", name, "|", n, "|", dt * 1000000000.0 / n, "|", acc);
}


# best-of-3 via literal calls (an `any`-typed callee cannot lower on na).
def pick(a: tuple[float, int], b: tuple[float, int]) -> tuple[float, int] {
    return a if a[0] < b[0] else b;
}


with entry {
    res = pick(
        pick(bench_extend_array(100000), bench_extend_array(100000)),
        bench_extend_array(100000)
    );
    emit_row("array.extend_array [8]", res[0], 100000, res[1]);
    res = pick(
        pick(bench_extend_bytes(100000), bench_extend_bytes(100000)),
        bench_extend_bytes(100000)
    );
    emit_row("array.extend_bytes 8B", res[0], 100000, res[1]);
    res = pick(
        pick(bench_read_slice(100000), bench_read_slice(100000)),
        bench_read_slice(100000)
    );
    emit_row("mmap.read_slice 64B", res[0], 100000, res[1]);
    res = pick(pick(bench_size(100000), bench_size(100000)), bench_size(100000));
    emit_row("mmap.size (file)", res[0], 100000, res[1]);
    res = pick(
        pick(bench_resize_grow(10000), bench_resize_grow(10000)),
        bench_resize_grow(10000)
    );
    emit_row("mmap.resize grow 8/16K", res[0], 10000, res[1]);
}
