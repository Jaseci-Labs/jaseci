"""Jaclang Library."""

from __future__ import annotations

from abc import ABCMeta
from typing import Any, Callable, cast

from jaclang.plugin.feature import JacFeature
from jaclang.runtimelib.architype import Root


class Jac(JacFeature):
    """Jac Library Addons."""

    @staticmethod
    def with_entry(func: Callable) -> Callable:
        """Mark a method as jac entry with this decorator."""
        setattr(func, "__jac_entry", True)  # noqa: B010
        return func

    @staticmethod
    def with_exit(func: Callable) -> Callable:
        """Mark a method as jac exit with this decorator."""
        setattr(func, "__jac_exit", True)  # noqa: B010
        return func

    @classmethod  # type: ignore[misc]
    @property
    def root(cls) -> Root:
        """Get current root."""
        return Jac.get_root()

    class JacMeta(ABCMeta):
        """Common metaclass for Jac types."""

        def __new__(
            cls,
            name: str,
            bases: tuple[type, ...],
            dct: dict[str, Any],
        ) -> Jac.JacMeta:
            """Initialize Metaclasses."""
            return JacFeature.make_architype2(super().__new__(cls, name, bases, dct))  # type: ignore

    class Arch(metaclass=JacMeta):
        """Arch Meta."""


__all__ = "Jac"
