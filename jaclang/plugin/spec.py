"""Jac Language Features."""
from __future__ import annotations


from typing import Any, Optional, Type, TypeVar

from jaclang.compiler.constant import EdgeDir
from jaclang.core.construct import Architype, DSFunc


import pluggy

hookspec = pluggy.HookspecMarker("jac")


T = TypeVar("T")
AT = TypeVar("AT", bound=Architype)


class JacFeatureSpec:
    """Jac Feature."""

    @staticmethod
    @hookspec(firstresult=True)
    def bind_architype(
        arch: Type[AT], arch_type: str, on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> bool:
        """Create a new architype."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def elvis(op1: Optional[T], op2: T) -> T:  # noqa: ANN401
        """Jac's elvis operator feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def report(expr: Any) -> Any:  # noqa: ANN401
        """Jac's report stmt feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def ignore(walker_obj: Any, expr: Any) -> bool:  # noqa: ANN401
        """Jac's ignore stmt feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def visit_node(walker_obj: Any, expr: Any) -> bool:  # noqa: ANN401
        """Jac's visit stmt feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def disengage(walker_obj: Any) -> bool:  # noqa: ANN401
        """Jac's disengage stmt feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def edge_ref(
        node_obj: Any, dir: EdgeDir, filter_type: Optional[type]  # noqa: ANN401
    ) -> list[Any]:
        """Jac's apply_dir stmt feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def connect(
        left: T, right: T, edge_spec: tuple[int, Optional[type], Optional[tuple]]
    ) -> T:  # noqa: ANN401
        """Jac's connect operator feature.

        Note: connect needs to call assign compr with tuple in op
        """
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def disconnect(op1: Optional[T], op2: T, op: Any) -> T:  # noqa: ANN401
        """Jac's connect operator feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def assign_compr(
        target: list[T], attr_val: tuple[tuple[str], tuple[Any]]
    ) -> list[T]:
        """Jac's assign comprehension feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def get_root() -> Architype:
        """Jac's root getter."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def build_edge(
        edge_spec: tuple[int, Optional[tuple], Optional[tuple]]
    ) -> Architype:
        """Jac's root getter."""
        raise NotImplementedError
