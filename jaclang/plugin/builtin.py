"""Jac Language Builtin ."""

from __future__ import annotations


from jaclang.core.construct import (
    EdgeArchitype,
    NodeArchitype,
    root,
)
from jaclang.plugin.utils import colors, traverse_graph

import pluggy

__all__ = [
    "NodeArchitype",
    "EdgeArchitype",
    "root",
]

hookimpl = pluggy.HookimplMarker("jac")


class JacBuiltin:
    """Jac Builtins."""

    @staticmethod
    @hookimpl
    def dotgen(
        node: NodeArchitype, depth: float,Traverse:bool, bfs: bool, edge_limit: int, node_limit: int
    ) -> str:
        """Generate Dot file for visualizing nodes and edges."""
        visited_nodes: list[NodeArchitype] = []
        dpeth_of_node: dict[NodeArchitype, int] = {node: 0}
        queue: list = [[node, 0]]
        connections: list[tuple[NodeArchitype, NodeArchitype, EdgeArchitype]] = []

        def dfs(node: NodeArchitype, cur_depth: int) -> None:
            """Depth first search."""
            if node not in visited_nodes:
                visited_nodes.append(node)
                traverse_graph(
                    Traverse,
                    node,
                    cur_depth,
                    depth,
                    connections,
                    dpeth_of_node,
                    visited_nodes,
                    queue,
                    bfs,
                    dfs,
                    node_limit,
                    edge_limit,
                )

        if bfs:
            cur_depth = 0
            while queue:
                current_node, cur_depth = queue.pop(0)
                if current_node not in visited_nodes:
                    visited_nodes.append(current_node)
                    traverse_graph(
                        Traverse,
                        current_node,
                        cur_depth,
                        depth,
                        connections,
                        dpeth_of_node,
                        visited_nodes,
                        queue,
                        bfs,
                        dfs,
                        node_limit,
                        edge_limit,
                    )
        else:
            dfs(node, cur_depth=0)
        dot_content = 'digraph {\nnode [style="filled", shape="ellipse", fillcolor="invis", fontcolor="black"];\n'
        for source, target, edge in connections:
            dot_content += (
                f"{visited_nodes.index(source)} -> {visited_nodes.index(target)} "
                f' [label="{edge._jac_.obj.__class__.__name__} "];\n'
            )
        for node_ in visited_nodes:
            color = (
                colors[dpeth_of_node[node_]]
                if dpeth_of_node[node_] < 25
                else colors[24]
            )
            dot_content += f'{visited_nodes.index(node_)} [label="{node_._jac_.obj}" fillcolor="{color}"];\n'
        return dot_content + "}"

