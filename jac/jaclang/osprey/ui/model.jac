"""OSP-native semantic UI graph model for Osprey's detached view session.

The live UI is a durable OSP graph of semantic regions connected by typed edges.
Nodes carry only stable keys and semantic state. Stable identity outside the graph
uses jid(node). Renderer geometry, caches, and closures live in process-local
runtime side tables (layout.jac, renderer.jac, runtime.jac), not on nodes.
"""


node UiNode {
    has key: str = "";
}


node UiContainer(UiNode) {}


node UiRegion(UiNode) {}


node UiSessionRoot(UiContainer) {}


node Screen(UiContainer) {}


node Overlay(UiContainer) {}


"""Osprey shell and shared semantic region archetypes."""
node MainScreen(Screen) {}


node Header(UiRegion) {
    has title: str = "";
}


node TranscriptView(UiRegion) {
    has scroll_offset: int = 0;
    has follow_tail: bool = True;
    has source_id: str = "";
    has observed_revision: int = 0;
}


node Prompt(UiRegion) {
    has draft: str = "";
    has mode: str = "insert";
    has caret: int = 0;
    has sel_anchor: int = -1;
    has sel_end: int = -1;
    has history: list[str] = [];
    has history_index: int = -1;
}


node Status(UiRegion) {
    has phase: str = "";
}


node ApprovalOverlay(Overlay) {}


"""Visual containment with deterministic sibling order."""
edge Child: UiContainer --> UiNode {
    has rank: int;
}


"""UI-local disposal responsibility."""
edge Owns: UiNode --> UiNode {}


"""UI-local invalidation dependency within the detached graph."""
edge Feeds: UiNode --> UiNode {}


"""Explicit focus order override."""
edge FocusNext: UiNode --> UiNode {}


"""Overlay layering outside normal-flow containment."""
edge Layer: Screen --> Overlay {
    has z_index: int;
    has modal: bool = False;
}


obj RankedChild {
    has rank: int,
        nd: UiNode;
}


"""Return the stable 32-char node identifier for side-table keys."""
def node_id(n: UiNode) -> str {
    return jid(n);
}


def _ranked_child_key(pair: RankedChild) -> int {
    return pair.rank;
}


"""Return direct Child descendants of parent in ascending rank order."""
def ordered_children(parent: UiContainer) -> list[UiNode] {
    pairs: list[RankedChild] = [];
    for child in [parent ->:Child:->] {
        for e in [edge parent ->:Child:-> child] {
            pairs.append(RankedChild(rank=e.rank, nd=child));
        }
    }
    pairs.sort(key=_ranked_child_key);
    return [pair.nd for pair in pairs];
}


"""Return ordered keys for direct Child descendants."""
def ordered_child_keys(parent: UiContainer) -> list[str] {
    return [child.key for child in ordered_children(parent)];
}


"""Return the Child rank for one mounted child, or -1 when absent."""
def child_rank(parent: UiContainer, child: UiNode) -> int {
    for e in [edge parent ->:Child:-> child] {
        return e.rank;
    }
    return -1;
}


"""Return the single Child parent when mounted, else None."""
def child_parent(child: UiNode) -> UiContainer | None {
    parents = [child <-:Child:<-];
    if not parents {
        return None;
    }
    return parents[0];
}


"""Walk upward through Child containment to the nearest Screen ancestor."""
def enclosing_screen(n: UiNode) -> Screen | None {
    current: UiNode | None = n;
    while current is not None {
        if isinstance(current, Screen) {
            return current;
        }
        parents = [current <-:Child:<-];
        if not parents {
            return None;
        }
        current = parents[0];
    }
    return None;
}


"""Collect duplicate sibling keys under one parent."""
def duplicate_sibling_keys(parent: UiContainer) -> list[str] {
    seen: dict[str, int] = {};
    dups: list[str] = [];
    for child in ordered_children(parent) {
        if not child.key {
            continue;
        }
        count = seen.get(child.key, 0) + 1;
        seen[child.key] = count;
        if count == 2 {
            dups.append(child.key);
        }
    }
    return dups;
}


"""True when ancestor is reachable upward from child via Child edges."""
def is_child_ancestor(ancestor: UiNode, child: UiNode) -> bool {
    current: UiNode | None = child;
    while current is not None {
        if current is ancestor {
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

"""Subtree lookup by jid (DFS in key order)."""
def find_node_by_jid(n: UiNode, target_jid: str) -> UiNode | None {
    if node_id(n) == target_jid {
        return n;
    }
    if isinstance(n, UiContainer) {
        for child in ordered_children(n) {
            found = find_node_by_jid(child, target_jid);
            if found is not None {
                return found;
            }
        }
    }
    return None;
}
