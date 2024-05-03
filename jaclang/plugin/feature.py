"""Jac Language Features."""

from __future__ import annotations

import types
from typing import Any, Callable, Optional, Type, TypeAlias, Union

from jaclang.compiler.absyntree import Module
from jaclang.core.construct import (
    Architype,
    EdgeArchitype,
    NodeArchitype,
    Root,
    WalkerArchitype,
)
from jaclang.plugin.spec import JacBuiltin, JacCmdSpec, JacFeatureSpec, T


import pluggy

pm = pluggy.PluginManager("jac")
pm.add_hookspecs(JacFeatureSpec)
pm.add_hookspecs(JacCmdSpec)
pm.add_hookspecs(JacBuiltin)


class JacFeature:
    """Jac Feature."""

    import abc
    from jaclang.plugin.spec import DSFunc
    from jaclang.compiler.constant import EdgeDir

    RootType: TypeAlias = Root

    @staticmethod
    def make_architype(
        cls: type,
        arch_base: Type[Architype],
        on_entry: list[DSFunc],
        on_exit: list[DSFunc],
    ) -> Type[Architype]:
        """Create a obj architype."""
        return pm.hook.make_architype(
            cls=cls, on_entry=on_entry, on_exit=on_exit, arch_base=arch_base
        )

    @staticmethod
    def make_obj(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a obj architype."""
        return pm.hook.make_obj(on_entry=on_entry, on_exit=on_exit)

    @staticmethod
    def make_node(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a node architype."""
        return pm.hook.make_node(on_entry=on_entry, on_exit=on_exit)

    @staticmethod
    def make_edge(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a edge architype."""
        return pm.hook.make_edge(on_entry=on_entry, on_exit=on_exit)

    @staticmethod
    def make_walker(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a walker architype."""
        return pm.hook.make_walker(on_entry=on_entry, on_exit=on_exit)

    @staticmethod
    def jac_import(
        target: str,
        base_path: str,
        absorb: bool = False,
        cachable: bool = True,
        mdl_alias: Optional[str] = None,
        override_name: Optional[str] = None,
        mod_bundle: Optional[Module] = None,
        lng: Optional[str] = None,
        items: Optional[dict[str, Union[str, bool]]] = None,
    ) -> Optional[types.ModuleType]:
        """Core Import Process."""
        return pm.hook.jac_import(
            target=target,
            base_path=base_path,
            absorb=absorb,
            cachable=cachable,
            mdl_alias=mdl_alias,
            override_name=override_name,
            mod_bundle=mod_bundle,
            lng=lng,
            items=items,
        )

    @staticmethod
    def create_test(test_fun: Callable) -> Callable:
        """Create a test."""
        return pm.hook.create_test(test_fun=test_fun)

    @staticmethod
    def run_test(
        filepath: str,
        filter: Optional[str] = None,
        xit: bool = False,
        maxfail: Optional[int] = None,
        directory: Optional[str] = None,
        verbose: bool = False,
    ) -> bool:
        """Run the test suite in the specified .jac file."""
        return pm.hook.run_test(
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
        return pm.hook.elvis(op1=op1, op2=op2)

    @staticmethod
    def has_instance_default(gen_func: Callable[[], T]) -> T:
        """Jac's has container default feature."""
        return pm.hook.has_instance_default(gen_func=gen_func)

    @staticmethod
    def spawn_call(op1: Architype, op2: Architype) -> WalkerArchitype:
        """Jac's spawn operator feature."""
        return pm.hook.spawn_call(op1=op1, op2=op2)

    @staticmethod
    def report(expr: Any) -> Any:  # noqa: ANN401
        """Jac's report stmt feature."""
        return pm.hook.report(expr=expr)

    @staticmethod
    def ignore(
        walker: WalkerArchitype,
        expr: list[NodeArchitype | EdgeArchitype] | NodeArchitype | EdgeArchitype,
    ) -> bool:  # noqa: ANN401
        """Jac's ignore stmt feature."""
        return pm.hook.ignore(walker=walker, expr=expr)

    @staticmethod
    def visit_node(
        walker: WalkerArchitype,
        expr: list[NodeArchitype | EdgeArchitype] | NodeArchitype | EdgeArchitype,
    ) -> bool:  # noqa: ANN401
        """Jac's visit stmt feature."""
        return pm.hook.visit_node(walker=walker, expr=expr)

    @staticmethod
    def disengage(walker: WalkerArchitype) -> bool:  # noqa: ANN401
        """Jac's disengage stmt feature."""
        return pm.hook.disengage(walker=walker)

    @staticmethod
    def edge_ref(
        node_obj: NodeArchitype | list[NodeArchitype],
        target_obj: Optional[NodeArchitype | list[NodeArchitype]],
        dir: EdgeDir,
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
        edges_only: bool = False,
    ) -> list[NodeArchitype] | list[EdgeArchitype]:
        """Jac's apply_dir stmt feature."""
        return pm.hook.edge_ref(
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
        edge_spec: Callable[[], EdgeArchitype],
        edges_only: bool = False,
    ) -> list[NodeArchitype] | list[EdgeArchitype]:
        """Jac's connect operator feature.

        Note: connect needs to call assign compr with tuple in op
        """
        return pm.hook.connect(
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
        return pm.hook.disconnect(
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
        return pm.hook.assign_compr(target=target, attr_val=attr_val)

    @staticmethod
    def get_root() -> Architype:
        """Jac's assign comprehension feature."""
        return pm.hook.get_root()

    @staticmethod
    def build_edge(
        is_undirected: bool,
        conn_type: Optional[Type[EdgeArchitype]],
        conn_assign: Optional[tuple[tuple, tuple]],
    ) -> Callable[[], EdgeArchitype]:
        """Jac's root getter."""
        return pm.hook.build_edge(
            is_undirected=is_undirected, conn_type=conn_type, conn_assign=conn_assign
        )

    @staticmethod
    def get_semstr_type(
        file_loc: str, scope: str, attr: str, return_semstr: bool
    ) -> Optional[str]:
        """Jac's get_semstr_type feature."""
        return pm.hook.get_semstr_type(
            file_loc=file_loc, scope=scope, attr=attr, return_semstr=return_semstr
        )

    @staticmethod
    def obj_scope(file_loc: str, attr: str) -> str:
        """Jac's get_semstr_type feature."""
        return pm.hook.obj_scope(file_loc=file_loc, attr=attr)

    @staticmethod
    def get_sem_type(file_loc: str, attr: str) -> tuple[str | None, str | None]:
        """Jac's get_semstr_type feature."""
        return pm.hook.get_sem_type(file_loc=file_loc, attr=attr)

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
    ) -> Any:  # noqa: ANN401
        """Jac's with_llm feature."""
        return pm.hook.with_llm(
            file_loc=file_loc,
            model=model,
            model_params=model_params,
            scope=scope,
            incl_info=incl_info,
            excl_info=excl_info,
            inputs=inputs,
            outputs=outputs,
            action=action,
        )


class JacCmd:
    """Jac CLI command."""

    @staticmethod
    def create_cmd() -> None:
        """Create Jac CLI cmds."""
        return pm.hook.create_cmd()
