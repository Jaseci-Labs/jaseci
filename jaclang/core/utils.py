"""Helper for construct."""
from typing import TYPE_CHECKING

from jaclang.compiler.constant import EdgeDir


if TYPE_CHECKING:
    from jaclang.core.construct import NodeArchitype


def collect_node_connections(
    current_node: "NodeArchitype",
    visited_nodes: set,
    connections: set,
) -> None:
    """Nodes and edges representing the graph are collected in visited_nodes and connections."""
    if current_node not in visited_nodes:
        visited_nodes.add(current_node)
        out_edges = current_node.edges.get(EdgeDir.OUT, [])
        in_edges = current_node.edges.get(EdgeDir.IN, [])

        for edge_ in out_edges:
            target__ = edge_._jac_.target
            connections.add(
                (current_node.obj, target__._jac_.obj, edge_.__class__.__name__)
            )
            collect_node_connections(target__._jac_, visited_nodes, connections)

        for edge_ in in_edges:
            source__ = edge_._jac_.source
            connections.add(
                (source__._jac_.obj, current_node.obj, edge_.__class__.__name__)
            )
            collect_node_connections(source__._jac_, visited_nodes, connections)
