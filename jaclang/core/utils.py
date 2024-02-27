"""Helper for construct."""

from __future__ import annotations

from typing import Callable, TYPE_CHECKING


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
