"""Jac Language Features."""

from __future__ import annotations

import ast as ast3
import fnmatch
import html
import os
import pickle
import types
from collections import OrderedDict
from dataclasses import field
from functools import wraps
from typing import Any, Callable, Mapping, Optional, Sequence, Type, Union
from uuid import UUID

import jaclang.compiler.absyntree as ast
from jaclang.compiler.constant import EdgeDir, colors
from jaclang.compiler.passes.main.pyast_gen_pass import PyastGenPass
from jaclang.compiler.semtable import SemInfo, SemRegistry, SemScope
from jaclang.runtimelib.constructs import (
    Architype,
    DSFunc,
    EdgeAnchor,
    EdgeArchitype,
    ExecutionContext,
    GenericEdge,
    JacTestCheck,
    NodeAnchor,
    NodeArchitype,
    Root,
    WalkerAnchor,
    WalkerArchitype,
)
from jaclang.runtimelib.importer import ImportPathSpec, JacImporter, PythonImporter
from jaclang.runtimelib.machine import JacMachine, JacProgram
from jaclang.runtimelib.utils import traverse_graph
from jaclang.plugin.feature import JacFeature as Jac  # noqa: I100
from jaclang.plugin.spec import P, T


import pluggy

hookimpl = pluggy.HookimplMarker("jac")

__all__ = [
    "EdgeAnchor",
    "GenericEdge",
    "hookimpl",
    "JacTestCheck",
    "NodeAnchor",
    "WalkerAnchor",
    "NodeArchitype",
    "EdgeArchitype",
    "Root",
    "WalkerArchitype",
    "Architype",
    "DSFunc",
    "T",
]


class JacFeatureDefaults:
    """Jac Feature."""

    pm = pluggy.PluginManager("jac")

    @staticmethod
    @hookimpl
    def get_context() -> ExecutionContext:
        """Get current execution context."""
        return ExecutionContext.get()

    @staticmethod
    @hookimpl
    def get_object(id: str) -> Architype | None:
        if id == "root":
            return Jac.get_context().root.architype
        elif obj := Jac.get_context().mem.find_by_id(UUID(id)):
            return obj.architype

        return None

    @staticmethod
    @hookimpl
    def object_ref(obj: Architype) -> str:
        return obj.__jac__.id.hex

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
    @hookimpl
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

        jac_machine = JacMachine.get(base_path)
        if not jac_machine.jac_program:
            jac_machine.attach_program(JacProgram(mod_bundle=None, bytecode=None))

        if lng == "py":
            import_result = PythonImporter(JacMachine.get()).run_import(spec)
        else:
            import_result = JacImporter(JacMachine.get()).run_import(
                spec, reload_module
            )

        return (
            (import_result.ret_mod,)
            if absorb or not items
            else tuple(import_result.ret_items)
        )

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
                Jac.jac_import(target=mod_name, base_path=base)
                JacTestCheck.run_test(xit, maxfail, verbose)
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
                        Jac.jac_import(target=file[:-4], base_path=root_dir)
                        JacTestCheck.run_test(xit, maxfail, verbose)

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
            return op1.__jac__.spawn_call(op2.__jac__)
        elif isinstance(op2, WalkerArchitype):
            return op2.__jac__.spawn_call(op1.__jac__)
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
            return walker.__jac__.ignore_node(
                (i.__jac__ for i in expr) if isinstance(expr, list) else [expr.__jac__]
            )
        else:
            raise TypeError("Invalid walker object")

    @staticmethod
    @hookimpl
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
            return walker.__jac__.visit_node(
                (i.__jac__ for i in expr) if isinstance(expr, list) else [expr.__jac__]
            )
        else:
            raise TypeError("Invalid walker object")

    @staticmethod
    @hookimpl
    def disengage(walker: WalkerArchitype) -> bool:  # noqa: ANN401
        """Jac's disengage stmt feature."""
        walker.__jac__.disengage_now()
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
                connected_edges += node.__jac__.get_edges(
                    dir, filter_func, target_obj=targ_obj_set
                )
            return list(set(connected_edges))
        else:
            connected_nodes: list[NodeArchitype] = []
            for node in node_obj:
                connected_nodes.extend(
                    node.__jac__.edges_to_nodes(
                        dir, filter_func, target_obj=targ_obj_set
                    )
                )
            return list(set(connected_nodes))

    @staticmethod
    @hookimpl
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

        root = Jac.get_root().__jac__

        for i in left:
            _left = i.__jac__
            if root.has_connect_access(_left):
                for j in right:
                    _right = j.__jac__
                    if root.has_connect_access(_right):
                        edges.append(edge_spec(_left, _right))
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

        root = Jac.get_root().__jac__

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
                        and root.has_write_access(target)
                    ):
                        anchor.destroy() if anchor.persistent else anchor.detach()
                        disconnect_occurred = True
                    if (
                        dir in [EdgeDir.IN, EdgeDir.ANY]
                        and node == target
                        and source.architype in right
                        and root.has_write_access(source)
                    ):
                        anchor.destroy() if anchor.persistent else anchor.detach()
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
    def get_root() -> Root:
        """Jac's assign comprehension feature."""
        return ExecutionContext.get_root()

    @staticmethod
    @hookimpl
    def get_root_type() -> Type[Root]:
        """Jac's root getter."""
        return Root

    @staticmethod
    @hookimpl
    def build_edge(
        is_undirected: bool,
        conn_type: Optional[Type[EdgeArchitype] | EdgeArchitype],
        conn_assign: Optional[tuple[tuple, tuple]],
    ) -> Callable[[NodeAnchor, NodeAnchor], EdgeArchitype]:
        """Jac's root getter."""
        conn_type = conn_type if conn_type else GenericEdge

        def builder(source: NodeAnchor, target: NodeAnchor) -> EdgeArchitype:
            edge = conn_type() if isinstance(conn_type, type) else conn_type
            edge.__attach__(source, target, is_undirected)
            if conn_assign:
                for fld, val in zip(conn_assign[0], conn_assign[1]):
                    if hasattr(edge, fld):
                        setattr(edge, fld, val)
                    else:
                        raise ValueError(f"Invalid attribute: {fld}")
            if source.persistent or target.persistent:
                edge.__jac__.save()
                target.save()
                source.save()
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
        return "", ""

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
        _globals: dict,
        _locals: Mapping,
    ) -> Any:  # noqa: ANN401
        """Jac's with_llm feature."""
        raise ImportError(
            "mtllm is not installed. Please install it with `pip install mtllm` and run `jac clean`."
        )

    @staticmethod
    @hookimpl
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
    @hookimpl
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
    @hookimpl
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
                f' [label="{html.escape(str(edge.__jac__.architype))} "];\n'
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


class JacCmdDefaults:
    """Jac CLI command."""

    @staticmethod
    @hookimpl
    def create_cmd() -> None:
        """Create Jac CLI cmds."""
        pass
