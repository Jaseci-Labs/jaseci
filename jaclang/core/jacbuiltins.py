"""Jac specific builtins."""

from __future__ import annotations

from jaclang.core.construct import NodeArchitype


def dotgen(node: NodeArchitype, radius: int = 0) -> str:
    """Print the dot graph."""
    return f"dot graph for {node} here"
