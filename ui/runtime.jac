"""UiSession runtime: detached graph ownership, focus, bindings, and disposal.

The public ui.runtime seam re-exports session state and foundational lifecycle
operations from runtime_core, while focus and overlay operations remain here.
"""

import from .model {
    UiNode,
    UiContainer,
    UiSessionRoot,
    Screen,
    Overlay,
    Child,
    Feeds,
    FocusNext,
    Layer,
    Owns,
    node_id,
    ordered_children,
}

import from .mutation {
    append_child,
    dispose_subtree,
    MutationResult,
}

import from .bindings {
    BindingRegistry,
    clear_bindings,
    find_orphan_bindings,
    is_empty,
}

import from .runtime_core {
    RendererState,
    CapabilityRegistry,
    InvalidationRecord,
    SessionEventRecord,
    UiSession,
    SessionLeak,
    UiSessionHandle,
    create_session,
    track_node,
    is_reachable_from_root,
    assert_mutation_parent,
    append_child_session,
    set_current_screen,
    set_focus,
    register_capability,
    release_capabilities,
    record_invalidation,
    validate_session,
    dispose_session,
    get_focus_node,
}

"""Unit 7 — focus order, layer z-order, and modal overlay lifecycle."""


obj OverlayBounds {
    has x: int = 0,
        y: int = 0,
        width: int = 0,
        height: int = 0;

    def is_empty() -> bool {
        return self.width <= 0 or self.height <= 0;
    }
}


obj OverlayOpenResult {
    has overlay_id: str,
        saved_focus_id: str,
        initial_focus_id: str;
}


obj OverlayCloseResult {
    has restored_focus_id: str,
        damage: OverlayBounds,
        overlay_id: str;
}


obj RankedOverlay {
    has z_index: int,
        overlay: Overlay;
}


def _layer_z(screen: Screen, overlay: Overlay) -> int {
    for layer_edge in [edge screen ->:Layer:-> overlay] {
        return layer_edge.z_index;
    }
    return 0;
}


def _ranked_overlay_asc(pair: RankedOverlay) -> int {
    return pair.z_index;
}


def _ranked_overlay_desc(pair: RankedOverlay) -> int {
    return -pair.z_index;
}


def _layer_pairs(screen: Screen) -> list[RankedOverlay] {
    pairs: list[RankedOverlay] = [];
    for candidate in [screen ->:Layer:->] {
        pairs.append(
            RankedOverlay(
                z_index=_layer_z(screen, candidate),
                overlay=candidate,
            )
        );
    }
    return pairs;
}


"""Paint order: ascending z_index (OSPUI.md §17)."""
def layers_paint_order(screen: Screen) -> list[Overlay] {
    pairs = _layer_pairs(screen);
    pairs.sort(key=_ranked_overlay_asc);
    return [p.overlay for p in pairs];
}


"""Input targeting order: descending z_index (OSPUI.md §17)."""
def layers_input_order(screen: Screen) -> list[Overlay] {
    pairs = _layer_pairs(screen);
    pairs.sort(key=_ranked_overlay_desc);
    return [p.overlay for p in pairs];
}


def _collect_focusable(n: UiNode) -> list[UiNode] {
    out: list[UiNode] = [];
    if isinstance(n, Overlay) {
        out.append(n);
    } elif not isinstance(n, UiContainer) {
        # UiRegion and other leaf semantic nodes.
        out.append(n);
    }
    if isinstance(n, UiContainer) {
        for child in ordered_children(n) {
            for leaf in _collect_focusable(child) {
                out.append(leaf);
            }
        }
    }
    return out;
}


def _collect_subtree_ids(n: UiNode) -> list[str] {
    ids: list[str] = [node_id(n)];
    if isinstance(n, UiContainer) {
        for child in ordered_children(n) {
            for sid in _collect_subtree_ids(child) {
                ids.append(sid);
            }
        }
    }
    return ids;
}


"""Ordered focusable nodes under screen: containment walk + FocusNext overrides."""
def focus_order(session: UiSession, screen: Screen) -> list[UiNode] {
    _ = session;
    structural = _collect_focusable(screen);
    if not structural {
        return [];
    }
    ordered: list[UiNode] = [];
    visited: set[str] = set();
    for n in structural {
        nid = node_id(n);
        if nid in visited {
            continue;
        }
        current: UiNode | None = n;
        while current is not None {
            cid = node_id(current);
            if cid in visited {
                break;
            }
            ordered.append(current);
            visited.add(cid);
            nxts = [current ->:FocusNext:->];
            if not nxts {
                break;
            }
            current = nxts[0];
        }
    }
    return ordered;
}


"""Advance focus along focus_order, honoring FocusNext overrides."""
def advance_focus(
    session: UiSession,
    direction: str = "next",
) -> UiNode | None {
    screen = session.current_screen;
    if screen is None {
        return None;
    }
    order = focus_order(session, screen);
    if not order {
        return None;
    }
    focused = get_focus_node(session);
    if focused is None {
        set_focus(session, order[0]);
        return order[0];
    }
    idx = 0;
    found = -1;
    for (i, n) in enumerate(order) {
        if n is focused {
            found = i;
            break;
        }
    }
    if found >= 0 {
        idx = found;
    }
    if direction == "prev" {
        idx = (idx - 1) % len(order);
    } else {
        idx = (idx + 1) % len(order);
    }
    target = order[idx];
    set_focus(session, target);
    return target;
}


"""Open a modal overlay: Layer edge, save focus, trap input, focus initial."""
def open_modal_overlay(
    session: UiSession,
    screen: Screen,
    overlay: Overlay,
    initial_focus: UiNode | None = None,
    z_index: int = 10,
) -> OverlayOpenResult {
    saved = session.focus_id;
    existing = False;
    for _cand in [screen ->:Layer:-> overlay] {
        existing = True;
    }
    if existing {
        for layer_edge in [edge screen ->:Layer:-> overlay] {
            layer_edge.z_index = z_index;
            layer_edge.modal = True;
        }
    } else {
        screen +>:Layer(z_index=z_index, modal=True):+> overlay;
    }
    track_node(session, overlay);
    if isinstance(overlay, UiContainer) {
        for child in ordered_children(overlay) {
            track_node(session, child);
        }
    }
    session.saved_focus_id = saved;
    target = overlay if initial_focus is None else initial_focus;
    track_node(session, target);
    set_focus(session, target);
    return OverlayOpenResult(
        overlay_id=node_id(overlay),
        saved_focus_id=saved,
        initial_focus_id=node_id(target),
    );
}


"""Close overlay: dispose subtree, restore focus, report damage bounds."""
def close_overlay(
    session: UiSession,
    overlay: Overlay,
) -> OverlayCloseResult {
    overlay_id = node_id(overlay);
    damage = OverlayBounds(x=0, y=0, width=0, height=0);
    layout_entry = session.renderer.layout.get(overlay_id);
    if layout_entry is not None {
        x = int(layout_entry.get("x", 0));
        y = int(layout_entry.get("y", 0));
        w = int(layout_entry.get("width", 0));
        h = int(layout_entry.get("height", 0));
        damage = OverlayBounds(x=x, y=y, width=w, height=h);
    }

    subtree_ids = _collect_subtree_ids(overlay);

    restored = "";
    saved = session.saved_focus_id;
    session.saved_focus_id = "";
    if saved and saved in session.tracked_node_ids and saved not in subtree_ids {
        session.focus_id = saved;
        restored = saved;
    } else {
        session.focus_id = "";
    }

    for parent in list([overlay <-:Layer:<-]) {
        for e in [edge parent ->:Layer:-> overlay] {
            del e;
        }
    }
    dispose_subtree(overlay);
    for sid in subtree_ids {
        if sid in session.tracked_node_ids {
            session.tracked_node_ids.remove(sid);
        }
        release_capabilities(session, sid);
        if sid in session.renderer.layout {
            del session.renderer.layout[sid];
        }
    }
    session.graph_revision += 1;
    return OverlayCloseResult(
        restored_focus_id=restored,
        damage=damage,
        overlay_id=overlay_id,
    );
}
