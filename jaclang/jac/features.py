"""Jac Language Features."""
from __future__ import annotations

from typing import Optional, TypeVar

T = TypeVar("T")


def elvis(op1: Optional[T], op2: T) -> T:
    """Jac's elvis operator feature."""
    return ret if (ret := op1) is not None else op2
