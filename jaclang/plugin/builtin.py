"""Jac Language Builtin ."""

from __future__ import annotations

# import subprocess

from jaclang.core.construct import (
    EdgeArchitype,
    NodeAnchor,
    NodeArchitype,
    root,
)

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
    def dotgen(node: NodeAnchor, radius: int) -> str:
        """Print the dot graph."""
        full = bool(radius)
        node = node or root._jac_
        visited_nodes: set[NodeAnchor] = set()
        connections: set[tuple[NodeAnchor, NodeAnchor, EdgeArchitype]] = set()
        unique_node_id_dict = {}

        def generate_unique_node_id(node: NodeAnchor, idx: int) -> str:
            """Generate a unique node ID for the given node."""
            unique_node_id_dict[node] = str(idx)
            return f'{idx} [label="{node.obj}"];\n'

        def collect_node_connections(
            current_node: NodeAnchor,
            visited_nodes: set,
            connections: set,
            depth: int,
        ) -> None:
            """Nodes and edges representing the graph are collected in visited_nodes and connections."""
            if full and depth > radius:
                return
            if current_node not in visited_nodes:
                visited_nodes.add((current_node))
                for edge_ in current_node.edges:
                    if edge_._jac_ is not None and edge_._jac_.target is not None:
                        target = edge_._jac_.target
                        connections.add(((current_node), (target._jac_), edge_))
                        collect_node_connections(
                            target._jac_, visited_nodes, connections, depth + 1
                        )

        if node is not None:
            collect_node_connections(node, visited_nodes, connections, 0)
        dot_content = 'digraph {\nnode [style="filled", shape="ellipse", fillcolor="invis", fontcolor="black"];\n'
        dot_content += "".join(
            generate_unique_node_id(node, idx) for idx, node in enumerate(visited_nodes)
        )
        dot_content += 'edge [color="gray", style="solid"];\n'
        for source, target, edge in set(connections):
            source_node = unique_node_id_dict.get(source)
            target_node = unique_node_id_dict.get(target)

            if source != target and source_node and target_node:
                dot_content += (
                    f"{source_node} -> {target_node}"
                    f' [label="{edge.__class__.__name__}"];\n'
                )

        # if dot_file:
        #     with open(dot_file, "w") as f:
        #         f.write(dot_content + "}")
        # with open("output.dot", "w") as f:
        #     f.write(dot_content+'}')

        # subprocess.run(["dot", "-Tpng", "output.dot", "-o", "output.png"])
        # subprocess.run(["explorer.exe", "output.png"])

        return dot_content + "}"
        # return   len(dot_content)
