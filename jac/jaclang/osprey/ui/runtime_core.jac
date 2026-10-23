"""UiSession runtime: detached graph ownership, focus, bindings, and disposal.

The view graph lives under UiSessionRoot and is never attached to Jac's
persistent root. Renderer geometry and capability tables are session-local
side tables keyed by jid(node).
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
    find_node_by_jid,
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


obj RendererState {
    has layout: dict[str, dict[str, int]] = {};
    has damage: list[dict[str, int]] = [];
    has cursor_holder_id: str = "";
}


obj CapabilityRegistry {
    has by_node: dict[str, list[str]] = {};
}


obj InvalidationRecord {
    has node_id: str,
        layout_root_id: str,
        reason: str;
}


"""Queued UI session event (resize, ...) for consumers to drain."""
obj SessionEventRecord {
    has kind: str = "";
    has payload: dict[str, int] = {};
}


obj UiSession {
    has bindings: BindingRegistry;
    has renderer: RendererState;
    has capabilities: CapabilityRegistry;
    has ui_root: UiSessionRoot | None = None;
    has current_screen: Screen | None = None;
    has focus_id: str = "";
    has saved_focus_id: str = "";
    has graph_revision: int = 0;
    has disposed: bool = False;
    has invalidation_journal: list[InvalidationRecord] = [];
    has event_queue: list[SessionEventRecord] = [];
    has tracked_node_ids: set[str] = set();
}


obj SessionLeak {
    has kind: str,
        detail: str;
}


obj UiSessionHandle {
    has session: UiSession;
    has ui_root_id: str;
}


def create_session() -> UiSessionHandle {
    ui_root = UiSessionRoot(key="session");
    session = UiSession(
        ui_root=ui_root,
        bindings=BindingRegistry(),
        renderer=RendererState(),
        capabilities=CapabilityRegistry(),
    );
    track_node(session, ui_root);
    return UiSessionHandle(session=session, ui_root_id=node_id(ui_root));
}


def track_node(session: UiSession, n: UiNode) {
    session.tracked_node_ids.add(node_id(n));
}


def is_reachable_from_root(session: UiSession, n: UiNode) -> bool {
    if session.disposed or session.ui_root is None {
        return False;
    }
    current: UiNode | None = n;
    while current is not None {
        if current is session.ui_root {
            return True;
        }
        parents = [current <-:Child:<-];
        if not parents {
            return False;
        }
        current = parents[0];
    }
    return False;
}


def assert_mutation_parent(session: UiSession, parent: UiContainer) {
    if session.disposed {
        raise ValueError("UiSession is disposed");
    }
    if not is_reachable_from_root(session, parent) {
        raise ValueError(
            "Mutation parent is not reachable from UiSessionRoot: "
            + parent.key
        );
    }
}


def append_child_session(
    session: UiSession,
    parent: UiContainer,
    child: UiNode,
) -> MutationResult {
    assert_mutation_parent(session, parent);
    result = append_child(parent, child);
    track_node(session, child);
    session.graph_revision += result.graph_revision;
    if result.layout_root_id {
        record_invalidation(
            session,
            node_id(child),
            result.layout_root_id,
            "append_child",
        );
    }
    return result;
}


def set_current_screen(session: UiSession, screen: Screen) {
    session.current_screen = screen;
    track_node(session, screen);
}


def set_focus(session: UiSession, n: UiNode | None) {
    if n is None {
        session.focus_id = "";
        return;
    }
    session.focus_id = node_id(n);
}


def register_capability(session: UiSession, node_id_str: str, cap_name: str) {
    if node_id_str not in session.capabilities.by_node {
        session.capabilities.by_node[node_id_str] = [];
    }
    session.capabilities.by_node[node_id_str].append(cap_name);
}


def release_capabilities(session: UiSession, node_id_str: str) {
    if node_id_str in session.capabilities.by_node {
        del session.capabilities.by_node[node_id_str];
    }
}


def record_invalidation(
    session: UiSession,
    node_id_str: str,
    layout_root_id: str,
    reason: str,
) {
    session.invalidation_journal.append(
        InvalidationRecord(
            node_id=node_id_str,
            layout_root_id=layout_root_id,
            reason=reason,
        )
    );
}


def _endpoint_tracked(session: UiSession, n: UiNode) -> bool {
    return node_id(n) in session.tracked_node_ids;
}


def _collect_stale_edges(session: UiSession) -> list[str] {
    stale: list[str] = [];
    if session.ui_root is None {
        return stale;
    }
    stack: list[UiNode] = [session.ui_root];
    while stack {
        current = stack.pop();
        if isinstance(current, UiContainer) {
            for child in ordered_children(current) {
                if not _endpoint_tracked(session, child) {
                    stale.append(
                        "Child:"
                        + node_id(current)
                        + "->"
                        + node_id(child)
                    );
                }
                stack.append(child);
            }
        }
        for target in [current ->:Owns:->] {
            if not _endpoint_tracked(session, target) {
                stale.append("Owns:" + node_id(current) + "->" + node_id(target));
            }
        }
        for target in [current ->:Feeds:->] {
            if not _endpoint_tracked(session, target) {
                stale.append("Feeds:" + node_id(current) + "->" + node_id(target));
            }
        }
        for target in [current ->:FocusNext:->] {
            if not _endpoint_tracked(session, target) {
                stale.append(
                    "FocusNext:" + node_id(current) + "->" + node_id(target)
                );
            }
        }
        for target in [current ->:Layer:->] {
            if not _endpoint_tracked(session, target) {
                stale.append("Layer:" + node_id(current) + "->" + node_id(target));
            }
        }
    }
    return stale;
}



def validate_session(session: UiSession) -> list[SessionLeak] {
    if session.disposed {
        return [];
    }
    leaks: list[SessionLeak] = [];
    for binding in find_orphan_bindings(
        session.bindings,
        session.tracked_node_ids,
    ) {
        leaks.append(
            SessionLeak(
                kind="orphan_binding",
                detail=binding.target_id,
            )
        );
    }
    if session.focus_id and session.focus_id not in session.tracked_node_ids {
        leaks.append(
            SessionLeak(
                kind="invalid_focus",
                detail=session.focus_id,
            )
        );
    }
    for cap_node_id in session.capabilities.by_node {
        if cap_node_id not in session.tracked_node_ids {
            leaks.append(
                SessionLeak(
                    kind="unreleased_capability",
                    detail=cap_node_id,
                )
            );
        }
    }
    for layout_id in session.renderer.layout {
        if layout_id not in session.tracked_node_ids {
            leaks.append(
                SessionLeak(
                    kind="stale_renderer_layout",
                    detail=layout_id,
                )
            );
        }
    }
    for edge_detail in _collect_stale_edges(session) {
        leaks.append(
            SessionLeak(
                kind="stale_edge",
                detail=edge_detail,
            )
        );
    }
    return leaks;
}


def dispose_session(session: UiSession) {
    if session.disposed {
        return;
    }
    session.disposed = True;
    clear_bindings(session.bindings);
    session.capabilities.by_node = {};
    session.renderer.layout = {};
    session.renderer.damage = [];
    session.renderer.cursor_holder_id = "";
    session.event_queue = [];
    session.invalidation_journal = [];
    session.focus_id = "";
    session.saved_focus_id = "";
    session.current_screen = None;
    if session.ui_root is not None {
        dispose_subtree(session.ui_root);
        session.ui_root = None;
    }
    session.tracked_node_ids.clear();
}


def get_focus_node(session: UiSession) -> UiNode | None {
    if session.disposed or session.ui_root is None or not session.focus_id {
        return None;
    }
    if session.focus_id not in session.tracked_node_ids {
        return None;
    }
    return find_node_by_jid(session.ui_root, session.focus_id);
}