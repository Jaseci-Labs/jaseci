"""Jac Language Features."""
from __future__ import annotations


from typing import Any, Callable, Optional, Type, TypeVar

from jaclang.core.construct import (
    Architype,
    DSFunc,
    EdgeAnchor,
    EdgeArchitype,
    EdgeDir,
    GenericEdge,
    NodeAnchor,
    NodeArchitype,
    ObjectAnchor,
    Root,
    WalkerAnchor,
    WalkerArchitype,
    root,
)

__all__ = [
    "EdgeAnchor",
    "GenericEdge",
    "NodeAnchor",
    "ObjectAnchor",
    "WalkerAnchor",
    "NodeArchitype",
    "EdgeArchitype",
    "WalkerArchitype",
    "Architype",
    "DSFunc",
    "EdgeDir",
    "root",
    "Root",
]

import pluggy

hookspec = pluggy.HookspecMarker("jac")


T = TypeVar("T")
ArchBound = TypeVar("ArchBound", bound=Architype)


class JacFeatureSpec:
    """Jac Feature."""

    @staticmethod
    @hookspec(firstresult=True)
    def make_architype(
        arch_type: str, on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a new architype."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def elvis(op1: Optional[T], op2: T) -> T:
        """Jac's elvis operator feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def report(expr: Any) -> Any:  # noqa: ANN401
        """Jac's report stmt feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def ignore(walker: Any, expr: Any) -> bool:  # noqa: ANN401
        """Jac's ignore stmt feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def visit_node(walker: Any, expr: Any) -> bool:  # noqa: ANN401
        """Jac's visit stmt feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def disengage(walker: Any) -> bool:  # noqa: ANN401
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
        left: Architype | list[Architype],
        right: Architype | list[Architype],
        edge_spec: Architype,
    ) -> Architype | list[Architype]:
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
        edge_dir: EdgeDir,
        conn_type: Optional[Type[Architype]],
        conn_assign: Optional[tuple],
    ) -> Architype:
        """Jac's root getter."""
        raise NotImplementedError
