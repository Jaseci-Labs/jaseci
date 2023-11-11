"""Jac Language Features."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional, TypeVar


T = TypeVar("T")


class JacFeature:
    """Jac Feature."""

    @staticmethod
    def make_architype(arch_type: str) -> Callable[[type], type]:
        """Create a new architype."""

        def decorator(cls: type) -> type:
            """Decorate class."""
            cls._jac_ = {"type": arch_type}
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
    def elvis(op1: Optional[T], op2: T) -> T:  # noqa: ANN401
        """Jac's elvis operator feature."""
        return ret if (ret := op1) is not None else op2

    @staticmethod
    def report(expr: Any) -> None:  # noqa: ANN401
        """Jac's report stmt feature."""

    @staticmethod
    def ignore(walker_obj: Any, expr: Any) -> None:  # noqa: ANN401
        """Jac's ignore stmt feature."""

    @staticmethod
    def visit(walker_obj: Any, expr: Any) -> bool:  # noqa: ANN401
        """Jac's visit stmt feature."""
        return True

    @staticmethod
    def disengage(walker_obj: Any) -> None:  # noqa: ANN401
        """Jac's disengage stmt feature."""

    @staticmethod
    def connect(op1: Optional[T], op2: T, op: Any) -> T:  # noqa: ANN401
        """Jac's connect operator feature."""
        return ret if (ret := op1) is not None else op2

    @staticmethod
    def disconnect(op1: Optional[T], op2: T, op: Any) -> T:  # noqa: ANN401
        """Jac's connect operator feature."""
        return ret if (ret := op1) is not None else op2
