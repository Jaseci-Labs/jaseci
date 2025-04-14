"""Jac Machine module."""

from __future__ import annotations

import ast as ast3
import fnmatch
import html
import inspect
import os
import sys
import tempfile
import types
from collections import OrderedDict
from contextvars import ContextVar
from dataclasses import field
from functools import wraps
from typing import (
    Any,
    Callable,
    ClassVar,
    Mapping,
    Optional,
    ParamSpec,
    Sequence,
    Type,
    TypeAlias,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID

from jaclang.compiler import absyntree as ast
from jaclang.compiler.constant import EdgeDir
from jaclang.compiler.constant import colors
from jaclang.compiler.passes.main.pyast_gen_pass import PyastGenPass
from jaclang.compiler.program import JacProgram
from jaclang.compiler.semtable import SemInfo, SemRegistry, SemScope
from jaclang.runtimelib.constructs import (
    AccessLevel,
    Anchor,
    Architype,
    DSFunc,
    EdgeAnchor,
    EdgeArchitype,
    GenericEdge,
    JacTestCheck,
    NodeAnchor,
    NodeArchitype,
    Root,
    WalkerArchitype,
)
from jaclang.runtimelib.context import ExecutionContext
from jaclang.runtimelib.importer import ImportPathSpec, JacImporter, PythonImporter
from jaclang.runtimelib.memory import Shelf, ShelfStorage
from jaclang.runtimelib.utils import (
    all_issubclass,
    collect_node_connections,
    traverse_graph,
)
from jaclang.utils.log import logging

T = TypeVar("T")
P = ParamSpec("P")

logger = logging.getLogger(__name__)


JACMACHINE_CONTEXT = ContextVar["JacMachine | None"]("JacMachine")


class JacMachine:
    """JacMachine to handle the VM-related functionalities and loaded programs."""

    def __init__(self, base_path: str = "") -> None:
        """Initialize the JacMachine object."""
        self.loaded_modules: dict[str, types.ModuleType] = {}
        if not base_path:
            base_path = os.getcwd()
        # Ensure the base_path is a list rather than a string
        self.base_path = base_path
        self.base_path_dir = (
            os.path.dirname(base_path)
            if not os.path.isdir(base_path)
            else os.path.abspath(base_path)
        )
        self.jac_program: JacProgram = JacProgram()

        JACMACHINE_CONTEXT.set(self)

    def attach_program(self, jac_program: "JacProgram") -> None:
        """Attach a JacProgram to the machine."""
        self.jac_program = jac_program

    def get_mod_bundle(self) -> Optional[ast.Module]:
        """Retrieve the mod_bundle from the attached JacProgram."""
        if self.jac_program:
            return self.jac_program.mod_bundle
        return None

    def get_bytecode(
        self,
        module_name: str,
        full_target: str,
        caller_dir: str,
        cachable: bool = True,
        reload: bool = False,
    ) -> Optional[types.CodeType]:
        """Retrieve bytecode from the attached JacProgram."""
        if self.jac_program:
            return self.jac_program.get_bytecode(
                module_name, full_target, caller_dir, cachable, reload=reload
            )
        return None

    def get_sem_ir(self, mod_sem_ir: SemRegistry | None) -> None:
        """Update semtable on the attached JacProgram."""
        if self.jac_program and mod_sem_ir:
            if self.jac_program.sem_ir:
                self.jac_program.sem_ir.registry.update(mod_sem_ir.registry)
            else:
                self.jac_program.sem_ir = mod_sem_ir

    def load_module(self, module_name: str, module: types.ModuleType) -> None:
        """Load a module into the machine."""
        self.loaded_modules[module_name] = module
        sys.modules[module_name] = module

    def list_modules(self) -> list[str]:
        """List all loaded modules."""
        return list(self.loaded_modules.keys())

    def list_walkers(self, module_name: str) -> list[str]:
        """List all walkers in a specific module."""
        module = self.loaded_modules.get(module_name)
        if module:
            walkers = []
            for name, obj in inspect.getmembers(module):
                if isinstance(obj, type) and issubclass(obj, WalkerArchitype):
                    walkers.append(name)
            return walkers
        return []

    def list_nodes(self, module_name: str) -> list[str]:
        """List all nodes in a specific module."""
        module = self.loaded_modules.get(module_name)
        if module:
            nodes = []
            for name, obj in inspect.getmembers(module):
                if isinstance(obj, type) and issubclass(obj, NodeArchitype):
                    nodes.append(name)
            return nodes
        return []

    def list_edges(self, module_name: str) -> list[str]:
        """List all edges in a specific module."""
        module = self.loaded_modules.get(module_name)
        if module:
            nodes = []
            for name, obj in inspect.getmembers(module):
                if isinstance(obj, type) and issubclass(obj, EdgeArchitype):
                    nodes.append(name)
            return nodes
        return []

    def create_architype_from_source(
        self,
        source_code: str,
        module_name: Optional[str] = None,
        base_path: Optional[str] = None,
        cachable: bool = False,
        keep_temporary_files: bool = False,
    ) -> Optional[types.ModuleType]:
        """Dynamically creates architypes (nodes, walkers, etc.) from Jac source code."""
        from jaclang.runtimelib.importer import JacImporter, ImportPathSpec

        if not base_path:
            base_path = self.base_path or os.getcwd()

        if base_path and not os.path.exists(base_path):
            os.makedirs(base_path)
        if not module_name:
            module_name = f"_dynamic_module_{len(self.loaded_modules)}"
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
            importer = JacImporter(self)
            tmp_file_basename = os.path.basename(tmp_file_path)
            tmp_module_name, _ = os.path.splitext(tmp_file_basename)

            spec = ImportPathSpec(
                target=tmp_module_name,
                base_path=base_path,
                absorb=False,
                cachable=cachable,
                mdl_alias=None,
                override_name=module_name,
                lng="jac",
                items=None,
            )

            import_result = importer.run_import(spec, reload=False)
            module = import_result.ret_mod

            self.loaded_modules[module_name] = module
            return module
        except Exception as e:
            logger.error(f"Error importing dynamic module '{module_name}': {e}")
            return None
        finally:
            if not keep_temporary_files and os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    def update_walker(
        self, module_name: str, items: Optional[dict[str, Union[str, Optional[str]]]]
    ) -> tuple[types.ModuleType, ...]:
        """Reimport the module."""
        from .importer import JacImporter, ImportPathSpec

        if module_name in self.loaded_modules:
            try:
                old_module = self.loaded_modules[module_name]
                importer = JacImporter(self)
                spec = ImportPathSpec(
                    target=module_name,
                    base_path=self.base_path,
                    absorb=False,
                    cachable=True,
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

    def spawn_node(
        self,
        node_name: str,
        attributes: Optional[dict] = None,
        module_name: str = "__main__",
    ) -> NodeArchitype:
        """Spawn a node instance of the given node_name with attributes."""
        node_class = self.get_architype(module_name, node_name)
        if isinstance(node_class, type) and issubclass(node_class, NodeArchitype):
            if attributes is None:
                attributes = {}
            node_instance = node_class(**attributes)
            return node_instance
        else:
            raise ValueError(f"Node {node_name} not found.")

    def spawn_walker(
        self,
        walker_name: str,
        attributes: Optional[dict] = None,
        module_name: str = "__main__",
    ) -> WalkerArchitype:
        """Spawn a walker instance of the given walker_name."""
        walker_class = self.get_architype(module_name, walker_name)
        if isinstance(walker_class, type) and issubclass(walker_class, WalkerArchitype):
            if attributes is None:
                attributes = {}
            walker_instance = walker_class(**attributes)
            return walker_instance
        else:
            raise ValueError(f"Walker {walker_name} not found.")

    def get_architype(
        self, module_name: str, architype_name: str
    ) -> Optional[Architype]:
        """Retrieve an architype class from a module."""
        module = self.loaded_modules.get(module_name)
        if module:
            return getattr(module, architype_name, None)
        return None

    @staticmethod
    def get(base_path: str = "") -> "JacMachine":
        """Get current jac machine."""
        if (jac_machine := JACMACHINE_CONTEXT.get(None)) is None:
            jac_machine = JacMachine(base_path)
        return jac_machine

    @staticmethod
    def detach_machine() -> None:
        """Detach current jac machine."""
        JACMACHINE_CONTEXT.set(None)

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
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
        target_obj: Optional[list[NodeArchitype]],
    ) -> list[EdgeArchitype]:
        """Get edges connected to this node."""
        ret_edges: list[EdgeArchitype] = []
        for anchor in node.edges:
            if (
                (source := anchor.source)
                and (target := anchor.target)
                and (not filter_func or filter_func([anchor.architype]))
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
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
        target_obj: Optional[list[NodeArchitype]],
    ) -> list[NodeArchitype]:
        """Get set of nodes connected to this node."""
        ret_edges: list[NodeArchitype] = []
        for anchor in node.edges:
            if (
                (source := anchor.source)
                and (target := anchor.target)
                and (not filter_func or filter_func([anchor.architype]))
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

    @staticmethod
    def detach(edge: EdgeAnchor) -> None:
        """Detach edge from nodes."""
        JacMachine.remove_edge(node=edge.source, edge=edge)
        JacMachine.remove_edge(node=edge.target, edge=edge)

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
    ) -> bool:
        """Jac's visit stmt feature."""
        if isinstance(walker, WalkerArchitype):
            """Walker visits node."""
            wanch = walker.__jac__
            before_len = len(wanch.next)
            for anchor in (
                (i.__jac__ for i in expr) if isinstance(expr, list) else [expr.__jac__]
            ):
                if anchor not in wanch.ignores:
                    if isinstance(anchor, NodeAnchor):
                        wanch.next.append(anchor)
                    elif isinstance(anchor, EdgeAnchor):
                        if target := anchor.target:
                            wanch.next.append(target)
                        else:
                            raise ValueError("Edge has no target.")
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
    ) -> bool:
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
    def spawn_call(op1: Architype, op2: Architype) -> WalkerArchitype:
        """Invoke data spatial call."""
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
            if i.func and not i.trigger:
                i.func(warch, current_node)
            if walker.disengaged:
                return warch

        while len(walker.next):
            if current_node := walker.next.pop(0).architype:
                # walker entry with
                for i in warch._jac_entry_funcs_:
                    if (
                        i.func
                        and i.trigger
                        and all_issubclass(i.trigger, NodeArchitype)
                        and isinstance(current_node, i.trigger)
                    ):
                        i.func(warch, current_node)
                    if walker.disengaged:
                        return warch

                # node entry
                for i in current_node._jac_entry_funcs_:
                    if i.func and not i.trigger:
                        i.func(current_node, warch)
                    if walker.disengaged:
                        return warch

                # node entry with
                for i in current_node._jac_entry_funcs_:
                    if (
                        i.func
                        and i.trigger
                        and all_issubclass(i.trigger, WalkerArchitype)
                        and isinstance(warch, i.trigger)
                    ):
                        i.func(current_node, warch)
                    if walker.disengaged:
                        return warch

                # node exit with
                for i in current_node._jac_exit_funcs_:
                    if (
                        i.func
                        and i.trigger
                        and all_issubclass(i.trigger, WalkerArchitype)
                        and isinstance(warch, i.trigger)
                    ):
                        i.func(current_node, warch)
                    if walker.disengaged:
                        return warch

                # node exit
                for i in current_node._jac_exit_funcs_:
                    if i.func and not i.trigger:
                        i.func(current_node, warch)
                    if walker.disengaged:
                        return warch

                # walker exit with
                for i in warch._jac_exit_funcs_:
                    if (
                        i.func
                        and i.trigger
                        and all_issubclass(i.trigger, NodeArchitype)
                        and isinstance(current_node, i.trigger)
                    ):
                        i.func(warch, current_node)
                    if walker.disengaged:
                        return warch
        # walker exit
        for i in warch._jac_exit_funcs_:
            if i.func and not i.trigger:
                i.func(warch, current_node)
            if walker.disengaged:
                return warch

        walker.ignores = []
        return warch

    @staticmethod
    def disengage(walker: WalkerArchitype) -> bool:  # noqa: ANN401
        """Jac's disengage stmt feature."""
        walker.__jac__.disengaged = True
        return True

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

    @staticmethod
    def create_cmd() -> None:
        """Create Jac CLI cmds."""
        pass

    @staticmethod
    def setup() -> None:
        """Set Class References."""
        pass

    @staticmethod
    def get_context() -> ExecutionContext:
        """Get current execution context."""
        return ExecutionContext.get()

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
        """Get object by id."""
        if id == "root":
            return JacMachine.get_context().root.architype
        elif obj := JacMachine.get_context().mem.find_by_id(UUID(id)):
            return obj.architype

        return None

    @staticmethod
    def object_ref(obj: Architype) -> str:
        """Get object's id."""
        return obj.__jac__.id.hex

    @staticmethod
    def make_architype(
        cls: type,
        arch_base: Type,
        on_entry: list[DSFunc],
        on_exit: list[DSFunc],
    ) -> Type[Architype]:
        """Create a new architype."""
        for i in on_entry + on_exit:
            i.resolve(cls)
        if not hasattr(cls, "_jac_entry_funcs_") or not hasattr(
            cls, "_jac_exit_funcs_"
        ):
            # Saving the module path and reassign it after creating cls
            # So the jac modules are part of the correct module
            cur_module = cls.__module__
            cls = type(cls.__name__, (cls, arch_base), {})
            cls.__module__ = cur_module
            cls._jac_entry_funcs_ = on_entry  # type: ignore
            cls._jac_exit_funcs_ = on_exit  # type: ignore
        else:
            new_entry_funcs = OrderedDict(zip([i.name for i in on_entry], on_entry))
            entry_funcs = OrderedDict(
                zip([i.name for i in cls._jac_entry_funcs_], cls._jac_entry_funcs_)
            )
            entry_funcs.update(new_entry_funcs)
            cls._jac_entry_funcs_ = list(entry_funcs.values())

            new_exit_funcs = OrderedDict(zip([i.name for i in on_exit], on_exit))
            exit_funcs = OrderedDict(
                zip([i.name for i in cls._jac_exit_funcs_], cls._jac_exit_funcs_)
            )
            exit_funcs.update(new_exit_funcs)
            cls._jac_exit_funcs_ = list(exit_funcs.values())

        inner_init = cls.__init__  # type: ignore

        @wraps(inner_init)
        def new_init(self: Architype, *args: object, **kwargs: object) -> None:
            arch_base.__init__(self)
            inner_init(self, *args, **kwargs)

        cls.__init__ = new_init  # type: ignore
        return cls

    @staticmethod
    def make_obj(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a new architype."""

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = JacMachine.make_architype(
                cls=cls, arch_base=Architype, on_entry=on_entry, on_exit=on_exit
            )
            return cls

        return decorator

    @staticmethod
    def make_node(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a obj architype."""

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = JacMachine.make_architype(
                cls=cls, arch_base=NodeArchitype, on_entry=on_entry, on_exit=on_exit
            )
            return cls

        return decorator

    @staticmethod
    def make_root(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a obj architype."""

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = JacMachine.make_architype(
                cls=cls, arch_base=Root, on_entry=on_entry, on_exit=on_exit
            )
            return cls

        return decorator

    @staticmethod
    def make_edge(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a edge architype."""

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = JacMachine.make_architype(
                cls=cls, arch_base=EdgeArchitype, on_entry=on_entry, on_exit=on_exit
            )
            return cls

        return decorator

    @staticmethod
    def make_generic_edge(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a edge architype."""

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = JacMachine.make_architype(
                cls=cls,
                arch_base=GenericEdge,
                on_entry=on_entry,
                on_exit=on_exit,
            )
            return cls

        return decorator

    @staticmethod
    def make_walker(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a walker architype."""

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = JacMachine.make_architype(
                cls=cls, arch_base=WalkerArchitype, on_entry=on_entry, on_exit=on_exit
            )
            return cls

        return decorator

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

    def jac_import(
        self,
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
        spec = ImportPathSpec(
            target,
            base_path,
            absorb,
            cachable,
            mdl_alias,
            override_name,
            lng,
            items,
        )
        if not self.jac_program:
            self.attach_program(JacProgram())

        if lng == "py":
            import_result = PythonImporter(self).run_import(spec)
        else:
            import_result = JacImporter(self).run_import(spec, reload_module)

        return (
            (import_result.ret_mod,)
            if absorb or not items
            else tuple(import_result.ret_items)
        )

    @staticmethod
    def create_test(test_fun: Callable) -> Callable:
        """Create a new test."""
        file_path = inspect.getfile(test_fun)
        func_name = test_fun.__name__

        def test_deco() -> None:
            test_fun(JacTestCheck())

        test_deco.__name__ = test_fun.__name__
        JacTestCheck.add_test(file_path, func_name, test_deco)

        return test_deco

    def run_test(
        self,
        filepath: str,
        func_name: Optional[str],
        filter: Optional[str],
        xit: bool,
        maxfail: Optional[int],
        directory: Optional[str],
        verbose: bool,
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
                self.jac_import(
                    target=mod_name,
                    base_path=base,
                    cachable=False,
                    absorb=False,
                    mdl_alias=None,
                    override_name=None,
                    lng="jac",
                    items=None,
                    reload_module=False,
                )
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
                        self.jac_import(
                            target=file[:-4],
                            base_path=root_dir,
                            absorb=False,
                            cachable=True,
                            mdl_alias=None,
                            override_name=None,
                            lng="jac",
                            items=None,
                            reload_module=False,
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
    def has_instance_default(gen_func: Callable[[], T]) -> T:
        """Jac's has container default feature."""
        return field(default_factory=lambda: gen_func())

    @staticmethod
    def report(expr: Any, custom: bool) -> None:  # noqa: ANN401
        """Jac's report stmt feature."""
        ctx = JacMachine.get_context()
        if custom:
            ctx.custom = expr
        else:
            ctx.reports.append(expr)

    @staticmethod
    def edge_ref(
        node_obj: NodeArchitype | list[NodeArchitype],
        target_obj: Optional[NodeArchitype | list[NodeArchitype]],
        dir: EdgeDir,
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
        edges_only: bool,
    ) -> list[NodeArchitype] | list[EdgeArchitype]:
        """Jac's apply_dir stmt feature."""
        if isinstance(node_obj, NodeArchitype):
            node_obj = [node_obj]
        targ_obj_set: Optional[list[NodeArchitype]] = (
            [target_obj]
            if isinstance(target_obj, NodeArchitype)
            else target_obj if target_obj else None
        )
        if edges_only:
            connected_edges: list[EdgeArchitype] = []
            for node in node_obj:
                edges = JacMachine.get_edges(
                    node.__jac__, dir, filter_func, target_obj=targ_obj_set
                )
                connected_edges.extend(
                    edge for edge in edges if edge not in connected_edges
                )
            return connected_edges
        else:
            connected_nodes: list[NodeArchitype] = []
            for node in node_obj:
                nodes = JacMachine.edges_to_nodes(
                    node.__jac__, dir, filter_func, target_obj=targ_obj_set
                )
                connected_nodes.extend(
                    node for node in nodes if node not in connected_nodes
                )
            return connected_nodes

    @staticmethod
    def connect(
        left: NodeArchitype | list[NodeArchitype],
        right: NodeArchitype | list[NodeArchitype],
        edge_spec: Callable[[NodeAnchor, NodeAnchor], EdgeArchitype],
        edges_only: bool,
    ) -> list[NodeArchitype] | list[EdgeArchitype]:
        """Jac's connect operator feature.

        Note: connect needs to call assign compr with tuple in op
        """
        left = [left] if isinstance(left, NodeArchitype) else left
        right = [right] if isinstance(right, NodeArchitype) else right
        edges = []

        for i in left:
            _left = i.__jac__
            if JacMachine.check_connect_access(_left):
                for j in right:
                    _right = j.__jac__
                    if JacMachine.check_connect_access(_right):
                        edges.append(edge_spec(_left, _right))
        return right if not edges_only else edges

    @staticmethod
    def disconnect(
        left: NodeArchitype | list[NodeArchitype],
        right: NodeArchitype | list[NodeArchitype],
        dir: EdgeDir,
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
    ) -> bool:  # noqa: ANN401
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
                    and (not filter_func or filter_func([anchor.architype]))
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
    def assign_compr(
        target: list[T], attr_val: tuple[tuple[str], tuple[Any]]
    ) -> list[T]:
        """Jac's assign comprehension feature."""
        for obj in target:
            attrs, values = attr_val
            for attr, value in zip(attrs, values):
                setattr(obj, attr, value)
        return target

    @staticmethod
    def get_root() -> Root:
        """Jac's assign comprehension feature."""
        return ExecutionContext.get_root()

    @staticmethod
    def get_root_type() -> Type[Root]:
        """Jac's root getter."""
        from jaclang import Root as JRoot

        return cast(Type[Root], JRoot)

    @staticmethod
    def build_edge(
        is_undirected: bool,
        conn_type: Optional[Type[EdgeArchitype] | EdgeArchitype],
        conn_assign: Optional[tuple[tuple, tuple]],
    ) -> Callable[[NodeAnchor, NodeAnchor], EdgeArchitype]:
        """Jac's root getter."""
        from jaclang import GenericEdge

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
    def save(obj: Architype | Anchor) -> None:
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
    def destroy(obj: Architype | Anchor) -> None:
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
    def get_semstr_type(
        file_loc: str, scope: str, attr: str, return_semstr: bool
    ) -> Optional[str]:
        """Jac's get_semstr_type feature."""
        from jaclang.compiler.semtable import SemInfo, SemScope, SemRegistry
        from jaclang.runtimelib.machine import JacMachine

        _scope = SemScope.get_scope_from_str(scope)
        jac_program = JacMachine.get().jac_program
        mod_registry: SemRegistry = (
            jac_program.sem_ir if jac_program is not None else SemRegistry()
        )
        _, attr_seminfo = mod_registry.lookup(_scope, attr)
        if attr_seminfo and isinstance(attr_seminfo, SemInfo):
            return attr_seminfo.semstr if return_semstr else attr_seminfo.type
        return None

    @staticmethod
    def obj_scope(file_loc: str, attr: str) -> str:
        """Jac's gather_scope feature."""
        from jaclang.runtimelib.machine import JacMachine

        jac_program = JacMachine.get().jac_program
        mod_registry: SemRegistry = (
            jac_program.sem_ir if jac_program is not None else SemRegistry()
        )

        attr_scope = None
        for x in attr.split("."):
            attr_scope, attr_sem_info = mod_registry.lookup(attr_scope, x)
            if isinstance(attr_sem_info, SemInfo) and attr_sem_info.type not in [
                "class",
                "obj",
                "node",
                "edge",
            ]:
                attr_scope, attr_sem_info = mod_registry.lookup(
                    None, attr_sem_info.type
                )
                if isinstance(attr_sem_info, SemInfo) and isinstance(
                    attr_sem_info.type, str
                ):
                    attr_scope = SemScope(
                        attr_sem_info.name, attr_sem_info.type, attr_scope
                    )
            else:
                if isinstance(attr_sem_info, SemInfo) and isinstance(
                    attr_sem_info.type, str
                ):
                    attr_scope = SemScope(
                        attr_sem_info.name, attr_sem_info.type, attr_scope
                    )
        return str(attr_scope)

    @staticmethod
    def get_sem_type(file_loc: str, attr: str) -> tuple[str | None, str | None]:
        """Jac's get_semstr_type implementation."""
        from jaclang.runtimelib.machine import JacMachine
        from jaclang.compiler.semtable import SemInfo, SemScope

        jac_program = JacMachine.get().jac_program
        mod_registry: SemRegistry = (
            jac_program.sem_ir if jac_program is not None else SemRegistry()
        )

        attr_scope = None
        for x in attr.split("."):
            attr_scope, attr_sem_info = mod_registry.lookup(attr_scope, x)
            if isinstance(attr_sem_info, SemInfo) and attr_sem_info.type not in [
                "class",
                "obj",
                "node",
                "edge",
            ]:
                attr_scope, attr_sem_info = mod_registry.lookup(
                    None, attr_sem_info.type
                )
                if isinstance(attr_sem_info, SemInfo) and isinstance(
                    attr_sem_info.type, str
                ):
                    attr_scope = SemScope(
                        attr_sem_info.name, attr_sem_info.type, attr_scope
                    )
            else:
                if isinstance(attr_sem_info, SemInfo) and isinstance(
                    attr_sem_info.type, str
                ):
                    attr_scope = SemScope(
                        attr_sem_info.name, attr_sem_info.type, attr_scope
                    )
        if isinstance(attr_sem_info, SemInfo) and isinstance(attr_scope, SemScope):
            return attr_sem_info.semstr, attr_scope.as_type_str
        return "", ""

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
        """Return the LLM Call, e.g. _Jac.with_llm()."""
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

    EdgeDir: ClassVar[TypeAlias] = EdgeDir
    DSFunc: ClassVar[TypeAlias] = DSFunc
    RootType: ClassVar[TypeAlias] = Root
    Obj: ClassVar[TypeAlias] = Architype
    Node: ClassVar[TypeAlias] = NodeArchitype
    Edge: ClassVar[TypeAlias] = EdgeArchitype
    Walker: ClassVar[TypeAlias] = WalkerArchitype
