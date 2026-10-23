"""Continuous flow allocation and recursive partition emission."""

import from ..constraints.algebra {
    Relation,
    StrengthTier,
}
import from .layout_types {
    AxisSize,
    LayoutDiagnostic,
    LayoutError,
    LayoutSeverity,
    Size,
    SizeMode,
}
import from .model { UiContainer, node_id, ordered_children }
import from .layout_compile_model {
    CompileResult,
    NodeEdges,
    PartitionInfo,
    _Allocation,
    _Entry,
    _FlowChild,
    _wants,
}
import from .layout_compile_emit {
    _axis_end,
    _axis_start,
    _emit,
    _emit_cross_axis,
    _emit_sized_axis,
    _expr,
    _prov,
    _req,
    _t,
}


def _flow_weight(size: AxisSize) -> float {
    if size.mode == SizeMode.GROW {
        return size.grow_weight;
    }
    if size.mode == SizeMode.FILL {
        return 1.0;
    }
    return 0.0;
}


"""Hard partition claim: only REQUIRED-exact sizes count. FIXED is a
required equality so its claim is load-bearing; every other non-flex
mode emits soft (WEAK) preferences and must NOT bear on the hard
partition arithmetic — a WEAK input inside a REQUIRED closure would let
solver drift turn the whole frame unsatisfiable (GoldLion review, BUG B).
This deliberately narrows plan §6.2 step 2 ("fixed/intrinsic/bounded
non-grow claims") to fixed-only; the soft claims still drive the OVERFLOW
warning via _flow_soft_claim."""
def _flow_hard_claim(size: AxisSize) -> float {
    if size.mode == SizeMode.FIXED {
        return _req(size.preferred);
    }
    return 0.0;
}


"""Soft best-estimate claim (plan §6.2 step 2 as written): used for the
OVERFLOW warning and for recursion spans of inflexible children — never
for hard partition arithmetic."""
def _flow_soft_claim(size: AxisSize, natural: float | None) -> float {
    if size.mode == SizeMode.FIXED {
        return _req(size.preferred);
    }
    if size.preferred is not None {
        return size.preferred;
    }
    if natural is not None {
        return natural;
    }
    if size.mode == SizeMode.BOUNDED {
        return size.minimum;
    }
    return 0.0;
}


"""Bounded proportional allocation with freeze-at-bound iteration
(plan §6.2 steps 2–5, with the §4.1-review hard/soft claim split).
Arithmetic uses hard claims only; `overflow` is flagged when either the
hard or the soft non-grow claims exceed the span (warning either way,
solver contradiction only in the hard case). Never returns negative
targets; grow children absorb zero when the hard remainder is spent."""
def _allocate_span(children: list[_FlowChild], span: float) -> _Allocation {
    n = len(children);
    alloc = _Allocation(targets=[0.0] * n);
    hard_sum = 0.0;
    soft_sum = 0.0;
    for i in range(n) {
        size = children[i].size;
        if _flow_weight(size) == 0.0 {
            hard_sum += max(0.0, _flow_hard_claim(size));
            soft_sum += max(0.0, _flow_soft_claim(size, children[i].natural));
        }
    }
    remaining = span - hard_sum;
    if remaining < 0.0 or soft_sum > span + 1e-8 {
        alloc.overflow = True;
        remaining = max(0.0, remaining);
    }
    if hard_sum > span + 1e-8 {
        alloc.hard_overflow = True;
    }
    active: list[int] = [];
    for i in range(n) {
        if _flow_weight(children[i].size) > 0.0 {
            active.append(i);
        } else {
            # Best-estimate target for inflexible children: drives the
            # recursion span for containers, never a hard equality.
            alloc.targets[i] = max(0.0, _flow_soft_claim(
                children[i].size, children[i].natural
            ));
        }
    }
    while len(active) {
        wsum = 0.0;
        for i in active {
            wsum += _flow_weight(children[i].size);
        }
        if wsum <= 0.0 {
            for i in active {
                alloc.targets[i] = 0.0;
            }
            break;
        }
        frozen: list[int] = [];
        for i in active {
            share = remaining * (_flow_weight(children[i].size) / wsum);
            mx = children[i].size.maximum;
            if share < children[i].size.minimum - 1e-8 {
                alloc.targets[i] = max(0.0, children[i].size.minimum);
                remaining -= alloc.targets[i];
                frozen.append(i);
            } elif mx is not None and share > mx + 1e-8 {
                alloc.targets[i] = mx;
                remaining -= mx;
                frozen.append(i);
            }
        }
        if not frozen {
            for i in active {
                alloc.targets[i] = max(
                    0.0, remaining * (_flow_weight(children[i].size) / wsum)
                );
            }
            break;
        }
        next_active: list[int] = [];
        for i in active {
            is_frozen = False;
            for f in frozen {
                if f == i {
                    is_frozen = True;
                }
            }
            if not is_frozen {
                next_active.append(i);
            }
        }
        active = next_active;
    }
    for i in range(n) {
        if alloc.targets[i] < 0.0 {
            alloc.targets[i] = 0.0;
        }
    }
    return alloc;
}


# ----------------------------------------------------------------------
# Flow partition + subtree emission.
# ----------------------------------------------------------------------

"""Compile one container's flow partition along spec.flow_axis: grow
allocation over the declared span, adjacency chain, per-child size facts,
cross-axis resolution, partition-closing edge when flexible, and
recursion into child containers with their allocated spans."""
def _emit_partition(
    result: CompileResult,
    owner: _Entry,
    entries_by_id: dict[str, _Entry],
    natural_sizes: dict[str, Size],
    span_w: float,
    span_h: float,
    phase: str,
) -> bool {
    spec = owner.spec;
    parent_edges = owner.edges;
    horizontal_flow = spec.flow_axis.value == "horizontal";
    flow_label = "h" if horizontal_flow else "v";

    flow_kids: list[_FlowChild] = [];
    for scoped in _ordered_flow_children(owner, entries_by_id) {
        child_spec = scoped.spec;
        nat: float | None = None;
        nid = scoped.edges.id_str;
        if horizontal_flow {
            size_axis = child_spec.width;
            if nid in natural_sizes {
                nat = float(natural_sizes[nid].width);
            }
        } else {
            size_axis = child_spec.height;
            if nid in natural_sizes {
                nat = float(natural_sizes[nid].height);
            }
        }
        flow_kids.append(_FlowChild(ent=scoped, size=size_axis, natural=nat));
    }

    span_flow = span_w if horizontal_flow else span_h;
    alloc = _allocate_span(flow_kids, span_flow);
    if _wants(phase, horizontal_flow) {
        info = PartitionInfo(
            parent_id=parent_edges.id_str,
            horizontal=horizontal_flow,
            span=span_flow,
        );
        for i in range(len(flow_kids)) {
            kid_size = flow_kids[i].size;
            mx = kid_size.maximum;
            if mx is None {
                mx = 1e308;
            }
            info.child_ids.append(flow_kids[i].ent.edges.id_str);
            info.targets.append(alloc.targets[i]);
            info.fixed.append(_flow_weight(kid_size) == 0.0);
            info.minimums.append(kid_size.minimum);
            info.maximums.append(mx);
        }
        result.partitions.append(info);
    }
    if alloc.overflow {
        # M5 seam: hard_overflow partitions must NOT go through
        # ui.layout_quantize.quantize_partition (no honest integer
        # closure exists); the publisher quantizes their children
        # clip-aware per the contract in the quantizer module docstring.
        result.diagnostics.append(LayoutDiagnostic(
            code=LayoutError.OVERFLOW,
            severity=LayoutSeverity.WARNING,
            message="flow partition exceeds parent span; "
                    "non-flexible claims kept",
            node_ids=[parent_edges.id_str],
        ));
    }

    # Adjacency chain: first start pinned to parent start; siblings chain.
    # Emitted only when this phase owns the flow axis.
    if len(flow_kids) and _wants(phase, horizontal_flow) {
        if not _emit(
            result,
            _expr([
                _t(_axis_start(flow_kids[0].ent.edges, horizontal_flow)),
                _t(_axis_start(parent_edges, horizontal_flow), -1.0),
            ]),
            Relation.EQ,
            StrengthTier.REQUIRED,
            _prov("flow", parent_edges.id_str, flow_label),
        ) {
            return False;
        }
        for i in range(1, len(flow_kids)) {
            if not _emit(
                result,
                _expr([
                    _t(_axis_start(flow_kids[i].ent.edges, horizontal_flow)),
                    _t(_axis_end(flow_kids[i - 1].ent.edges, horizontal_flow), -1.0),
                ]),
                Relation.EQ,
                StrengthTier.REQUIRED,
                _prov("flow", parent_edges.id_str, flow_label),
            ) {
                return False;
            }
        }
    }

    has_flexible = False;
    for i in range(len(flow_kids)) {
        # Cross-axis facts (further down) must be emitted in BOTH phases
        # when they fall on the current axis; only FLOW-axis size facts
        # are gated to the phase that owns the flow axis.
        kid = flow_kids[i];
        kid_edges = kid.ent.edges;
        kid_scoped = kid.ent.scoped;
        if _wants(phase, horizontal_flow) and _flow_weight(kid.size) > 0.0 {
            has_flexible = True;
            if not _emit(
                result,
                _expr([
                    _t(_axis_end(kid_edges, horizontal_flow)),
                    _t(_axis_start(kid_edges, horizontal_flow), -1.0),
                ], -alloc.targets[i]),
                Relation.EQ,
                StrengthTier.REQUIRED,
                _prov(
                    "grow", kid_edges.id_str, flow_label,
                    key=kid_edges.key,
                    parent=parent_edges.id_str,
                    rank=kid_scoped.rank,
                    src="spec",
                    extra="weight=" + repr(_flow_weight(kid.size))
                          + " target=" + repr(alloc.targets[i]),
                ),
            ) {
                return False;
            }
        } elif _wants(phase, horizontal_flow) {
            if not _emit_sized_axis(
                result,
                kid.size,
                _axis_start(kid_edges, horizontal_flow),
                _axis_end(kid_edges, horizontal_flow),
                horizontal_flow,
                kid_edges.id_str,
                kid.natural,
                "src=spec parent=" + parent_edges.id_str
                + "#" + str(kid_scoped.rank),
            ) {
                return False;
            }
        }

        # Cross-axis resolution against the parent content box. The
        # cross axis is the opposite of THIS container's flow axis.
        if _wants(phase, not horizontal_flow) {
            if not _emit_cross_axis(
                result, kid.ent, owner, natural_sizes,
                not horizontal_flow,
            ) {
                return False;
            }
        }

        # Recurse: the child's own flow span is what it was allocated;
        # the cross span passes straight through from this container.
        child_span_w = alloc.targets[i] if horizontal_flow else span_w;
        child_span_h = span_h if horizontal_flow else alloc.targets[i];
        if isinstance(kid.ent.scoped.target, UiContainer) {
            if not _emit_partition(
                result, kid.ent, entries_by_id, natural_sizes,
                child_span_w, child_span_h, phase,
            ) {
                return False;
            }
        }
    }

    # Close the partition only when a flexible child absorbs the slack;
    # otherwise trailing space stays empty like the legacy engine. On
    # overflow the closure is omitted too: fixed claims already stick
    # out of the parent and the publisher clips them (plan §6.2 step 3)
    # — forcing closure here would turn the warned overflow into an
    # UNSATISFIABLE frame.
    if has_flexible and not alloc.hard_overflow and _wants(phase, horizontal_flow) {
        last_edges = flow_kids[len(flow_kids) - 1].ent.edges;
        if not _emit(
            result,
            _expr([
                _t(_axis_end(last_edges, horizontal_flow)),
                _t(_axis_end(parent_edges, horizontal_flow), -1.0),
            ]),
            Relation.EQ,
            StrengthTier.REQUIRED,
            _prov("flow", parent_edges.id_str, flow_label),
        ) {
            return False;
        }
    }
    return True;
}


"""Ordered non-overlay Child entries of a container entry."""
def _ordered_flow_children(
    owner: _Entry,
    entries_by_id: dict[str, _Entry],
) -> list[_Entry] {
    out: list[_Entry] = [];
    if not isinstance(owner.scoped.target, UiContainer) {
        return out;
    }
    for child in ordered_children(owner.scoped.target) {
        cid = node_id(child);
        if cid in entries_by_id and not entries_by_id[cid].scoped.is_overlay {
            out.append(entries_by_id[cid]);
        }
    }
    return out;
}


