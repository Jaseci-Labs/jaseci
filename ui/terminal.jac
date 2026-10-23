"""Product-owned terminal seam: process adapter + shared interface contract.

ProcessTerminal ports the required host behavior from the floor reference
(raw mode, alternate screen, bracketed paste enable, synchronized output,
SIGWINCH resize plus poll-tick size re-check, SIGTERM/SIGHUP clean restore,
and reliable restoration) using Python stdlib only
(`termios`, `tty`, `select`, `signal`, `fcntl`).
It does not import or modify `tui/pi_jac_floor`.

VirtualTerminal (virtual_terminal.jac) is the primary test adapter.

Native-lowering status: the former `atexit` safety-net registration was
removed app-side — teardown is owned by explicit restore paths (signal
handlers here plus the `term.stop()` in tui.run_tui's finally). The
remaining imports are irreducible OS interfaces with no pure-Jac
substitute. VENDOR NA_STDLIB FLOOR REQUEST (blocks native lowering,
error E5090): incremental UTF-8 decoding (`codecs.getincrementaldecoder`
— or any streaming text decode), POSIX termios raw-mode get/set
(`termios.tcgetattr/tcsetattr`, `tty.setraw`), window-size ioctl
(`fcntl.ioctl` + `termios.TIOCGWINSZ`), POSIX signal handling
(`signal.signal` for SIGWINCH/SIGINT/SIGTERM/SIGHUP), and multiplexed
stdin readiness (`select.select`).
"""

import sys;
import os;
import codecs;
import signal;
import select;
import termios;
import tty;
import fcntl;
import struct;


glob ENABLE_BRACKETED_PASTE: str = "\x1b[?2004h";
glob DISABLE_BRACKETED_PASTE: str = "\x1b[?2004l";
glob ENTER_ALT_SCREEN: str = "\x1b[?1049h";
glob LEAVE_ALT_SCREEN: str = "\x1b[?1049l";
glob SYNC_BEGIN: str = "\x1b[?2026h";
glob SYNC_END: str = "\x1b[?2026l";
glob HIDE_CURSOR: str = "\x1b[?25l";
glob SHOW_CURSOR: str = "\x1b[?25h";
glob CLEAR_SCREEN: str = "\x1b[2J\x1b[H";


"""Minimal terminal capability surface used by the renderer and host loop."""
obj Terminal {
    has columns: int = 80,
        rows: int = 24,
        started: bool = False,
        restored: bool = True,
        alternate_screen: bool = False,
        bracketed_paste: bool = False,
        cursor_visible: bool = True,
        sync_active: bool = False;

    def size() -> tuple[int, int] {
        return (self.columns, self.rows);
    }

    def write(data: str) -> None {
        raise NotImplementedError("Terminal.write");
    }

    def start() -> None {
        raise NotImplementedError("Terminal.start");
    }

    def stop() -> None {
        raise NotImplementedError("Terminal.stop");
    }

    def enter_alternate_screen() -> None {
        self.write(ENTER_ALT_SCREEN);
        self.alternate_screen = True;
    }

    def leave_alternate_screen() -> None {
        self.write(LEAVE_ALT_SCREEN);
        self.alternate_screen = False;
    }

    def begin_synchronized_update() -> None {
        self.write(SYNC_BEGIN);
        self.sync_active = True;
    }

    def end_synchronized_update() -> None {
        self.write(SYNC_END);
        self.sync_active = False;
    }

    def hide_cursor() -> None {
        self.write(HIDE_CURSOR);
        self.cursor_visible = False;
    }

    def show_cursor() -> None {
        self.write(SHOW_CURSOR);
        self.cursor_visible = True;
    }

    def clear_screen() -> None {
        self.write(CLEAR_SCREEN);
    }

    def enable_bracketed_paste() -> None {
        self.write(ENABLE_BRACKETED_PASTE);
        self.bracketed_paste = True;
    }

    def disable_bracketed_paste() -> None {
        self.write(DISABLE_BRACKETED_PASTE);
        self.bracketed_paste = False;
    }

    def set_title(title: str) -> None {
        self.write(f"\x1b]0;{title}\x07");
    }

    def move_cursor(row: int, col: int) -> None {
        self.write(f"\x1b[{row};{col}H");
    }

    """Restore host terminal modes. Safe to call more than once."""
    def restore() -> None {
        self.stop();
    }
}


def _ioctl_winsize(fd: int) -> tuple[int, int] | None {
    try {
        packed = fcntl.ioctl(fd, termios.TIOCGWINSZ, struct.pack("HHHH", 0, 0, 0, 0));
        (rows, cols, _x, _y) = struct.unpack("HHHH", packed);
        if rows > 0 and cols > 0 {
            return (cols, rows);
        }
    } except Exception {
    }
    return None;
}


"""Incremental UTF-8 decoder holding split multibyte sequences across reads.

A multibyte character split across two os.read chunks must not be corrupted:
bytes are buffered until they form a complete sequence; invalid bytes become
U+FFFD replacement characters without losing the surrounding text.
"""
obj Utf8StreamDecoder {
    has _pending: bytes = b"";

    def init() {}

    def feed(data: bytes) -> str {
        buf: bytes = self._pending;
        if len(data) > 0 {
            if len(buf) == 0 {
                buf = data;
            } else {
                buf = buf + data;
            }
        }
        out: str = "";
        n: int = len(buf);
        i: int = 0;
        while i < n {
            b0: int = buf[i];
            need: int = 0;
            lo: int = 0x80;
            hi: int = 0xBF;
            cp: int = 0;
            ok: bool = True;
            if b0 < 0x80 {
                out += chr(b0);
                i += 1;
                continue;
            } elif b0 >= 0xC2 and b0 <= 0xDF {
                need = 1;
                cp = b0 - 0xC0;
            } elif b0 == 0xE0 {
                need = 2;
                lo = 0xA0;
                cp = b0 - 0xE0;
            } elif b0 >= 0xE1 and b0 <= 0xEC {
                need = 2;
                cp = b0 - 0xE0;
            } elif b0 == 0xED {
                need = 2;
                hi = 0x9F;
                cp = b0 - 0xE0;
            } elif b0 >= 0xEE and b0 <= 0xEF {
                need = 2;
                cp = b0 - 0xE0;
            } elif b0 == 0xF0 {
                need = 3;
                lo = 0x90;
                cp = b0 - 0xF0;
            } elif b0 >= 0xF1 and b0 <= 0xF3 {
                need = 3;
                cp = b0 - 0xF0;
            } elif b0 == 0xF4 {
                need = 3;
                hi = 0x8F;
                cp = b0 - 0xF0;
            } else {
                ok = False;
            }
            if not ok {
                out += "\uFFFD";
                i += 1;
                continue;
            }
            if i + need > n - 1 {
                break;
            }
            j: int = 1;
            good: bool = True;
            while j <= need {
                bj: int = buf[i + j];
                lim_lo: int = lo;
                lim_hi: int = hi;
                if j > 1 {
                    lim_lo = 0x80;
                    lim_hi = 0xBF;
                }
                if bj < lim_lo or bj > lim_hi {
                    good = False;
                    break;
                }
                cp = cp * 64 + (bj - 0x80);
                j += 1;
            }
            if not good {
                out += "\uFFFD";
                i += j;
                continue;
            }
            out += chr(cp);
            i += need + 1;
        }
        if i >= n {
            self._pending = b"";
        } else {
            self._pending = buf[i:n];
        }
        return out;
    }
}


def read_terminal_size(fallback_cols: int = 80, fallback_rows: int = 24) -> tuple[int, int] {
    for stream in [sys.stdout, sys.stdin, sys.stderr] {
        try {
            fd = stream.fileno() as int;
        } except Exception {
            continue;
        }
        got = _ioctl_winsize(fd);
        if got is not None {
            return got;
        }
    }
    env_cols = os.environ.get("COLUMNS");
    env_rows = os.environ.get("LINES");
    cols = int(env_cols) if env_cols else fallback_cols;
    rows = int(env_rows) if env_rows else fallback_rows;
    if cols <= 0 {
        cols = fallback_cols;
    }
    if rows <= 0 {
        rows = fallback_rows;
    }
    return (cols, rows);
}


"""POSIX process terminal using termios raw mode and signal-driven resize."""
obj ProcessTerminal(Terminal) {
    has _fd: int = -1,
        _old_attrs: any = None,
        _old_handler: any = None,
        _old_sigint: any = None,
        _old_sigterm: any = None,
        _old_sighup: any = None,
        _utf8: any = None,
        _stdin_buf: str = "",
        eof: bool = False,
        on_resize: any = None,
        on_input: any = None,
        on_interrupt: any = None,
        on_terminate: any = None;

    def init(
        on_input: any = None,
        on_resize: any = None,
        on_interrupt: any = None,
        on_terminate: any = None,
    ) {
        super.init();
        self.on_input = on_input;
        self.on_resize = on_resize;
        self.on_interrupt = on_interrupt;
        self.on_terminate = on_terminate;
        self._fd = -1;
        self._old_attrs = None;
        self._old_handler = None;
        self._old_sigint = None;
        self._old_sigterm = None;
        self._old_sighup = None;
        self._utf8 = Utf8StreamDecoder();
        self._stdin_buf = "";
        self.eof = False;
        self.restored = True;
    }

    def write(data: str) -> None {
        if not data {
            return;
        }
        sys.stdout.write(data);
        sys.stdout.flush();
    }

    def _refresh_size() {
        (cols, rows) = read_terminal_size(self.columns, self.rows);
        changed = cols != self.columns or rows != self.rows;
        self.columns = cols;
        self.rows = rows;
        if changed and self.on_resize is not None {
            self.on_resize(cols, rows);
        }
    }

    def _on_sigwinch(signum: int, frame: any) {
        self._refresh_size();
    }

    """SIGTERM/SIGHUP handler: restore the host terminal before the process dies."""
    def _on_terminate_signal(signum: int, frame: any) {
        self.restore();
        if self.on_terminate is not None {
            self.on_terminate();
        } else {
            raise SystemExit(128 + signum);
        }
    }

    def _on_sigint(signum: int, frame: any) {
        self.restore();
        if self.on_interrupt is not None {
            self.on_interrupt();
        } else {
            raise KeyboardInterrupt();
        }
    }

    def start() -> None {
        if self.started {
            return;
        }
        if not sys.stdin.isatty() {
            raise RuntimeError("ProcessTerminal requires a TTY stdin");
        }
        self._fd = sys.stdin.fileno() as int;
        self._old_attrs = termios.tcgetattr(self._fd);
        tty.setraw(self._fd);
        # Mark active before anything fallible so stop() can unwind a partial start.
        self.started = True;
        self.restored = False;
        try {
            self._refresh_size();
            sigwinch = signal.SIGWINCH as int;
            sigint = signal.SIGINT as int;
            self._old_handler = signal.signal(sigwinch, self._on_sigwinch);
            self._old_sigint = signal.signal(sigint, self._on_sigint);
            self._old_sigterm = signal.signal(signal.SIGTERM as int, self._on_terminate_signal);
            self._old_sighup = signal.signal(signal.SIGHUP as int, self._on_terminate_signal);
            self.enable_bracketed_paste();
            self.enter_alternate_screen();
            self.hide_cursor();
        } except Exception {
            self.stop();
            raise;
        }
    }

    def stop() -> None {
        if self.restored and not self.started {
            return;
        }
        try {
            if self.sync_active {
                self.end_synchronized_update();
            }
            if self.bracketed_paste {
                self.disable_bracketed_paste();
            }
            if self.alternate_screen {
                self.leave_alternate_screen();
            }
            if not self.cursor_visible {
                self.show_cursor();
            }
        } except Exception {
        }
        if self._old_handler is not None {
            try {
                signal.signal(signal.SIGWINCH as int, self._old_handler);
            } except Exception {
            }
            self._old_handler = None;
        }
        if self._old_sigint is not None {
            try {
                signal.signal(signal.SIGINT as int, self._old_sigint);
            } except Exception {
            }
            self._old_sigint = None;
        }
        if self._old_sigterm is not None {
            try {
                signal.signal(signal.SIGTERM as int, self._old_sigterm);
            } except Exception {
            }
            self._old_sigterm = None;
        }
        if self._old_sighup is not None {
            try {
                signal.signal(signal.SIGHUP as int, self._old_sighup);
            } except Exception {
            }
            self._old_sighup = None;
        }
        if self._old_attrs is not None and self._fd >= 0 {
            try {
                termios.tcsetattr(self._fd, termios.TCSADRAIN, self._old_attrs);
            } except Exception {
            }
            self._old_attrs = None;
        }
        self.started = False;
        self.restored = True;
    }

    """Non-blocking poll of stdin. Returns decoded text (may be empty).

    Re-checks the winsize each tick: select() auto-retries after SIGWINCH
    (PEP 475), so a resize would otherwise go unnoticed unless the host loop
    polls size itself. The re-check fires on_resize only on dimension change.
    """
    def poll_input(timeout_s: float = 0.0) -> str {
        if not self.started or self._fd < 0 {
            return "";
        }
        self._refresh_size();
        ready = select.select([self._fd], [], [], timeout_s);
        if not ready[0] {
            return "";
        }
        try {
            data = os.read(self._fd, 8192);
        } except BlockingIOError {
            return "";
        } except OSError {
            return "";
        }
        if not data {
            self.eof = True;
            return "";
        }
        text = self._utf8.feed(data);
        if self.on_input is not None {
            self.on_input(text);
        }
        return text;
    }
}


"""Emit one synchronized write: begin sync, body, end sync."""
def synchronized_write(term: Terminal, data: str) {
    term.begin_synchronized_update();
    try {
        term.write(data);
    } finally {
        term.end_synchronized_update();
    }
}
