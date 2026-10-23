"""Persistent-graph reachability probe (diagnostic; server-placed).

Reads the Jac persistent root — inherently host-side. Kept in its own
module so `runtime_core.jac` (which owns the session types) is not pulled
server-side by the root-access classifier.
"""


"""BFS from Jac persistent root across all edge types; return UI jids found."""
def ui_jids_reachable_from_persistent_root(ui_jids: set[str]) -> list[str] {
    found: list[str] = [];
    visited: set[str] = set();
    # Seed via append: an any-typed list literal (`= [root]`) does not lower
    # natively, while append onto an explicitly typed list does.
    queue: list[any] = [];
    queue.append(root);
    while queue {
        current = queue.pop(0);
        current_jid = jid(current);
        if current_jid in ui_jids {
            found.append(current_jid);
        }
        for neighbor in [current -->] {
            nj = jid(neighbor);
            if nj not in visited {
                visited.add(nj);
                queue.append(neighbor);
            }
        }
        for neighbor in [current <--] {
            nj = jid(neighbor);
            if nj not in visited {
                visited.add(nj);
                queue.append(neighbor);
            }
        }
    }
    return found;
}
