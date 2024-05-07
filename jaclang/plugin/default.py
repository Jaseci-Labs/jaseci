"""Jac Language Features."""

from __future__ import annotations

import fnmatch
import html
import os
import pickle
import types
from dataclasses import field
from functools import wraps
from typing import Any, Callable, Optional, Type, Union

from jaclang.compiler.absyntree import Module
from jaclang.compiler.constant import EdgeDir, colors
from jaclang.core.aott import (
    aott_raise,
    extract_non_primary_type,
    get_all_type_explanations,
    get_info_types,
    get_object_string,
    get_reasoning_output,
    get_type_annotation,
)
from jaclang.core.construct import (
    Architype,
    DSFunc,
    EdgeAnchor,
    EdgeArchitype,
    GenericEdge,
    JacTestCheck,
    NodeAnchor,
    NodeArchitype,
    ObjectAnchor,
    Root,
    WalkerAnchor,
    WalkerArchitype,
    root,
)
from jaclang.core.importer import jac_importer
from jaclang.core.registry import SemInfo, SemRegistry, SemScope
from jaclang.core.utils import traverse_graph
from jaclang.plugin.feature import JacFeature as Jac
from jaclang.plugin.spec import T


import pluggy


__all__ = [
    "EdgeAnchor",
    "GenericEdge",
    "JacTestCheck",
    "NodeAnchor",
    "ObjectAnchor",
    "WalkerAnchor",
    "NodeArchitype",
    "EdgeArchitype",
    "WalkerArchitype",
    "Architype",
    "DSFunc",
    "root",
    "Root",
    "jac_importer",
    "T",
]


hookimpl = pluggy.HookimplMarker("jac")


class JacFeatureDefaults:
    """Jac Feature."""

    pm = pluggy.PluginManager("jac")

    @staticmethod
    @hookimpl
    def make_architype(
        cls: type,
        arch_base: Type[Architype],
        on_entry: list[DSFunc],
        on_exit: list[DSFunc],
    ) -> Type[Architype]:
        """Create a new architype."""
        for i in on_entry + on_exit:
            i.resolve(cls)
        if not issubclass(cls, arch_base):
            # Saving the module path and reassign it after creating cls
            # So the jac modules are part of the correct module
            cur_module = cls.__module__
            cls = type(cls.__name__, (cls, arch_base), {})
            cls.__module__ = cur_module
            cls._jac_entry_funcs_ = on_entry  # type: ignore
            cls._jac_exit_funcs_ = on_exit  # type: ignore
        else:
            cls._jac_entry_funcs_ = cls._jac_entry_funcs_ + [
                x for x in on_entry if x not in cls._jac_entry_funcs_
            ]
            cls._jac_exit_funcs_ = cls._jac_exit_funcs_ + [
                x for x in on_exit if x not in cls._jac_exit_funcs_
            ]
        inner_init = cls.__init__  # type: ignore

        @wraps(inner_init)
        def new_init(self: Architype, *args: object, **kwargs: object) -> None:
            inner_init(self, *args, **kwargs)
            arch_base.__init__(self)

        cls.__init__ = new_init  # type: ignore
        return cls

    @staticmethod
    @hookimpl
    def make_obj(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a new architype."""

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = Jac.make_architype(
                cls=cls, arch_base=Architype, on_entry=on_entry, on_exit=on_exit
            )
            return cls

        return decorator

    @staticmethod
    @hookimpl
    def make_node(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a obj architype."""

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = Jac.make_architype(
                cls=cls, arch_base=NodeArchitype, on_entry=on_entry, on_exit=on_exit
            )
            return cls

        return decorator

    @staticmethod
    @hookimpl
    def make_edge(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a edge architype."""

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = Jac.make_architype(
                cls=cls, arch_base=EdgeArchitype, on_entry=on_entry, on_exit=on_exit
            )
            return cls

        return decorator

    @staticmethod
    @hookimpl
    def make_walker(
        on_entry: list[DSFunc], on_exit: list[DSFunc]
    ) -> Callable[[type], type]:
        """Create a walker architype."""

        def decorator(cls: Type[Architype]) -> Type[Architype]:
            """Decorate class."""
            cls = Jac.make_architype(
                cls=cls, arch_base=WalkerArchitype, on_entry=on_entry, on_exit=on_exit
            )
            return cls

        return decorator

    @staticmethod
    @hookimpl
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
        result = jac_importer(
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
        return result

    @staticmethod
    @hookimpl
    def create_test(test_fun: Callable) -> Callable:
        """Create a new test."""

        def test_deco() -> None:
            test_fun(JacTestCheck())

        test_deco.__name__ = test_fun.__name__
        JacTestCheck.add_test(test_deco)

        return test_deco

    @staticmethod
    @hookimpl
    def run_test(
        filepath: str,
        filter: Optional[str],
        xit: bool,
        maxfail: Optional[int],
        directory: Optional[str],
        verbose: bool,
    ) -> bool:
        """Run the test suite in the specified .jac file."""
        test_file = False
        if filepath:
            if filepath.endswith(".jac"):
                base, mod_name = os.path.split(filepath)
                base = base if base else "./"
                mod_name = mod_name[:-4]
                JacTestCheck.reset()
                Jac.jac_import(target=mod_name, base_path=base)
                JacTestCheck.run_test(xit, maxfail, verbose)
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
                        Jac.jac_import(target=file[:-4], base_path=root_dir)
                        JacTestCheck.run_test(xit, maxfail, verbose)

                    if JacTestCheck.breaker and (xit or maxfail):
                        break
                if JacTestCheck.breaker and (xit or maxfail):
                    break
            JacTestCheck.breaker = False
            JacTestCheck.failcount = 0
            print("No test files found.") if not test_file else None

        return True

    @staticmethod
    @hookimpl
    def elvis(op1: Optional[T], op2: T) -> T:
        """Jac's elvis operator feature."""
        return ret if (ret := op1) is not None else op2

    @staticmethod
    @hookimpl
    def has_instance_default(gen_func: Callable[[], T]) -> T:
        """Jac's has container default feature."""
        return field(default_factory=lambda: gen_func())

    @staticmethod
    @hookimpl
    def spawn_call(op1: Architype, op2: Architype) -> WalkerArchitype:
        """Jac's spawn operator feature."""
        if isinstance(op1, WalkerArchitype):
            return op1._jac_.spawn_call(op2)
        elif isinstance(op2, WalkerArchitype):
            return op2._jac_.spawn_call(op1)
        else:
            raise TypeError("Invalid walker object")

    @staticmethod
    @hookimpl
    def report(expr: Any) -> Any:  # noqa: ANN401
        """Jac's report stmt feature."""

    @staticmethod
    @hookimpl
    def ignore(
        walker: WalkerArchitype,
        expr: list[NodeArchitype | EdgeArchitype] | NodeArchitype | EdgeArchitype,
    ) -> bool:
        """Jac's ignore stmt feature."""
        return walker._jac_.ignore_node(expr)

    @staticmethod
    @hookimpl
    def visit_node(
        walker: WalkerArchitype,
        expr: list[NodeArchitype | EdgeArchitype] | NodeArchitype | EdgeArchitype,
    ) -> bool:
        """Jac's visit stmt feature."""
        if isinstance(walker, WalkerArchitype):
            return walker._jac_.visit_node(expr)
        else:
            raise TypeError("Invalid walker object")

    @staticmethod
    @hookimpl
    def disengage(walker: WalkerArchitype) -> bool:  # noqa: ANN401
        """Jac's disengage stmt feature."""
        walker._jac_.disengage_now()
        return True

    @staticmethod
    @hookimpl
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
                connected_edges += node._jac_.get_edges(
                    dir, filter_func, target_obj=targ_obj_set
                )
            return list(set(connected_edges))
        else:
            connected_nodes: list[NodeArchitype] = []
            for node in node_obj:
                connected_nodes.extend(
                    node._jac_.edges_to_nodes(dir, filter_func, target_obj=targ_obj_set)
                )
            return list(set(connected_nodes))

    @staticmethod
    @hookimpl
    def connect(
        left: NodeArchitype | list[NodeArchitype],
        right: NodeArchitype | list[NodeArchitype],
        edge_spec: Callable[[], EdgeArchitype],
        edges_only: bool,
    ) -> list[NodeArchitype] | list[EdgeArchitype]:
        """Jac's connect operator feature.

        Note: connect needs to call assign compr with tuple in op
        """
        left = [left] if isinstance(left, NodeArchitype) else left
        right = [right] if isinstance(right, NodeArchitype) else right
        edges = []
        for i in left:
            for j in right:
                conn_edge = edge_spec()
                edges.append(conn_edge)
                i._jac_.connect_node(j, conn_edge)
        return right if not edges_only else edges

    @staticmethod
    @hookimpl
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
            for j in right:
                edge_list: list[EdgeArchitype] = [*i._jac_.edges]
                edge_list = filter_func(edge_list) if filter_func else edge_list
                for e in edge_list:
                    if e._jac_.target and e._jac_.source:
                        if (
                            dir in ["OUT", "ANY"]  # TODO: Not ideal
                            and i._jac_.obj == e._jac_.source
                            and e._jac_.target == j._jac_.obj
                        ):
                            e._jac_.detach(i._jac_.obj, e._jac_.target)
                            disconnect_occurred = True
                        if (
                            dir in ["IN", "ANY"]
                            and i._jac_.obj == e._jac_.target
                            and e._jac_.source == j._jac_.obj
                        ):
                            e._jac_.detach(i._jac_.obj, e._jac_.source)
                            disconnect_occurred = True
        return disconnect_occurred

    @staticmethod
    @hookimpl
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
    @hookimpl
    def get_root() -> Architype:
        """Jac's assign comprehension feature."""
        return root

    @staticmethod
    @hookimpl
    def build_edge(
        is_undirected: bool,
        conn_type: Optional[Type[EdgeArchitype]],
        conn_assign: Optional[tuple[tuple, tuple]],
    ) -> Callable[[], EdgeArchitype]:
        """Jac's root getter."""
        conn_type = conn_type if conn_type else GenericEdge

        def builder() -> EdgeArchitype:
            edge = conn_type()
            edge._jac_.is_undirected = is_undirected
            if conn_assign:
                for fld, val in zip(conn_assign[0], conn_assign[1]):
                    if hasattr(edge, fld):
                        setattr(edge, fld, val)
                    else:
                        raise ValueError(f"Invalid attribute: {fld}")
            return edge

        return builder

    @staticmethod
    @hookimpl
    def get_semstr_type(
        file_loc: str, scope: str, attr: str, return_semstr: bool
    ) -> Optional[str]:
        """Jac's get_semstr_type feature."""
        _scope = SemScope.get_scope_from_str(scope)
        with open(
            os.path.join(
                os.path.dirname(file_loc),
                "__jac_gen__",
                os.path.basename(file_loc).replace(".jac", ".registry.pkl"),
            ),
            "rb",
        ) as f:
            mod_registry: SemRegistry = pickle.load(f)
        _, attr_seminfo = mod_registry.lookup(_scope, attr)
        if attr_seminfo and isinstance(attr_seminfo, SemInfo):
            return attr_seminfo.semstr if return_semstr else attr_seminfo.type
        return None

    @staticmethod
    @hookimpl
    def obj_scope(file_loc: str, attr: str) -> str:
        """Jac's gather_scope feature."""
        with open(
            os.path.join(
                os.path.dirname(file_loc),
                "__jac_gen__",
                os.path.basename(file_loc).replace(".jac", ".registry.pkl"),
            ),
            "rb",
        ) as f:
            mod_registry: SemRegistry = pickle.load(f)

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
    @hookimpl
    def get_sem_type(file_loc: str, attr: str) -> tuple[str | None, str | None]:
        with open(
            os.path.join(
                os.path.dirname(file_loc),
                "__jac_gen__",
                os.path.basename(file_loc).replace(".jac", ".registry.pkl"),
            ),
            "rb",
        ) as f:
            mod_registry: SemRegistry = pickle.load(f)

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
        return "", ""  #

    @staticmethod
    @hookimpl
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
        with open(
            os.path.join(
                os.path.dirname(file_loc),
                "__jac_gen__",
                os.path.basename(file_loc).replace(".jac", ".registry.pkl"),
            ),
            "rb",
        ) as f:
            mod_registry = pickle.load(f)

        outputs = outputs[0] if isinstance(outputs, list) else outputs
        _scope = SemScope.get_scope_from_str(scope)
        assert _scope is not None

        reason = False
        if "reason" in model_params:
            reason = model_params.pop("reason")

        type_collector: list = []
        information, collected_types = get_info_types(_scope, mod_registry, incl_info)
        type_collector.extend(collected_types)
        inputs_information_list = []
        for i in inputs:
            typ_anno = get_type_annotation(i[3])
            type_collector.extend(extract_non_primary_type(typ_anno))
            inputs_information_list.append(
                f"{i[0]} ({i[2]}) ({typ_anno}) = {get_object_string(i[3])}"
            )
        inputs_information = "\n".join(inputs_information_list)

        output_information = f"{outputs[0]} ({outputs[1]})"
        type_collector.extend(extract_non_primary_type(outputs[1]))

        type_explanations_list = list(
            get_all_type_explanations(type_collector, mod_registry).values()
        )
        type_explanations = "\n".join(type_explanations_list)

        meaning_in = aott_raise(
            information,
            inputs_information,
            output_information,
            type_explanations,
            action,
            reason,
        )
        meaning_out = model.__infer__(meaning_in, **model_params)
        reasoning, output = get_reasoning_output(meaning_out)
        return output


class JacBuiltin:
    """Jac Builtins."""

    @staticmethod
    @hookimpl
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
            dot_content += (
                f"{visited_nodes.index(source)} -> {visited_nodes.index(target)} "
                f' [label="{html.escape(str(edge._jac_.obj.__class__.__name__))} "];\n'
            )
        for node_ in visited_nodes:
            color = (
                colors[node_depths[node_]] if node_depths[node_] < 25 else colors[24]
            )
            dot_content += (
                f'{visited_nodes.index(node_)} [label="{html.escape(str(node_._jac_.obj))}"'
                f'fillcolor="{color}"];\n'
            )
        if dot_file:
            with open(dot_file, "w") as f:
                f.write(dot_content + "}")
        return dot_content + "}"


class JacCmdDefaults:
    """Jac CLI command."""

    @staticmethod
    @hookimpl
    def create_cmd() -> None:
        """Create Jac CLI cmds."""
        pass
