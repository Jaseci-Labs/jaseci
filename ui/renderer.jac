"""Retained terminal renderer: damage, cell diff, cursor, ANSI paint.

Queries OSP topology and layout side tables. Emits one synchronized ANSI
update per frame. Damage is the union of old and new rectangles
(OSPUI.md §15.4–15.6). Full-screen clears must not hide damage bugs —
FrameResult.used_full_clear and patch_rects exist so tests can assert
patch scope.
"""

import from .model {
    UiNode,
    UiContainer,
    Screen,
    Overlay,
    ordered_children,
    node_id,
}

import from .layout_types {
    FrameEntry,
    LayoutResult,
    LayoutSpec,
    LayoutState,
    Rect,
    Viewport,
    clear_node,
    create_layout_state,
    frame_entry_of,
    rect_union,
    set_content,
    set_spec,
}

import from .layout {
    compute_layout,
}

import from .terminal {
    Terminal,
    synchronized_write,
}

import from .cells {
    CellBuffer,
    StyleAttrs,
    StyledCell,
    create_buffer,
    buffer_clear_rect,
    buffer_blit_text,
    buffer_to_plain_rows,
    diff_buffers_ansi,
}

import from .renderer_types {
    DamageRect,
    FrameResult,
    Renderer,
}

import from .renderer_paint {
    _paint_frame_buffer,
}

import from .renderer_damage {
    compute_damage,
    _diff_ansi,
    _merge_damage,
    _resolve_cursor,
    _run_layout,
    _snapshot_rects,
}


def create_renderer(columns: int = 80, rows: int = 24) -> Renderer {
    return Renderer(layout=create_layout_state(columns, rows));
}


# The permanent seam has no contracts: callers install a LayoutSpec via
# set_spec (see screen.jac configure_main_shell_layout for the idiom).
def set_node_contract(renderer: Renderer, n: UiNode, spec: LayoutSpec) {
    set_spec(renderer.layout, n, spec);
}


# set_content requires monotonic revisions; keep the legacy three-arg
# surface by minting a per-node revision counter here.
def set_node_content(renderer: Renderer, n: UiNode, lines: list[str]) {
    nid = node_id(n);
    rev = renderer.content_revisions.get(nid, 0) + 1;
    renderer.content_revisions[nid] = rev;
    set_content(renderer.layout, n, lines, rev);
}


# No dirty tracking exists anymore — frames recompute wholesale; the
# pending sets only steer same-bounds semantic damage attribution.
def mark_semantic_dirty(renderer: Renderer, n: UiNode) {
    renderer.pending_semantic.add(node_id(n));
}


def mark_layout_dirty(renderer: Renderer, n: UiNode) {
    renderer.pending_layout.add(node_id(n));
}


def request_cursor(
    renderer: Renderer,
    n: UiNode,
    row_offset: int = 0,
    col_offset: int = 0,
) {
    renderer.cursor_node_id = node_id(n);
    renderer.cursor_row_offset = row_offset;
    renderer.cursor_col_offset = col_offset;
}


def clear_cursor(renderer: Renderer) {
    renderer.cursor_node_id = "";
    renderer.cursor_row_offset = 0;
    renderer.cursor_col_offset = 0;
}


"""Detach a node: damage its previous rect and drop registry state."""
def detach_node(renderer: Renderer, n: UiNode) {
    ent = frame_entry_of(renderer.layout, n);
    if ent is not None and not ent.rect.is_empty() {
        renderer.damage.append(
            DamageRect(rect=ent.rect.copy(), reason="detach")
        );
    }
    if renderer.cursor_node_id == node_id(n) {
        clear_cursor(renderer);
    }
    renderer.content_revisions.pop(node_id(n), None);
    clear_node(renderer.layout, n);
}

"""Recompute the layout frame without painting (drivers/tests)."""
def relayout(renderer: Renderer, layout_root: UiNode) -> LayoutResult {
    return _run_layout(renderer, layout_root);
}


"""Materialize the desired full-frame cell rows without writing a terminal."""
def desired_cells(renderer: Renderer, layout_root: UiNode) -> list[str] {
    _run_layout(renderer, layout_root);
    buf = _paint_frame_buffer(renderer, layout_root);
    return buffer_to_plain_rows(buf);
}


"""Layout, damage, paint, and cursor for one frame."""
def render_frame(
    renderer: Renderer,
    layout_root: UiNode,
    term: Terminal,
) -> FrameResult {
    state = renderer.layout;
    cols = term.columns if term.columns > 0 else state.viewport.columns;
    rows_n = term.rows if term.rows > 0 else state.viewport.rows;
    state.viewport.columns = cols;
    state.viewport.rows = rows_n;

    # A viewport change between emitted frames invalidates every cell:
    # exposed rows/columns were never painted by us, surviving cells may
    # have been reflowed/truncated by the terminal, so the retained
    # previous buffer no longer describes the screen. Drop it (full
    # repaint of non-blank cells) plus full-frame *damage* — never a
    # clear escape, so patch scope stays assertable.
    resized = (
        renderer.previous is not None
        and (
            cols != renderer.last_frame_columns
            or rows_n != renderer.last_frame_rows
        )
    );
    if resized {
        renderer.damage.append(
            DamageRect(
                rect=Rect(x=0, y=0, width=cols, height=rows_n),
                reason="resize",
            )
        );
        renderer.previous = None;
    }

    _run_layout(renderer, layout_root);
    damage = compute_damage(renderer, layout_root);
    desired = _paint_frame_buffer(renderer, layout_root);
    patch_rects = _merge_damage(damage);
    # previous=None (first frame, resize, node detach) means the terminal's
    # real cells are unknown: blank-desired cells must be overwritten with
    # spaces or stale glyphs survive (e.g. old box-drawing after resize).
    diff = _diff_ansi(
        renderer.previous, desired, patch_rects, cols, rows_n,
        force=(renderer.previous is None),
    );
    cursor = _resolve_cursor(renderer);
    cursor_visible = cursor.row >= 0 and cursor.col >= 0;
    ansi = diff.text;
    if cursor_visible {
        if not term.cursor_visible {
            term.show_cursor();
        }
        ansi = ansi + f"\x1b[{cursor.row + 1};{cursor.col + 1}H";
    } else {
        if term.cursor_visible {
            term.hide_cursor();
        }
    }
    synchronized_write(term, ansi);
    used_full_clear = "\x1b[2J" in ansi or "\x1b[3J" in ansi;
    renderer.last_frame_columns = cols;
    renderer.last_frame_rows = rows_n;
    renderer.previous = desired;
    renderer.damage = [];
    renderer.pending_semantic = set();
    renderer.pending_layout = set();
    _snapshot_rects(renderer);
    renderer.last_cursor_row = cursor.row;
    renderer.last_cursor_col = cursor.col;
    renderer.last_cursor_visible = cursor_visible;
    return FrameResult(
        damage=damage,
        cells_written=diff.cells_written,
        used_full_clear=used_full_clear,
        patch_rects=patch_rects,
        cursor_row=cursor.row,
        cursor_col=cursor.col,
        cursor_visible=cursor_visible,
        sync_wrapped=True,
    );
}


"""True if any emitted write contains a full-screen clear sequence."""
def frame_used_full_clear(writes: list[str]) -> bool {
    joined = "".join(writes);
    return "\x1b[2J" in joined or "\x1b[3J" in joined;
}


"""Sum of widths*heights for damage rects (upper bound on cells touched)."""
def damage_cell_count(damage: list[DamageRect]) -> int {
    total = 0;
    for d in damage {
        if not d.rect.is_empty() {
            total += d.rect.width * d.rect.height;
        }
    }
    return total;
}
