"""Jac Language Features."""

from __future__ import annotations

import ast as ast3
import types
from typing import (
    Any,
    Callable,
    Mapping,
    Optional,
    ParamSpec,
    Sequence,
    Type,
    TypeVar,
    Union,
)
from uuid import UUID

from jaclang.compiler import absyntree as ast
from jaclang.compiler.constant import EdgeDir
from jaclang.compiler.passes.main.pyast_gen_pass import PyastGenPass
from jaclang.runtimelib.constructs import (
    AccessLevel,
    Anchor,
    Architype,
    DSFunc,
    EdgeAnchor,
    EdgeArchitype,
    NodeAnchor,
    NodeArchitype,
    Root,
    WalkerArchitype,
)
from jaclang.runtimelib.context import ExecutionContext

import pluggy

hookspec = pluggy.HookspecMarker("jac")
plugin_manager = pluggy.PluginManager("jac")

T = TypeVar("T")
P = ParamSpec("P")


class JacAccessValidationSpec:
    """Jac Access Validation Specs."""

    @staticmethod
    @hookspec(firstresult=True)
    def allow_root(
        architype: Architype, root_id: UUID, level: AccessLevel | int | str
    ) -> None:
        """Allow all access from target root graph to current Architype."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def disallow_root(
        architype: Architype, root_id: UUID, level: AccessLevel | int | str
    ) -> None:
        """Disallow all access from target root graph to current Architype."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def unrestrict(architype: Architype, level: AccessLevel | int | str) -> None:
        """Allow everyone to access current Architype."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def restrict(architype: Architype) -> None:
        """Disallow others to access current Architype."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def check_read_access(to: Anchor) -> bool:
        """Read Access Validation."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def check_connect_access(to: Anchor) -> bool:
        """Write Access Validation."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def check_write_access(to: Anchor) -> bool:
        """Write Access Validation."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def check_access_level(to: Anchor) -> AccessLevel:
        """Access validation."""
        raise NotImplementedError


class JacNodeSpec:
    """Jac Node Operations."""

    @staticmethod
    @hookspec(firstresult=True)
    def node_dot(node: NodeArchitype, dot_file: Optional[str]) -> str:
        """Generate Dot file for visualizing nodes and edges."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def get_edges(
        node: NodeAnchor,
        dir: EdgeDir,
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
        target_obj: Optional[list[NodeArchitype]],
    ) -> list[EdgeArchitype]:
        """Get edges connected to this node."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def edges_to_nodes(
        node: NodeAnchor,
        dir: EdgeDir,
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
        target_obj: Optional[list[NodeArchitype]],
    ) -> list[NodeArchitype]:
        """Get set of nodes connected to this node."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def remove_edge(node: NodeAnchor, edge: EdgeAnchor) -> None:
        """Remove reference without checking sync status."""
        raise NotImplementedError


class JacEdgeSpec:
    """Jac Edge Operations."""

    @staticmethod
    @hookspec(firstresult=True)
    def detach(edge: EdgeAnchor) -> None:
        """Detach edge from nodes."""
        raise NotImplementedError


class JacWalkerSpec:
    """Jac Edge Operations."""

    @staticmethod
    @hookspec(firstresult=True)
    def visit_node(
        walker: WalkerArchitype,
        expr: (
            list[NodeArchitype | EdgeArchitype]
            | list[NodeArchitype]
            | list[EdgeArchitype]
            | NodeArchitype
            | EdgeArchitype
        ),
    ) -> bool:  # noqa: ANN401
        """Jac's visit stmt feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def ignore(
        walker: WalkerArchitype,
        expr: (
            list[NodeArchitype | EdgeArchitype]
            | list[NodeArchitype]
            | list[EdgeArchitype]
            | NodeArchitype
            | EdgeArchitype
        ),
    ) -> bool:
        """Jac's ignore stmt feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def spawn_call(op1: Architype, op2: Architype) -> WalkerArchitype:
        """Invoke data spatial call."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def disengage(walker: WalkerArchitype) -> bool:
        """Jac's disengage stmt feature."""
        raise NotImplementedError


class JacBuiltinSpec:
    """Jac Builtins."""

    @staticmethod
    @hookspec(firstresult=True)
    def dotgen(
        node: NodeArchitype,
        depth: int,
        traverse: bool,
        edge_type: Optional[list[str]],
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


class JacFeatureSpec(
    JacAccessValidationSpec,
    JacNodeSpec,
    JacEdgeSpec,
    JacWalkerSpec,
    JacBuiltinSpec,
    JacCmdSpec,
):
    """Jac Feature."""

    @staticmethod
    @hookspec(firstresult=True)
    def setup() -> None:
        """Set Class References."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def get_context() -> ExecutionContext:
        """Get current execution context."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def get_object(id: str) -> Architype | None:
        """Get object by id."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def object_ref(obj: Architype) -> str:
        """Get object's id."""
        raise NotImplementedError

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
    def impl_patch_filename(
        file_loc: str,
    ) -> Callable[[Callable[P, T]], Callable[P, T]]:
        """Update impl file location."""
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
        lng: Optional[str],
        items: Optional[dict[str, Union[str, Optional[str]]]],
        reload_module: Optional[bool],
    ) -> tuple[types.ModuleType, ...]:
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
    ) -> int:
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
    def report(expr: Any, custom: bool) -> None:  # noqa: ANN401
        """Jac's report stmt feature."""
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
        edge_spec: Callable[[NodeAnchor, NodeAnchor], EdgeArchitype],
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
    def get_root() -> Root:
        """Jac's root getter."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def get_root_type() -> Type[Root]:
        """Jac's root getter."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def build_edge(
        is_undirected: bool,
        conn_type: Optional[Type[EdgeArchitype] | EdgeArchitype],
        conn_assign: Optional[tuple[tuple, tuple]],
    ) -> Callable[[NodeAnchor, NodeAnchor], EdgeArchitype]:
        """Jac's root getter."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def save(
        obj: Architype | Anchor,
    ) -> None:
        """Destroy object."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def destroy(
        obj: Architype | Anchor,
    ) -> None:
        """Destroy object."""
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
    @hookspec(firstresult=True)
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
        _globals: dict,
        _locals: Mapping,
    ) -> Any:  # noqa: ANN401
        """Jac's with_llm stmt feature."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def gen_llm_body(_pass: PyastGenPass, node: ast.Ability) -> list[ast3.AST]:
        """Generate the by LLM body."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def by_llm_call(
        _pass: PyastGenPass,
        model: ast3.AST,
        model_params: dict[str, ast.Expr],
        scope: ast3.AST,
        inputs: Sequence[Optional[ast3.AST]],
        outputs: Sequence[Optional[ast3.AST]] | ast3.Call,
        action: Optional[ast3.AST],
        include_info: list[tuple[str, ast3.AST]],
        exclude_info: list[tuple[str, ast3.AST]],
    ) -> ast3.Call:
        """Return the LLM Call, e.g. _Jac.with_llm()."""
        raise NotImplementedError

    @staticmethod
    @hookspec(firstresult=True)
    def get_by_llm_call_args(_pass: PyastGenPass, node: ast.FuncCall) -> dict:
        """Get the by LLM call args."""
        raise NotImplementedError


plugin_manager.add_hookspecs(JacFeatureSpec)
