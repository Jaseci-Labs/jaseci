"""Permanent public layout seam (LAYOUT-ENGINE-PLAN §3/§4).

Everything downstream (renderer, screen, gates, demos, tests) imports the
layout surface from here and only from here:

- value types + registry lifecycle re-exported from ui.layout_types;
- frame accessors (rect_of, frame_entry_of) over the last published frame;
- compute_layout — the axis-separated pipeline of §7.1.

compute_layout lives here while its phases (compile / measure / quantize)
stay in sibling modules; those siblings depend on ui.layout_types, never
back on this module, so the import graph stays acyclic.
"""

import from .layout_types {
    Align,
    Axis,
    AxisSize,
    ContentEntry,
    FrameEntry,
    LayoutDiagnostic,
    LayoutError,
    LayoutFrame,
    LayoutRelation,
    LayoutRelationKind,
    LayoutResult,
    LayoutSeverity,
    LayoutSpec,
    LayoutState,
    MeasureEntry,
    MutationResult,
    OverlayAnchor,
    Rect,
    RelationHandle,
    Size,
    SizeMode,
    Viewport,
    rect_union,
    fill_axis,
    fixed_axis,
    grow_axis,
    intrinsic_axis,
    create_layout_state,
    validate_spec,
    set_spec,
    add_relation,
    remove_relation,
    set_content,
    set_scroll_offset,
    clear_node,
    frame_entry_of,
    rect_of,
    _copy_rect,
}
import from .layout_compile {
    CompileResult,
    PartitionInfo,
    compile_layout,
}
import from .layout_measure {
    natural_width,
    wrapped_lines_at,
    invalidate_measurement_cache,
}
import from .layout_quantize {
    PartitionRequest,
    quantize_partition,
    snap_edge,
}
import from .model {
    UiNode,
    UiContainer,
    Screen,
    Overlay,
    node_id,
    ordered_children,
}
import from .width {
    wrap_text_joined,
}
import from .layout_scope {
    _ScopedNode,
    _Scope,
    _collect_scope,
}


# ----------------------------------------------------------------------
# Compute pipeline (plan §7.1).
#
# Scope collection is isolated in ui.layout_scope; this module retains
# the public pipeline and frame publication seam.
# ----------------------------------------------------------------------


def _fail(diagnostics: list[LayoutDiagnostic]) -> LayoutResult {
    return LayoutResult(ok=False, frame=None, diagnostics=diagnostics);
}


def _overflow_warning(node_ids: list[str]) -> LayoutDiagnostic {
    return LayoutDiagnostic(
        code=LayoutError.OVERFLOW,
        severity=LayoutSeverity.WARNING,
        message="partition exceeded span; quantized clip-aware",
        node_ids=node_ids,
    );
}


"""Non-overlay ordered child ids of one scoped parent.

scope.order is BFS: each parent's children appear contiguously in rank
order, so a single scan groups them correctly."""
def _child_ids(scope_order: list[_ScopedNode], parent_id: str) -> list[str] {
    out: list[str] = [];
    for scoped in scope_order {
        if scoped.parent_id == parent_id and not scoped.is_overlay {
            out.append(scoped.id_str);
        }
    }
    return out;
}


"""Place one axis of the tree top-down.

Partition members are positioned by largest-remainder sizes cumulative
from the parent's start cell (exact closure); every other child snaps
its solved edges — pinned children hold byte-identical solved floats to
their parent, so snapping preserves pinning exactly."""
def _place_axis(
    result: CompileResult,
    values: dict[int, float],
    order: list[_ScopedNode],
    parent_id: str,
    p_start: int,
    p_end: int,
    infos: dict[str, PartitionInfo],
    starts: dict[str, int],
    ends: dict[str, int],
    warnings: list[LayoutDiagnostic],
    horizontal: bool,
) -> None {
    kids = _child_ids(order, parent_id);
    if len(kids) == 0 {
        return;
    }

    placed = False;
    info = infos.get(parent_id);
    aligned = False;
    if info is not None and len(info.child_ids) == len(kids) {
        # Element-wise identity, not just length: quantized sizes must
        # never map onto the wrong children if grouping ever drifts.
        aligned = True;
        for i in range(len(kids)) {
            if info.child_ids[i] != kids[i] {
                aligned = False;
            }
        }
        if not aligned {
            warnings.append(LayoutDiagnostic(
                code=LayoutError.INTERNAL_INVARIANT,
                severity=LayoutSeverity.ERROR,
                message="partition child order misaligned with scope walk",
                node_ids=[parent_id],
            ));
        }
    }
    if info is not None and aligned {
        req = PartitionRequest(
            span=p_end - p_start,
            targets=info.targets,
            fixed=info.fixed,
            minimums=info.minimums,
            maximums=info.maximums,
        );
        qr = quantize_partition(req);
        if qr.ok {
            pos = p_start;
            for i in range(len(kids)) {
                kid = kids[i];
                starts[kid] = pos;
                ends[kid] = pos + qr.sizes[i];
                pos += qr.sizes[i];
            }
            placed = True;
        } else {
            # Hard overflow: no honest integer closure exists; snap the
            # solved edges clip-aware and warn (quantizer contract).
            warnings.append(_overflow_warning([parent_id]));
        }
    }

    if not placed {
        for kid in kids {
            e = result.nodes[kid];
            if horizontal {
                starts[kid] = snap_edge(values[e.left.id]);
                ends[kid] = snap_edge(values[e.right.id]);
            } else {
                starts[kid] = snap_edge(values[e.top.id]);
                ends[kid] = snap_edge(values[e.bottom.id]);
            }
        }
    }

    for kid in kids {
        _place_axis(
            result, values, order, kid,
            starts[kid], ends[kid], infos,
            starts, ends, warnings, horizontal,
        );
    }
}


"""Structural naturals, mirroring the frozen legacy measure semantics:
leaf size from wrapped content at the hint width; containers sum along
their flow axis and take the max across it; FIXED uses preferred;
FILL/GROW contribute their content natural (legacy grow measured value).
Computed bottom-up over reversed BFS order."""
def _structural_naturals(
    order: list[_ScopedNode],
    state: LayoutState,
    wrap_widths: dict[str, int],
) -> dict[str, Size] {
    out: dict[str, Size] = {};
    rev: list[_ScopedNode] = [];
    for i in range(len(order)) {
        rev.insert(0, order[i]);
    }
    for scoped in rev {
        id_str = scoped.id_str;
        spec = state.specs.get(id_str);
        lines: list[str] = [];
        ent = state.content.get(id_str);
        if ent is not None {
            lines = ent.lines;
        }
        w_cols = wrap_widths.get(id_str, 80);
        if w_cols < 1 {
            w_cols = 1;
        }
        leaf_h = 0;
        for line in lines {
            leaf_h += wrap_text_joined(line, w_cols).count("\n") + 1;
        }

        kids = _child_ids(order, id_str);
        if spec is None or len(kids) == 0 {
            out[id_str] = Size(
                width=natural_width(lines),
                height=leaf_h,
            );
            continue;
        }
        flow_horiz = False;
        if spec.flow_axis == Axis.HORIZONTAL {
            flow_horiz = True;
        }
        sum_flow = 0.0;
        max_cross = 0.0;
        for kid_id in kids {
            nat = out[kid_id];
            kid_w: float = float(nat.width);
            kid_h: float = float(nat.height);
            kspec = state.specs.get(kid_id);
            if kspec is not None {
                if kspec.width.mode == SizeMode.FIXED
                    and kspec.width.preferred is not None {
                    kid_w = kspec.width.preferred;
                }
                if kspec.height.mode == SizeMode.FIXED
                    and kspec.height.preferred is not None {
                    kid_h = kspec.height.preferred;
                }
            }
            if flow_horiz {
                sum_flow += kid_w;
                if kid_h > max_cross {
                    max_cross = kid_h;
                }
            } else {
                sum_flow += kid_h;
                if kid_w > max_cross {
                    max_cross = kid_w;
                }
            }
        }
        if flow_horiz {
            out[id_str] = Size(
                width=int(sum_flow),
                height=int(max_cross),
            );
        } else {
            out[id_str] = Size(
                width=int(max_cross),
                height=int(sum_flow),
            );
        }
    }
    return out;
}


"""Full pipeline: registry + topology -> published LayoutFrame."""
def compute_layout(
    state: LayoutState,
    layout_root: UiNode,
    viewport: Viewport,
) -> LayoutResult {
    scope = _collect_scope(layout_root);
    if scope.error is not None {
        return _fail([scope.error]);
    }
    order = scope.order;
    root_id = node_id(layout_root);

    # ---- Phase H ----------------------------------------------------
    # Legacy measures leaves at the available width (full viewport here);
    # containers get structural sum/max naturals.
    hint_all: dict[str, int] = {};
    for scoped in order {
        hint_all[scoped.id_str] = viewport.columns;
    }
    naturals_w = _structural_naturals(order, state, hint_all);

    ch = compile_layout(state, layout_root, viewport, naturals_w, "h");
    if not ch.ok or ch.solver is None {
        return _fail(ch.diagnostics);
    }
    hv = ch.solver.snapshot().values;

    L: dict[str, int] = {};
    R: dict[str, int] = {};
    L[root_id] = 0;
    R[root_id] = viewport.columns;
    hinfos: dict[str, PartitionInfo] = {};
    for info in ch.partitions {
        if info.horizontal {
            hinfos[info.parent_id] = info;
        }
    }
    warnings: list[LayoutDiagnostic] = [];
    _place_axis(
        ch, hv, order, root_id, 0, viewport.columns,
        hinfos, L, R, warnings, True,
    );
    # Overlays sit outside every flow partition: snap each axis's cells
    # in its own phase before that axis is consumed.
    for scoped in order {
        if not scoped.is_overlay {
            continue;
        }
        id_str = scoped.id_str;
        eh = ch.nodes[id_str];
        L[id_str] = snap_edge(hv[eh.left.id]);
        R[id_str] = snap_edge(hv[eh.right.id]);
    }

    # ---- Measure once at integer widths ------------------------------
    widths: dict[str, int] = {};
    wrapped_by_node: dict[str, list[str]] = {};
    for scoped in order {
        id_str = scoped.id_str;
        w = R[id_str] - L[id_str];
        if w < 0 {
            return _fail([LayoutDiagnostic(
                code=LayoutError.INTERNAL_INVARIANT,
                severity=LayoutSeverity.ERROR,
                message="negative derived width",
                node_ids=[id_str],
            )]);
        }
        widths[id_str] = w;
        ent_w = state.content.get(id_str);
        if ent_w is not None {
            wrapped_by_node[id_str] = list(
                wrapped_lines_at(
                    ent_w.lines,
                    ent_w.content_revision,
                    ent_w.style_revision,
                    id_str,
                    w
                )
            );
        } else {
            wrapped_by_node[id_str] = [];
        }
    }


    # ---- Phase V -----------------------------------------------------
    # Leaves rewrap at their quantized integer widths; containers use
    # structural sum/max over those measured children.
    naturals_h = _structural_naturals(order, state, widths);

    cv = compile_layout(state, layout_root, viewport, naturals_h, "v");
    if not cv.ok or cv.solver is None {
        return _fail(cv.diagnostics);
    }
    vv = cv.solver.snapshot().values;

    T: dict[str, int] = {};
    B: dict[str, int] = {};
    T[root_id] = 0;
    B[root_id] = viewport.rows;
    vinfos: dict[str, PartitionInfo] = {};
    for info in cv.partitions {
        if not info.horizontal {
            vinfos[info.parent_id] = info;
        }
    }
    _place_axis(
        cv, vv, order, root_id, 0, viewport.rows,
        vinfos, T, B, warnings, False,
    );
    for scoped in order {
        if not scoped.is_overlay {
            continue;
        }
        id_str = scoped.id_str;
        ev = cv.nodes[id_str];
        T[id_str] = snap_edge(vv[ev.top.id]);
        B[id_str] = snap_edge(vv[ev.bottom.id]);
    }


    # ---- Frame construction ------------------------------------------
    entries: dict[str, FrameEntry] = {};
    clips: dict[str, Rect] = {};

    for scoped in order {
        id_str = scoped.id_str;
        l = L[id_str];
        r = R[id_str];
        t = T[id_str];
        b = B[id_str];

        w = r - l;
        h = b - t;
        if scoped.is_overlay {
            # Origin clamped into the viewport; SIZE KEPT AS SOLVED so a
            # too-big fixed overlay clips instead of shrinking (§6.3).
            if l < 0 {
                l = 0;
            }
            if t < 0 {
                t = 0;
            }
        }
        if w < 0 or h < 0 {
            return _fail([LayoutDiagnostic(
                code=LayoutError.INTERNAL_INVARIANT,
                severity=LayoutSeverity.ERROR,
                message="negative derived size",
                node_ids=[id_str],
            )]);
        }
        rect = Rect(x=l, y=t, width=w, height=h);

        # Clip propagation: BFS order guarantees the parent clip exists.
        if scoped.parent_id == "" {
            # Root and Layer-reached overlays have no Child parent; both
            # keep clip == rect like the frozen oracle (plan 8.3 strict
            # parity — the renderer bounds its own paint).
            clip = _copy_rect(rect);
        } else {
            pclip = clips[scoped.parent_id];
            if pclip.width <= 0 or pclip.height <= 0 or w <= 0 or h <= 0 {
                clip = Rect(x=0, y=0, width=0, height=0);
            } else {
                # Mirror oracle _clip_intersect exactly: a non-positive
                # intersection yields the empty sentinel at origin 0,0.
                x0 = pclip.x if pclip.x > l else l;
                y0 = pclip.y if pclip.y > t else t;
                pr_end = pclip.x + pclip.width;
                pb_end = pclip.y + pclip.height;
                x1 = pr_end if pr_end < r else r;
                y1 = pb_end if pb_end < b else b;
                cw = x1 - x0;
                chh = y1 - y0;
                if cw <= 0 or chh <= 0 {
                    clip = Rect(x=0, y=0, width=0, height=0);
                } else {
                    clip = Rect(x=x0, y=y0, width=cw, height=chh);
                }
            }
        }
        clips[id_str] = clip;

        wrapped = wrapped_by_node[id_str];
        requested = 0;
        spec = state.specs.get(id_str);
        if spec is not None and spec.scroll_vertical {
            requested = state.scroll_requests.get(id_str, 0);
        }
        max_off = max(0, len(wrapped) - max(1, h));
        off = min(max(requested, 0), max_off);

        entries[id_str] = FrameEntry(
            measured=Size(width=w, height=h),
            rect=_copy_rect(rect),
            clip=clip,
            wrapped_lines=list(wrapped),
            requested_scroll_offset=requested,
            scroll_offset=off,
            max_scroll_offset=max_off,
        );
    }

    overlay_ids: list[str] = [];
    for scoped in order {
        if scoped.is_overlay {
            overlay_ids.append(scoped.id_str);
        }
    }

    prev_gen = 0;
    if state.last_frame is not None {
        prev_gen = state.last_frame.generation;
    }
    frame = LayoutFrame(
        generation=prev_gen + 1,
        viewport=Viewport(columns=viewport.columns, rows=viewport.rows),
        entries=entries,
        overlay_ids=overlay_ids,
    );
    state.last_frame = frame;

    diags: list[LayoutDiagnostic] = [];
    for d in warnings {
        diags.append(d);
    }
    return LayoutResult(ok=True, frame=frame, diagnostics=diags);
}
