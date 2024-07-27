import types
from _typeshed import Incomplete
from jaclang.compiler.absyntree import Module as Module
from jaclang.plugin.default import (
    Architype as Architype,
    DSFunc as DSFunc,
    EdgeDir as EdgeDir,
    ExecutionContext as ExecutionContext,
    Root as Root,
    WalkerArchitype as WalkerArchitype,
)
from jaclang.runtimelib.constructs import (
    EdgeArchitype as EdgeArchitype,
    NodeArchitype as NodeArchitype,
)
from jaclang.runtimelib.memory import Memory as Memory
from typing import Any, Callable, ParamSpec, TypeVar

hookspec: Incomplete
T = TypeVar("T")
P = ParamSpec("P")

class JacFeatureSpec:
    @staticmethod
    def context(session: str = "") -> ExecutionContext: ...
    @staticmethod
    def reset_context() -> None: ...
    @staticmethod
    def memory_hook() -> Memory | None: ...
    @staticmethod
    def make_architype(
        cls, arch_base: type[Architype], on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> type[Architype]: ...
    @staticmethod
    def make_obj(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]: ...
    @staticmethod
    def make_node(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]: ...
    @staticmethod
    def make_edge(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]: ...
    @staticmethod
    def make_walker(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]: ...
    @staticmethod
    def impl_patch_filename(
        file_loc: str,
    ) -> Callable[[Callable[P, T]], Callable[P, T]]: ...
    @staticmethod
    def jac_import(
        target: str,
        base_path: str,
        absorb: bool,
        cachable: bool,
        mdl_alias: str | None,
        override_name: str | None,
        mod_bundle: Module | str | None,
        lng: str | None,
        items: dict[str, str | str | None] | None,
    ) -> tuple[types.ModuleType, ...]: ...
    @staticmethod
    def create_test(test_fun: Callable) -> Callable: ...
    @staticmethod
    def run_test(
        filepath: str,
        filter: str | None,
        xit: bool,
        maxfail: int | None,
        directory: str | None,
        verbose: bool,
    ) -> int: ...
    @staticmethod
    def elvis(op1: T | None, op2: T) -> T: ...
    @staticmethod
    def has_instance_default(gen_func: Callable[[], T]) -> T: ...
    @staticmethod
    def spawn_call(op1: Architype, op2: Architype) -> WalkerArchitype: ...
    @staticmethod
    def report(expr: Any) -> Any: ...
    @staticmethod
    def ignore(
        walker: WalkerArchitype,
        expr: (
            list[NodeArchitype | EdgeArchitype]
            | list[NodeArchitype]
            | list[EdgeArchitype]
            | NodeArchitype
            | EdgeArchitype
        ),
    ) -> bool: ...
    @staticmethod
    def visit_node(
        walker: WalkerArchitype,
        expr: (
            list[NodeArchitype | EdgeArchitype]
            | list[NodeArchitype]
            | list[EdgeArchitype]
            | NodeArchitype
            | EdgeArchitype
        ),
    ) -> bool: ...
    @staticmethod
    def disengage(walker: WalkerArchitype) -> bool: ...
    @staticmethod
    def edge_ref(
        node_obj: NodeArchitype | list[NodeArchitype],
        target_obj: NodeArchitype | list[NodeArchitype] | None,
        dir: EdgeDir,
        filter_func: Callable[[list[EdgeArchitype]], list[EdgeArchitype]] | None,
        edges_only: bool,
    ) -> list[NodeArchitype] | list[EdgeArchitype]: ...
    @staticmethod
    def connect(
        left: NodeArchitype | list[NodeArchitype],
        right: NodeArchitype | list[NodeArchitype],
        edge_spec: Callable[[], EdgeArchitype],
        edges_only: bool,
    ) -> list[NodeArchitype] | list[EdgeArchitype]: ...
    @staticmethod
    def disconnect(
        left: NodeArchitype | list[NodeArchitype],
        right: NodeArchitype | list[NodeArchitype],
        dir: EdgeDir,
        filter_func: Callable[[list[EdgeArchitype]], list[EdgeArchitype]] | None,
    ) -> bool: ...
    @staticmethod
    def assign_compr(
        target: list[T], attr_val: tuple[tuple[str], tuple[Any]]
    ) -> list[T]: ...
    @staticmethod
    def get_root() -> Root: ...
    @staticmethod
    def get_root_type() -> type[Root]: ...
    @staticmethod
    def build_edge(
        is_undirected: bool,
        conn_type: type[EdgeArchitype] | EdgeArchitype | None,
        conn_assign: tuple[tuple, tuple] | None,
    ) -> Callable[[], EdgeArchitype]: ...
    @staticmethod
    def get_semstr_type(
        file_loc: str, scope: str, attr: str, return_semstr: bool
    ) -> str | None: ...
    @staticmethod
    def obj_scope(file_loc: str, attr: str) -> str: ...
    @staticmethod
    def get_sem_type(file_loc: str, attr: str) -> tuple[str | None, str | None]: ...
    @staticmethod
    def with_llm(
        file_loc: str,
        model: Any,
        model_params: dict[str, Any],
        scope: str,
        incl_info: list[tuple[str, str]],
        excl_info: list[tuple[str, str]],
        inputs: list[tuple[str, str, str, Any]],
        outputs: tuple,
        action: str,
    ) -> Any: ...

class JacBuiltin:
    @staticmethod
    def dotgen(
        node: NodeArchitype,
        depth: int,
        traverse: bool,
        edge_type: list[str],
        bfs: bool,
        edge_limit: int,
        node_limit: int,
        dot_file: str | None,
    ) -> str: ...

class JacCmdSpec:
    @staticmethod
    def create_cmd() -> None: ...
