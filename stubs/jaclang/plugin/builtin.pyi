"""Jac specific builtins."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Optional
    from jaclang.core.constructs import NodeArchitype

def dotgen(
    node: Optional[NodeArchitype] = None,
    depth: Optional[int] = None,
    traverse: Optional[bool] = None,
    edge_type: Optional[list[str]] = None,
    bfs: Optional[bool] = None,
    edge_limit: Optional[int] = None,
    node_limit: Optional[int] = None,
    dot_file: Optional[str] = None,
) -> str: ...
