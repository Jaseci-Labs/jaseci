"""Plugin interface for Jac."""
from __future__ import annotations

from .default import hookimpl
from .spec import AbsRootHook, Architype, ArchitypeProtocol, DSFunc

__all__ = ["Architype", "ArchitypeProtocol", "AbsRootHook", "DSFunc", "hookimpl"]
