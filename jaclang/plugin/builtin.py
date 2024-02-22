"""Jac specific builtins."""

from __future__ import annotations

from typing import Optional

from jaclang.core.construct import (
    NodeArchitype,
)
from jaclang.core.construct import root
from jaclang.plugin.feature import pm
from jaclang.plugin.spec import JacBuiltin


pm.add_hookspecs(JacBuiltin)


def dotgen(
    node: NodeArchitype = root,
    depth: float = float("inf"),
    traverse: bool = False,
    edge_type: Optional[list[str]] = None,
    bfs: bool = True,
    edge_limit: int = 512,
    node_limit: int = 512,
    dot_file: Optional[str] = None,
) -> str:
    """Print the dot graph."""
    return pm.hook.dotgen(
        edge_type=edge_type,
        node=node,
        depth=depth,
        traverse=traverse,
        bfs=bfs,
        edge_limit=edge_limit,
        node_limit=node_limit,
        dot_file=dot_file,
    )
