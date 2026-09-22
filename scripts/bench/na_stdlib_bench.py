"""Raw CPython reference lane for na_stdlib_bench.jac.

    python3 scripts/bench/na_stdlib_bench.py [scale]

Rows print pipe-separated: name|n|ns_per_op|acc -- identical bench
functions and workloads as the .jac source so `acc` checksums are
directly comparable across lanes.
"""

import array
import binascii
import io
import math
import mmap
import struct
import sys
import time


def _bchk(b):
    n = len(b)
    if n == 0:
        return 0
    return n * 131 + b[0] * 17 + b[n - 1]


def bench_sqrt(n):
    t0 = time.perf_counter()
    acc = 0.0
    for i in range(n):
        acc += math.sqrt(i + 0.5)
    return time.perf_counter() - t0, acc


# ---------- struct ----------


def bench_struct_pack(n):
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        p = struct.pack("<iid", i, i * 2, 1.5)
        acc += len(p)
    return time.perf_counter() - t0, acc


def bench_struct_unpack(n):
    p = struct.pack("<iid", 7, 14, 1.5)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        a, b, c = struct.unpack("<iid", p)
        acc += a + b
    return time.perf_counter() - t0, acc


def bench_struct_pack_into(n):
    buf = bytearray(16)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        struct.pack_into("<iid", buf, 0, i, i * 2, 1.5)
        acc += buf[0]
    return time.perf_counter() - t0, acc


def bench_struct_unpack_from(n):
    buf = bytearray(32)
    struct.pack_into("<iid", buf, 8, 3, 6, 2.5)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        a, b, c = struct.unpack_from("<iid", buf, 8)
        acc += a + b
    return time.perf_counter() - t0, acc


def bench_struct_calcsize(n):
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        acc += struct.calcsize("<iid")
    return time.perf_counter() - t0, acc


# ---------- binascii ----------


def bench_hexlify(n):
    data = b"the quick brown fox jumps over the lazy dog"
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        h = binascii.hexlify(data)
        acc += _bchk(h)
    return time.perf_counter() - t0, acc


def bench_b2a_hex(n):
    data = b"the quick brown fox jumps over the lazy dog"
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        h = binascii.b2a_hex(data)
        acc += _bchk(h)
    return time.perf_counter() - t0, acc


def bench_unhexlify(n):
    data = b"the quick brown fox jumps over the lazy dog"
    h = binascii.hexlify(data)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        d = binascii.unhexlify(h)
        acc += _bchk(d)
    return time.perf_counter() - t0, acc


def bench_a2b_hex(n):
    data = b"the quick brown fox jumps over the lazy dog"
    h = binascii.b2a_hex(data)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        d = binascii.a2b_hex(h)
        acc += _bchk(d)
    return time.perf_counter() - t0, acc


def bench_b2a_base64(n):
    data = b"the quick brown fox jumps over the lazy dog"
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        e = binascii.b2a_base64(data)
        acc += _bchk(e)
    return time.perf_counter() - t0, acc


def bench_a2b_base64(n):
    data = b"the quick brown fox jumps over the lazy dog"
    e = binascii.b2a_base64(data)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        d = binascii.a2b_base64(e)
        acc += _bchk(d)
    return time.perf_counter() - t0, acc


def bench_crc32(n):
    data = b"the quick brown fox jumps over the lazy dog"
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        acc += binascii.crc32(data)
    return time.perf_counter() - t0, acc


def bench_crc_hqx(n):
    data = b"the quick brown fox jumps over the lazy dog"
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        acc += binascii.crc_hqx(data, 0)
    return time.perf_counter() - t0, acc


def bench_b2a_uu(n):
    data = b"the quick brown fox jumps over the lazy dog"
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        u = binascii.b2a_uu(data)
        acc += _bchk(u)
    return time.perf_counter() - t0, acc


def bench_a2b_uu(n):
    data = b"the quick brown fox jumps over the lazy dog"
    u = binascii.b2a_uu(data)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        d = binascii.a2b_uu(u)
        acc += _bchk(d)
    return time.perf_counter() - t0, acc


def bench_a2b_qp(n):
    data = b"the quick = brown\tfox \x01 jumps\n"
    q = binascii.b2a_qp(data)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        d = binascii.a2b_qp(q)
        acc += _bchk(d)
    return time.perf_counter() - t0, acc


def bench_b2a_qp(n):
    data = b"the quick = brown\tfox \x01 jumps\n"
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        q = binascii.b2a_qp(data)
        acc += _bchk(q)
    return time.perf_counter() - t0, acc


# ---------- array ----------


def _mk_iarray(k):
    a = array.array("i")
    for i in range(k):
        a.append(i)
    return a


def bench_arr_init(n):
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        a = array.array("i", [i, i * 2])
        acc += a.__len__()
    return time.perf_counter() - t0, acc


def bench_arr_append(n):
    a = array.array("i")
    t0 = time.perf_counter()
    for i in range(n):
        a.append(i)
    acc = 0
    for i in range(n):
        acc += a.__getitem__(i)
    return time.perf_counter() - t0, acc


def bench_arr_extend(n):
    a = array.array("i")
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        a.extend([i, i + 1, i + 2])
        acc += a.__len__()
    return time.perf_counter() - t0, acc


def bench_arr_fromlist(n):
    a = array.array("i")
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        a.fromlist([i])
        acc += a.__len__()
    return time.perf_counter() - t0, acc


def bench_arr_insert(n):
    a = array.array("i")
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        a.insert(0, i)
        acc += a.__len__()
    return time.perf_counter() - t0, acc


def bench_arr_pop(n):
    a = _mk_iarray(n)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        acc += a.pop()
    return time.perf_counter() - t0, acc


def bench_arr_remove(n):
    a = _mk_iarray(1024)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        v = 512 + i % 512
        a.remove(v)
        a.append(v)
        acc += a.__len__()
    return time.perf_counter() - t0, acc


def bench_arr_index(n):
    a = _mk_iarray(1024)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        acc += a.index(i * 7 % 1024)
    return time.perf_counter() - t0, acc


def bench_arr_count(n):
    a = _mk_iarray(1024)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        acc += a.count(i * 7 % 1024)
    return time.perf_counter() - t0, acc


def bench_arr_contains(n):
    a = _mk_iarray(1024)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        if a.__contains__(i * 7 % 2048):
            acc += 1
    return time.perf_counter() - t0, acc


def bench_arr_reverse(n):
    a = _mk_iarray(256)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        a.reverse()
        acc += a.__getitem__(i % 256)
    return time.perf_counter() - t0, acc


def bench_arr_byteswap(n):
    a = _mk_iarray(256)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        a.byteswap()
        acc += a.__getitem__(i % 256)
    return time.perf_counter() - t0, acc


def bench_arr_tobytes(n):
    a = _mk_iarray(256)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        acc += _bchk(a.tobytes())
    return time.perf_counter() - t0, acc


def bench_arr_frombytes(n):
    a = array.array("i")
    payload = b"\x01\x00\x00\x00" * 4
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        a.frombytes(payload)
        acc += a.__len__()
    return time.perf_counter() - t0, acc


def bench_arr_tolist(n):
    a = _mk_iarray(256)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        acc += len(a.tolist())
    return time.perf_counter() - t0, acc


def bench_arr_buffer_info(n):
    a = _mk_iarray(256)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        acc += a.buffer_info()[1]
    return time.perf_counter() - t0, acc


def bench_arr_len(n):
    a = _mk_iarray(256)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        acc += a.__len__()
    return time.perf_counter() - t0, acc


def bench_arr_getitem(n):
    a = _mk_iarray(1024)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        acc += a.__getitem__(i * 7 % 1024)
    return time.perf_counter() - t0, acc


def bench_arr_setitem(n):
    a = _mk_iarray(1024)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        off = i * 7 % 1024
        a.__setitem__(off, i & 255)
        acc += a.__getitem__(off)
    return time.perf_counter() - t0, acc


def bench_arr_eq(n):
    a = _mk_iarray(256)
    b = _mk_iarray(256)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        if a.__eq__(b):
            acc += 1
    return time.perf_counter() - t0, acc


def bench_arr_ne(n):
    a = _mk_iarray(256)
    b = _mk_iarray(256)
    b.__setitem__(255, -1)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        if a.__ne__(b):
            acc += 1
    return time.perf_counter() - t0, acc


def bench_arr_add(n):
    a = _mk_iarray(256)
    b = _mk_iarray(256)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        acc += a.__add__(b).__len__()
    return time.perf_counter() - t0, acc


def bench_arr_mul(n):
    a = _mk_iarray(256)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        acc += a.__mul__(3).__len__()
    return time.perf_counter() - t0, acc


def bench_arr_tofile(n):
    a = _mk_iarray(256)
    bio = io.BytesIO()
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        bio.seek(0)
        a.tofile(bio)
        acc += bio.tell()
    return time.perf_counter() - t0, acc


def bench_arr_fromfile(n):
    a = _mk_iarray(256)
    bio = io.BytesIO()
    a.tofile(bio)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        bio.seek(0)
        c = array.array("i")
        c.fromfile(bio, 256)
        acc += c.__getitem__(255)
    return time.perf_counter() - t0, acc


# ---------- mmap ----------


def bench_mmap_init(n):
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        m = mmap.mmap(-1, 4096)
        acc += m.__len__()
        m.close()
    return time.perf_counter() - t0, acc


def bench_mmap_ctx(n):
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        m = mmap.mmap(-1, 4096)
        e = m.__enter__()
        acc += e.__len__()
        m.__exit__(None, None, None)
    return time.perf_counter() - t0, acc


def bench_mmap_len(n):
    m = mmap.mmap(-1, 65536)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        acc += m.__len__()
    dt = time.perf_counter() - t0
    m.close()
    return dt, acc


def bench_mmap_tell(n):
    m = mmap.mmap(-1, 65536)
    m.seek(1234)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        acc += m.tell()
    dt = time.perf_counter() - t0
    m.close()
    return dt, acc


def bench_mmap_seek(n):
    m = mmap.mmap(-1, 65536)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        m.seek(i * 7 % 60000)
        acc += m.tell()
    dt = time.perf_counter() - t0
    m.close()
    return dt, acc


def bench_mmap_read(n):
    m = mmap.mmap(-1, 65536)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        m.seek(0)
        acc += _bchk(m.read(64))
    dt = time.perf_counter() - t0
    m.close()
    return dt, acc


def bench_mmap_read_byte(n):
    m = mmap.mmap(-1, 65536)
    m.__setitem__(0, 77)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        m.seek(0)
        acc += m.read_byte()
    dt = time.perf_counter() - t0
    m.close()
    return dt, acc


def bench_mmap_readline(n):
    m = mmap.mmap(-1, 65536)
    m.seek(0)
    m.write(b"x" * 100 + b"\n")
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        m.seek(0)
        acc += _bchk(m.readline())
    dt = time.perf_counter() - t0
    m.close()
    return dt, acc


def bench_mmap_write(n):
    m = mmap.mmap(-1, 65536)
    payload = b"y" * 64
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        m.seek(0)
        acc += m.write(payload)
    dt = time.perf_counter() - t0
    m.close()
    return dt, acc


def bench_mmap_write_byte(n):
    m = mmap.mmap(-1, 65536)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        m.seek(0)
        m.write_byte(i & 255)
        acc += m.tell()
    dt = time.perf_counter() - t0
    m.close()
    return dt, acc


def bench_mmap_getitem(n):
    m = mmap.mmap(-1, 65536)
    m.seek(0)
    m.write(b"z" * 60000)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        acc += m.__getitem__(i * 7 % 60000)
    dt = time.perf_counter() - t0
    m.close()
    return dt, acc


def bench_mmap_setitem(n):
    m = mmap.mmap(-1, 65536)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        off = i * 7 % 60000
        m.__setitem__(off, i & 255)
        acc += m.__getitem__(off)
    dt = time.perf_counter() - t0
    m.close()
    return dt, acc


def bench_mmap_find(n):
    m = mmap.mmap(-1, 65536)
    m.seek(50000)
    m.write(b"needle")
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        acc += m.find(b"needle", 0, 65536)
    dt = time.perf_counter() - t0
    m.close()
    return dt, acc


def bench_mmap_rfind(n):
    m = mmap.mmap(-1, 65536)
    m.seek(50000)
    m.write(b"needle")
    m.seek(60000)
    m.write(b"needle")
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        acc += m.rfind(b"needle", 0, 65536)
    dt = time.perf_counter() - t0
    m.close()
    return dt, acc


def bench_mmap_flush(n):
    m = mmap.mmap(-1, 65536)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        m.flush()
        acc += 1
    dt = time.perf_counter() - t0
    m.close()
    return dt, acc


def bench_mmap_move(n):
    m = mmap.mmap(-1, 65536)
    m.__setitem__(1024, 55)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        m.move(0, 1024, 512)
        acc += m.__getitem__(0)
    dt = time.perf_counter() - t0
    m.close()
    return dt, acc


def bench_mmap_resize(n):
    m = mmap.mmap(-1, 8192)
    t0 = time.perf_counter()
    acc = 0
    for i in range(n):
        m.resize(8192)
        acc += m.__len__()
    dt = time.perf_counter() - t0
    m.close()
    return dt, acc


def emit_row(name, dt, n, acc):
    print(f"ROW|{name}|{n}|{dt * 1e9 / n}|{acc}")


def emit_sec(name):
    print(f"SEC|{name}")


def best_of(fn, n, rounds=3):
    dt, acc = fn(n)
    for _ in range(rounds - 1):
        d2, acc = fn(n)
        dt = min(dt, d2)
    return dt, acc


def run(name, fn, n):
    dt, acc = best_of(fn, n)
    emit_row(name, dt, n, acc)


BENCHES = [
    ("math.sqrt loop", bench_sqrt, 2000000),
    ("SEC", "struct", 0),
    ("struct.pack `<iid`", bench_struct_pack, 200000),
    ("struct.unpack `<iid`", bench_struct_unpack, 200000),
    ("struct.pack_into `<iid`", bench_struct_pack_into, 200000),
    ("struct.unpack_from `<iid`", bench_struct_unpack_from, 200000),
    ("struct.calcsize `<iid`", bench_struct_calcsize, 500000),
    ("SEC", "binascii (43B payload)", 0),
    ("binascii.hexlify", bench_hexlify, 50000),
    ("binascii.b2a_hex", bench_b2a_hex, 50000),
    ("binascii.unhexlify", bench_unhexlify, 50000),
    ("binascii.a2b_hex", bench_a2b_hex, 50000),
    ("binascii.b2a_base64", bench_b2a_base64, 50000),
    ("binascii.a2b_base64", bench_a2b_base64, 50000),
    ("binascii.crc32", bench_crc32, 100000),
    ("binascii.crc_hqx", bench_crc_hqx, 50000),
    ("binascii.b2a_uu", bench_b2a_uu, 50000),
    ("binascii.a2b_uu", bench_a2b_uu, 50000),
    ("binascii.a2b_qp", bench_a2b_qp, 50000),
    ("binascii.b2a_qp", bench_b2a_qp, 50000),
    ("SEC", "array (`i` typecode)", 0),
    ("array.array init [2]", bench_arr_init, 200000),
    ("array append+get", bench_arr_append, 300000),
    ("array.extend [3]", bench_arr_extend, 100000),
    ("array.fromlist [1]", bench_arr_fromlist, 100000),
    ("array.insert(0)", bench_arr_insert, 10000),
    ("array.pop()", bench_arr_pop, 300000),
    ("array.remove+reappend", bench_arr_remove, 30000),
    ("array.index", bench_arr_index, 50000),
    ("array.count", bench_arr_count, 30000),
    ("array.__contains__", bench_arr_contains, 100000),
    ("array.reverse", bench_arr_reverse, 50000),
    ("array.byteswap", bench_arr_byteswap, 50000),
    ("array.tobytes", bench_arr_tobytes, 100000),
    ("array.frombytes", bench_arr_frombytes, 100000),
    ("array.tolist", bench_arr_tolist, 20000),
    ("array.buffer_info", bench_arr_buffer_info, 200000),
    ("array.__len__", bench_arr_len, 300000),
    ("array.__getitem__", bench_arr_getitem, 300000),
    ("array.__setitem__", bench_arr_setitem, 300000),
    ("array.__eq__", bench_arr_eq, 50000),
    ("array.__ne__", bench_arr_ne, 50000),
    ("array.__add__", bench_arr_add, 50000),
    ("array.__mul__ x3", bench_arr_mul, 20000),
    ("array.tofile (BytesIO)", bench_arr_tofile, 50000),
    ("array.fromfile (BytesIO)", bench_arr_fromfile, 50000),
    ("SEC", "mmap (64KiB anon)", 0),
    ("mmap init+close", bench_mmap_init, 20000),
    ("mmap enter/exit", bench_mmap_ctx, 20000),
    ("mmap.__len__", bench_mmap_len, 200000),
    ("mmap.tell", bench_mmap_tell, 200000),
    ("mmap.seek", bench_mmap_seek, 200000),
    ("mmap.read(64)", bench_mmap_read, 100000),
    ("mmap.read_byte", bench_mmap_read_byte, 200000),
    ("mmap.readline", bench_mmap_readline, 50000),
    ("mmap.write(64)", bench_mmap_write, 100000),
    ("mmap.write_byte", bench_mmap_write_byte, 200000),
    ("mmap.__getitem__", bench_mmap_getitem, 300000),
    ("mmap.__setitem__", bench_mmap_setitem, 300000),
    ("mmap.find", bench_mmap_find, 20000),
    ("mmap.rfind", bench_mmap_rfind, 20000),
    ("mmap.flush", bench_mmap_flush, 50000),
    ("mmap.move 512B", bench_mmap_move, 50000),
    ("mmap.resize same 8K", bench_mmap_resize, 10000),
]


if __name__ == "__main__":
    scale = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    for name, fn, n in BENCHES:
        if name == "SEC":
            emit_sec(fn)
            continue
        run(name, fn, n * scale)
