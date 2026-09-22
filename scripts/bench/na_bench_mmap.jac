"""mmap bench split -- same workloads as na_stdlib_bench.jac.

Run: jac run -b {"native"|"python"} scripts/bench/na_bench_mmap.jac
"""

import time;
import mmap;


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


def bench_mmap_init(n: int) -> tuple[float, int] {
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        m = mmap.mmap(-1, 4096);
        acc = acc + m.__len__();
        m.close();
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_mmap_ctx(n: int) -> tuple[float, int] {
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        m = mmap.mmap(-1, 4096);
        e = m.__enter__();
        acc = acc + e.__len__();
        m.__exit__(None, None, None);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    return (t1 - t0, acc);
}


def bench_mmap_len(n: int) -> tuple[float, int] {
    m = mmap.mmap(-1, 65536);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        acc = acc + m.__len__();
        i = i + 1;
    }
    t1: float = time.perf_counter();
    m.close();
    return (t1 - t0, acc);
}


def bench_mmap_tell(n: int) -> tuple[float, int] {
    m = mmap.mmap(-1, 65536);
    m.seek(1234);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        acc = acc + m.tell();
        i = i + 1;
    }
    t1: float = time.perf_counter();
    m.close();
    return (t1 - t0, acc);
}


def bench_mmap_seek(n: int) -> tuple[float, int] {
    m = mmap.mmap(-1, 65536);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        m.seek(i * 7 % 60000);
        acc = acc + m.tell();
        i = i + 1;
    }
    t1: float = time.perf_counter();
    m.close();
    return (t1 - t0, acc);
}


def bench_mmap_read(n: int) -> tuple[float, int] {
    m = mmap.mmap(-1, 65536);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        m.seek(0);
        d = m.read(64);
        acc = acc + _bchk(d);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    m.close();
    return (t1 - t0, acc);
}


def bench_mmap_read_byte(n: int) -> tuple[float, int] {
    m = mmap.mmap(-1, 65536);
    m.__setitem__(0, 77);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        m.seek(0);
        v: int = m.read_byte();
        acc = acc + v;
        i = i + 1;
    }
    t1: float = time.perf_counter();
    m.close();
    return (t1 - t0, acc);
}


def bench_mmap_readline(n: int) -> tuple[float, int] {
    m = mmap.mmap(-1, 65536);
    m.seek(0);
    _ = m.write(b"x" * 100 + b"\n");
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        m.seek(0);
        d = m.readline();
        acc = acc + _bchk(d);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    m.close();
    return (t1 - t0, acc);
}


def bench_mmap_write(n: int) -> tuple[float, int] {
    m = mmap.mmap(-1, 65536);
    payload = b"y" * 64;
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        m.seek(0);
        w = m.write(payload);
        acc = acc + w;
        i = i + 1;
    }
    t1: float = time.perf_counter();
    m.close();
    return (t1 - t0, acc);
}


def bench_mmap_write_byte(n: int) -> tuple[float, int] {
    m = mmap.mmap(-1, 65536);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        m.seek(0);
        m.write_byte(i & 255);
        acc = acc + m.tell();
        i = i + 1;
    }
    t1: float = time.perf_counter();
    m.close();
    return (t1 - t0, acc);
}


def bench_mmap_getitem(n: int) -> tuple[float, int] {
    m = mmap.mmap(-1, 65536);
    m.seek(0);
    _ = m.write(b"z" * 60000);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        v: int = m.__getitem__(i * 7 % 60000);
        acc = acc + v;
        i = i + 1;
    }
    t1: float = time.perf_counter();
    m.close();
    return (t1 - t0, acc);
}


def bench_mmap_setitem(n: int) -> tuple[float, int] {
    m = mmap.mmap(-1, 65536);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        off: int = i * 7 % 60000;
        m.__setitem__(off, i & 255);
        v: int = m.__getitem__(off);
        acc = acc + v;
        i = i + 1;
    }
    t1: float = time.perf_counter();
    m.close();
    return (t1 - t0, acc);
}


def bench_mmap_find(n: int) -> tuple[float, int] {
    m = mmap.mmap(-1, 65536);
    m.seek(50000);
    _ = m.write(b"needle");
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        acc = acc + m.find(b"needle", 0, 65536);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    m.close();
    return (t1 - t0, acc);
}


def bench_mmap_rfind(n: int) -> tuple[float, int] {
    m = mmap.mmap(-1, 65536);
    m.seek(50000);
    _ = m.write(b"needle");
    m.seek(60000);
    _ = m.write(b"needle");
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        acc = acc + m.rfind(b"needle", 0, 65536);
        i = i + 1;
    }
    t1: float = time.perf_counter();
    m.close();
    return (t1 - t0, acc);
}


def bench_mmap_flush(n: int) -> tuple[float, int] {
    m = mmap.mmap(-1, 65536);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        m.flush();
        acc = acc + 1;
        i = i + 1;
    }
    t1: float = time.perf_counter();
    m.close();
    return (t1 - t0, acc);
}


def bench_mmap_move(n: int) -> tuple[float, int] {
    m = mmap.mmap(-1, 65536);
    m.__setitem__(1024, 55);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        m.move(0, 1024, 512);
        v: int = m.__getitem__(0);
        acc = acc + v;
        i = i + 1;
    }
    t1: float = time.perf_counter();
    m.close();
    return (t1 - t0, acc);
}


def bench_mmap_resize(n: int) -> tuple[float, int] {
    m = mmap.mmap(-1, 8192);
    t0: float = time.perf_counter();
    acc: int = 0;
    i: int = 0;
    while i < n {
        m.resize(8192);
        acc = acc + m.__len__();
        i = i + 1;
    }
    t1: float = time.perf_counter();
    m.close();
    return (t1 - t0, acc);
}


with entry {
    emit_sec("mmap (64KiB anon)");
    res = pick(
        pick(bench_mmap_init(20000), bench_mmap_init(20000)), bench_mmap_init(20000)
    );
    emit_row("mmap init+close", res[0], 20000, res[1]);
    res = pick(
        pick(bench_mmap_ctx(20000), bench_mmap_ctx(20000)), bench_mmap_ctx(20000)
    );
    emit_row("mmap enter/exit", res[0], 20000, res[1]);
    res = pick(
        pick(bench_mmap_len(200000), bench_mmap_len(200000)), bench_mmap_len(200000)
    );
    emit_row("mmap.__len__", res[0], 200000, res[1]);
    res = pick(
        pick(bench_mmap_tell(200000), bench_mmap_tell(200000)), bench_mmap_tell(200000)
    );
    emit_row("mmap.tell", res[0], 200000, res[1]);
    res = pick(
        pick(bench_mmap_seek(200000), bench_mmap_seek(200000)), bench_mmap_seek(200000)
    );
    emit_row("mmap.seek", res[0], 200000, res[1]);
    res = pick(
        pick(bench_mmap_read(100000), bench_mmap_read(100000)), bench_mmap_read(100000)
    );
    emit_row("mmap.read(64)", res[0], 100000, res[1]);
    res = pick(
        pick(bench_mmap_read_byte(200000), bench_mmap_read_byte(200000)),
        bench_mmap_read_byte(200000)
    );
    emit_row("mmap.read_byte", res[0], 200000, res[1]);
    res = pick(
        pick(bench_mmap_readline(50000), bench_mmap_readline(50000)),
        bench_mmap_readline(50000)
    );
    emit_row("mmap.readline", res[0], 50000, res[1]);
    res = pick(
        pick(bench_mmap_write(100000), bench_mmap_write(100000)),
        bench_mmap_write(100000)
    );
    emit_row("mmap.write(64)", res[0], 100000, res[1]);
    res = pick(
        pick(bench_mmap_write_byte(200000), bench_mmap_write_byte(200000)),
        bench_mmap_write_byte(200000)
    );
    emit_row("mmap.write_byte", res[0], 200000, res[1]);
    res = pick(
        pick(bench_mmap_getitem(300000), bench_mmap_getitem(300000)),
        bench_mmap_getitem(300000)
    );
    emit_row("mmap.__getitem__", res[0], 300000, res[1]);
    res = pick(
        pick(bench_mmap_setitem(300000), bench_mmap_setitem(300000)),
        bench_mmap_setitem(300000)
    );
    emit_row("mmap.__setitem__", res[0], 300000, res[1]);
    res = pick(
        pick(bench_mmap_find(20000), bench_mmap_find(20000)), bench_mmap_find(20000)
    );
    emit_row("mmap.find", res[0], 20000, res[1]);
    res = pick(
        pick(bench_mmap_rfind(20000), bench_mmap_rfind(20000)), bench_mmap_rfind(20000)
    );
    emit_row("mmap.rfind", res[0], 20000, res[1]);
    res = pick(
        pick(bench_mmap_flush(50000), bench_mmap_flush(50000)), bench_mmap_flush(50000)
    );
    emit_row("mmap.flush", res[0], 50000, res[1]);
    res = pick(
        pick(bench_mmap_move(50000), bench_mmap_move(50000)), bench_mmap_move(50000)
    );
    emit_row("mmap.move 512B", res[0], 50000, res[1]);
    res = pick(
        pick(bench_mmap_resize(10000), bench_mmap_resize(10000)),
        bench_mmap_resize(10000)
    );
    emit_row("mmap.resize same 8K", res[0], 10000, res[1]);
}
