"""Constraint compilation coordinator.

The public API remains `compile_layout` and `collect_scope_for_engine`.
Phase-specific responsibilities live in explicit internal modules so this
coordinator only validates scope, allocates variables, and orchestrates
emission.
"""

import from ..constraints.solver { Solver }
import from .layout_types {
    LayoutDiagnostic,
    LayoutError,
    LayoutSeverity,
    LayoutState,
    Size,
    SizeMode,
    Viewport,
}
import from .model { UiContainer, UiNode, node_id }
import from .layout_compile_model {
    CompileResult,
    NodeEdges,
    PartitionInfo,
    _Entry,
    _Scope,
}
import from .layout_compile_scope { _collect_scope }
import from .layout_compile_emit {
    _emit_invariants,
    _emit_root,
    _req,
}
import from .layout_compile_flow { _emit_partition }
import from .layout_compile_overlays { _emit_overlay }
import from .layout_compile_relations { _emit_relation }


def compile_layout(
    state: LayoutState,
    layout_root: UiNode,
    viewport: Viewport,
    natural_sizes: dict[str, Size] = {},
    phase: str = "full",
) -> CompileResult {
    scope = _collect_scope(layout_root);
    if scope.error is not None {
        r = CompileResult(ok=False);
        r.diagnostics.append(scope.error);
        return r;
    }

    # Spec liveness for every scoped node.
    missing: list[str] = [];
    for scoped in scope.order {
        if scoped.id_str not in state.specs {
            missing.append(scoped.id_str);
        }
    }
    if missing {
        r = CompileResult(ok=False);
        r.diagnostics.append(LayoutDiagnostic(
            code=LayoutError.INVALID_SPEC,
            severity=LayoutSeverity.ERROR,
            message="scoped nodes missing LayoutSpec registration",
            node_ids=missing,
        ));
        return r;
    }

    # Relation scope + ownership (owner must be the direct Child parent
    # of both endpoints, plan §6).
    scope_ids: dict[str, bool] = {};
    for scoped in scope.order {
        scope_ids[scoped.id_str] = True;
    }
    for rid in sorted(state.relations.keys()) {
        rel = state.relations[rid];
        for endpoint in [rel.source_id, rel.target_id] {
            if endpoint not in scope_ids {
                r = CompileResult(ok=False);
                r.diagnostics.append(LayoutDiagnostic(
                    code=LayoutError.OUT_OF_SCOPE,
                    severity=LayoutSeverity.ERROR,
                    message="relation endpoint outside compiled scope",
                    node_ids=[endpoint],
                ));
                return r;
            }
        }
        if (
            scope.parent_of.get(rel.source_id) != rel.owner_id
            or scope.parent_of.get(rel.target_id) != rel.owner_id
        ) {
            r = CompileResult(ok=False);
            r.diagnostics.append(LayoutDiagnostic(
                code=LayoutError.INVALID_TOPOLOGY,
                severity=LayoutSeverity.ERROR,
                message="relation owner is not the direct Child parent "
                        "of both endpoints",
                node_ids=[rel.source_id, rel.target_id],
            ));
            return r;
        }
    }

    solver = Solver();
    result = CompileResult(ok=True, solver=solver);

    # Deterministic variable allocation in traversal order.
    entries_by_id: dict[str, _Entry] = {};
    for scoped in scope.order {
        edges = NodeEdges(
            id_str=scoped.id_str,
            key=scoped.key,
            left=solver.new_variable(),
            top=solver.new_variable(),
            right=solver.new_variable(),
            bottom=solver.new_variable(),
        );
        result.nodes[scoped.id_str] = edges;
        ent = _Entry(scoped=scoped, edges=edges, spec=state.specs[scoped.id_str]);
        entries_by_id[scoped.id_str] = ent;
    }
    root_entry = entries_by_id[node_id(layout_root)];

    # Root pins + per-node geometric invariants.
    if not _emit_root(result, root_entry.edges, viewport, phase) {
        result.solver = None;
        return result;
    }
    for scoped in scope.order {
        if not _emit_invariants(result, result.nodes[scoped.id_str], phase) {
            result.solver = None;
            return result;
        }
    }

    # Top-down continuous partition emission from the root.
    if not _emit_partition(
        result,
        root_entry,
        entries_by_id,
        natural_sizes,
        float(viewport.columns),
        float(viewport.rows),
        phase,
    ) {
        result.solver = None;
        return result;
    }

    # Overlays: out-of-flow sizing and anchoring against the root box,
    # then partition emission for their own subtrees. An overlay's
    # provisional span is its FIXED size where declared, else the root
    # viewport span (M5 threads real solved spans here).
    for scoped in scope.order {
        if not scoped.is_overlay {
            continue;
        }
        ov_entry = entries_by_id[scoped.id_str];
        if not _emit_overlay(
            result,
            ov_entry,
            root_entry.edges,
            natural_sizes,
            phase,
        ) {
            result.solver = None;
            return result;
        }
        if isinstance(scoped.target, UiContainer) {
            ov_w = float(viewport.columns);
            ov_h = float(viewport.rows);
            if ov_entry.spec.width.mode == SizeMode.FIXED {
                ov_w = _req(ov_entry.spec.width.preferred);
            }
            if ov_entry.spec.height.mode == SizeMode.FIXED {
                ov_h = _req(ov_entry.spec.height.preferred);
            }
            if not _emit_partition(
                result,
                ov_entry,
                entries_by_id,
                natural_sizes,
                ov_w,
                ov_h,
                phase,
            ) {
                result.solver = None;
                return result;
            }
        }
    }

    # Registered spatial relations, ascending handle order.
    for rid in sorted(state.relations.keys()) {
        rel = state.relations[rid];
        if not _emit_relation(result, rid, rel, result.nodes, phase) {
            result.solver = None;
            return result;
        }
    }
    return result;
}


# ----------------------------------------------------------------------
# Engine-facing helpers (compute pipeline lives in ui.layout).
# ----------------------------------------------------------------------

"""Validated scope walk shared with the engine: Child tree plus
Screen-owned Layer overlays, z-index/jid ordered."""
def collect_scope_for_engine(layout_root: UiNode) -> _Scope {
    return _collect_scope(layout_root);
}
