"""Jac specific builtins."""

from __future__ import annotations

import json
from typing import Optional

from jaclang.plugin.feature import JacFeature as Jac
from jaclang.runtimelib.constructs import Architype, NodeArchitype

__all__ = [
    "dotgen",
    "jid",
    "jobj",
    "jac_graph_json",
]


def dotgen(
    node: Optional[NodeArchitype] = None,
    depth: Optional[int] = None,
    traverse: Optional[bool] = None,
    edge_type: Optional[list[str]] = None,
    bfs: Optional[bool] = None,
    edge_limit: Optional[int] = None,
    node_limit: Optional[int] = None,
    dot_file: Optional[str] = None,
) -> str:
    """Print the dot graph."""
    from jaclang.plugin.feature import JacFeature as Jac

    root = Jac.get_root()
    node = node if node is not None else root
    depth = depth if depth is not None else -1
    traverse = traverse if traverse is not None else False
    bfs = bfs if bfs is not None else True
    edge_limit = edge_limit if edge_limit is not None else 512
    node_limit = node_limit if node_limit is not None else 512

    return Jac.dotgen(
        edge_type=edge_type,
        node=node,
        depth=depth,
        traverse=traverse,
        bfs=bfs,
        edge_limit=edge_limit,
        node_limit=node_limit,
        dot_file=dot_file,
    )


def jid(obj: Architype) -> str:
    """Get the id of the object."""
    return Jac.object_ref(obj)


def jobj(id: str) -> Architype | None:
    """Get the object from the id."""
    return Jac.get_object(id)


def jac_graph_json() -> str:
    """Get the graph in json string."""
    import jaclang as jl
    from jaclang import Root, Node

    processed: list[Root | Node] = []
    nodes: list[dict] = []
    edges: list[dict] = []
    working_set: list[tuple] = []

    root: Root = jl.root
    nodes.append({"id": id(root), "label": "root"})

    processed.append(root)
    working_set = [(root, ref) for ref in root.refs()]

    while working_set:
        start, end = working_set.pop(0)
        edges.append({"from": id(start), "to": id(end)})
        nodes.append({"id": id(end), "label": repr(end)})
        processed.append(end)
        for ref in end.refs():
            if ref not in processed:
                working_set.append((end, ref))
    return json.dumps(
        {
            "version": "1.0",
            "nodes": nodes,
            "edges": edges,
        }
    )
