"""Jac specific builtins."""

from __future__ import annotations

import json
from abc import abstractmethod
from typing import ClassVar, Optional, override

from sympy import false

from jaclang.runtimelib.constructs import Architype, NodeArchitype
from jaclang.runtimelib.machine import JacMachine as Jac


def dotgen(
    node: Optional[NodeArchitype] = None,
    depth: int = -1,
    traverse: bool = False,
    edge_type: Optional[list[str]] = None,
    bfs: bool = True,
    edge_limit: int = 512,
    node_limit: int = 512,
    dot_file: Optional[str] = None,
    as_json: bool = False,
) -> str:
    """Print the dot graph."""
    from jaclang.runtimelib.machine import JacMachine as Jac

    root = Jac.root()
    node = node or root

    if as_json:
        return(_jac_graph_json())

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


def _jac_graph_json() -> str:
    """Get the graph in json string."""
    import jaclang as jl
    from jaclang import Root, Node

    processed: list[Root | Node] = []
    nodes: list[dict] = []
    edges: list[dict] = []
    working_set: list[tuple] = []

    root = Jac.root()
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

__all__ = [
    "abstractmethod",
    "ClassVar",
    "override",
    "dotgen",
    "jid",
    "jobj",
]