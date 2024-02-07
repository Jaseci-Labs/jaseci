"""Plugin interface for Jac."""

from __future__ import annotations

from .default import hookimpl
from .spec import Architype, DSFunc

__all__ = ["Architype", "DSFunc", "hookimpl"]
