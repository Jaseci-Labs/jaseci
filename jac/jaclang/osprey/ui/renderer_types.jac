"""Retained renderer state and frame-result value objects."""

import from .model {
    UiNode,
}

import from .layout_types {
    LayoutState,
    Rect,
}

import from .cells {
    CellBuffer,
}


obj DamageRect {
    has rect: Rect = Rect(),
        reason: str = "";
}


obj FrameResult {
    has damage: list[DamageRect] = [],
        cells_written: int = 0,
        used_full_clear: bool = False,
        patch_rects: list[Rect] = [],
        cursor_row: int = -1,
        cursor_col: int = -1,
        cursor_visible: bool = False,
        sync_wrapped: bool = False;
}


obj AnsiDiff {
    has text: str = "",
        cells_written: int = 0;
}


obj _OverlayHit {
    has nd: UiNode,
        z: int = 0,
        id_str: str = "";
}


obj CursorPos {
    has row: int = -1,
        col: int = -1;
}


obj Renderer {
    has layout: LayoutState,
        # Retained previous frame as styled cells (OSPUI §15.1).
        previous: CellBuffer | None = None,
        # Previous-frame rects per node id (replaces the legacy engine's
        # entry.prev_rect / snapshot_rects damage baseline).
        prev_rects: dict[str, Rect] = {},
        damage: list[DamageRect] = [],
        cursor_node_id: str = "",
        cursor_row_offset: int = 0,
        cursor_col_offset: int = 0,
        last_cursor_row: int = -1,
        last_cursor_col: int = -1,
        last_cursor_visible: bool = False,
        graph_revision: int = 0,
        # Monotonic per-node content revisions for set_content.
        content_revisions: dict[str, int] = {},
        # Node ids marked dirty before the next frame clears the flags.
        pending_semantic: set[str] = set(),
        pending_layout: set[str] = set(),
        # Viewport of the last emitted frame; a change between frames is
        # resize damage for the full new viewport (host marks additive).
        last_frame_columns: int = 0,
        last_frame_rows: int = 0;
}
