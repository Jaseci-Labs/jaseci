"""Plugin interface for Jac."""
from __future__ import annotations

from .default import hookimpl
from .spec import AbsRootNode, Architype

__all__ = ["Architype", "AbsRootNode", "hookimpl"]
