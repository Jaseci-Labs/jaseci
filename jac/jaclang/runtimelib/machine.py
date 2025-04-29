"""Jac Language Features."""

from __future__ import annotations

import ast as ast3
import copy
import fnmatch
import html
import inspect
import os
import sys
import tempfile
import types
from collections import OrderedDict
from dataclasses import dataclass, field
from functools import wraps
from inspect import getfile
from logging import getLogger
from typing import (
    Any,
    Callable,
    Mapping,
    Optional,
    ParamSpec,
    Sequence,
    TYPE_CHECKING,
    Type,
    TypeAlias,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID

from jaclang.compiler import unitree as ast
from jaclang.compiler.constant import EdgeDir, colors
from jaclang.compiler.passes.main.pyast_gen_pass import PyastGenPass
from jaclang.compiler.program import JacProgram
from jaclang.runtimelib.architype import (
    DataSpatialFunction,
    GenericEdge as _GenericEdge,
    Root as _Root,
)
from jaclang.runtimelib.constructs import (
    AccessLevel,
    Anchor,
    Architype,
    EdgeAnchor,
    EdgeArchitype,
    GenericEdge,
    JacTestCheck,
    NodeAnchor,
    NodeArchitype,
    Root,
    WalkerArchitype,
)
from jaclang.runtimelib.jacgo import jacroutine
from jaclang.runtimelib.machinestate import ExecutionContext, JacMachineState
from jaclang.runtimelib.memory import Shelf, ShelfStorage
from jaclang.runtimelib.utils import (
    all_issubclass,
    collect_node_connections,
    traverse_graph,
)

import pluggy


plugin_manager = pluggy.PluginManager("jac")
hookspec = pluggy.HookspecMarker("jac")
hookimpl = pluggy.HookimplMarker("jac")
logger = getLogger(__name__)

T = TypeVar("T")
P = ParamSpec("P")


class JacAccessValidation:
    """Jac Access Validation Specs."""

    @staticmethod
    def elevate_root() -> None:
        """Elevate context root to system_root."""
        jctx = JacMachine.get_context()
        jctx.root = jctx.system_root

    @staticmethod
    def allow_root(
        architype: Architype,
        root_id: UUID,
        level: AccessLevel | int | str = AccessLevel.READ,
    ) -> None:
        """Allow all access from target root graph to current Architype."""
        level = AccessLevel.cast(level)
        access = architype.__jac__.access.roots

        _root_id = str(root_id)
        if level != access.anchors.get(_root_id, AccessLevel.NO_ACCESS):
            access.anchors[_root_id] = level

    @staticmethod
    def disallow_root(
        architype: Architype,
        root_id: UUID,
        level: AccessLevel | int | str = AccessLevel.READ,
    ) -> None:
        """Disallow all access from target root graph to current Architype."""
        level = AccessLevel.cast(level)
        access = architype.__jac__.access.roots

        access.anchors.pop(str(root_id), None)

    @staticmethod
    def unrestrict(
        architype: Architype, level: AccessLevel | int | str = AccessLevel.READ
    ) -> None:
        """Allow everyone to access current Architype."""
        anchor = architype.__jac__
        level = AccessLevel.cast(level)
        if level != anchor.access.all:
            anchor.access.all = level

    @staticmethod
    def restrict(architype: Architype) -> None:
        """Disallow others to access current Architype."""
        anchor = architype.__jac__
        if anchor.access.all > AccessLevel.NO_ACCESS:
            anchor.access.all = AccessLevel.NO_ACCESS

    @staticmethod
    def check_read_access(to: Anchor) -> bool:
        """Read Access Validation."""
        if not (
            access_level := JacMachine.check_access_level(to) > AccessLevel.NO_ACCESS
        ):
            logger.info(
                f"Current root doesn't have read access to {to.__class__.__name__}[{to.id}]"
            )
        return access_level

    @staticmethod
    def check_connect_access(to: Anchor) -> bool:
        """Write Access Validation."""
        if not (access_level := JacMachine.check_access_level(to) > AccessLevel.READ):
            logger.info(
                f"Current root doesn't have connect access to {to.__class__.__name__}[{to.id}]"
            )
        return access_level

    @staticmethod
    def check_write_access(to: Anchor) -> bool:
        """Write Access Validation."""
        if not (
            access_level := JacMachine.check_access_level(to) > AccessLevel.CONNECT
        ):
            logger.info(
                f"Current root doesn't have write access to {to.__class__.__name__}[{to.id}]"
            )
        return access_level

    @staticmethod
    def check_access_level(to: Anchor) -> AccessLevel:
        """Access validation."""
        if not to.persistent:
            return AccessLevel.WRITE

        jctx = JacMachine.get_context()

        jroot = jctx.root

        # if current root is system_root
        # if current root id is equal to target anchor's root id
        # if current root is the target anchor
        if jroot == jctx.system_root or jroot.id == to.root or jroot == to:
            return AccessLevel.WRITE

        access_level = AccessLevel.NO_ACCESS

        # if target anchor have set access.all
        if (to_access := to.access).all > AccessLevel.NO_ACCESS:
            access_level = to_access.all

        # if target anchor's root have set allowed roots
        # if current root is allowed to the whole graph of target anchor's root
        if to.root and isinstance(to_root := jctx.mem.find_one(to.root), Anchor):
            if to_root.access.all > access_level:
                access_level = to_root.access.all

            if (level := to_root.access.roots.check(str(jroot.id))) is not None:
                access_level = level

        # if target anchor have set allowed roots
        # if current root is allowed to target anchor
        if (level := to_access.roots.check(str(jroot.id))) is not None:
            access_level = level

        return access_level


class JacNode:
    """Jac Node Operations."""

    @staticmethod
    def node_dot(node: NodeArchitype, dot_file: Optional[str] = None) -> str:
        """Generate Dot file for visualizing nodes and edges."""
        visited_nodes: set[NodeAnchor] = set()
        connections: set[tuple[NodeArchitype, NodeArchitype, str]] = set()
        unique_node_id_dict = {}

        collect_node_connections(node.__jac__, visited_nodes, connections)
        dot_content = 'digraph {\nnode [style="filled", shape="ellipse", fillcolor="invis", fontcolor="black"];\n'
        for idx, i in enumerate([nodes_.architype for nodes_ in visited_nodes]):
            unique_node_id_dict[i] = (i.__class__.__name__, str(idx))
            dot_content += f'{idx} [label="{i}"];\n'
        dot_content += 'edge [color="gray", style="solid"];\n'

        for pair in list(set(connections)):
            dot_content += (
                f"{unique_node_id_dict[pair[0]][1]} -> {unique_node_id_dict[pair[1]][1]}"
                f' [label="{pair[2]}"];\n'
            )
        if dot_file:
            with open(dot_file, "w") as f:
                f.write(dot_content + "}")
        return dot_content + "}"

    @staticmethod
    def get_edges(
        node: NodeAnchor,
        dir: EdgeDir,
        filter: Callable[[EdgeArchitype], bool] | None,
        target_obj: list[NodeArchitype] | None,
    ) -> list[EdgeArchitype]:
        """Get edges connected to this node."""
        ret_edges: list[EdgeArchitype] = []
        for anchor in node.edges:
            if (
                (source := anchor.source)
                and (target := anchor.target)
                and (not filter or filter(anchor.architype))
                and source.architype
                and target.architype
            ):
                if (
                    dir in [EdgeDir.OUT, EdgeDir.ANY]
                    and node == source
                    and (not target_obj or target.architype in target_obj)
                    and JacMachine.check_read_access(target)
                ):
                    ret_edges.append(anchor.architype)
                if (
                    dir in [EdgeDir.IN, EdgeDir.ANY]
                    and node == target
                    and (not target_obj or source.architype in target_obj)
                    and JacMachine.check_read_access(source)
                ):
                    ret_edges.append(anchor.architype)
        return ret_edges

    @staticmethod
    def edges_to_nodes(
        node: NodeAnchor,
        dir: EdgeDir,
        filter: Callable[[EdgeArchitype], bool] | None,
        target_obj: list[NodeArchitype] | None,
    ) -> list[NodeArchitype]:
        """Get set of nodes connected to this node."""
        ret_edges: list[NodeArchitype] = []
        for anchor in node.edges:
            if (
                (source := anchor.source)
                and (target := anchor.target)
                and (not filter or filter(anchor.architype))
                and source.architype
                and target.architype
            ):
                if (
                    dir in [EdgeDir.OUT, EdgeDir.ANY]
                    and node == source
                    and (not target_obj or target.architype in target_obj)
                    and JacMachine.check_read_access(target)
                ):
                    ret_edges.append(target.architype)
                if (
                    dir in [EdgeDir.IN, EdgeDir.ANY]
                    and node == target
                    and (not target_obj or source.architype in target_obj)
                    and JacMachine.check_read_access(source)
                ):
                    ret_edges.append(source.architype)
        return ret_edges

    @staticmethod
    def remove_edge(node: NodeAnchor, edge: EdgeAnchor) -> None:
        """Remove reference without checking sync status."""
        for idx, ed in enumerate(node.edges):
            if ed.id == edge.id:
                node.edges.pop(idx)
                break


class JacEdge:
    """Jac Edge Operations."""

    @staticmethod
    def detach(edge: EdgeAnchor) -> None:
        """Detach edge from nodes."""
        JacMachine.remove_edge(node=edge.source, edge=edge)
        JacMachine.remove_edge(node=edge.target, edge=edge)


class JacWalker:
    """Jac Edge Operations."""

    @staticmethod
    def visit(
        walker: WalkerArchitype,
        expr: (
            list[NodeArchitype | EdgeArchitype]
            | list[NodeArchitype]
            | list[EdgeArchitype]
            | NodeArchitype
            | EdgeArchitype
        ),
        is_jacgo: bool = False,
    ) -> bool:  # noqa: ANN401
        """Jac's visit stmt feature."""
        nodes = []
        if isinstance(walker, WalkerArchitype):
            """Walker visits node."""
            wanch = walker.__jac__
            before_len = len(wanch.next)
            for anchor in (
                (i.__jac__ for i in expr) if isinstance(expr, list) else [expr.__jac__]
            ):
                if anchor not in wanch.ignores:
                    if isinstance(anchor, NodeAnchor):
                        nodes.append(anchor)
                    elif isinstance(anchor, EdgeAnchor):
                        if target := anchor.target:
                            nodes.append(target)
                        else:
                            raise ValueError("Edge has no target.")
            if nodes and is_jacgo:
                wanch.next.append(nodes)  # type: ignore
            elif nodes:
                wanch.next.extend(nodes)
            return len(wanch.next) > before_len
        else:
            raise TypeError("Invalid walker object")

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
        if isinstance(walker, WalkerArchitype):
            wanch = walker.__jac__
            before_len = len(wanch.ignores)
            for anchor in (
                (i.__jac__ for i in expr) if isinstance(expr, list) else [expr.__jac__]
            ):
                if anchor not in wanch.ignores:
                    if isinstance(anchor, NodeAnchor):
                        wanch.ignores.append(anchor)
                    elif isinstance(anchor, EdgeAnchor):
                        if target := anchor.target:
                            wanch.ignores.append(target)
                        else:
                            raise ValueError("Edge has no target.")
            return len(wanch.ignores) > before_len
        else:
            raise TypeError("Invalid walker object")

    @staticmethod
    def spawn(op1: Architype, op2: Architype) -> WalkerArchitype:
        """Jac's spawn operator feature."""
        if isinstance(op1, WalkerArchitype):
            warch = op1
            walker = op1.__jac__
            if isinstance(op2, NodeArchitype):
                node = op2.__jac__
            elif isinstance(op2, EdgeArchitype):
                node = op2.__jac__.target
            else:
                raise TypeError("Invalid target object")
        elif isinstance(op2, WalkerArchitype):
            warch = op2
            walker = op2.__jac__
            if isinstance(op1, NodeArchitype):
                node = op1.__jac__
            elif isinstance(op1, EdgeArchitype):
                node = op1.__jac__.target
            else:
                raise TypeError("Invalid target object")
        else:
            raise TypeError("Invalid walker object")

        walker.path = []
        walker.next = [node]
        current_node = node.architype

        # walker entry
        for i in warch._jac_entry_funcs_:
            if not i.trigger:
                i.func(warch, current_node)
            if walker.disengaged:
                return warch

        while len(walker.next):

            def run_spawn(
                current_node: NodeArchitype,
                warch: WalkerArchitype,
            ) -> WalkerArchitype:
                # walker entry with
                for i in warch._jac_entry_funcs_:
                    if (
                        i.trigger
                        and all_issubclass(i.trigger, NodeArchitype)
                        and isinstance(current_node, i.trigger)
                    ):
                        i.func(warch, current_node)
                    if walker.disengaged:
                        return warch

                # node entry
                for i in current_node._jac_entry_funcs_:
                    if not i.trigger:
                        i.func(current_node, warch)
                    if walker.disengaged:
                        return warch

                # node entry with
                for i in current_node._jac_entry_funcs_:
                    if (
                        i.trigger
                        and all_issubclass(i.trigger, WalkerArchitype)
                        and isinstance(warch, i.trigger)
                    ):
                        i.func(current_node, warch)
                    if walker.disengaged:
                        return warch

                # node exit with
                for i in current_node._jac_exit_funcs_:
                    if (
                        i.trigger
                        and all_issubclass(i.trigger, WalkerArchitype)
                        and isinstance(warch, i.trigger)
                    ):
                        i.func(current_node, warch)
                    if walker.disengaged:
                        return warch

                # node exit
                for i in current_node._jac_exit_funcs_:
                    if not i.trigger:
                        i.func(current_node, warch)
                    if walker.disengaged:
                        return warch

                # walker exit with
                for i in warch._jac_exit_funcs_:
                    if (
                        i.trigger
                        and all_issubclass(i.trigger, NodeArchitype)
                        and isinstance(current_node, i.trigger)
                    ):
                        i.func(warch, current_node)
                    if walker.disengaged:
                        return warch

                return warch

            current = walker.next.pop(0)
            if isinstance(current, list):
                for i in current:
                    jacroutine(func=run_spawn, args=(i.architype, copy.copy(warch)))
            else:
                run_spawn(current.architype, warch)
        # walker exit
        for i in warch._jac_exit_funcs_:
            if not i.trigger:
                i.func(warch, current_node)
            if walker.disengaged:
                return warch

        walker.ignores = []
        return warch

    @staticmethod
    def disengage(walker: WalkerArchitype) -> bool:
        """Jac's disengage stmt feature."""
        walker.__jac__.disengaged = True
        return True


class JacClassReferences:
    """Default Classes References."""

    TYPE_CHECKING: bool = TYPE_CHECKING
    EdgeDir: TypeAlias = EdgeDir
    DSFunc: TypeAlias = DataSpatialFunction

    Obj: TypeAlias = Architype
    Node: TypeAlias = NodeArchitype
    Edge: TypeAlias = EdgeArchitype
    Walker: TypeAlias = WalkerArchitype

    Root: TypeAlias = _Root
    GenericEdge: TypeAlias = _GenericEdge


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
        edge_type = edge_type if edge_type else []
        visited_nodes: list[NodeArchitype] = []
        node_depths: dict[NodeArchitype, int] = {node: 0}
        queue: list = [[node, 0]]
        connections: list[tuple[NodeArchitype, NodeArchitype, EdgeArchitype]] = []

        def dfs(node: NodeArchitype, cur_depth: int) -> None:
            """Depth first search."""
            if node not in visited_nodes:
                visited_nodes.append(node)
                traverse_graph(
                    node,
                    cur_depth,
                    depth,
                    edge_type,
                    traverse,
                    connections,
                    node_depths,
                    visited_nodes,
                    queue,
                    bfs,
                    dfs,
                    node_limit,
                    edge_limit,
                )

        if bfs:
            cur_depth = 0
            while queue:
                current_node, cur_depth = queue.pop(0)
                if current_node not in visited_nodes:
                    visited_nodes.append(current_node)
                    traverse_graph(
                        current_node,
                        cur_depth,
                        depth,
                        edge_type,
                        traverse,
                        connections,
                        node_depths,
                        visited_nodes,
                        queue,
                        bfs,
                        dfs,
                        node_limit,
                        edge_limit,
                    )
        else:
            dfs(node, cur_depth=0)
        dot_content = (
            'digraph {\nnode [style="filled", shape="ellipse", '
            'fillcolor="invis", fontcolor="black"];\n'
        )
        for source, target, edge in connections:
            edge_label = html.escape(str(edge.__jac__.architype))
            dot_content += (
                f"{visited_nodes.index(source)} -> {visited_nodes.index(target)} "
                f' [label="{edge_label if "GenericEdge" not in edge_label else ""}"];\n'
            )
        for node_ in visited_nodes:
            color = (
                colors[node_depths[node_]] if node_depths[node_] < 25 else colors[24]
            )
            dot_content += (
                f'{visited_nodes.index(node_)} [label="{html.escape(str(node_.__jac__.architype))}"'
                f'fillcolor="{color}"];\n'
            )
        if dot_file:
            with open(dot_file, "w") as f:
                f.write(dot_content + "}")
        return dot_content + "}"


class JacCmd:
    """Jac CLI command."""

    @staticmethod
    def create_cmd() -> None:
        """Create Jac CLI cmds."""


class JacBasics:
    """Jac Feature."""

    @staticmethod
    def setup() -> None:
        """Set Class References."""

    @staticmethod
    def get_context() -> ExecutionContext:
        """Get current execution context."""
        return JacMachine.py_get_jac_machine().exec_ctx

    @staticmethod
    def reset_graph(root: Optional[Root] = None) -> int:
        """Purge current or target graph."""
        ctx = JacMachine.get_context()
        mem = cast(ShelfStorage, ctx.mem)
        ranchor = root.__jac__ if root else ctx.root

        deleted_count = 0
        for anchor in (
            anchors.values()
            if isinstance(anchors := mem.__shelf__, Shelf)
            else mem.__mem__.values()
        ):
            if anchor == ranchor or anchor.root != ranchor.id:
                continue

            if loaded_anchor := mem.find_by_id(anchor.id):
                deleted_count += 1
                JacMachine.destroy(loaded_anchor)

        return deleted_count

    @staticmethod
    def get_object(id: str) -> Architype | None:
        """Get object given id."""
        if id == "root":
            return JacMachine.get_context().root.architype
        elif obj := JacMachine.get_context().mem.find_by_id(UUID(id)):
            return obj.architype

        return None

    @staticmethod
    def object_ref(obj: Architype) -> str:
        """Get object reference id."""
        return obj.__jac__.id.hex

    @staticmethod
    def make_architype(cls: Type[Architype]) -> Type[Architype]:
        """Create a obj architype."""
        entries: OrderedDict[str, JacMachine.DSFunc] = OrderedDict(
            (fn.name, fn) for fn in cls._jac_entry_funcs_
        )
        exits: OrderedDict[str, JacMachine.DSFunc] = OrderedDict(
            (fn.name, fn) for fn in cls._jac_exit_funcs_
        )
        for func in cls.__dict__.values():
            if callable(func):
                if hasattr(func, "__jac_entry"):
                    entries[func.__name__] = JacMachine.DSFunc(func.__name__, func)
                if hasattr(func, "__jac_exit"):
                    exits[func.__name__] = JacMachine.DSFunc(func.__name__, func)

        cls._jac_entry_funcs_ = [*entries.values()]
        cls._jac_exit_funcs_ = [*exits.values()]

        dataclass(eq=False)(cls)
        return cls

    @staticmethod
    def impl_patch_filename(
        file_loc: str,
    ) -> Callable[[Callable[P, T]], Callable[P, T]]:
        """Update impl file location."""

        def decorator(func: Callable[P, T]) -> Callable[P, T]:
            try:
                code = func.__code__
                new_code = types.CodeType(
                    code.co_argcount,
                    code.co_posonlyargcount,
                    code.co_kwonlyargcount,
                    code.co_nlocals,
                    code.co_stacksize,
                    code.co_flags,
                    code.co_code,
                    code.co_consts,
                    code.co_names,
                    code.co_varnames,
                    file_loc,
                    code.co_name,
                    code.co_qualname,
                    code.co_firstlineno,
                    code.co_linetable,
                    code.co_exceptiontable,
                    code.co_freevars,
                    code.co_cellvars,
                )
                func.__code__ = new_code
            except AttributeError:
                pass
            return func

        return decorator

    @staticmethod
    def py_get_jac_machine() -> JacMachineState:
        """Get jac machine from python context."""
        machine = None
        for i in inspect.stack():
            machine = i.frame.f_globals.get("__jac_mach__") or i.frame.f_locals.get(
                "__jac_mach__"
            )
            if machine:
                break
        if not machine:
            raise RuntimeError("Jac machine not found in python context. ")
        return machine

    @staticmethod
    def py_jac_import(
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
        machine = JacMachine.py_get_jac_machine()
        if not machine:
            machine = JacMachineState(base_path=base_path)
        return JacMachine.jac_import(
            mach=machine,
            target=target,
            base_path=base_path,
            absorb=absorb,
            mdl_alias=mdl_alias,
            override_name=override_name,
            lng=lng,
            items=items,
            reload_module=reload_module,
        )

    @staticmethod
    def jac_import(
        mach: JacMachineState,
        target: str,
        base_path: str,
        absorb: bool = False,
        mdl_alias: Optional[str] = None,
        override_name: Optional[str] = None,
        lng: Optional[str] = "jac",
        items: Optional[dict[str, Union[str, Optional[str]]]] = None,
        reload_module: Optional[bool] = False,
    ) -> tuple[types.ModuleType, ...]:
        """Core Import Process."""
        from jaclang.runtimelib.importer import (
            ImportPathSpec,
            JacImporter,
            PythonImporter,
        )

        spec = ImportPathSpec(
            target,
            base_path,
            absorb,
            mdl_alias,
            override_name,
            lng,
            items,
        )

        if not mach.jac_program:
            JacMachine.attach_program(mach, JacProgram())

        if lng == "py":
            import_result = PythonImporter(mach).run_import(spec)
        else:
            import_result = JacImporter(mach).run_import(spec, reload_module)

        return (
            (import_result.ret_mod,)
            if absorb or not items
            else tuple(import_result.ret_items)
        )

    @staticmethod
    def jac_test(test_fun: Callable) -> Callable:
        """Create a test."""
        file_path = getfile(test_fun)
        func_name = test_fun.__name__

        def test_deco() -> None:
            test_fun(JacTestCheck())

        test_deco.__name__ = test_fun.__name__
        JacTestCheck.add_test(file_path, func_name, test_deco)

        return test_deco

    @staticmethod
    def run_test(
        mach: JacMachineState,
        filepath: str,
        func_name: Optional[str] = None,
        filter: Optional[str] = None,
        xit: bool = False,
        maxfail: Optional[int] = None,
        directory: Optional[str] = None,
        verbose: bool = False,
    ) -> int:
        """Run the test suite in the specified .jac file."""
        test_file = False
        ret_count = 0
        if filepath:
            if filepath.endswith(".jac"):
                base, mod_name = os.path.split(filepath)
                base = base if base else "./"
                mod_name = mod_name[:-4]
                if mod_name.endswith(".test"):
                    mod_name = mod_name[:-5]
                JacTestCheck.reset()
                JacMachine.jac_import(mach=mach, target=mod_name, base_path=base)
                JacTestCheck.run_test(
                    xit, maxfail, verbose, os.path.abspath(filepath), func_name
                )
                ret_count = JacTestCheck.failcount
            else:
                print("Not a .jac file.")
        else:
            directory = directory if directory else os.getcwd()

        if filter or directory:
            current_dir = directory if directory else os.getcwd()
            for root_dir, _, files in os.walk(current_dir, topdown=True):
                files = (
                    [file for file in files if fnmatch.fnmatch(file, filter)]
                    if filter
                    else files
                )
                files = [
                    file
                    for file in files
                    if not file.endswith((".test.jac", ".impl.jac"))
                ]
                for file in files:
                    if file.endswith(".jac"):
                        test_file = True
                        print(f"\n\n\t\t* Inside {root_dir}" + "/" + f"{file} *")
                        JacTestCheck.reset()
                        JacMachine.jac_import(
                            mach=mach, target=file[:-4], base_path=root_dir
                        )
                        JacTestCheck.run_test(
                            xit, maxfail, verbose, os.path.abspath(file), func_name
                        )

                    if JacTestCheck.breaker and (xit or maxfail):
                        break
                if JacTestCheck.breaker and (xit or maxfail):
                    break
            JacTestCheck.breaker = False
            ret_count += JacTestCheck.failcount
            JacTestCheck.failcount = 0
            print("No test files found.") if not test_file else None

        return ret_count

    @staticmethod
    def field(factory: Callable[[], T] | None = None, init: bool = True) -> T:
        """Jac's field handler."""
        if factory:
            return field(default_factory=factory)
        return field(init=init)

    @staticmethod
    def report(expr: Any, custom: bool = False) -> None:  # noqa: ANN401
        """Jac's report stmt feature."""
        ctx = JacMachine.get_context()
        if custom:
            ctx.custom = expr
        else:
            ctx.reports.append(expr)

    @staticmethod
    def refs(
        sources: NodeArchitype | list[NodeArchitype],
        targets: NodeArchitype | list[NodeArchitype] | None = None,
        dir: EdgeDir = EdgeDir.OUT,
        filter: Callable[[EdgeArchitype], bool] | None = None,
        edges_only: bool = False,
    ) -> list[NodeArchitype] | list[EdgeArchitype]:
        """Jac's apply_dir stmt feature."""
        if isinstance(sources, NodeArchitype):
            sources = [sources]
        targ_obj_set: Optional[list[NodeArchitype]] = (
            [targets]
            if isinstance(targets, NodeArchitype)
            else targets if targets else None
        )
        if edges_only:
            connected_edges: list[EdgeArchitype] = []
            for node in sources:
                edges = JacMachine.get_edges(
                    node.__jac__, dir, filter, target_obj=targ_obj_set
                )
                connected_edges.extend(
                    edge for edge in edges if edge not in connected_edges
                )
            return connected_edges
        else:
            connected_nodes: list[NodeArchitype] = []
            for node in sources:
                nodes = JacMachine.edges_to_nodes(
                    node.__jac__, dir, filter, target_obj=targ_obj_set
                )
                connected_nodes.extend(
                    node for node in nodes if node not in connected_nodes
                )
            return connected_nodes

    @staticmethod
    def filter(
        items: list[Architype],
        func: Callable[[Architype], bool],
    ) -> list[Architype]:
        """Jac's filter architype list."""
        return [item for item in items if func(item)]

    @staticmethod
    def connect(
        left: NodeArchitype | list[NodeArchitype],
        right: NodeArchitype | list[NodeArchitype],
        edge: Type[EdgeArchitype] | EdgeArchitype | None = None,
        undir: bool = False,
        conn_assign: tuple[tuple, tuple] | None = None,
        edges_only: bool = False,
    ) -> list[NodeArchitype] | list[EdgeArchitype]:
        """Jac's connect operator feature."""
        left = [left] if isinstance(left, NodeArchitype) else left
        right = [right] if isinstance(right, NodeArchitype) else right
        edges = []

        for i in left:
            _left = i.__jac__
            if JacMachine.check_connect_access(_left):
                for j in right:
                    _right = j.__jac__
                    if JacMachine.check_connect_access(_right):
                        edges.append(
                            JacMachine.build_edge(
                                is_undirected=undir,
                                conn_type=edge,
                                conn_assign=conn_assign,
                            )(_left, _right)
                        )
        return right if not edges_only else edges

    @staticmethod
    def disconnect(
        left: NodeArchitype | list[NodeArchitype],
        right: NodeArchitype | list[NodeArchitype],
        dir: EdgeDir = EdgeDir.OUT,
        filter: Callable[[EdgeArchitype], bool] | None = None,
    ) -> bool:
        """Jac's disconnect operator feature."""
        disconnect_occurred = False
        left = [left] if isinstance(left, NodeArchitype) else left
        right = [right] if isinstance(right, NodeArchitype) else right

        for i in left:
            node = i.__jac__
            for anchor in set(node.edges):
                if (
                    (source := anchor.source)
                    and (target := anchor.target)
                    and (not filter or filter(anchor.architype))
                    and source.architype
                    and target.architype
                ):
                    if (
                        dir in [EdgeDir.OUT, EdgeDir.ANY]
                        and node == source
                        and target.architype in right
                        and JacMachine.check_connect_access(target)
                    ):
                        (
                            JacMachine.destroy(anchor)
                            if anchor.persistent
                            else JacMachine.detach(anchor)
                        )
                        disconnect_occurred = True
                    if (
                        dir in [EdgeDir.IN, EdgeDir.ANY]
                        and node == target
                        and source.architype in right
                        and JacMachine.check_connect_access(source)
                    ):
                        (
                            JacMachine.destroy(anchor)
                            if anchor.persistent
                            else JacMachine.detach(anchor)
                        )
                        disconnect_occurred = True

        return disconnect_occurred

    @staticmethod
    def assign(target: list[T], attr_val: tuple[tuple[str], tuple[Any]]) -> list[T]:
        """Jac's assign comprehension feature."""
        for obj in target:
            attrs, values = attr_val
            for attr, value in zip(attrs, values):
                setattr(obj, attr, value)
        return target

    @staticmethod
    def root() -> Root:
        """Jac's root getter."""
        return JacMachine.py_get_jac_machine().exec_ctx.get_root()

    @staticmethod
    def build_edge(
        is_undirected: bool,
        conn_type: Optional[Type[EdgeArchitype] | EdgeArchitype],
        conn_assign: Optional[tuple[tuple, tuple]],
    ) -> Callable[[NodeAnchor, NodeAnchor], EdgeArchitype]:
        """Jac's root getter."""
        ct = conn_type if conn_type else GenericEdge

        def builder(source: NodeAnchor, target: NodeAnchor) -> EdgeArchitype:
            edge = ct() if isinstance(ct, type) else ct

            eanch = edge.__jac__ = EdgeAnchor(
                architype=edge,
                source=source,
                target=target,
                is_undirected=is_undirected,
            )
            source.edges.append(eanch)
            target.edges.append(eanch)

            if conn_assign:
                for fld, val in zip(conn_assign[0], conn_assign[1]):
                    if hasattr(edge, fld):
                        setattr(edge, fld, val)
                    else:
                        raise ValueError(f"Invalid attribute: {fld}")
            if source.persistent or target.persistent:
                JacMachine.save(eanch)
            return edge

        return builder

    @staticmethod
    def save(
        obj: Architype | Anchor,
    ) -> None:
        """Destroy object."""
        anchor = obj.__jac__ if isinstance(obj, Architype) else obj

        jctx = JacMachine.get_context()

        anchor.persistent = True
        anchor.root = jctx.root.id

        jctx.mem.set(anchor.id, anchor)

        match anchor:
            case NodeAnchor():
                for ed in anchor.edges:
                    if ed.is_populated() and not ed.persistent:
                        JacMachine.save(ed)
            case EdgeAnchor():
                if (src := anchor.source) and src.is_populated() and not src.persistent:
                    JacMachine.save(src)
                if (trg := anchor.target) and trg.is_populated() and not trg.persistent:
                    JacMachine.save(trg)
            case _:
                pass

    @staticmethod
    def destroy(
        obj: Architype | Anchor,
    ) -> None:
        """Destroy object."""
        anchor = obj.__jac__ if isinstance(obj, Architype) else obj

        if JacMachine.check_write_access(anchor):
            match anchor:
                case NodeAnchor():
                    for edge in anchor.edges:
                        JacMachine.destroy(edge)
                case EdgeAnchor():
                    JacMachine.detach(anchor)
                case _:
                    pass

            JacMachine.get_context().mem.remove(anchor.id)

    @staticmethod
    def entry(func: Callable) -> Callable:
        """Mark a method as jac entry with this decorator."""
        setattr(func, "__jac_entry", None)  # noqa:B010
        return func

    @staticmethod
    def exit(func: Callable) -> Callable:
        """Mark a method as jac exit with this decorator."""
        setattr(func, "__jac_exit", None)  # noqa:B010
        return func

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
        raise ImportError(
            "mtllm is not installed. Please install it with `pip install mtllm` and run `jac clean`."
        )

    @staticmethod
    def gen_llm_body(_pass: PyastGenPass, node: ast.Ability) -> list[ast3.AST]:
        """Generate the by LLM body."""
        _pass.log_warning(
            "MT-LLM is not installed. Please install it with `pip install mtllm`."
        )
        return [
            _pass.sync(
                ast3.Raise(
                    _pass.sync(
                        ast3.Call(
                            func=_pass.sync(
                                ast3.Name(id="ImportError", ctx=ast3.Load())
                            ),
                            args=[
                                _pass.sync(
                                    ast3.Constant(
                                        value="mtllm is not installed. Please install it with `pip install mtllm` and run `jac clean`."  # noqa: E501
                                    )
                                )
                            ],
                            keywords=[],
                        )
                    )
                )
            )
        ]

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
        """Return the LLM Call, e.g. _JacFeature.with_llm()."""
        _pass.log_warning(
            "MT-LLM is not installed. Please install it with `pip install mtllm`."
        )
        return ast3.Call(
            func=_pass.sync(
                ast3.Attribute(
                    value=_pass.sync(ast3.Name(id="_Jac", ctx=ast3.Load())),
                    attr="with_llm",
                    ctx=ast3.Load(),
                )
            ),
            args=[],
            keywords=[
                _pass.sync(
                    ast3.keyword(
                        arg="file_loc",
                        value=_pass.sync(ast3.Constant(value="None")),
                    )
                ),
                _pass.sync(
                    ast3.keyword(
                        arg="model",
                        value=_pass.sync(ast3.Constant(value="None")),
                    )
                ),
                _pass.sync(
                    ast3.keyword(
                        arg="model_params",
                        value=_pass.sync(ast3.Dict(keys=[], values=[])),
                    )
                ),
                _pass.sync(
                    ast3.keyword(
                        arg="scope",
                        value=_pass.sync(ast3.Constant(value="None")),
                    )
                ),
                _pass.sync(
                    ast3.keyword(
                        arg="incl_info",
                        value=_pass.sync(ast3.List(elts=[], ctx=ast3.Load())),
                    )
                ),
                _pass.sync(
                    ast3.keyword(
                        arg="excl_info",
                        value=_pass.sync(ast3.List(elts=[], ctx=ast3.Load())),
                    )
                ),
                _pass.sync(
                    ast3.keyword(
                        arg="inputs",
                        value=_pass.sync(ast3.List(elts=[], ctx=ast3.Load())),
                    )
                ),
                _pass.sync(
                    ast3.keyword(
                        arg="outputs",
                        value=_pass.sync(ast3.List(elts=[], ctx=ast3.Load())),
                    )
                ),
                _pass.sync(
                    ast3.keyword(
                        arg="action",
                        value=_pass.sync(ast3.Constant(value="None")),
                    )
                ),
                _pass.sync(
                    ast3.keyword(
                        arg="_globals",
                        value=_pass.sync(ast3.Constant(value="None")),
                    )
                ),
                _pass.sync(
                    ast3.keyword(
                        arg="_locals",
                        value=_pass.sync(ast3.Constant(value="None")),
                    )
                ),
            ],
        )

    @staticmethod
    def get_by_llm_call_args(_pass: PyastGenPass, node: ast.FuncCall) -> dict:
        """Get the by LLM call args."""
        return {
            "model": None,
            "model_params": {},
            "scope": None,
            "inputs": [],
            "outputs": [],
            "action": None,
            "include_info": [],
            "exclude_info": [],
        }


class JacUtils:
    """Jac Machine Utilities."""

    @staticmethod
    def attach_program(mach: JacMachineState, jac_program: JacProgram) -> None:
        """Attach a JacProgram to the machine."""
        mach.jac_program = jac_program

    @staticmethod
    def load_module(
        mach: JacMachineState, module_name: str, module: types.ModuleType
    ) -> None:
        """Load a module into the machine."""
        mach.loaded_modules[module_name] = module
        sys.modules[module_name] = module  # TODO: May want to nuke this one day

    @staticmethod
    def list_modules(mach: JacMachineState) -> list[str]:
        """List all loaded modules."""
        return list(mach.loaded_modules.keys())

    @staticmethod
    def list_walkers(mach: JacMachineState, module_name: str) -> list[str]:
        """List all walkers in a specific module."""
        module = mach.loaded_modules.get(module_name)
        if module:
            walkers = []
            for name, obj in inspect.getmembers(module):
                if isinstance(obj, type) and issubclass(obj, WalkerArchitype):
                    walkers.append(name)
            return walkers
        return []

    @staticmethod
    def list_nodes(mach: JacMachineState, module_name: str) -> list[str]:
        """List all nodes in a specific module."""
        module = mach.loaded_modules.get(module_name)
        if module:
            nodes = []
            for name, obj in inspect.getmembers(module):
                if isinstance(obj, type) and issubclass(obj, NodeArchitype):
                    nodes.append(name)
            return nodes
        return []

    @staticmethod
    def list_edges(mach: JacMachineState, module_name: str) -> list[str]:
        """List all edges in a specific module."""
        module = mach.loaded_modules.get(module_name)
        if module:
            nodes = []
            for name, obj in inspect.getmembers(module):
                if isinstance(obj, type) and issubclass(obj, EdgeArchitype):
                    nodes.append(name)
            return nodes
        return []

    @staticmethod
    def create_architype_from_source(
        mach: JacMachineState,
        source_code: str,
        module_name: Optional[str] = None,
        base_path: Optional[str] = None,
        cachable: bool = False,
        keep_temporary_files: bool = False,
    ) -> Optional[types.ModuleType]:
        """Dynamically creates architypes (nodes, walkers, etc.) from Jac source code."""
        from jaclang.runtimelib.importer import JacImporter, ImportPathSpec

        if not base_path:
            base_path = mach.base_path or os.getcwd()

        if base_path and not os.path.exists(base_path):
            os.makedirs(base_path)
        if not module_name:
            module_name = f"_dynamic_module_{len(mach.loaded_modules)}"
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".jac",
            prefix=module_name + "_",
            dir=base_path,
            delete=False,
        ) as tmp_file:
            tmp_file_path = tmp_file.name
            tmp_file.write(source_code)

        try:
            importer = JacImporter(mach)
            tmp_file_basename = os.path.basename(tmp_file_path)
            tmp_module_name, _ = os.path.splitext(tmp_file_basename)

            spec = ImportPathSpec(
                target=tmp_module_name,
                base_path=base_path,
                absorb=False,
                mdl_alias=None,
                override_name=module_name,
                lng="jac",
                items=None,
            )

            import_result = importer.run_import(spec, reload=False)
            module = import_result.ret_mod

            mach.loaded_modules[module_name] = module
            return module
        except Exception as e:
            logger.error(f"Error importing dynamic module '{module_name}': {e}")
            return None
        finally:
            if not keep_temporary_files and os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    @staticmethod
    def update_walker(
        mach: JacMachineState,
        module_name: str,
        items: Optional[dict[str, Union[str, Optional[str]]]],
    ) -> tuple[types.ModuleType, ...]:
        """Reimport the module."""
        from .importer import JacImporter, ImportPathSpec

        if module_name in mach.loaded_modules:
            try:
                old_module = mach.loaded_modules[module_name]
                importer = JacImporter(mach)
                spec = ImportPathSpec(
                    target=module_name,
                    base_path=mach.base_path,
                    absorb=False,
                    mdl_alias=None,
                    override_name=None,
                    lng="jac",
                    items=items,
                )
                import_result = importer.run_import(spec, reload=True)
                ret_items = []
                if items:
                    for item_name in items:
                        if hasattr(old_module, item_name):
                            new_attr = getattr(import_result.ret_mod, item_name, None)
                            if new_attr:
                                ret_items.append(new_attr)
                                setattr(
                                    old_module,
                                    item_name,
                                    new_attr,
                                )
                return (old_module,) if not items else tuple(ret_items)
            except Exception as e:
                logger.error(f"Failed to update module {module_name}: {e}")
        else:
            logger.warning(f"Module {module_name} not found in loaded modules.")
        return ()

    @staticmethod
    def spawn_node(
        mach: JacMachineState,
        node_name: str,
        attributes: Optional[dict] = None,
        module_name: str = "__main__",
    ) -> NodeArchitype:
        """Spawn a node instance of the given node_name with attributes."""
        node_class = JacMachine.get_architype(mach, module_name, node_name)
        if isinstance(node_class, type) and issubclass(node_class, NodeArchitype):
            if attributes is None:
                attributes = {}
            node_instance = node_class(**attributes)
            return node_instance
        else:
            raise ValueError(f"Node {node_name} not found.")

    @staticmethod
    def spawn_walker(
        mach: JacMachineState,
        walker_name: str,
        attributes: Optional[dict] = None,
        module_name: str = "__main__",
    ) -> WalkerArchitype:
        """Spawn a walker instance of the given walker_name."""
        walker_class = JacMachine.get_architype(mach, module_name, walker_name)
        if isinstance(walker_class, type) and issubclass(walker_class, WalkerArchitype):
            if attributes is None:
                attributes = {}
            walker_instance = walker_class(**attributes)
            return walker_instance
        else:
            raise ValueError(f"Walker {walker_name} not found.")

    @staticmethod
    def get_architype(
        mach: JacMachineState, module_name: str, architype_name: str
    ) -> Optional[Architype]:
        """Retrieve an architype class from a module."""
        module = mach.loaded_modules.get(module_name)
        if module:
            return getattr(module, architype_name, None)
        return None


class JacMachine(
    JacClassReferences,
    JacAccessValidation,
    JacNode,
    JacEdge,
    JacWalker,
    JacBuiltin,
    JacCmd,
    JacBasics,
    JacUtils,
):
    """Jac Feature."""


def generate_plugin_helpers(
    plugin_class: Type[Any],
) -> tuple[Type[Any], Type[Any], Type[Any]]:
    """Generate three helper classes based on a plugin class.

    - Spec class: contains @hookspec placeholder methods.
    - Impl class: contains original plugin methods decorated with @hookimpl.
    - Proxy class: contains methods that call plugin_manager.hook.<method>.

    Returns:
        Tuple of (SpecClass, ImplClass, ProxyClass).
    """
    # Markers for spec and impl
    spec_methods = {}
    impl_methods = {}
    proxy_methods = {}

    for name, method in inspect.getmembers(plugin_class, predicate=inspect.isfunction):
        if name.startswith("_"):
            continue

        sig = inspect.signature(method)
        sig_nodef = sig.replace(
            parameters=[
                p.replace(default=inspect.Parameter.empty)
                for p in sig.parameters.values()
            ]
        )
        doc = method.__doc__ or ""

        # --- Spec placeholder ---
        def make_spec(
            name: str, sig_nodef: inspect.Signature, doc: str, method: Callable
        ) -> Callable:
            """Create a placeholder method for the spec class."""

            @wraps(method)
            def placeholder(*args: object, **kwargs: object) -> None:
                pass

            placeholder.__name__ = name
            placeholder.__doc__ = doc
            placeholder.__signature__ = sig_nodef  # type: ignore
            return placeholder

        spec_methods[name] = hookspec(firstresult=True)(
            make_spec(name, sig_nodef, doc, method)
        )

        # --- Impl class: original methods with @hookimpl ---
        wrapped_impl = wraps(method)(method)
        wrapped_impl.__signature__ = sig_nodef  # type: ignore
        impl_methods[name] = hookimpl(wrapped_impl)

        # --- Proxy class: call through plugin_manager.hook ---
        # Gather class variables and annotations from entire MRO (excluding built-ins)
        class_vars: dict[str, Any] = {}
        annotations: dict[str, Any] = {}
        for base in reversed(plugin_class.__mro__):
            if base is object:
                continue
            # collect annotations first so bases are overridden by subclasses
            base_ann = getattr(base, "__annotations__", {})
            annotations.update(base_ann)
            for key, value in base.__dict__.items():
                # skip private/special, methods, and descriptors
                if key.startswith("__"):
                    continue
                if callable(value) and not isinstance(value, type):
                    continue
                class_vars[key] = value

        def make_proxy(name: str, sig: inspect.Signature) -> Callable:
            """Create a proxy method for the proxy class."""

            def proxy(*args: object, **kwargs: object) -> object:
                # bind positionals to parameter names
                bound = sig.bind_partial(*args, **kwargs)  # noqa
                bound.apply_defaults()
                # grab the HookCaller
                hookcaller = getattr(plugin_manager.hook, name)  # noqa
                # call with named args only
                return hookcaller(**bound.arguments)

            proxy.__name__ = name
            proxy.__signature__ = sig  # type: ignore
            return proxy

        proxy_methods[name] = make_proxy(name, sig)

    # Construct classes
    spec_cls = type(f"{plugin_class.__name__}Spec", (object,), spec_methods)
    impl_cls = type(f"{plugin_class.__name__}Impl", (object,), impl_methods)
    proxy_namespace = {}
    proxy_namespace.update(class_vars)
    if annotations:
        proxy_namespace["__annotations__"] = annotations
    proxy_namespace.update(proxy_methods)
    proxy_cls = type(f"{plugin_class.__name__}", (object,), proxy_namespace)

    return spec_cls, impl_cls, proxy_cls


JacMachineSpec, JacMachineImpl, JacMachine = generate_plugin_helpers(JacMachine)  # type: ignore[misc]
plugin_manager.add_hookspecs(JacMachineSpec)
