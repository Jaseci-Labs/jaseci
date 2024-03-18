"""Helper for construct."""

from __future__ import annotations

from typing import Any, Callable, TYPE_CHECKING


if TYPE_CHECKING:
    from jaclang.core.construct import NodeAnchor, NodeArchitype


def collect_node_connections(
    current_node: NodeAnchor,
    visited_nodes: set,
    connections: set,
) -> None:
    """Nodes and edges representing the graph are collected in visited_nodes and connections."""
    if current_node not in visited_nodes:
        visited_nodes.add(current_node)
        edges = current_node.edges
        for edge_ in edges:
            target = edge_._jac_.target
            if target:
                connections.add(
                    (current_node.obj, target._jac_.obj, edge_.__class__.__name__)
                )
                collect_node_connections(target._jac_, visited_nodes, connections)


def traverse_graph(
    node: NodeArchitype,
    cur_depth: int,
    depth: int,
    edge_type: list[str],
    traverse: bool,
    connections: list,
    node_depths: dict[NodeArchitype, int],
    visited_nodes: list,
    queue: list,
    bfs: bool,
    dfs: Callable,
    node_limit: int,
    edge_limit: int,
) -> None:
    """Traverse the graph using Breadth-First Search (BFS) or Depth-First Search (DFS)."""
    for edge in node._jac_.edges:
        is_self_loop = id(edge._jac_.source) == id(edge._jac_.target)
        is_in_edge = edge._jac_.target == node
        if (traverse and is_in_edge) or edge._jac_.obj.__class__.__name__ in edge_type:
            continue
        if is_self_loop:
            continue  # lets skip self loop for a while, need to handle it later
        else:
            other_nd = edge._jac_.target if not is_in_edge else edge._jac_.source
            new_con = (
                (node, other_nd, edge) if not is_in_edge else (other_nd, node, edge)
            )
            if node in node_depths and node_depths[node] is not None:
                if other_nd in node_depths:
                    node_depths[node] = min(
                        cur_depth, node_depths[node], node_depths[other_nd] + 1
                    )
                    node_depths[other_nd] = min(
                        cur_depth + 1, node_depths[node] + 1, node_depths[other_nd]
                    )
                else:
                    if other_nd:
                        node_depths[other_nd] = min(
                            cur_depth + 1, node_depths[node] + 1
                        )
                    else:
                        raise ValueError("Edge is detached from node in graph")
            if (
                other_nd
                and new_con not in connections
                and (
                    (
                        depth < 0
                        or min(node_depths[node], node_depths[other_nd]) + 1 <= depth
                    )
                    and node_limit > len(visited_nodes)
                    and edge_limit > len(connections)
                )
            ):
                connections.append(new_con)
                if bfs:
                    queue.append([other_nd, cur_depth + 1])
                else:

                    dfs(other_nd, cur_depth + 1)


def get_type_annotation(data: Any) -> str:  # noqa: ANN401  # TODO: Need to Modify
    """Get the type annotation of the input data."""
    if isinstance(data, dict):
        class_name = next(
            (value.__class__.__name__ for value in data.values() if value is not None),
            None,
        )

        if class_name:
            return f"dict[str, {class_name}]"
        else:
            return "dict[str, Any]"
    else:
        return type(data).__name__


def filter(
    scope: str, registry_data: dict, info_str: str, incl_info: tuple[str, str]
) -> str:
    """Filter the registry data based on the scope and return the info string."""
    parts = scope.split(".")
    avail_scopes = [scope]
    for i in range(1, len(parts)):
        avail_scopes.append(".".join(parts[:i]))

    filtered_data = {}
    for key in avail_scopes:
        if key in registry_data:
            filtered_data[key] = registry_data[key]

    def key_exists(dictionary: dict, key: str) -> Any:  # noqa: ANN401
        """Check if key exists in registry."""
        for k, v in dictionary.items():
            if k == key:
                return v
            if isinstance(v, dict) and key_exists(v, key):
                return v[key]
        return False

    info_str = ""  # TODO: We have to generate this
    for incl in incl_info:
        if not key_exists(filtered_data, incl[0]):
            raise ValueError(f"Invalid scope: {incl[0]}")
        else:
            info_str += f"{key_exists(filtered_data, incl[0])}\n"
    return info_str


registry_data = {
    "get_emoji(Module)": {
        "model": ["obj", ""],
        "llm": [None, ""],
        "emoji_examples": ["list[dict[str,str]]", "Examples of Text to Emoji"],
        "outer": ["obj", "out sem "],
        "personality_examples": [
            "dict[str,Personality|None]",
            "Personality Information of Famous People",
        ],
    },
    "get_emoji(Module).outer(obj).inner(obj)": {
        "self.vv": ["int", "semstr of  self.vv "]
    },
    "get_emoji(Module).outer(obj)": {"inner": ["obj", "inner sem"]},
}
