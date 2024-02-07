"""Jac Language Features."""

from __future__ import annotations

import types
from typing import Any, Callable, Optional, Type, TypeVar

from jaclang.compiler.absyntree import Module
from jaclang.plugin.default import (
    Architype,
    DSFunc,
    EdgeArchitype,
    EdgeDir,
    NodeArchitype,
    WalkerArchitype,
)

import pluggy

hookspec = pluggy.HookspecMarker("jac")

T = TypeVar("T")


class JacFeatureSpec:
    """Jac Feature."""

    @staticmethod
    @hookspec(firstresult=True)
    def make_architype(
        cls: type,
        arch_base: Type[Architype],
        on_entry: list[DSFunc],
        on_exit: list[DSFunc],
    ) -> Type[Architype]:
        """Create a obj architype."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def make_obj(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a obj architype."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def make_node(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a node architype."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def make_edge(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a edge architype."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def make_walker(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a walker architype."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def jac_import(
        target: str,
        base_path: str,
        cachable: bool,
        override_name: Optional[str],
        mod_bundle: Optional[Module],
    ) -> Optional[types.ModuleType]:
        """Core Import Process."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def create_test(test_fun: Callable) -> Callable:
        """Create a new test."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def run_test(filename: str) -> bool:
        """Run the test suite in the specified .jac file.

        :param filename: The path to the .jac file.
        """
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def elvis(op1: Optional[T], op2: T) -> T:
        """Jac's elvis operator feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def has_instance_default(gen_func: Callable[[], T]) -> T:
        """Jac's has container default feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def spawn_call(op1: Architype, op2: Architype) -> bool:
        """Jac's spawn operator feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def report(expr: Any) -> Any:  # noqa: ANN401
        """Jac's report stmt feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def ignore(
        walker: WalkerArchitype,
        expr: list[NodeArchitype | EdgeArchitype] | NodeArchitype | EdgeArchitype,
    ) -> bool:
        """Jac's ignore stmt feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def visit_node(
        walker: WalkerArchitype,
        expr: list[NodeArchitype | EdgeArchitype] | NodeArchitype | EdgeArchitype,
    ) -> bool:  # noqa: ANN401
        """Jac's visit stmt feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def disengage(walker: WalkerArchitype) -> bool:  # noqa: ANN401
        """Jac's disengage stmt feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def edge_ref(
        node_obj: NodeArchitype,
        dir: EdgeDir,
        filter_type: Optional[type],
        filter_func: Optional[Callable],
    ) -> list[NodeArchitype]:
        """Jac's apply_dir stmt feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def connect(
        left: NodeArchitype | list[NodeArchitype],
        right: NodeArchitype | list[NodeArchitype],
        edge_spec: EdgeArchitype,
    ) -> NodeArchitype | list[NodeArchitype]:
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
        conn_assign: Optional[tuple[tuple, tuple]],
    ) -> Architype:
        """Jac's root getter."""
        raise NotImplementedError
