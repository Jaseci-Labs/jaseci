"""Bundled native `termios` cross-backend equivalence fixture.

The SAME `import from termios { ... }` binds CPython's `termios` on the sv
(Python) backend and the bundled `na_stdlib/termios.jac` on the na (native
LLVM) backend. `tcgetattr` needs a tty (pipes answer ENOTTY), so both lanes
run against the slave side of a pseudo-terminal: `os.openpty()` on sv, libc
`openpty(3)` on na (its name/termios/winsize out-params are passed as NULL).
The master fd stays open until the end -- closing it first makes the
slave's termios calls fail with EIO. Pins the CPython result shape (7
elements, `cc` of NCCS ints), the per-OS constant values, an attribute
round trip, a cc write, and the raise paths (ENOTTY pipe, invalid `when`)
as raised/did-not-raise, since the error TYPE diverges (ValueError vs
termios.error). ES/JS opts out (POSIX-only).
"""

import os;
import termios;
import from termios { TCSADRAIN, TCSANOW, ECHO, ICANON, VMIN, VTIME }
import from c {
    def openpty(am: bytes, asl: bytes, name: int, t: int, w: int) -> i32;  def pipe(
        fds: bytes
    ) -> i32;  def close(fd: i32) -> i32;
}


"""A pty pair from libc openpty(3); NULL name/termios/winsize out-params."""
def _pty_pair_na -> tuple[(int, int)] {
    am: bytes = b"\x00" * 4;
    asl: bytes = b"\x00" * 4;
    openpty(am, asl, 0, 0, 0);
    m: int = int.from_bytes(am[0:4], "little");
    s: int = int.from_bytes(asl[0:4], "little");
    return (m, s);
}


def termios_py -> dict[any, any] {
    d: dict[any, any] = {};
    (m, s) = os.openpty();
    attrs = termios.tcgetattr(s);
    d["attrs_len"] = len(attrs);
    d["cc_len"] = len(attrs[6]);
    d["iflag"] = attrs[0];
    d["lflag"] = attrs[3];
    d["ispeed"] = attrs[4];
    d["ospeed"] = attrs[5];
    d["tcsadrain"] = TCSADRAIN;
    d["tcsanow"] = TCSANOW;
    d["echo"] = ECHO;
    d["icanon"] = ICANON;
    d["vmin"] = VMIN;
    d["vtime"] = VTIME;
    saved_iflag = attrs[0];
    termios.tcsetattr(s, TCSADRAIN, attrs);
    attrs2 = termios.tcgetattr(s);
    d["iflag_roundtrip"] = 1 if attrs2[0] == saved_iflag else 0;
    d["speed_roundtrip"] = 1 if attrs2[4] == attrs[4] and attrs2[5] == attrs[5] else 0;
    cc2 = attrs2[6];
    d["cc_vmin_after_restore"] = _cc_int(cc2[VMIN]);
    cc3 = attrs2[6];
    cc3[VMIN] = 7;
    termios.tcsetattr(s, TCSANOW, attrs2);
    attrs4 = termios.tcgetattr(s);
    d["cc_vmin_write"] = _cc_int(attrs4[6][VMIN]);
    raised = 0;
    try {
        termios.tcsetattr(s, 99, attrs4);
    } except Exception {
        raised = 1;
    }
    d["bad_when_raised"] = raised;
    raised = 0;
    try {
        termios.tcsetattr(s, TCSANOW, attrs + [0]);
    } except Exception {
        raised = 1;
    }
    d["bad_attrs_len_raised"] = raised;
    termios.tcsetattr(s, TCSADRAIN, attrs);
    (prfd, pwfd) = os.pipe();
    raised = 0;
    try {
        termios.tcgetattr(prfd);
    } except Exception {
        raised = 1;
    }
    d["pipe_enotty_raised"] = raised;
    os.close(prfd);
    os.close(pwfd);
    os.close(s);
    os.close(m);
    return d;
}


def termios_cl -> dict[any, any] {
    return {};
}


def termios_na -> dict[str, any] {
    d: dict[str, any] = {};
    (m, s) = _pty_pair_na();
    attrs = termios.tcgetattr(s);
    d["attrs_len"] = len(attrs);
    cc = attrs[6];
    cclen: int = 0;
    if isinstance(cc, list) {
        cclen = len(cc);
    }
    d["cc_len"] = cclen;
    iflag: int = attrs[0];
    lflag: int = attrs[3];
    ispeed: int = attrs[4];
    ospeed: int = attrs[5];
    d["iflag"] = iflag;
    d["lflag"] = lflag;
    d["ispeed"] = ispeed;
    d["ospeed"] = ospeed;
    d["tcsadrain"] = TCSADRAIN;
    d["tcsanow"] = TCSANOW;
    d["echo"] = ECHO;
    d["icanon"] = ICANON;
    d["vmin"] = VMIN;
    d["vtime"] = VTIME;
    termios.tcsetattr(s, TCSADRAIN, attrs);
    attrs2 = termios.tcgetattr(s);
    iflag2: int = attrs2[0];
    d["iflag_roundtrip"] = 1 if iflag2 == iflag else 0;
    d["speed_roundtrip"] = 1 if attrs2[4] == attrs[4] and attrs2[5] == attrs[5] else 0;
    cc2 = attrs2[6];
    vmin_after: int = 0;
    if isinstance(cc2, list) {
        v = cc2[VMIN];
        vmin_after = v;
    }
    d["cc_vmin_after_restore"] = vmin_after;
    cc3 = attrs2[6];
    if isinstance(cc3, list) {
        cc3[VMIN] = 7;
    }
    termios.tcsetattr(s, TCSANOW, attrs2);
    attrs4 = termios.tcgetattr(s);
    cc4 = attrs4[6];
    vmin_wrote: int = 0;
    if isinstance(cc4, list) {
        v4 = cc4[VMIN];
        vmin_wrote = v4;
    }
    d["cc_vmin_write"] = vmin_wrote;
    raised: int = 0;
    try {
        termios.tcsetattr(s, 99, attrs4);
    } except Exception {
        raised = 1;
    }
    d["bad_when_raised"] = raised;
    raised = 0;
    try {
        termios.tcsetattr(s, TCSANOW, attrs + [0]);
    } except Exception {
        raised = 1;
    }
    d["bad_attrs_len_raised"] = raised;
    termios.tcsetattr(s, TCSADRAIN, attrs);
    fds: bytes = b"\x00" * 8;
    pipe(fds);
    prfd: int = int.from_bytes(fds[0:4], "little");
    pwfd: int = int.from_bytes(fds[4:8], "little");
    raised = 0;
    try {
        termios.tcgetattr(prfd);
    } except Exception {
        raised = 1;
    }
    d["pipe_enotty_raised"] = raised;
    close(i32(prfd));
    close(i32(pwfd));
    close(i32(s));
    close(i32(m));
    return d;
}

def _cc_int(value: any) -> int {
    if isinstance(value, int) {
        return value;
    }
    if isinstance(value, bytes) {
        return int.from_bytes(value, "little");
    }
    return 0;
}
