"""Retained styled cell buffer and ANSI cell-diff (OSPUI.md §15).

Paint authoring may still feed plain strings via the host; those convert to
default-attr cells here. Style lives in the retained buffer and damage path —
not on OSP nodes and not as a frozen markup DSL.
"""

import from .layout_types { Rect }

import from .width {
    segment_graphemes,
    grapheme_width,
}


"""SGR / display attributes for one terminal cell."""
obj StyleAttrs {
    has fg: int | None = None,
        bg: int | None = None,
        bold: bool = False,
        dim: bool = False,
        italic: bool = False,
        underline: bool = False,
        reverse: bool = False;
}


"""One display cell: a single column char plus style."""
obj StyledCell {
    has ch: str = " ",
        attrs: StyleAttrs = StyleAttrs(),
        # True on the trailing column of a wide grapheme (not painted).
        wide_cont: bool = False;
}


obj CellBuffer {
    has columns: int = 80,
        rows: int = 24,
        cells: list[list[StyledCell]] = [];
}


obj CellDiff {
    has text: str = "",
        cells_written: int = 0;
}


def blank_cell() -> StyledCell {
    return StyledCell(ch=" ", attrs=StyleAttrs());
}


def attrs_eq(a: StyleAttrs, b: StyleAttrs) -> bool {
    return (
        a.fg == b.fg
        and a.bg == b.bg
        and a.bold == b.bold
        and a.dim == b.dim
        and a.italic == b.italic
        and a.underline == b.underline
        and a.reverse == b.reverse
    );
}


def cell_eq(a: StyledCell, b: StyledCell) -> bool {
    if a.wide_cont != b.wide_cont {
        return False;
    }
    if a.ch != b.ch {
        return False;
    }
    return attrs_eq(a.attrs, b.attrs);
}


def copy_attrs(a: StyleAttrs) -> StyleAttrs {
    return StyleAttrs(
        fg=a.fg,
        bg=a.bg,
        bold=a.bold,
        dim=a.dim,
        italic=a.italic,
        underline=a.underline,
        reverse=a.reverse,
    );
}


def copy_cell(c: StyledCell) -> StyledCell {
    return StyledCell(
        ch=c.ch,
        attrs=copy_attrs(c.attrs),
        wide_cont=c.wide_cont,
    );
}


def sgr_reset() -> str {
    return "\x1b[0m";
}


"""Emit CSI SGR for attrs (includes leading reset)."""
def sgr_for(attrs: StyleAttrs) -> str {
    parts: list[str] = ["0"];
    if attrs.bold {
        parts.append("1");
    }
    if attrs.dim {
        parts.append("2");
    }
    if attrs.italic {
        parts.append("3");
    }
    if attrs.underline {
        parts.append("4");
    }
    if attrs.reverse {
        parts.append("7");
    }
    if attrs.fg is not None {
        fg = attrs.fg as int;
        if fg >= 0 and fg <= 7 {
            parts.append(str(30 + fg));
        } elif fg >= 8 and fg <= 15 {
            parts.append(str(90 + (fg - 8)));
        } elif fg >= 0 and fg <= 255 {
            parts.append("38;5;" + str(fg));
        }
    }
    if attrs.bg is not None {
        bg = attrs.bg as int;
        if bg >= 0 and bg <= 7 {
            parts.append(str(40 + bg));
        } elif bg >= 8 and bg <= 15 {
            parts.append(str(100 + (bg - 8)));
        } elif bg >= 0 and bg <= 255 {
            parts.append("48;5;" + str(bg));
        }
    }
    return "\x1b[" + ";".join(parts) + "m";
}


def create_buffer(columns: int, rows: int) -> CellBuffer {
    cols = max(1, columns);
    rows_n = max(1, rows);
    grid: list[list[StyledCell]] = [];
    for _r in range(rows_n) {
        row: list[StyledCell] = [];
        for _c in range(cols) {
            row.append(blank_cell());
        }
        grid.append(row);
    }
    return CellBuffer(columns=cols, rows=rows_n, cells=grid);
}


def buffer_get(buf: CellBuffer, row: int, col: int) -> StyledCell {
    if row < 0 or row >= buf.rows or col < 0 or col >= buf.columns {
        return blank_cell();
    }
    return buf.cells[row][col];
}


def buffer_clear_rect(
    buf: CellBuffer,
    x: int,
    y: int,
    width: int,
    height: int,
    attrs: StyleAttrs | None = None,
) {
    style = attrs if attrs is not None else StyleAttrs();
    y0 = max(0, y);
    y1 = min(buf.rows, y + height);
    x0 = max(0, x);
    x1 = min(buf.columns, x + width);
    for r in range(y0, y1) {
        for c in range(x0, x1) {
            buf.cells[r][c] = StyledCell(ch=" ", attrs=copy_attrs(style));
        }
    }
}


"""Blit text by display columns: wide graphemes occupy N cells (wide_cont trail)."""
def buffer_blit_text(
    buf: CellBuffer,
    row: int,
    col: int,
    text: str,
    attrs: StyleAttrs | None = None,
    max_width: int = -1,
) {
    style = attrs if attrs is not None else StyleAttrs();
    if row < 0 or row >= buf.rows or col < 0 or col >= buf.columns {
        return;
    }
    limit = max_width if max_width >= 0 else (buf.columns - col);
    if limit <= 0 {
        return;
    }
    end = col + limit;
    if end > buf.columns {
        end = buf.columns;
    }
    x = col;
    for g in segment_graphemes(text) {
        seg = g.text;
        if not seg {
            continue;
        }
        if "\n" in seg or "\r" in seg {
            break;
        }
        w = grapheme_width(seg);
        if w <= 0 {
            continue;
        }
        if x + w > end {
            break;
        }
        buf.cells[row][x] = StyledCell(
            ch=seg, attrs=copy_attrs(style), wide_cont=False
        );
        for i in range(1, w) {
            buf.cells[row][x + i] = StyledCell(
                ch=" ", attrs=copy_attrs(style), wide_cont=True
            );
        }
        x += w;
    }
}


"""Blit a run of {text, attrs} spans with wide-grapheme column advance."""
obj TextSpan {
    has text: str = "";
    has attrs: StyleAttrs | None = None;
}


def buffer_blit_spans(
    buf: CellBuffer,
    row: int,
    col: int,
    spans: list[TextSpan],
    max_width: int = -1,
) {
    if row < 0 or row >= buf.rows or col < 0 or col >= buf.columns {
        return;
    }
    limit = max_width if max_width >= 0 else (buf.columns - col);
    if limit <= 0 {
        return;
    }
    x = col;
    remaining = limit;
    for span in spans {
        if remaining <= 0 or x >= buf.columns {
            break;
        }
        if not span.text {
            continue;
        }
        buffer_blit_text(buf, row, x, span.text, span.attrs, remaining);
        text = span.text;
        adv = grapheme_width(text);
        if adv > remaining {
            adv = remaining;
        }
        if adv < 1 {
            continue;
        }
        x += adv;
        remaining -= adv;
    }
}


def buffer_to_plain_rows(buf: CellBuffer) -> list[str] {
    out: list[str] = [];
    for r in range(buf.rows) {
        chars: list[str] = [];
        for c in range(buf.columns) {
            cell = buf.cells[r][c];
            if cell.wide_cont {
                continue;
            }
            chars.append(cell.ch if cell.ch else " ");
        }
        out.append("".join(chars));
    }
    return out;
}


"""Build a buffer from plain row strings (interim host paint API)."""
def buffer_from_plain_rows(
    rows: list[str], columns: int, rows_n: int
) -> CellBuffer {
    buf = create_buffer(columns, rows_n);
    for r in range(rows_n) {
        line = rows[r] if r < len(rows) else "";
        buffer_blit_text(buf, r, 0, line, None, columns);
    }
    return buf;
}


def _rect_bounds(
    rect: Rect, columns: int, rows_n: int
) -> tuple[int, int, int, int] {
    x = rect.x;
    y = rect.y;
    w = rect.width;
    h = rect.height;
    x0 = max(0, x);
    y0 = max(0, y);
    x1 = min(columns, x + w);
    y1 = min(rows_n, y + h);
    return (x0, y0, x1, y1);
}


"""Diff previous vs desired within patch rects; emit moves + SGR + chars."""
def diff_buffers_ansi(
    previous: CellBuffer | None,
    desired: CellBuffer,
    patch_rects: list[Rect],
    force: bool = False,
) -> CellDiff {
    parts: list[str] = [];
    written = 0;
    columns = desired.columns;
    rows_n = desired.rows;
    rects: list[any] = patch_rects;
    if not rects {
        rects = [Rect(x=0, y=0, width=columns, height=rows_n)];
    }
    cur_attrs = StyleAttrs();
    sgr_on = False;
    need_attrs = True;

    for rect in rects {
        (x0, y0, x1, y1) = _rect_bounds(rect, columns, rows_n);
        for y in range(y0, y1) {
            run_start = -1;
            run_chars: list[str] = [];
            run_attrs = StyleAttrs();
            for x in range(x0, x1) {
                want = blank_cell();
                if y < len(desired.cells) and x < len(desired.cells[y]) {
                    want = desired.cells[y][x];
                }
                if want.wide_cont {
                    if run_start >= 0 {
                        if need_attrs or not attrs_eq(cur_attrs, run_attrs) {
                            parts.append(sgr_for(run_attrs));
                            cur_attrs = copy_attrs(run_attrs);
                            sgr_on = True;
                            need_attrs = False;
                        }
                        parts.append(
                            f"\x1b[{y + 1};{run_start + 1}H"
                            + "".join(run_chars)
                        );
                        written += len(run_chars);
                        run_start = -1;
                        run_chars = [];
                    }
                    continue;
                }
                had = blank_cell();
                if (
                    previous is not None
                    and y < previous.rows
                    and x < previous.columns
                ) {
                    had = previous.cells[y][x];
                }
                if cell_eq(want, had) and not force {
                    if run_start >= 0 {
                        if need_attrs or not attrs_eq(cur_attrs, run_attrs) {
                            parts.append(sgr_for(run_attrs));
                            cur_attrs = copy_attrs(run_attrs);
                            sgr_on = True;
                            need_attrs = False;
                        }
                        parts.append(
                            f"\x1b[{y + 1};{run_start + 1}H"
                            + "".join(run_chars)
                        );
                        written += len(run_chars);
                        run_start = -1;
                        run_chars = [];
                    }
                    continue;
                }
                ch = want.ch if want.ch else " ";
                if run_start < 0 {
                    run_start = x;
                    run_attrs = copy_attrs(want.attrs);
                    run_chars = [ch];
                } elif attrs_eq(run_attrs, want.attrs) {
                    run_chars.append(ch);
                } else {
                    if need_attrs or not attrs_eq(cur_attrs, run_attrs) {
                        parts.append(sgr_for(run_attrs));
                        cur_attrs = copy_attrs(run_attrs);
                        sgr_on = True;
                        need_attrs = False;
                    }
                    parts.append(
                        f"\x1b[{y + 1};{run_start + 1}H" + "".join(run_chars)
                    );
                    written += len(run_chars);
                    run_start = x;
                    run_attrs = copy_attrs(want.attrs);
                    run_chars = [ch];
                }
            }
            if run_start >= 0 {
                if need_attrs or not attrs_eq(cur_attrs, run_attrs) {
                    parts.append(sgr_for(run_attrs));
                    cur_attrs = copy_attrs(run_attrs);
                    sgr_on = True;
                    need_attrs = False;
                }
                parts.append(
                    f"\x1b[{y + 1};{run_start + 1}H" + "".join(run_chars)
                );
                written += len(run_chars);
            }
        }
    }
    if sgr_on {
        parts.append(sgr_reset());
    }
    return CellDiff(text="".join(parts), cells_written=written);
}
