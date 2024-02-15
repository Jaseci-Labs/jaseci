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
    # def dotgen(node, depth):
    #     full = bool(depth)
    #     print(depth,' mmmmmmm ')
    #     node = node or root._jac_
    #     visited_nodes = []
    #     node_mapping = {}
    #     queue = [(node, 0)]  
    #     idx_counter = 1  
    #     dot_content = 'digraph {\nnode [style="filled", shape="ellipse", fillcolor="invis", fontcolor="black"];'
    #     while queue:
    #         current_node, current_depth = queue.pop(0)
    #         current_id = id(current_node)
    #         if current_id in visited_nodes:
    #             continue
    #         visited_nodes.append(current_id)
    #         node_number = visited_nodes.index(current_id)
    #         node_mapping[current_id] = node_number
    #         dot_content += f'\n{node_number} [label="{current_node._jac_.obj}"];'
    #         connected_nodes = []
    #         for edge in current_node._jac_.edges:
    #             target_node_id = id(edge._jac_.target._jac_.obj)
    #             if target_node_id==current_id:
    #                 continue
    #             if target_node_id not in node_mapping:
    #                 node_mapping[target_node_id] = len(node_mapping)
    #                 queue.append((edge._jac_.target, current_depth + 1))
    #             connected_nodes.append(node_mapping[target_node_id])
    #             dot_content += f'\n{node_number} -> {node_mapping[target_node_id]} [label="{edge._jac_.obj.__class__.__name__}"];'
    #         idx_counter += 1 
    #         if current_depth < depth:
    #             childs = [edge._jac_.target for edge in current_node._jac_.edges]
    #             queue.extend([(child, current_depth + 1) for child in childs])

    #     return dot_content + '\n}'
    def dotgen(node, depth):
        full = bool(depth)
        print(depth, ' mmmmmmm ')
        node = node or root._jac_
        visited_nodes = []
        node_mapping = {}
        queue = [(node, 0)]
        idx_counter = 1
        dot_content = 'digraph {\nnode [style="filled", shape="ellipse", fillcolor="invis", fontcolor="black"];'

        while queue:
            current_node, current_depth = queue.pop(0)
            current_id = id(current_node)
            if current_id in visited_nodes or current_depth > depth:
                continue

            visited_nodes.append(current_id)
            node_number = visited_nodes.index(current_id)
            node_mapping[current_id] = node_number
            dot_content += f'\n{node_number} [label="{current_node._jac_.obj}"];'
            connected_nodes = []

            for edge in current_node._jac_.edges:
                target_node_id = id(edge._jac_.target._jac_.obj)
                if target_node_id == current_id:
                    continue
                if target_node_id not in node_mapping:
                    node_mapping[target_node_id] = len(node_mapping)
                    if current_depth + 1 <= depth:  
                        queue.append((edge._jac_.target, current_depth + 1))
                connected_nodes.append(node_mapping[target_node_id])
                if target_node_id not in node_mapping:
                    continue
                dot_content += f'\n{node_number} -> {node_mapping[target_node_id]} [label="{edge._jac_.obj.__class__.__name__}"];'

            idx_counter += 1

        return dot_content + '\n}'
