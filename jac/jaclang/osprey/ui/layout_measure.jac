"""Width-dependent text measurement with a bounded cache (plan §7.1).

Axis separation puts this NON-linear operation outside the solver:
natural (unwrapped) width feeds the horizontal phase; wrapped line
counts at QUANTIZED integer widths feed the vertical phase. Text is
wrapped exactly once per (node, content revision, integer width, style
revision) — the cache holds one entry per node because revisions are
monotonic and older wraps can never be reused again (plan §4 invariant
6); memory is therefore O(nodes), never O(history).

Known cost by design: viewport resize ping-pong (A->B->A widths)
invalidates the single entry per width change and recomputes wraps every
frame. That is correct behavior under this bound, not a bug to fix with
a multi-entry cache; revisit only if resize benchmarks say otherwise.

Native lowering notes: signatures use primitive types only (no
LayoutState / MeasureEntry objects as parameters) so the module lowers
cleanly to native. The cache is a parallel tuple of primitive dicts
keyed by node id. Wrapping itself is delegated to the server-pinned
`wrap_text_joined` helper, whose `-> str` return type crosses the
native->Python ctypes callback table; we split on '\n' to recover the
wrapped line list. `wrap_text` is intentionally NOT imported here —
calling it directly would hit E5093 (list[str] return crosses boundary).
"""

import from .width {
    display_width,
    wrap_text_joined,
}


"""Natural (unwrapped) display width of registered content lines.

Empty or missing content measures 0 — callers decide their own fallback
for INTRINSIC nodes without content."""
def natural_width(lines: list[str]) -> int {
    best = 0;
    for line in lines {
        w = display_width(line);
        if w > best {
            best = w;
        }
    }
    return best;
}


# Native-friendly cache representation: parallel primitive dicts keyed
# by node id. Replaces the previous MeasureEntry obj, which failed to
# lower natively (E5092) because the signature type 'MeasureEntry'
# could not be lowered.
glob _CACHE_WIDTH: dict[str, int] = {};
glob _CACHE_CONTENT_REV: dict[str, int] = {};
glob _CACHE_STYLE_REV: dict[str, int] = {};
glob _CACHE_LINES: dict[str, list[str]] = {};


def _cache_valid(
    cached_width: int,
    cached_content_revision: int,
    cached_style_revision: int,
    width: int,
    content_revision: int,
    style_revision: int,
) -> bool {
    return (
        cached_width == width
        and cached_content_revision == content_revision
        and cached_style_revision == style_revision
    );
}


"""Wrap content to exactly `width` columns, cached per node.

Returns the wrapped lines for the CURRENT content at this width,
populating or reusing the per-node cache. Width is clamped to >= 1 so
degenerate viewports still wrap deterministically.

Native callers must supply the per-node `content_lines`, `content_revision`,
and `style_revision` from LayoutState.content (server->native reads are
free; this module's signature deliberately avoids LayoutState because the
obj's measurement_cache field type can't be lowered natively)."""
def wrapped_lines_at(
    content_lines: list[str],
    content_revision: int,
    style_revision: int,
    id_str: str,
    width: int,
) -> list[str] {
    if width < 1 {
        width = 1;
    }
    cached_width = _CACHE_WIDTH.get(id_str);
    cached_cr = _CACHE_CONTENT_REV.get(id_str, 0);
    cached_sr = _CACHE_STYLE_REV.get(id_str, 0);
    if cached_width is not None {
        cached_lines = _CACHE_LINES.get(id_str);
        if cached_lines is not None
        and _cache_valid(
            cached_width, cached_cr, cached_sr,
            width, content_revision, style_revision
        ) {
            return cached_lines;
        }
    }

    wrapped: list[str] = [];
    for line in content_lines {
        joined = wrap_text_joined(line, width);
        wrapped.extend(joined.split("\n"));
    }
    _CACHE_WIDTH[id_str] = width;
    _CACHE_CONTENT_REV[id_str] = content_revision;
    _CACHE_STYLE_REV[id_str] = style_revision;
    _CACHE_LINES[id_str] = wrapped;
    return wrapped;
}


"""Wrapped height in rows for one node at one integer width."""
def wrapped_height(
    content_lines: list[str],
    content_revision: int,
    style_revision: int,
    id_str: str,
    width: int,
) -> int {
    if width < 1 {
        width = 1;
    }
    return len(
        wrapped_lines_at(
            content_lines, content_revision, style_revision, id_str, width
        )
    );
}


"""Drop every cached entry whose node id is `id_str`.

Called from `layout_types.set_content` / `clear_node` so cache invalidation
on content replacement or node removal works for the parallel-dict cache
that this module owns (state.measurement_cache.pop is preserved for
backward compatibility but is now a no-op for this module)."""
def invalidate_measurement_cache(id_str: str) {
    _CACHE_WIDTH.pop(id_str, None);
    _CACHE_CONTENT_REV.pop(id_str, None);
    _CACHE_STYLE_REV.pop(id_str, None);
    _CACHE_LINES.pop(id_str, None);
}