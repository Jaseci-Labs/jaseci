"""Dual-lane stdlib benchmark -- same source, two backends.

    jac run -b python scripts/bench/na_stdlib_bench.jac   # sv lane: Jac on
        # embedded CPython -- `import math` reaches CPython's math.sqrt
        # through the interop bridge; struct/binascii/array/mmap are the
        # CPython modules.
    jac run -b native scripts/bench/na_stdlib_bench.jac   # na lane: the bundled
        # native modules (struct intercept, na_stdlib/*) directly.

Compare against `python3 scripts/bench/na_stdlib_bench.py` for the raw
CPython loop timings. Rows print pipe-separated: name|n|ns_per_op|acc.

Covers the full shared public surface of the PR's modules; na-only
helpers (extend_array/extend_bytes/read_slice/size) live in
na_stdlib_extra.jac since CPython has no such attribute.
"""

import time;
import math;
import struct;
import binascii;
import array;
import mmap;
import io;


def _bchk(b: bytes) -> int {
    n: int = len(b);
    if n == 0 {
        return 0;
    }
    return n * 131 + b[0] * 17 + b[n - 1];
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


def emit_row(name: str, dt: float, n: int, acc: any) {
    print("ROW|", name, "|", n, "|", dt * 1000000000.0 / n, "|", acc);
}


def emit_sec(name: str) {
    print("SEC|", name);
}


# best-of-3 without indirect calls (an `any`-typed callee cannot lower on
# the na pathway): each bench is invoked literally three times at the call
# site and pick() keeps the fastest run -- same policy as the .py best_of.
def pick(a: tuple[float, int], b: tuple[float, int]) -> tuple[float, int] {
    return a if a[0] < b[0] else b;
}


def pickf(a: tuple[float, float], b: tuple[float, float]) -> tuple[float, float] {
    return a if a[0] < b[0] else b;
}


def run_struct {
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


def run_binascii {
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


def run_array {
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
    res = pick(
        pick(bench_arr_pop(300000), bench_arr_pop(300000)), bench_arr_pop(300000)
    );
    emit_row("array.pop()", res[0], 300000, res[1]);
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
    res = pick(
        pick(bench_arr_fromfile(50000), bench_arr_fromfile(50000)),
        bench_arr_fromfile(50000)
    );
    emit_row("array.fromfile (BytesIO)", res[0], 50000, res[1]);
}


def run_mmap {
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


# Section bodies stay in separate functions: a single entry block carrying
# all ~180 call sites hits a superlinear native-codegen path.
with entry {
    resf = pickf(pickf(bench_sqrt(2000000), bench_sqrt(2000000)), bench_sqrt(2000000));
    emit_row("math.sqrt loop", resf[0], 2000000, resf[1]);

    run_struct();
    run_binascii();
    run_array();
    run_mmap();
}
