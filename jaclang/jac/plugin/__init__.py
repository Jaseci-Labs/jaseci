"""Plugin interface for Jac."""
from __future__ import annotations

from .default import hookimpl
from .spec import AbsRootHook, Architype

__all__ = ["Architype", "AbsRootHook", "hookimpl"]
