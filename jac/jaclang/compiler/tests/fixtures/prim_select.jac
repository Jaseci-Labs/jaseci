"""Bundled native `select` cross-backend equivalence fixture.

`import select` binds CPython's `select` on sv and the bundled
`na_stdlib/select.jac` on na. Pipe fds: `os.pipe()` on sv, libc `pipe(2)`
on na. Pins: a written pipe end answers readable, a pipe's write end
answers writable at timeout 0.0, the empty probe answers three empty
lists, and the block-forever sentinel answers immediately for a ready fd
(spelled `None` on sv -- CPython's sentinel -- and `-1.0` on na: the
documented divergence, so each lane pins its own spelling of the same
observable). ES/JS opts out (POSIX-only).
"""

import os;
import select;
import from c {
    def pipe(fds: bytes) -> i32;  def write(fd: i32, buf: bytes, n: u64) -> i64;  def close(
        fd: i32
    ) -> i32;
}


def _pipe_na -> tuple[(int, int)] {
    fds: bytes = b"\x00" * 8;
    pipe(fds);
    r: int = int.from_bytes(fds[0:4], "little");
    w: int = int.from_bytes(fds[4:8], "little");
    return (r, w);
}


def select_py -> dict[any, any] {
    d: dict[any, any] = {};
    (rfd, wfd) = os.pipe();
    os.write(wfd, b"x");
    (rr, _wr, _xr) = select.select([rfd], [], [], 0.0);
    d["read_ready"] = 1 if len(rr) > 0 else 0;
    (_r2, wlist, _x2) = select.select([], [wfd], [], 0.0);
    d["write_ready"] = 1 if len(wlist) > 0 else 0;
    (br, _bw, _bx) = select.select([rfd], [], [], None);
    d["block_ready"] = 1 if len(br) > 0 else 0;
    (er, ew, ex) = select.select([], [], [], 0.0);
    d["empty_ok"] = 1 if (len(er) == 0 and len(ew) == 0 and len(ex) == 0) else 0;
    (r3, w3, x3) = select.select([rfd], [wfd], [], 0.0);
    d["both_ready"] = 1 if (len(r3) == 1 and len(w3) == 1 and len(x3) == 0) else 0;
    d["pollin"] = select.POLLIN;
    d["pollout"] = select.POLLOUT;
    os.close(rfd);
    os.close(wfd);
    return d;
}


def select_cl -> dict[any, any] {
    return {};
}


def select_na -> dict[str, any] {
    d: dict[str, any] = {};
    (rfd, wfd) = _pipe_na();
    payload: bytes = b"x";
    write(i32(wfd), payload, u64(1));
    (rr, _wr, _xr) = select.select([rfd], [], [], 0.0);
    d["read_ready"] = 1 if len(rr) > 0 else 0;
    (_r2, wlist, _x2) = select.select([], [wfd], [], 0.0);
    d["write_ready"] = 1 if len(wlist) > 0 else 0;
    (br, _bw, _bx) = select.select([rfd], [], [], -1.0);
    d["block_ready"] = 1 if len(br) > 0 else 0;
    (er, ew, ex) = select.select([], [], [], 0.0);
    d["empty_ok"] = 1 if (len(er) == 0 and len(ew) == 0 and len(ex) == 0) else 0;
    (r3, w3, x3) = select.select([rfd], [wfd], [], 0.0);
    d["both_ready"] = 1 if (len(r3) == 1 and len(w3) == 1 and len(x3) == 0) else 0;
    d["pollin"] = select.POLLIN;
    d["pollout"] = select.POLLOUT;
    close(i32(rfd));
    close(i32(wfd));
    return d;
}
