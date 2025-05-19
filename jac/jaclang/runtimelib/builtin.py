"""Jac specific builtins."""

from __future__ import annotations

import json
from abc import abstractmethod
from typing import ClassVar, Optional, override

from jaclang.runtimelib.constructs import Archetype, NodeArchetype, Root
from jaclang.runtimelib.machine import JacMachineInterface as Jac


# FIXME: Retname this to something common, doing this way so this doesn't break
# the existing code. Currently it can return the jac graph in both dot and json format.
# So the name shuouldn't be dotgen but something more generic.
def dotgen(
    node: Optional[NodeArchetype] = None,
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
    from jaclang.runtimelib.machine import JacMachineInterface as Jac

    if as_json:
        return _jac_graph_json()

    return Jac.dotgen(
        edge_type=edge_type,
        node=node or Jac.root(),
        depth=depth,
        traverse=traverse,
        bfs=bfs,
        edge_limit=edge_limit,
        node_limit=node_limit,
        dot_file=dot_file,
    )


def jid(obj: Archetype) -> str:
    """Get the id of the object."""
    return Jac.object_ref(obj)


def jobj(id: str) -> Archetype | None:
    """Get the object from the id."""
    return Jac.get_object(id)


def _jac_graph_json() -> str:
    """Get the graph in json string."""
    processed: list[Root | NodeArchetype] = []
    nodes: list[dict] = []
    edges: list[dict] = []
    working_set: list[tuple] = []

    root = Jac.root()
    nodes.append({"id": id(root), "label": "root"})

    processed.append(root)
    working_set = [(root, ref) for ref in Jac.refs(root)]

    while working_set:
        start, end = working_set.pop(0)
        edges.append({"from": id(start), "to": id(end)})
        nodes.append({"id": id(end), "label": repr(end)})
        processed.append(end)
        for ref in Jac.refs(end):
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
