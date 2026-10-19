"""Bundled native `fcntl` cross-backend equivalence fixture.

The SAME `import fcntl` binds CPython's `fcntl` on the sv (Python) backend
and the bundled `na_stdlib/fcntl.jac` on the na (native LLVM) backend. Pipe
fds: `os.pipe()` on sv, libc `pipe(2)` on na. Pins the F_GETFL/F_SETFL
O_NONBLOCK round trip (toggle on, read back, restore, read back), the
per-OS constant values (sv reads O_NONBLOCK from `os`, na from the `fcntl`
floor -- same value on the host), an EBADF raise as raised/did-not-raise
(the error TYPE diverges: OSError vs ValueError), and an
`ioctl(TIOCGWINSZ)` probe on stdin fd 0 that degrades to zeros when fd 0
is not a terminal (CI), so the key set never drifts. ES/JS opts out
(POSIX-only).
"""

import os;
import fcntl;
import from termios { TIOCGWINSZ }
import from c { def pipe(fds: bytes) -> i32;  def close(fd: i32) -> i32;  }


def _pipe_na -> tuple[(int, int)] {
    fds: bytes = b"\x00" * 8;
    pipe(fds);
    r: int = int.from_bytes(fds[0:4], "little");
    w: int = int.from_bytes(fds[4:8], "little");
    return (r, w);
}


def fcntl_py -> dict[any, any] {
    d: dict[any, any] = {};
    (rfd, wfd) = os.pipe();
    flags0 = fcntl.fcntl(rfd, fcntl.F_GETFL);
    nb_on = flags0 | os.O_NONBLOCK;
    fcntl.fcntl(rfd, fcntl.F_SETFL, nb_on);
    flags1 = fcntl.fcntl(rfd, fcntl.F_GETFL);

    fcntl.fcntl(rfd, fcntl.F_SETFL, flags0);
    flags2 = fcntl.fcntl(rfd, fcntl.F_GETFL);
    d["nb_toggled"] = 1 if (flags1 & os.O_NONBLOCK) != 0 else 0;
    d["restored"] = 1 if flags2 == flags0 else 0;
    raised = 0;
    try {
        fcntl.fcntl(9999, fcntl.F_GETFL);
    } except Exception {
        raised = 1;
    }
    d["ebadf_raised"] = raised;
    d["c_f_getfl"] = fcntl.F_GETFL;
    d["c_f_setfl"] = fcntl.F_SETFL;
    d["c_o_nonblock"] = os.O_NONBLOCK;

    ws_ok = 0;
    ws_rows = 0;
    ws_cols = 0;
    ws_bytes = 0;
    try {
        buf = b"\x00" * 8;
        buf = fcntl.ioctl(0, TIOCGWINSZ, buf);
        ws_ok = 1;
        ws_bytes = len(buf);
        ws_rows = int.from_bytes(buf[0:2], "little");
        ws_cols = int.from_bytes(buf[2:4], "little");
    } except Exception {
        ws_rows = 0;
    }
    d["ws_ok"] = ws_ok;
    d["ws_rows"] = ws_rows;
    d["ws_cols"] = ws_cols;
    d["ws_bytes"] = ws_bytes;
    os.close(rfd);
    os.close(wfd);
    return d;
}


def fcntl_cl -> dict[any, any] {
    return {};
}


def fcntl_na -> dict[str, any] {
    d: dict[str, any] = {};
    (rfd, wfd) = _pipe_na();
    flags0: int = fcntl.fcntl(rfd, fcntl.F_GETFL);
    nb_on: int = flags0 | os.O_NONBLOCK;
    fcntl.fcntl(rfd, fcntl.F_SETFL, nb_on);
    flags1: int = fcntl.fcntl(rfd, fcntl.F_GETFL);

    fcntl.fcntl(rfd, fcntl.F_SETFL, flags0);
    flags2: int = fcntl.fcntl(rfd, fcntl.F_GETFL);
    d["nb_toggled"] = 1 if (flags1 & os.O_NONBLOCK) != 0 else 0;
    d["restored"] = 1 if flags2 == flags0 else 0;
    raised: int = 0;
    try {
        fcntl.fcntl(9999, fcntl.F_GETFL);
    } except Exception {
        raised = 1;
    }
    d["ebadf_raised"] = raised;
    d["c_f_getfl"] = fcntl.F_GETFL;
    d["c_f_setfl"] = fcntl.F_SETFL;
    d["c_o_nonblock"] = fcntl.O_NONBLOCK;

    ws_ok: int = 0;
    ws_rows: int = 0;
    ws_cols: int = 0;
    ws_bytes: int = 0;
    try {
        buf: bytes = b"\x00" * 8;
        buf = fcntl.ioctl(0, TIOCGWINSZ, buf);
        ws_ok = 1;
        ws_bytes = len(buf);
        ws_rows = int.from_bytes(buf[0:2], "little");
        ws_cols = int.from_bytes(buf[2:4], "little");
    } except Exception {
        ws_rows = 0;
    }
    d["ws_ok"] = ws_ok;
    d["ws_rows"] = ws_rows;
    d["ws_cols"] = ws_cols;
    d["ws_bytes"] = ws_bytes;
    close(i32(rfd));
    close(i32(wfd));
    return d;
}
