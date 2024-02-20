"""Jac Language Builtin ."""

from __future__ import annotations

from typing import Any

from jaclang.core.construct import (
    EdgeArchitype,
    NodeArchitype,
    root,
)
from jaclang.plugin.utils import helper

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
        node: NodeArchitype, depth: float, bfs: bool, edge_limit: int, node_limit: int
    ) -> str:
        visited_nodes: list[Any] = []
        dpeth_of_node: dict[NodeArchitype, int] = {}
        queue: list = [[node, 0]]
        connections: list[tuple[NodeArchitype, NodeArchitype, EdgeArchitype]] = []
        found_node = next((item for item in visited_nodes if item[0] == node), None)

        def dfs(node: NodeArchitype, cur_depth: int) -> None:
            """Depth first search."""
            if found_node == 1:
                return
            elif found_node is not None:
                found_node[1] = 1
            else:
                visited_nodes.append([node, 1])
            dpeth_of_node[node] = cur_depth
            helper(
                node,
                cur_depth,
                connections,
                visited_nodes,
                queue,
                bfs,
                dfs,
                depth,
                node_limit,
                edge_limit,
            )

        if bfs:
            cur_depth = 0
            while queue:
                current_node, cur_depth = queue.pop(0)
                found_node = next(
                    (item for item in visited_nodes if item[0] == current_node), None
                )
                if found_node == 1:
                    continue
                elif found_node is not None:
                    found_node[1] = 1
                else:
                    visited_nodes.append([current_node, 1])
                helper(
                    current_node,
                    cur_depth,
                    connections,
                    visited_nodes,
                    queue,
                    bfs,
                    dfs,
                    depth,
                    node_limit,
                    edge_limit,
                )
        else:
            dfs(node, cur_depth=0)
        dot_content = 'digraph {\nnode [style="filled", shape="ellipse", fillcolor="invis", fontcolor="black"];\n'
        for unique_node in visited_nodes:
            dot_content += f'{visited_nodes.index(unique_node)} [label="{unique_node[0]._jac_.obj}"];\n'
        result_dict: dict[NodeArchitype, int] = {
            item[0]: index for index, item in enumerate(visited_nodes)
        }
        for source, target, edge in connections:
            dot_content += (
                f"{ result_dict[source]} -> {result_dict[target]}"
                f' [label="{edge._jac_.obj.__class__.__name__}"];\n'
            )
        print(visited_nodes)
        return dot_content + "}"

    # @staticmethod
    # @hookimpl
    # def dijkstra(start_node):
    #     start_node_id = id(start_node)
    #     distances = {start_node_id: (start_node, 0)}
    #     visited = set()
    #     def get_node_by_id(start_node, target_id):
    #         stack = [start_node]
    #         visited = set()
    #         while stack:
    #             current_node = stack.pop()
    #             current_node_id = id(current_node)
    #             if current_node_id in visited:
    #                 continue
    #             visited.add(current_node_id)
    #             if current_node_id == target_id:
    #                 return current_node
    #             stack.extend(edge._jac_.target for edge in current_node._jac_.edges)
    #         return None
    #     while True:
    #         current_node_id = min((node_id for node_id in distances if node_id not in visited),
    #                             key=lambda k: distances[k][1], default=None)
    #         if current_node_id is None:
    #             break
    #         visited.add(current_node_id)
    #         current_node = get_node_by_id(start_node, current_node_id)
    #         for edge in current_node._jac_.edges:
    #             target_node = edge._jac_.target
    #             target_node_id = id(target_node)
    #             new_distance = distances[current_node_id][1] + 1
    #             if target_node_id not in distances or new_distance < distances[target_node_id][1]:
    #                 distances[target_node_id] = (target_node, new_distance)

    #     return {node_name: distance for node_id, (node_name, distance) in distances.items()}
