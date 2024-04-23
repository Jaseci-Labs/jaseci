"""Jac Language Features."""

from __future__ import annotations

import types
from typing import Any, Callable, Optional, Type, TypeVar, Union

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
        absorb: bool,
        cachable: bool,
        mdl_alias: Optional[str],
        override_name: Optional[str],
        mod_bundle: Optional[Module],
        lng: Optional[str],
        items: Optional[dict[str, Union[str, bool]]],
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
    def run_test(
        filepath: str,
        filter: Optional[str],
        xit: bool,
        maxfail: Optional[int],
        directory: Optional[str],
        verbose: bool,
    ) -> bool:
        """Run the test suite in the specified .jac file."""
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
    def spawn_call(op1: Architype, op2: Architype) -> WalkerArchitype:
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
        node_obj: NodeArchitype | list[NodeArchitype],
        target_obj: Optional[NodeArchitype | list[NodeArchitype]],
        dir: EdgeDir,
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
        edges_only: bool,
    ) -> list[NodeArchitype] | list[EdgeArchitype]:
        """Jac's apply_dir stmt feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def connect(
        left: NodeArchitype | list[NodeArchitype],
        right: NodeArchitype | list[NodeArchitype],
        edge_spec: Callable[[], EdgeArchitype],
        edges_only: bool,
    ) -> list[NodeArchitype] | list[EdgeArchitype]:
        """Jac's connect operator feature.

        Note: connect needs to call assign compr with tuple in op
        """
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def disconnect(
        left: NodeArchitype | list[NodeArchitype],
        right: NodeArchitype | list[NodeArchitype],
        dir: EdgeDir,
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
    ) -> bool:  # noqa: ANN401
        """Jac's disconnect operator feature."""
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
        is_undirected: bool,
        conn_type: Optional[Type[EdgeArchitype]],
        conn_assign: Optional[tuple[tuple, tuple]],
    ) -> Callable[[], EdgeArchitype]:
        """Jac's root getter."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def get_semstr_type(
        file_loc: str, scope: str, attr: str, return_semstr: bool
    ) -> Optional[str]:
        """Jac's get_semstr_type stmt feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def obj_scope(file_loc: str, attr: str) -> str:
        """Jac's get_semstr_type feature."""
        raise NotImplementedError

    @staticmethod
    def get_sem_type(file_loc: str, attr: str) -> tuple[str | None, str | None]:
        """Jac's get_semstr_type feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def with_llm(
        file_loc: str,
        model: Any,  # noqa: ANN401
        model_params: dict[str, Any],
        scope: str,
        incl_info: list[tuple[str, str]],
        excl_info: list[tuple[str, str]],
        inputs: list[tuple[str, str, str, Any]],
        outputs: tuple,
        action: str,
    ) -> Any:  # noqa: ANN401
        """Jac's with_llm stmt feature."""
        raise NotImplementedError


class JacBuiltin:
    """Jac Builtins."""

    @staticmethod
    @hookspec(firstresult=True)
    def dotgen(
        node: NodeArchitype,
        depth: int,
        traverse: bool,
        edge_type: list[str],
        bfs: bool,
        edge_limit: int,
        node_limit: int,
        dot_file: Optional[str],
    ) -> str:
        """Print the dot graph."""
        raise NotImplementedError


class JacCmdSpec:
    """Jac CLI command."""

    @staticmethod
    @hookspec
    def create_cmd() -> None:
        """Create Jac CLI cmds."""
        raise NotImplementedError
