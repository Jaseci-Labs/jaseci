"""In-memory Terminal adapter for deterministic tests.

Captures writes, maintains a simple cell grid for paint assertions, and
accepts injected input / resize / interrupt events without touching a TTY.
Restoration is tracked so normal exit, exception, and SIGINT paths can be
asserted without a real process terminal.
"""

import from .terminal {
    Terminal,
    ENTER_ALT_SCREEN,
    LEAVE_ALT_SCREEN,
    ENABLE_BRACKETED_PASTE,
    DISABLE_BRACKETED_PASTE,
    SYNC_BEGIN,
    SYNC_END,
    HIDE_CURSOR,
    SHOW_CURSOR,
    CLEAR_SCREEN,
}


obj Cell {
    has ch: str = " ",
        style: str = "";
}


obj VirtualTerminal(Terminal) {
    has writes: list[str] = [],
        input_queue: list[str] = [],
        resize_events: list[tuple[int, int]] = [],
        interrupt_count: int = 0,
        exception_exits: int = 0,
        cells: list[list[Cell]] = [],
        cursor_row: int = 0,
        cursor_col: int = 0,
        on_input: any = None,
        on_resize: any = None,
        on_interrupt: any = None;

    def init(
        columns: int = 80,
        rows: int = 24,
        on_input: any = None,
        on_resize: any = None,
        on_interrupt: any = None,
    ) {
        super.init();
        self.columns = columns;
        self.rows = rows;
        self.on_input = on_input;
        self.on_resize = on_resize;
        self.on_interrupt = on_interrupt;
        self.writes = [];
        self.input_queue = [];
        self.resize_events = [];
        self.interrupt_count = 0;
        self.exception_exits = 0;
        self.cursor_row = 0;
        self.cursor_col = 0;
        self.started = False;
        self.restored = True;
        self.alternate_screen = False;
        self.bracketed_paste = False;
        self.cursor_visible = True;
        self.sync_active = False;
        self._reset_cells();
    }

    def _reset_cells() {
        grid: list[list[Cell]] = [];
        for _r in range(self.rows) {
            row: list[Cell] = [];
            for _c in range(self.columns) {
                row.append(Cell());
            }
            grid.append(row);
        }
        self.cells = grid;
        self.cursor_row = 0;
        self.cursor_col = 0;
    }

    def write(data: str) -> None {
        if not data {
            return;
        }
        self.writes.append(data);
        self._apply_output(data);
    }

    """Override the base one-liner so calls resolve this body: the inherited
    Terminal.move_cursor dispatches self.write, which the seal-time checker
    refuses across the native/Python shadow boundary (E5089) and demotes the
    whole module to the server codespace."""
    def move_cursor(row: int, col: int) -> None {
        self.write(f"\x1b[{row};{col}H");
    }

    def start() -> None {
        if self.started {
            return;
        }
        self.enable_bracketed_paste();
        self.enter_alternate_screen();
        self.hide_cursor();
        self.started = True;
        self.restored = False;
    }

    def stop() -> None {
        if self.restored and not self.started {
            return;
        }
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
        self.started = False;
        self.restored = True;
    }

    """Inject raw bytes as if they arrived from stdin."""
    def inject(data: str) {
        self.input_queue.append(data);
        if self.on_input is not None {
            self.on_input(data);
        }
    }

    """Inject a resize. Updates size and notifies the host callback."""
    def inject_resize(columns: int, rows: int) {
        self.columns = columns;
        self.rows = rows;
        self.resize_events.append((columns, rows));
        self._reset_cells();
        if self.on_resize is not None {
            self.on_resize(columns, rows);
        }
    }

    """Simulate SIGINT: restore then invoke interrupt callback."""
    def inject_sigint() {
        self.interrupt_count += 1;
        self.restore();
        if self.on_interrupt is not None {
            self.on_interrupt();
        }
    }

    """Simulate an exception exit path: restore must still run."""
    def run_with_exception_guard(body: any) {
        self.start();
        try {
            body(self);
        } except Exception {
            self.exception_exits += 1;
            self.restore();
            raise;
        }
        self.restore();
    }

    """Drain queued stdin chunks (non-destructive copy)."""
    def pending_input() -> list[str] {
        return list(self.input_queue);
    }

    """Non-blocking poll compatible with ProcessTerminal.poll_input."""
    def poll_input(timeout_s: float = 0.0) -> str {
        _ = timeout_s;
        if not self.input_queue {
            return "";
        }
        data = self.input_queue.pop(0);
        return data;
    }

    def take_input() -> list[str] {
        queued = self.input_queue;
        self.input_queue = [];
        return queued;
    }

    """Return all bytes written since start/reset."""
    def written_text() -> str {
        return "".join(self.writes);
    }

    def clear_writes() {
        self.writes = [];
    }

    """Snapshot the cell grid as a list of row strings (no styles)."""
    def capture_cells() -> list[str] {
        rows: list[str] = [];
        for row in self.cells {
            chars = "";
            for cell in row {
                chars += cell.ch;
            }
            rows.append(chars.rstrip());
        }
        return rows;
    }

    def _put_char(ch: str) {
        if self.cursor_row < 0 or self.cursor_row >= self.rows {
            return;
        }
        if self.cursor_col < 0 or self.cursor_col >= self.columns {
            return;
        }
        self.cells[self.cursor_row][self.cursor_col] = Cell(ch=ch);
        self.cursor_col += 1;
        if self.cursor_col >= self.columns {
            self.cursor_col = 0;
            self.cursor_row += 1;
        }
    }

    def _apply_output(data: str) {
        i = 0;
        while i < len(data) {
            ch = data[i];
            if ch == "\x1b" {
                # Skip known full sequences; leave cursor ops handled below.
                if data.startswith(CLEAR_SCREEN, i) {
                    self._reset_cells();
                    i += len(CLEAR_SCREEN);
                    continue;
                }
                if data.startswith(ENTER_ALT_SCREEN, i) {
                    self.alternate_screen = True;
                    i += len(ENTER_ALT_SCREEN);
                    continue;
                }
                if data.startswith(LEAVE_ALT_SCREEN, i) {
                    self.alternate_screen = False;
                    i += len(LEAVE_ALT_SCREEN);
                    continue;
                }
                if data.startswith(ENABLE_BRACKETED_PASTE, i) {
                    self.bracketed_paste = True;
                    i += len(ENABLE_BRACKETED_PASTE);
                    continue;
                }
                if data.startswith(DISABLE_BRACKETED_PASTE, i) {
                    self.bracketed_paste = False;
                    i += len(DISABLE_BRACKETED_PASTE);
                    continue;
                }
                if data.startswith(SYNC_BEGIN, i) {
                    self.sync_active = True;
                    i += len(SYNC_BEGIN);
                    continue;
                }
                if data.startswith(SYNC_END, i) {
                    self.sync_active = False;
                    i += len(SYNC_END);
                    continue;
                }
                if data.startswith(HIDE_CURSOR, i) {
                    self.cursor_visible = False;
                    i += len(HIDE_CURSOR);
                    continue;
                }
                if data.startswith(SHOW_CURSOR, i) {
                    self.cursor_visible = True;
                    i += len(SHOW_CURSOR);
                    continue;
                }
                # CSI cursor position: ESC [ row ; col H
                if i + 1 < len(data) and data[i + 1] == "[" {
                    j = i + 2;
                    while j < len(data) {
                        code = ord(data[j]);
                        if code >= 64 and code <= 126 {
                            seq = data[i:j + 1];
                            if data[j] == "H" or data[j] == "f" {
                                body = seq[2:-1];
                                parts = body.split(";") if body else [];
                                row = int(parts[0]) if len(parts) > 0 and parts[0] else 1;
                                col = int(parts[1]) if len(parts) > 1 and parts[1] else 1;
                                self.cursor_row = max(0, row - 1);
                                self.cursor_col = max(0, col - 1);
                            }
                            i = j + 1;
                            break;
                        }
                        j += 1;
                    }
                    if j >= len(data) {
                        i += 1;
                    }
                    continue;
                }
                i += 1;
                continue;
            }
            if ch == "\n" {
                self.cursor_row += 1;
                self.cursor_col = 0;
                i += 1;
                continue;
            }
            if ch == "\r" {
                self.cursor_col = 0;
                i += 1;
                continue;
            }
            if ch == "\b" {
                if self.cursor_col > 0 {
                    self.cursor_col -= 1;
                }
                i += 1;
                continue;
            }
            if ord(ch) >= 32 {
                self._put_char(ch);
            }
            i += 1;
        }
    }
}
