"""CPython-equivalent workloads for na_stdlib_extra.jac.

These rows stand in for the na-only APIs: `a.extend(arr)` ~
extend_array, `a.extend(bytes)` ~ extend_bytes, `m[a:b]` slicing ~
read_slice, `os.open` + `mmap.mmap(fd,0).size()` ~ size.
"""

import array
import mmap
import os
import time


def _bchk(b):
    n = len(b)
    if n == 0:
        return 0
    return n * 131 + b[0] * 17 + b[n - 1]


def _mk_iarray(k):
    a = array.array("i")
    for i in range(k):
        a.append(i)
    return a


def bench_extend_array(n):
    a = array.array("i")
    src = _mk_iarray(8)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        a.extend(src)
        acc += a.__len__()
    return time.perf_counter() - t0, acc


def bench_extend_bytes(n):
    a = array.array("i")
    payload = b"\x01\x00\x00\x00\x02\x00\x00\x00"
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        a.extend(payload)
        acc += a.__len__()
    return time.perf_counter() - t0, acc


def bench_read_slice(n):
    m = mmap.mmap(-1, 65536)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        d = m[i * 7 % 60000: i * 7 % 60000 + 64]
        acc += _bchk(d)
    dt = time.perf_counter() - t0
    m.close()
    return dt, acc


def bench_resize_grow(n):
    m = mmap.mmap(
        -1,
        8192,
        flags=mmap.MAP_PRIVATE,
        prot=mmap.PROT_READ | mmap.PROT_WRITE,
    )
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        m.resize(16384 if i % 2 == 0 else 8192)
        acc += m.__len__()
    dt = time.perf_counter() - t0
    m.close()
    return dt, acc


def bench_size(n):
    fd = os.open("scripts/bench/na_stdlib_bench.py", os.O_RDONLY)
    m = mmap.mmap(fd, 0, access=mmap.ACCESS_READ)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        acc += m.size()
    dt = time.perf_counter() - t0
    m.close()
    os.close(fd)
    return dt, acc


def emit_row(name, dt, n, acc):
    print(f"ROW|{name}|{n}|{dt * 1e9 / n}|{acc}")


def best_of(fn, n, rounds=3):
    dt, acc = fn(n)
    for _ in range(rounds - 1):
        d2, acc = fn(n)
        dt = min(dt, d2)
    return dt, acc


if __name__ == "__main__":
    for name, fn, n in [
        ("array.extend_array [8]", bench_extend_array, 100000),
        ("array.extend_bytes 8B", bench_extend_bytes, 100000),
        ("mmap.read_slice 64B", bench_read_slice, 100000),
        ("mmap.size (file)", bench_size, 100000),
        ("mmap.resize grow 8/16K", bench_resize_grow, 10000),
    ]:
        dt, acc = best_of(fn, n)
        emit_row(name, dt, n, acc)
