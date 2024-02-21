"""Helper for the plugin builtin."""

from __future__ import annotations

from typing import Any, Callable

from jaclang.core.construct import (
    EdgeArchitype,
    NodeArchitype,
)

__all__ = [
    "NodeArchitype",
    "EdgeArchitype",
]

colors = [
    "#FFE9E9",
    "#F0FFF0",
    "#F5E5FF",
    "#FFFFE0",
    "#D2FEFF ",
    "#E8FFD7",
    "#FFDEAD",
    "#FFF0F5",
    "#F5FFFA",
    "#FFC0CB",
    "#7FFFD4",
    "#C0C0C0",
    "#ADD8E6",
    "#FFFAF0",
    "#f4f3f7",
    "#f5efff",
    "#b5d7fd",
    "#ffc0cb",
    "#FFC0CB",
    "#e1d4c0",
    "#FCDFFF",
    "#F0FFFF",
    "#F0F8FF",
    "#F8F8FF",
    "#F0FFFF",
]


def traverse_graph(
    node: NodeArchitype,
    cur_depth: float,
    depth: float,
    edge_type: list[str],
    Traverse:bool,
    connections: list,
    dpeth_of_node: dict[NodeArchitype, Any],
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
        if (Traverse and is_in_edge) or edge._jac_.obj.__class__.__name__  in edge_type:
            continue
        if is_self_loop:
            continue  # lets skip self loop for a while, need to handle it later
        else:
            other_nd = edge._jac_.target if not is_in_edge else edge._jac_.source
            new_con = (
                (node, other_nd, edge) if not is_in_edge else (other_nd, node, edge)
            )
            if node in dpeth_of_node and dpeth_of_node[node] is not None:
                if other_nd in dpeth_of_node:
                    dpeth_of_node[node] = min(
                        cur_depth, dpeth_of_node[node], dpeth_of_node[other_nd] + 1
                    )
                    dpeth_of_node[other_nd] = min(
                        cur_depth + 1, dpeth_of_node[node] + 1, dpeth_of_node[other_nd]
                    )
                else:
                    dpeth_of_node[other_nd] = min(
                        cur_depth + 1, dpeth_of_node[node] + 1
                    )
            if new_con not in connections and (
                min(dpeth_of_node[node], dpeth_of_node[other_nd]) + 1 <= depth
                and node_limit > len(visited_nodes)
                and edge_limit > len(connections)
            ):
                connections.append(new_con)
                if bfs:
                    queue.append([other_nd, cur_depth + 1])
                else:

                    dfs(other_nd, cur_depth + 1)
