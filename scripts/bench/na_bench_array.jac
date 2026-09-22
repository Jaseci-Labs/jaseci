"""array bench split -- same workloads as na_stdlib_bench.jac.

Run: jac run -b {"native"|"python"} scripts/bench/na_bench_array.jac
"""

import time;
import array;
import io;


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


def _mk_iarray(k: int) -> array.array {
    a = array.array("i");
    i: int = 0;
    while i < k {
        a.append(i);
        i += 1;
    }
    return a;
}


def bench_arr_init(n: int) -> tuple[float, int] {
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        a = array.array("i", [i, i * 2]);
        acc = acc + a.__len__();
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_append(n: int) -> tuple[float, int] {
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


def bench_arr_extend(n: int) -> tuple[float, int] {
    a = array.array("i");
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        a.extend([i, i + 1, i + 2]);
        acc = acc + a.__len__();
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_fromlist(n: int) -> tuple[float, int] {
    a = array.array("i");
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        a.fromlist([i]);
        acc = acc + a.__len__();
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_insert(n: int) -> tuple[float, int] {
    a = array.array("i");
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        a.insert(0, i);
        acc = acc + a.__len__();
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_pop(n: int) -> tuple[float, int] {
    a = _mk_iarray(n);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        v: int = a.pop();
        acc = acc + v;
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_remove(n: int) -> tuple[float, int] {
    a = _mk_iarray(1024);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        v: int = 512 + i % 512;
        a.remove(v);
        a.append(v);
        acc = acc + a.__len__();
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_index(n: int) -> tuple[float, int] {
    a = _mk_iarray(1024);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        acc = acc + a.index(i * 7 % 1024);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_count(n: int) -> tuple[float, int] {
    a = _mk_iarray(1024);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        acc = acc + a.count(i * 7 % 1024);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_contains(n: int) -> tuple[float, int] {
    a = _mk_iarray(1024);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        if a.__contains__(i * 7 % 2048) {
            acc = acc + 1;
        }
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_reverse(n: int) -> tuple[float, int] {
    a = _mk_iarray(256);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        a.reverse();
        v: int = a.__getitem__(i % 256);
        acc = acc + v;
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_byteswap(n: int) -> tuple[float, int] {
    a = _mk_iarray(256);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        a.byteswap();
        v: int = a.__getitem__(i % 256);
        acc = acc + v;
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_tobytes(n: int) -> tuple[float, int] {
    a = _mk_iarray(256);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        b = a.tobytes();
        acc = acc + _bchk(b);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_frombytes(n: int) -> tuple[float, int] {
    a = array.array("i");
    payload = b"\x01\x00\x00\x00" * 4;
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        a.frombytes(payload);
        acc = acc + a.__len__();
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_tolist(n: int) -> tuple[float, int] {
    a = _mk_iarray(256);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        l = a.tolist();
        acc = acc + len(l);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_buffer_info(n: int) -> tuple[float, int] {
    a = _mk_iarray(256);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        info = a.buffer_info();
        acc = acc + info[1];
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_len(n: int) -> tuple[float, int] {
    a = _mk_iarray(256);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        acc = acc + a.__len__();
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_getitem(n: int) -> tuple[float, int] {
    a = _mk_iarray(1024);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        v: int = a.__getitem__(i * 7 % 1024);
        acc = acc + v;
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_setitem(n: int) -> tuple[float, int] {
    a = _mk_iarray(1024);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        off: int = i * 7 % 1024;
        a.__setitem__(off, i & 255);
        v: int = a.__getitem__(off);
        acc = acc + v;
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_eq(n: int) -> tuple[float, int] {
    a = _mk_iarray(256);
    b = _mk_iarray(256);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        if a.__eq__(b) {
            acc = acc + 1;
        }
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_ne(n: int) -> tuple[float, int] {
    a = _mk_iarray(256);
    b = _mk_iarray(256);
    b.__setitem__(255, -1);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        if a.__ne__(b) {
            acc = acc + 1;
        }
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_add(n: int) -> tuple[float, int] {
    a = _mk_iarray(256);
    b = _mk_iarray(256);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        c = a.__add__(b);
        acc = acc + c.__len__();
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_mul(n: int) -> tuple[float, int] {
    a = _mk_iarray(256);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        c = a.__mul__(3);
        acc = acc + c.__len__();
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_tofile(n: int) -> tuple[float, int] {
    a = _mk_iarray(256);
    bio = io.BytesIO();
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        bio.seek(0);
        a.tofile(bio);
        acc = acc + bio.tell();
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_arr_fromfile(n: int) -> tuple[float, int] {
    a = _mk_iarray(256);
    bio = io.BytesIO();
    a.tofile(bio);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        bio.seek(0);
        c = array.array("i");
        c.fromfile(bio, 256);
        v: int = c.__getitem__(255);
        acc = acc + v;
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


# ---------- mmap ----------
with entry {
    emit_sec("array (`i` typecode)");
    res = pick(
        pick(bench_arr_init(200000), bench_arr_init(200000)), bench_arr_init(200000)
    );
    emit_row("array.array init [2]", res[0], 200000, res[1]);
    res = pick(
        pick(bench_arr_append(300000), bench_arr_append(300000)),
        bench_arr_append(300000)
    );
    emit_row("array append+get", res[0], 300000, res[1]);
    res = pick(
        pick(bench_arr_extend(100000), bench_arr_extend(100000)),
        bench_arr_extend(100000)
    );
    emit_row("array.extend [3]", res[0], 100000, res[1]);
    res = pick(
        pick(bench_arr_fromlist(100000), bench_arr_fromlist(100000)),
        bench_arr_fromlist(100000)
    );
    emit_row("array.fromlist [1]", res[0], 100000, res[1]);
    res = pick(
        pick(bench_arr_insert(10000), bench_arr_insert(10000)), bench_arr_insert(10000)
    );
    emit_row("array.insert(0)", res[0], 10000, res[1]);
    emit_row("array.pop() [skipped: na lowering blowup]", 0.0, 0, -1);
    res = pick(
        pick(bench_arr_remove(30000), bench_arr_remove(30000)), bench_arr_remove(30000)
    );
    emit_row("array.remove+reappend", res[0], 30000, res[1]);
    res = pick(
        pick(bench_arr_index(50000), bench_arr_index(50000)), bench_arr_index(50000)
    );
    emit_row("array.index", res[0], 50000, res[1]);
    res = pick(
        pick(bench_arr_count(30000), bench_arr_count(30000)), bench_arr_count(30000)
    );
    emit_row("array.count", res[0], 30000, res[1]);
    res = pick(
        pick(bench_arr_contains(100000), bench_arr_contains(100000)),
        bench_arr_contains(100000)
    );
    emit_row("array.__contains__", res[0], 100000, res[1]);
    res = pick(
        pick(bench_arr_reverse(50000), bench_arr_reverse(50000)),
        bench_arr_reverse(50000)
    );
    emit_row("array.reverse", res[0], 50000, res[1]);
    res = pick(
        pick(bench_arr_byteswap(50000), bench_arr_byteswap(50000)),
        bench_arr_byteswap(50000)
    );
    emit_row("array.byteswap", res[0], 50000, res[1]);
    res = pick(
        pick(bench_arr_tobytes(100000), bench_arr_tobytes(100000)),
        bench_arr_tobytes(100000)
    );
    emit_row("array.tobytes", res[0], 100000, res[1]);
    res = pick(
        pick(bench_arr_frombytes(100000), bench_arr_frombytes(100000)),
        bench_arr_frombytes(100000)
    );
    emit_row("array.frombytes", res[0], 100000, res[1]);
    res = pick(
        pick(bench_arr_tolist(20000), bench_arr_tolist(20000)), bench_arr_tolist(20000)
    );
    emit_row("array.tolist", res[0], 20000, res[1]);
    res = pick(
        pick(bench_arr_buffer_info(200000), bench_arr_buffer_info(200000)),
        bench_arr_buffer_info(200000)
    );
    emit_row("array.buffer_info", res[0], 200000, res[1]);
    res = pick(
        pick(bench_arr_len(300000), bench_arr_len(300000)), bench_arr_len(300000)
    );
    emit_row("array.__len__", res[0], 300000, res[1]);
    res = pick(
        pick(bench_arr_getitem(300000), bench_arr_getitem(300000)),
        bench_arr_getitem(300000)
    );
    emit_row("array.__getitem__", res[0], 300000, res[1]);
    res = pick(
        pick(bench_arr_setitem(300000), bench_arr_setitem(300000)),
        bench_arr_setitem(300000)
    );
    emit_row("array.__setitem__", res[0], 300000, res[1]);
    res = pick(pick(bench_arr_eq(50000), bench_arr_eq(50000)), bench_arr_eq(50000));
    emit_row("array.__eq__", res[0], 50000, res[1]);
    res = pick(pick(bench_arr_ne(50000), bench_arr_ne(50000)), bench_arr_ne(50000));
    emit_row("array.__ne__", res[0], 50000, res[1]);
    res = pick(pick(bench_arr_add(50000), bench_arr_add(50000)), bench_arr_add(50000));
    emit_row("array.__add__", res[0], 50000, res[1]);
    res = pick(pick(bench_arr_mul(20000), bench_arr_mul(20000)), bench_arr_mul(20000));
    emit_row("array.__mul__ x3", res[0], 20000, res[1]);
    res = pick(
        pick(bench_arr_tofile(50000), bench_arr_tofile(50000)), bench_arr_tofile(50000)
    );
    emit_row("array.tofile (BytesIO)", res[0], 50000, res[1]);
    emit_row("array.fromfile (BytesIO) [skipped: tofile writes nothing]", 0.0, 0, -1);
}
