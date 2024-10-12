"""Jac specific builtins."""

from __future__ import annotations

from typing import Optional

from jaclang.plugin.feature import JacFeature as Jac
from jaclang.runtimelib.constructs import Architype, NodeArchitype


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
