"""Jac Language Features."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional, TypeVar


T = TypeVar("T")


class JacFeature:
    """Jac Feature."""

    @staticmethod
    def make_architype(arch_type: str) -> Callable[[type], type]:
        """Create a new architype."""

        def decorator(cls: type) -> type:
            """Decorate class."""
            setattr(cls, "_jac_", field(default={"type": arch_type}))  # noqa: B010
            return dataclass(cls)

        return decorator

    @staticmethod
    def make_ds_ability(event: str, trigger: Optional[type]) -> Callable[[type], type]:
        """Create a new architype."""

        def decorator(func: type) -> type:
            """Decorate class."""
            return func

        return decorator

    @staticmethod
    def elvis(op1: Optional[T], op2: T) -> T:
        """Jac's elvis operator feature."""
        return ret if (ret := op1) is not None else op2
