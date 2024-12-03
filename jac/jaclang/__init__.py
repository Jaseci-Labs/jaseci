"""The Jac Programming Language."""

import inspect
import types
import typing
from abc import ABC, ABCMeta, abstractmethod
from dataclasses import dataclass, field as dc_field
from typing import Any, Callable, ClassVar, Dict, Tuple, Type, TypeVar, override

from jaclang.plugin.builtin import dotgen, jid  # noqa: F401
from jaclang.plugin.default import JacFeatureImpl
from jaclang.plugin.feature import JacFeature as _Jac, plugin_manager
from jaclang.plugin.spec import EdgeDir, Root
from jaclang.runtimelib.architype import Root as RootType

__all__ = [
    "JacObj",
    "JacWalker",
    "JacNode",
    "JacEdge",
    "EdgeDir",
    "RootType",
    "jac_import",
    "with_entry",
    "with_exit",
    "jac_test",
    "abstract",
    "override",
    "field",
    "static",
    "root",
    # Builtin-functions.
    "dotgen",
    "jid",
    "jobj",
    # This is not part of the jaclib for a python user but used internally to generate by jac compiler.
    "_impl_patch_filename",
]


# ----------------------------------------------------------------------------
# Plugin Initialization.
# ----------------------------------------------------------------------------

plugin_manager.register(JacFeatureImpl)
plugin_manager.load_setuptools_entrypoints("jac")

T = TypeVar("T")

# ----------------------------------------------------------------------------
# Meta classes.
# ----------------------------------------------------------------------------


# https://stackoverflow.com/a/9639512/10846399
class _JacArchiTypeBase:
    pass


class JacMetaCommon(ABCMeta):
    """Common metaclass for Jac types."""

    def __new__(  # noqa: D102
        cls,
        name: str,
        bases: Tuple[Type, ...],
        dct: Dict[str, Any],
        make_func: Callable[[list, list], Callable[[type], type]],
    ) -> "JacMetaCommon":

        # We have added this "__init__" to the jac base class just to make the type checkers happy.
        # Actually the dataclass decorator will create an __init__ function and assign it here bellow.
        if bases == (_JacArchiTypeBase,) and "__init__" in dct:
            del dct["__init__"]

        on_entry, on_exit = [], []
        for value in dct.values():
            if hasattr(value, "__jac_entry"):
                entry_node = getattr(value, "__jac_entry")  # noqa: B009
                on_entry.append(_Jac.DSFunc(value.__name__, entry_node))
            if hasattr(value, "__jac_exit"):
                exit_node = getattr(value, "__jac_exit")  # noqa: B009
                on_exit.append(_Jac.DSFunc(value.__name__, exit_node))

        inst = super().__new__(cls, name, bases, dct)
        inst = dataclass(eq=False)(inst)  # type: ignore [arg-type, assignment]
        inst = make_func(on_entry, on_exit)(inst)  # type: ignore [assignment]
        return inst


class JacMetaObj(JacMetaCommon, ABC):  # noqa: D101
    def __new__(  # noqa: D102
        cls, name: str, bases: Tuple[Type, ...], dct: Dict[str, Any]
    ) -> "JacMetaCommon":
        return super().__new__(cls, name, bases, dct, _Jac.make_obj)


class JacMetaWalker(JacMetaCommon, ABC):  # noqa: D101
    def __new__(  # noqa: D102
        cls, name: str, bases: Tuple[Type, ...], dct: Dict[str, Any]
    ) -> "JacMetaCommon":
        return super().__new__(cls, name, bases, dct, _Jac.make_walker)


class JacMetaNode(JacMetaCommon, ABC):  # noqa: D101
    def __new__(  # noqa: D102
        cls, name: str, bases: Tuple[Type, ...], dct: Dict[str, Any]
    ) -> "JacMetaCommon":
        return super().__new__(cls, name, bases, dct, _Jac.make_node)


class JacMetaEdge(JacMetaCommon, ABC):  # noqa: D101
    def __new__(  # noqa: D102
        cls, name: str, bases: Tuple[Type, ...], dct: Dict[str, Any]
    ) -> "JacMetaCommon":
        return super().__new__(cls, name, bases, dct, _Jac.make_edge)


# ----------------------------------------------------------------------------
# Base classes.
# ----------------------------------------------------------------------------


class JacObj(_JacArchiTypeBase, metaclass=JacMetaObj):
    """Base class for all the jac object types."""

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Initialize Jac architype base."""


class JacWalker(_JacArchiTypeBase, metaclass=JacMetaWalker):
    """Base class for all the jac walker types."""

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Initialize Jac architype base."""

    def spawn(self, node: "JacNode") -> "JacWalker":
        """Spawn a new node from the walker."""
        return _Jac.spawn_call(self, node)  # type: ignore [arg-type, return-value]

    def ignore(
        self,
        expr: """(
        list[JacNode | JacEdge]
        | JacNodeList
        | JacEdgeList
        | JacNode
        | JacEdge
        )""",
    ) -> bool:
        """Ignore statement."""
        return _Jac.ignore(self, expr)  # type: ignore [arg-type]

    def visit(
        self,
        expr: """(
            Root
            | list[JacNode | JacEdge]
            | JacNodeList
            | JacEdgeList
            | JacNode
            | JacEdge
        )""",
    ) -> bool:
        """Visit statement."""
        return _Jac.visit_node(self, expr)  # type: ignore [arg-type]

    def disengage(self) -> None:
        """Disengage statement."""
        _Jac.disengage(self)  # type: ignore [arg-type]


class JacNode(_JacArchiTypeBase, metaclass=JacMetaNode):
    """Base class for all the jac node types."""

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Initialize Jac architype base."""

    def spawn(self, walker: JacWalker) -> "JacWalker":
        """Spawn a new node from the walker."""
        return _Jac.spawn_call(self, walker)  # type: ignore [arg-type, return-value]

    def connect(
        self,
        node: "JacNode | JacNodeList",
        edge: "type[JacEdge] | JacEdge | None" = None,
        unidir: bool = False,
        conn_assign: tuple[tuple, tuple] | None = None,
        edges_only: bool = False,
    ) -> "JacNodeList | JacEdgeList":
        """Connect the current node to another node."""
        # TODO: The above edge type should be reviewed, as the bellow can also take None, Edge, type[Edge].
        ret = _Jac.connect(
            left=self,  # type: ignore [arg-type]
            right=node,  # type: ignore [arg-type]
            edge_spec=_Jac.build_edge(
                is_undirected=unidir, conn_type=edge, conn_assign=conn_assign  # type: ignore [arg-type]
            ),
            edges_only=edges_only,
        )
        if edges_only:
            return JacEdgeList(ret)  # type: ignore [arg-type]
        return JacNodeList(ret)  # type: ignore [arg-type]

    def disconnect(
        self,
        node: "JacNode | JacNodeList",
        edge: "type[JacEdge] | None" = None,
        dir: EdgeDir = EdgeDir.OUT,
    ) -> bool:
        """Disconnect the current node from the graph."""
        filter_func = None
        if edge:
            filter_func = lambda edges: [  # noqa: E731
                ed for ed in edges if isinstance(ed, edge)
            ]
        return _Jac.disconnect(self, node, dir=dir, filter_func=filter_func)  # type: ignore [arg-type]

    def refs(
        self,
        edge: "type[JacEdge] | None" = None,
        cond: "Callable[[JacEdge], bool] | None" = None,
        target: "JacNode | JacNodeList | None" = None,
        dir: EdgeDir = EdgeDir.OUT,
        edges_only: bool = False,
    ) -> "JacNodeList | JacEdgeList":
        """Return all the connected nodes / edges."""
        filter_func = (
            (
                lambda edges: (  # noqa: E731
                    [ed for ed in edges if isinstance(ed, edge) if not cond or cond(ed)]
                )
            )
            if edge
            else None
        )
        ret = plugin_manager.hook.edge_ref(
            node_obj=self,
            target_obj=target,
            dir=dir,
            filter_func=filter_func,
            edges_only=edges_only,
        )
        if edges_only:
            return JacEdgeList(ret)
        return JacNodeList(ret)


class JacEdge(_JacArchiTypeBase, metaclass=JacMetaEdge):
    """Base class for all the jac edge types."""

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Initialize Jac architype base."""


class JacEdgeList(list[JacEdge]):
    """List of jac edges."""

    def filter_type(self, ty: "type[JacEdge]") -> "JacEdgeList":
        """Filter the list with a type."""
        return JacEdgeList([elem for elem in self if isinstance(elem, ty)])

    def filter_func(self, fn: Callable) -> "JacEdgeList":
        """Filter the list with a function."""
        return JacEdgeList([elem for elem in self if fn(elem)])


class JacNodeList(list[JacNode]):
    """List of jac nodes."""

    # Reuse the methods.
    connect = JacNode.connect
    disconnect = JacNode.disconnect
    refs = JacNode.refs

    def filter_type(self, ty: "type[JacNode]") -> "JacNodeList":
        """Filter the list with a type."""
        return JacNodeList([elem for elem in self if isinstance(elem, ty)])

    def filter_func(self, fn: Callable) -> "JacNodeList":
        """Filter the list with a function."""
        return JacNodeList([elem for elem in self if fn(elem)])


# ----------------------------------------------------------------------------
# Decorators.
# ----------------------------------------------------------------------------


def with_entry(func: Callable) -> Callable:
    """Mark a method as jac entry with this decorator."""
    # Ensure the functioin has 2 parameters (self, here).
    sig = inspect.signature(func, eval_str=True)
    param_count = len(sig.parameters)
    if param_count != 2:
        raise ValueError("Jac entry function must have exactly 2 parameters.")

    # Get the entry node from the type hints.
    second_param_name = list(sig.parameters.keys())[1]
    entry_node = typing.get_type_hints(func).get(second_param_name)

    # Mark the function as jac entry.
    setattr(func, "__jac_entry", entry_node)  # noqa: B010
    return func


def with_exit(func: Callable) -> Callable:
    """Mark a method as jac exit with this decorator."""
    # Ensure the functioin has 2 parameters (self, here).
    sig = inspect.signature(func, eval_str=True)
    param_count = len(sig.parameters)
    if param_count != 2:
        raise ValueError("Jac exit function must have exactly 2 parameters.")

    # Get the entry node from the type hints.
    second_param_name = list(sig.parameters.keys())[1]
    exit_node = typing.get_type_hints(func).get(second_param_name)

    # Mark the function as jac entry.
    setattr(func, "__jac_exit", exit_node)  # noqa: B010
    return func


# ----------------------------------------------------------------------------
# Functions.
# ----------------------------------------------------------------------------


def field(
    value: T | None = None,
    gen: None | Callable[[], T] = None,
    postinit: bool = False,
) -> T:
    """Set the default value to jac architype dataclass."""
    if postinit:
        return dc_field(init=False)
    if value is not None:
        gen = lambda: value  # noqa: E731
    assert gen is not None
    return _Jac.has_instance_default(gen_func=gen)


static = ClassVar
abstract = abstractmethod

jac_import = _Jac.jac_import
jac_test = _Jac.create_test
root = _Jac.get_root()
jobj = _Jac.get_object
_impl_patch_filename = _Jac.impl_patch_filename

root.spawn = types.MethodType(JacNode.spawn, root)
root.connect = types.MethodType(JacNode.connect, root)
root.disconnect = types.MethodType(JacNode.disconnect, root)
root.refs = types.MethodType(JacNode.refs, root)
