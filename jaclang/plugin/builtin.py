"""Jac Language Builtin ."""

from __future__ import annotations


from jaclang.core.construct import (
    EdgeArchitype,
    NodeAnchor,
    NodeArchitype,
    root,
)

import heapq
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
    def dotgen(node, depth):
        unique_nodes = {}
        queue = [(node, 0)]  
        dot_content = 'digraph {\nnode [style="filled", shape="ellipse", fillcolor="invis", fontcolor="black"];'
        while queue:
            current_node, current_depth = queue.pop(0)
            current_id = id(current_node)
            if current_id in unique_nodes and unique_nodes[current_id][0] == 1:
                continue
            if current_id in unique_nodes:
                unique_nodes[current_id][0] = 1
            else:
                unique_nodes[current_id] = [1, len(unique_nodes), current_depth]
            node_number = unique_nodes[current_id][1]
            dot_content += f'\n{node_number} [label="{current_node._jac_.obj}"];'
            if current_depth >= depth:
                    continue
            for edge in current_node._jac_.edges:
                target_node_id = id(edge._jac_.target._jac_.obj)
                if target_node_id==current_id:
                    if edge._jac_.target==edge._jac_.source:
                        print(edge._jac_.target,edge._jac_.source)
                    continue
                if target_node_id not in unique_nodes:
                    unique_nodes[target_node_id] = [0, len(unique_nodes), current_depth + 1]
                    queue.append((edge._jac_.target, current_depth + 1))
                dot_content += f'\n{node_number} -> {unique_nodes[target_node_id][1]} [label="{edge._jac_.obj.__class__.__name__}"];'
                childs = [edge._jac_.target for edge in current_node._jac_.edges]
                queue.extend([(child, current_depth + 1) for child in childs])
        
       
        return dot_content + '\n}'
    
    @staticmethod
    @hookimpl
    def dijkstra(start_node):
        start_node_id = id(start_node)
        distances = {start_node_id: (start_node, 0)}
        visited = set()
        def get_node_by_id(start_node, target_id):
            stack = [start_node]
            visited = set()
            while stack:
                current_node = stack.pop()
                current_node_id = id(current_node)
                if current_node_id in visited:
                    continue
                visited.add(current_node_id)
                if current_node_id == target_id:
                    return current_node
                stack.extend(edge._jac_.target for edge in current_node._jac_.edges)
            return None
        while True:
            current_node_id = min((node_id for node_id in distances if node_id not in visited),
                                key=lambda k: distances[k][1], default=None)
            if current_node_id is None:
                break
            visited.add(current_node_id)
            current_node = get_node_by_id(start_node, current_node_id)
            for edge in current_node._jac_.edges:
                target_node = edge._jac_.target
                target_node_id = id(target_node)
                new_distance = distances[current_node_id][1] + 1  
                if target_node_id not in distances or new_distance < distances[target_node_id][1]:
                    distances[target_node_id] = (target_node, new_distance)
        for x,y in distances.items():
            print(y[0],' : ',y[1])
        # return {node_name: distance for node_id, (node_name, distance) in distances.items()}
        return ''