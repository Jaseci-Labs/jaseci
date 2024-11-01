"""Jac Language Features."""

from __future__ import annotations

import ast as ast3
import types
from typing import (
    Any,
    Callable,
    ClassVar,
    Mapping,
    Optional,
    Sequence,
    Type,
    TypeAlias,
    Union,
)
from uuid import UUID

from jaclang.plugin.spec import (
    AccessLevel,
    Anchor,
    Architype,
    DSFunc,
    EdgeAnchor,
    EdgeArchitype,
    EdgeDir,
    ExecutionContext,
    NodeAnchor,
    NodeArchitype,
    P,
    PyastGenPass,
    Root,
    T,
    WalkerArchitype,
    ast,
    plugin_manager,
)


class JacAccessValidation:
    """Jac Access Validation Specs."""

    @staticmethod
    def allow_root(
        architype: Architype,
        root_id: UUID,
        level: AccessLevel | int | str = AccessLevel.READ,
    ) -> None:
        """Allow all access from target root graph to current Architype."""
        plugin_manager.hook.allow_root(
            architype=architype, root_id=root_id, level=level
        )

    @staticmethod
    def disallow_root(
        architype: Architype,
        root_id: UUID,
        level: AccessLevel | int | str = AccessLevel.READ,
    ) -> None:
        """Disallow all access from target root graph to current Architype."""
        plugin_manager.hook.disallow_root(
            architype=architype, root_id=root_id, level=level
        )

    @staticmethod
    def unrestrict(
        architype: Architype, level: AccessLevel | int | str = AccessLevel.READ
    ) -> None:
        """Allow everyone to access current Architype."""
        plugin_manager.hook.unrestrict(architype=architype, level=level)

    @staticmethod
    def restrict(architype: Architype) -> None:
        """Disallow others to access current Architype."""
        plugin_manager.hook.restrict(architype=architype)

    @staticmethod
    def check_read_access(to: Anchor) -> bool:
        """Read Access Validation."""
        return plugin_manager.hook.check_read_access(to=to)

    @staticmethod
    def check_connect_access(to: Anchor) -> bool:
        """Write Access Validation."""
        return plugin_manager.hook.check_connect_access(to=to)

    @staticmethod
    def check_write_access(to: Anchor) -> bool:
        """Write Access Validation."""
        return plugin_manager.hook.check_write_access(to=to)

    @staticmethod
    def check_access_level(to: Anchor) -> AccessLevel:
        """Access validation."""
        return plugin_manager.hook.check_access_level(to=to)


class JacNode:
    """Jac Node Operations."""

    @staticmethod
    def node_dot(node: NodeArchitype, dot_file: Optional[str] = None) -> str:
        """Generate Dot file for visualizing nodes and edges."""
        return plugin_manager.hook.node_dot(node=node, dot_file=dot_file)

    @staticmethod
    def get_edges(
        node: NodeAnchor,
        dir: EdgeDir,
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
        target_obj: Optional[list[NodeArchitype]],
    ) -> list[EdgeArchitype]:
        """Get edges connected to this node."""
        return plugin_manager.hook.get_edges(
            node=node, dir=dir, filter_func=filter_func, target_obj=target_obj
        )

    @staticmethod
    def edges_to_nodes(
        node: NodeAnchor,
        dir: EdgeDir,
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
        target_obj: Optional[list[NodeArchitype]],
    ) -> list[NodeArchitype]:
        """Get set of nodes connected to this node."""
        return plugin_manager.hook.edges_to_nodes(
            node=node, dir=dir, filter_func=filter_func, target_obj=target_obj
        )

    @staticmethod
    def remove_edge(node: NodeAnchor, edge: EdgeAnchor) -> None:
        """Remove reference without checking sync status."""
        return plugin_manager.hook.remove_edge(node=node, edge=edge)


class JacEdge:
    """Jac Edge Operations."""

    @staticmethod
    def detach(edge: EdgeAnchor) -> None:
        """Detach edge from nodes."""
        return plugin_manager.hook.detach(edge=edge)


class JacWalker:
    """Jac Edge Operations."""

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
    ) -> bool:  # noqa: ANN401
        """Jac's visit stmt feature."""
        return plugin_manager.hook.visit_node(walker=walker, expr=expr)

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
    ) -> bool:  # noqa: ANN401
        """Jac's ignore stmt feature."""
        return plugin_manager.hook.ignore(walker=walker, expr=expr)

    @staticmethod
    def spawn_call(op1: Architype, op2: Architype) -> WalkerArchitype:
        """Jac's spawn operator feature."""
        return plugin_manager.hook.spawn_call(op1=op1, op2=op2)

    @staticmethod
    def disengage(walker: WalkerArchitype) -> bool:
        """Jac's disengage stmt feature."""
        return plugin_manager.hook.disengage(walker=walker)


class JacClassReferences:
    """Default Classes References."""

    EdgeDir: ClassVar[TypeAlias] = EdgeDir
    DSFunc: ClassVar[TypeAlias] = DSFunc
    RootType: ClassVar[TypeAlias] = Root
    Obj: ClassVar[TypeAlias] = Architype
    Node: ClassVar[TypeAlias] = NodeArchitype
    Edge: ClassVar[TypeAlias] = EdgeArchitype
    Walker: ClassVar[TypeAlias] = WalkerArchitype


class JacBuiltin:
    """Jac Builtins."""

    @staticmethod
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
        """Generate Dot file for visualizing nodes and edges."""
        return plugin_manager.hook.dotgen(
            node=node,
            depth=depth,
            traverse=traverse,
            edge_type=edge_type,
            bfs=bfs,
            edge_limit=edge_limit,
            node_limit=node_limit,
            dot_file=dot_file,
        )


class JacCmd:
    """Jac CLI command."""

    @staticmethod
    def create_cmd() -> None:
        """Create Jac CLI cmds."""
        return plugin_manager.hook.create_cmd()


class JacFeature(
    JacClassReferences,
    JacAccessValidation,
    JacNode,
    JacEdge,
    JacWalker,
    JacBuiltin,
    JacCmd,
):
    """Jac Feature."""

    @staticmethod
    def setup() -> None:
        """Set Class References."""
        plugin_manager.hook.setup()

    @staticmethod
    def get_context() -> ExecutionContext:
        """Get current execution context."""
        return plugin_manager.hook.get_context()

    @staticmethod
    def get_object(id: str) -> Architype | None:
        """Get object given id."""
        return plugin_manager.hook.get_object(id=id)

    @staticmethod
    def object_ref(obj: Architype) -> str:
        """Get object reference id."""
        return plugin_manager.hook.object_ref(obj=obj)

    @staticmethod
    def make_architype(
        cls: type,
        arch_base: Type[Architype],
        on_entry: list[DSFunc],
        on_exit: list[DSFunc],
    ) -> Type[Architype]:
        """Create a obj architype."""
        return plugin_manager.hook.make_architype(
            cls=cls, on_entry=on_entry, on_exit=on_exit, arch_base=arch_base
        )

    @staticmethod
    def make_obj(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a obj architype."""
        return plugin_manager.hook.make_obj(on_entry=on_entry, on_exit=on_exit)

    @staticmethod
    def make_node(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a node architype."""
        return plugin_manager.hook.make_node(on_entry=on_entry, on_exit=on_exit)

    @staticmethod
    def make_edge(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a edge architype."""
        return plugin_manager.hook.make_edge(on_entry=on_entry, on_exit=on_exit)

    @staticmethod
    def make_walker(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a walker architype."""
        return plugin_manager.hook.make_walker(on_entry=on_entry, on_exit=on_exit)

    @staticmethod
    def impl_patch_filename(
        file_loc: str,
    ) -> Callable[[Callable[P, T]], Callable[P, T]]:
        """Update impl file location."""
        return plugin_manager.hook.impl_patch_filename(file_loc=file_loc)

    @staticmethod
    def jac_import(
        target: str,
        base_path: str,
        absorb: bool = False,
        cachable: bool = True,
        mdl_alias: Optional[str] = None,
        override_name: Optional[str] = None,
        lng: Optional[str] = "jac",
        items: Optional[dict[str, Union[str, Optional[str]]]] = None,
        reload_module: Optional[bool] = False,
    ) -> tuple[types.ModuleType, ...]:
        """Core Import Process."""
        return plugin_manager.hook.jac_import(
            target=target,
            base_path=base_path,
            absorb=absorb,
            cachable=cachable,
            mdl_alias=mdl_alias,
            override_name=override_name,
            lng=lng,
            items=items,
            reload_module=reload_module,
        )

    @staticmethod
    def create_test(test_fun: Callable) -> Callable:
        """Create a test."""
        return plugin_manager.hook.create_test(test_fun=test_fun)

    @staticmethod
    def run_test(
        filepath: str,
        filter: Optional[str] = None,
        xit: bool = False,
        maxfail: Optional[int] = None,
        directory: Optional[str] = None,
        verbose: bool = False,
    ) -> int:
        """Run the test suite in the specified .jac file."""
        return plugin_manager.hook.run_test(
            filepath=filepath,
            filter=filter,
            xit=xit,
            maxfail=maxfail,
            directory=directory,
            verbose=verbose,
        )

    @staticmethod
    def elvis(op1: Optional[T], op2: T) -> T:
        """Jac's elvis operator feature."""
        return plugin_manager.hook.elvis(op1=op1, op2=op2)

    @staticmethod
    def has_instance_default(gen_func: Callable[[], T]) -> T:
        """Jac's has container default feature."""
        return plugin_manager.hook.has_instance_default(gen_func=gen_func)

    @staticmethod
    def report(expr: Any, custom: bool = False) -> None:  # noqa: ANN401
        """Jac's report stmt feature."""
        plugin_manager.hook.report(expr=expr, custom=custom)

    @staticmethod
    def edge_ref(
        node_obj: NodeArchitype | list[NodeArchitype],
        target_obj: Optional[NodeArchitype | list[NodeArchitype]],
        dir: EdgeDir,
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
        edges_only: bool = False,
    ) -> list[NodeArchitype] | list[EdgeArchitype]:
        """Jac's apply_dir stmt feature."""
        return plugin_manager.hook.edge_ref(
            node_obj=node_obj,
            target_obj=target_obj,
            dir=dir,
            filter_func=filter_func,
            edges_only=edges_only,
        )

    @staticmethod
    def connect(
        left: NodeArchitype | list[NodeArchitype],
        right: NodeArchitype | list[NodeArchitype],
        edge_spec: Callable[[NodeAnchor, NodeAnchor], EdgeArchitype],
        edges_only: bool = False,
    ) -> list[NodeArchitype] | list[EdgeArchitype]:
        """Jac's connect operator feature.

        Note: connect needs to call assign compr with tuple in op
        """
        return plugin_manager.hook.connect(
            left=left, right=right, edge_spec=edge_spec, edges_only=edges_only
        )

    @staticmethod
    def disconnect(
        left: NodeArchitype | list[NodeArchitype],
        right: NodeArchitype | list[NodeArchitype],
        dir: EdgeDir,
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
    ) -> bool:
        """Jac's disconnect operator feature."""
        return plugin_manager.hook.disconnect(
            left=left,
            right=right,
            dir=dir,
            filter_func=filter_func,
        )

    @staticmethod
    def assign_compr(
        target: list[T], attr_val: tuple[tuple[str], tuple[Any]]
    ) -> list[T]:
        """Jac's assign comprehension feature."""
        return plugin_manager.hook.assign_compr(target=target, attr_val=attr_val)

    @staticmethod
    def get_root() -> Root:
        """Jac's root getter."""
        return plugin_manager.hook.get_root()

    @staticmethod
    def get_root_type() -> Type[Root]:
        """Jac's root type getter."""
        return plugin_manager.hook.get_root_type()

    @staticmethod
    def build_edge(
        is_undirected: bool,
        conn_type: Optional[Type[EdgeArchitype] | EdgeArchitype],
        conn_assign: Optional[tuple[tuple, tuple]],
    ) -> Callable[[NodeAnchor, NodeAnchor], EdgeArchitype]:
        """Jac's root getter."""
        return plugin_manager.hook.build_edge(
            is_undirected=is_undirected, conn_type=conn_type, conn_assign=conn_assign
        )

    @staticmethod
    def save(
        obj: Architype | Anchor,
    ) -> None:
        """Destroy object."""
        plugin_manager.hook.save(obj=obj)

    @staticmethod
    def destroy(
        obj: Architype | Anchor,
    ) -> None:
        """Destroy object."""
        plugin_manager.hook.destroy(obj=obj)

    @staticmethod
    def get_semstr_type(
        file_loc: str, scope: str, attr: str, return_semstr: bool
    ) -> Optional[str]:
        """Jac's get_semstr_type feature."""
        return plugin_manager.hook.get_semstr_type(
            file_loc=file_loc, scope=scope, attr=attr, return_semstr=return_semstr
        )

    @staticmethod
    def obj_scope(file_loc: str, attr: str) -> str:
        """Jac's get_semstr_type feature."""
        return plugin_manager.hook.obj_scope(file_loc=file_loc, attr=attr)

    @staticmethod
    def get_sem_type(file_loc: str, attr: str) -> tuple[str | None, str | None]:
        """Jac's get_semstr_type feature."""
        return plugin_manager.hook.get_sem_type(file_loc=file_loc, attr=attr)

    @staticmethod
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
        """Jac's with_llm feature."""
        return plugin_manager.hook.with_llm(
            file_loc=file_loc,
            model=model,
            model_params=model_params,
            scope=scope,
            incl_info=incl_info,
            excl_info=excl_info,
            inputs=inputs,
            outputs=outputs,
            action=action,
            _globals=_globals,
            _locals=_locals,
        )

    @staticmethod
    def gen_llm_body(_pass: PyastGenPass, node: ast.Ability) -> list[ast3.AST]:
        """Generate the by LLM body."""
        return plugin_manager.hook.gen_llm_body(_pass=_pass, node=node)

    @staticmethod
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
        return plugin_manager.hook.by_llm_call(
            _pass=_pass,
            model=model,
            model_params=model_params,
            scope=scope,
            inputs=inputs,
            outputs=outputs,
            action=action,
            include_info=include_info,
            exclude_info=exclude_info,
        )

    @staticmethod
    def get_by_llm_call_args(_pass: PyastGenPass, node: ast.FuncCall) -> dict:
        """Get the by LLM call args."""
        return plugin_manager.hook.get_by_llm_call_args(_pass=_pass, node=node)
