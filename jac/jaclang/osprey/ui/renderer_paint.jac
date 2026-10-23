"""Cell-buffer painting for the retained renderer."""

import from .model {
    UiNode,
    UiContainer,
    Screen,
    Overlay,
    Layer,
    ordered_children,
    node_id,
}

import from .layout_types {
    FrameEntry,
    LayoutState,
}

import from .cells {
    CellBuffer,
    StyleAttrs,
    create_buffer,
    buffer_clear_rect,
    buffer_blit_text,
}

import from .renderer_types {
    Renderer,
    _OverlayHit,
}


def _blank_buffer(columns: int, rows: int) -> CellBuffer {
    return create_buffer(columns, rows);
}


def _paint_text_into(
    buf: CellBuffer,
    text: str,
    row: int,
    col: int,
    max_width: int,
    attrs: StyleAttrs | None = None,
) {
    if max_width <= 0 {
        return;
    }
    buffer_blit_text(buf, row, col, text, attrs, max_width);
}


def _paint_entry_lines(
    buf: CellBuffer,
    layout_entry: FrameEntry,
    scrolls: bool,
) {
    rect = layout_entry.rect;
    clip = layout_entry.clip if not layout_entry.clip.is_empty() else rect;
    if clip.is_empty() or rect.is_empty() {
        return;
    }
    lines = layout_entry.wrapped_lines;
    scroll = 0;
    if scrolls {
        scroll = layout_entry.scroll_offset;
    }
    for vis_i in range(clip.height) {
        src_i = vis_i + scroll;
        term_row = clip.y + vis_i;
        if term_row < 0 or term_row >= buf.rows {
            continue;
        }
        buffer_clear_rect(buf, clip.x, term_row, clip.width, 1);
        if src_i < 0 or src_i >= len(lines) {
            continue;
        }
        _paint_text_into(
            buf,
            lines[src_i],
            term_row,
            clip.x,
            clip.width,
            None,
        );
    }
}


# Layer-reached overlays of one Screen, ordered by (z_index, jid) —
# same ordering the compiler's scope walk uses (plan §6.3).
def _overlay_z_key(hit: _OverlayHit) -> int {
    return hit.z;
}


def _overlay_jid_key(hit: _OverlayHit) -> str {
    return hit.id_str;
}


def _layered_overlays(layout_root: UiNode) -> list[UiNode] {
    found: list[_OverlayHit] = [];
    if isinstance(layout_root, Screen) {
        for ov in [layout_root ->:Layer:->] {
            z = 0;
            for e in [edge layout_root ->:Layer:-> ov] {
                z = e.z_index;
            }
            found.append(_OverlayHit(nd=ov, z=z, id_str=node_id(ov)));
        }
    }
    if not found {
        return [];
    }
    found.sort(key=_overlay_jid_key);
    found.sort(key=_overlay_z_key);
    return [hit.nd for hit in found];
}


def _paint_node(state: LayoutState, n: UiNode, buf: CellBuffer) {
    frame = state.last_frame;
    if frame is None {
        return;
    }
    nid = node_id(n);
    ent = frame.entries.get(nid);
    if ent is None {
        return;
    }
    if ent.wrapped_lines or nid in state.content {
        spec = state.specs.get(nid);
        scrolls = spec is not None and spec.scroll_vertical;
        _paint_entry_lines(buf, ent, scrolls);
    }
}


def _paint_tree(state: LayoutState, n: UiNode, buf: CellBuffer) {
    _paint_node(state, n, buf);
    if isinstance(n, UiContainer) {
        for child in ordered_children(n) {
            # Overlays hang off Layer edges; skip them in the flow walk so
            # a Child-mounted overlay is painted exactly once.
            if isinstance(child, Overlay) {
                continue;
            }
            _paint_tree(state, child, buf);
        }
    }
}


def _paint_frame_buffer(renderer: Renderer, layout_root: UiNode) -> CellBuffer {
    state = renderer.layout;
    buf = _blank_buffer(state.viewport.columns, state.viewport.rows);
    _paint_tree(state, layout_root, buf);
    for overlay in _layered_overlays(layout_root) {
        _paint_node(state, overlay, buf);
    }
    return buf;
}
