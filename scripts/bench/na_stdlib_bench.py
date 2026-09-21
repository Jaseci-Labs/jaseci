"""Raw CPython reference lane for na_stdlib_bench.jac.

    python3 scripts/bench/na_stdlib_bench.py [scale]
"""

import array
import binascii
import math
import mmap
import struct
import sys
import time


def bench_sqrt(n):
    t0 = time.perf_counter()
    acc = 0.0
    for i in range(n):
        acc += math.sqrt(i + 0.5)
    return time.perf_counter() - t0, acc


def bench_struct(n):
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        p = struct.pack("<iid", i, i * 2, 1.5)
        a, b, c = struct.unpack("<iid", p)
        acc += a + b
    return time.perf_counter() - t0, acc


def bench_binascii(n):
    data = b"the quick brown fox jumps over the lazy dog"
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        h = binascii.hexlify(data)
        acc += len(binascii.unhexlify(h))
    return time.perf_counter() - t0, acc


def bench_array(n):
    a = array.array("i")
    t0 = time.perf_counter()
    for i in range(n):
        a.append(i)
    acc = 0
    for i in range(n):
        acc += a[i]
    return time.perf_counter() - t0, acc


def bench_mmap(n):
    m = mmap.mmap(-1, 65536)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        off = (i * 7) % 60000
        m[off] = i & 255
        acc += m[off]
    t1 = time.perf_counter()
    m.close()
    return t1 - t0, acc


def report(name, dt, n, acc):
    print(f"   {name} n={n}   {dt * 1000.0:.2f} ms   "
          f"{dt * 1e9 / n:.1f} ns/op   acc={acc}")


def best_of(fn, n, rounds=3):
    dt, acc = fn(n)
    for _ in range(rounds - 1):
        d2, acc = fn(n)
        dt = min(dt, d2)
    return dt, acc


if __name__ == "__main__":
    scale = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    for name, fn, n in [
        ("math.sqrt loop    ", bench_sqrt, 2000000),
        ("struct pack/unpack", bench_struct, 200000),
        ("binascii hexlify  ", bench_binascii, 50000),
        ("array append/get  ", bench_array, 300000),
        ("mmap set/get byte ", bench_mmap, 200000),
    ]:
        dt, acc = best_of(fn, n * scale)
        report(name, dt, n * scale, acc)
