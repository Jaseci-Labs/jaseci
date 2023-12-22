"""Plugin interface for Jac."""
from __future__ import annotations

from .default import hookimpl
from .spec import AbsRootHook, Architype, DSFunc

__all__ = ["Architype", "AbsRootHook", "DSFunc", "hookimpl"]
