"""Bundled native ``mmap`` cross-backend equivalence fixture.

The SAME ``import mmap`` binds CPython's ``mmap`` module on the sv (Python)
backend and the bundled ``na_stdlib/mmap.jac`` Mechanism-B module (over the
``_mmap_native`` OS FFI floors) on the na (native LLVM) backend. This fixture
pins the two congruent using anonymous mappings, which both lanes can create
with ``mmap.mmap(-1, length)``.

Byte results are compared via ``_digest`` of ``read`` output --
raw ``bytes`` cannot be marshalled across the sv/na boundary.

Dunder divergence: the na pathway does not dispatch operator syntax to
dunder methods on objs, so BOTH lanes call them explicitly
(``m.__getitem__``, ``m.__setitem__``, ``m.__len__``) -- explicit calls are
legal on CPython too.

Not exercised (documented na divergences or platform-dependent):
  - ``m.size()`` on an anonymous map (CPython raises ``OSError: Bad file
    descriptor`` -- the na surface reports the map length),
  - ``m[1:3]`` slicing, file-backed maps, ``ACCESS_COPY`` semantics.

ES/JS opts out (``mmap_cl`` returns an empty dict).
"""

import mmap;


def _digest(data: bytes) -> int {
    acc: int = 2166136261;
    n: int = len(data);
    i: int = 0;
    while i < n {
        acc = (acc * 131 + data[i]) % 2147483647;
        i += 1;
    }
    return acc;
}


def mmap_py -> dict[any, any] {
    m = mmap.mmap(-1, 64);
    m.write(b"hello mmap world");
    m.seek(0);
    first = m.read(5);
    m.__setitem__(0, 74);
    m.seek(6);
    m.write_byte(88);
    m.seek(0);
    whole = m.read(16);
    r: dict[str, any] = {
        "len": m.__len__(),
        "g0": m.__getitem__(0),
        "g6": m.__getitem__(6),
        "read5_digest": _digest(first),
        "whole_digest": _digest(whole),
        "find": m.find(b"mmap"),
        "rfind": m.rfind(b"o"),
        "find_none": m.find(b"zzz"),
        "tell_after": m.tell(),
        "readbyte": m.read_byte()
    };
    m.seek(0);
    r["find2"] = m.find(b"mmap");
    r["rfind2"] = m.rfind(b"o");
    m.move(20, 0, 5);
    m.seek(20);
    r["move_digest"] = _digest(m.read(5));
    m.close();
    pm = mmap.mmap(-1, 64, access=mmap.ACCESS_WRITE);
    pm.write(b"hello mmap world");
    try {
        pm.resize(128);
        r["err_resize"] = "noraise";
    } except ValueError as e {
        r["err_resize"] = str(e);
    }
    pm.close();
    m2 = mmap.mmap(-1, 64);
    m2.seek(0);
    m2.seek(2, 1);
    r["seek_cur"] = m2.tell();
    m2.seek(-2, 2);
    r["seek_end"] = m2.tell();
    try {
        m2.seek(999);
        r["err_seek"] = "noraise";
    } except ValueError as e {
        r["err_seek"] = str(e);
    }
    try {
        m2.__setitem__(200, 65);
        r["err_setitem"] = "noraise";
    } except IndexError as e {
        r["err_setitem"] = str(e);
    }
    try {
        m2.__getitem__(200);
        r["err_getitem"] = "noraise";
    } except IndexError as e {
        r["err_getitem"] = str(e);
    }
    m2.close();
    r["closed"] = 1 if m2.closed else 0;
    try {
        m2.read(1);
        r["err_closed"] = "noraise";
    } except ValueError as e {
        r["err_closed"] = str(e);
    }
    ro = mmap.mmap(-1, 32, access=mmap.ACCESS_READ);
    try {
        ro.write(b"x");
        r["err_rote"] = "noraise";
    } except TypeError as e {
        r["err_rote"] = str(e);
    }
    ro.close();
    return r;
}


def mmap_cl -> dict[any, any] {
    return {};
}


def _digest_na(data: bytes) -> int {
    acc: int = 2166136261;
    n: int = len(data);
    i: int = 0;
    while i < n {
        acc = (acc * 131 + data[i]) % 2147483647;
        i += 1;
    }
    return acc;
}


def _core_na(r: dict[str, any]) {
    m = mmap.mmap(-1, 64);
    m.write(b"hello mmap world");
    m.seek(0);
    first = m.read(5);
    m.__setitem__(0, 74);
    m.seek(6);
    m.write_byte(88);
    m.seek(0);
    whole = m.read(16);
    r["len"] = m.__len__();
    r["g0"] = m.__getitem__(0);
    r["g6"] = m.__getitem__(6);
    r["read5_digest"] = _digest_na(first);
    r["whole_digest"] = _digest_na(whole);
    r["find"] = m.find(b"mmap");
    r["rfind"] = m.rfind(b"o");
    r["find_none"] = m.find(b"zzz");
    r["tell_after"] = m.tell();
    r["readbyte"] = m.read_byte();
    m.seek(0);
    r["find2"] = m.find(b"mmap");
    r["rfind2"] = m.rfind(b"o");
    m.move(20, 0, 5);
    m.seek(20);
    r["move_digest"] = _digest_na(m.read(5));
    m.close();
}


def _seek_resize_na(r: dict[str, any]) {
    # MAP_PRIVATE anonymous: CPython refuses to expand a MAP_SHARED anonymous
    # mapping on Linux ("can't expand a shared anonymous mapping"), so the sv
    # lane uses MAP_PRIVATE and this lane matches.
    pm = mmap.mmap(-1, 64, access=mmap.ACCESS_WRITE);
    pm.write(b"hello mmap world");
    try {
        pm.resize(128);
        r["err_resize"] = "noraise";
    } except ValueError as e {
        r["err_resize"] = str(e);
    }
    pm.close();
    m = mmap.mmap(-1, 64);
    m.seek(0);
    m.seek(2, 1);
    r["seek_cur"] = m.tell();
    m.seek(-2, 2);
    r["seek_end"] = m.tell();
    m.close();
}


def _err_na(r: dict[str, any]) {
    m = mmap.mmap(-1, 64);
    m.write(b"hello mmap world");
    try {
        m.seek(999);
        r["err_seek"] = "noraise";
    } except ValueError as e {
        r["err_seek"] = str(e);
    }
    try {
        m.__setitem__(200, 65);
        r["err_setitem"] = "noraise";
    } except IndexError as e {
        r["err_setitem"] = str(e);
    }
    try {
        m.__getitem__(200);
        r["err_getitem"] = "noraise";
    } except IndexError as e {
        r["err_getitem"] = str(e);
    }
    m.close();
    r["closed"] = 1 if m.closed else 0;
    try {
        m.read(1);
        r["err_closed"] = "noraise";
    } except ValueError as e {
        r["err_closed"] = str(e);
    }
    ro = mmap.mmap(-1, 32, access=mmap.ACCESS_READ);
    try {
        ro.write(b"x");
        r["err_rote"] = "noraise";
    } except TypeError as e {
        r["err_rote"] = str(e);
    }
    ro.close();
}


def mmap_na -> dict[str, any] {
    r: dict[str, any] = {};
    _core_na(r);
    _seek_resize_na(r);
    _err_na(r);
    return r;
}
