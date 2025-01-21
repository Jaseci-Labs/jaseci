"""The Jac Programming Language."""

import inspect
import os
from abc import ABCMeta, abstractmethod as abstract
from dataclasses import dataclass, field as dc_field
from types import ModuleType
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    Generic,
    Tuple,
    Type,
    TypeVar,
    override,
)

from jaclang.plugin.builtin import dotgen, jid  # noqa: F401
from jaclang.plugin.default import JacFeatureImpl
from jaclang.plugin.feature import JacFeature as Jac, plugin_manager
from jaclang.plugin.spec import EdgeDir
from jaclang.runtimelib.architype import GenericEdge, Root
from jaclang.runtimelib.context import ExecutionContext

__all__ = [
    # Jac types.
    "Obj",
    "Walker",
    "Node",
    "Edge",
    "List",
    "EdgeDir",
    "Root",
    # Decorators.
    "with_entry",
    "with_exit",
    "jac_test",
    "abstract",
    "override",
    # Functions.
    "jac_import",
    "field",
    # Builtin.
    "Jac",
    "root",
    "static",
    "dotgen",
    "jid",
    "jobj",
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
class _ArchiTypeBase:
    pass


class MetaCommon(ABCMeta):
    """Common metaclass for Jac types."""

    def __new__(  # noqa: D102
        cls,
        name: str,
        bases: Tuple[Type, ...],
        dct: Dict[str, Any],
        make_func: Callable[[list, list], Callable[[type], type]],
    ) -> "MetaCommon":

        # We have added this "__init__" to the jac base class just to make the type checkers happy.
        # Actually the dataclass decorator will create an __init__ function and assign it here bellow.
        if bases == (_ArchiTypeBase,) and "__init__" in dct:
            del dct["__init__"]

        on_entry, on_exit = [], []
        for func in dct.values():
            if hasattr(func, "__jac_entry"):
                on_entry.append(Jac.DSFunc(func.__name__, func))
            if hasattr(func, "__jac_exit"):
                on_exit.append(Jac.DSFunc(func.__name__, func))

        inst = super().__new__(cls, name, bases, dct)
        inst = dataclass(eq=False)(inst)  # type: ignore [arg-type, assignment]
        inst = make_func(on_entry, on_exit)(inst)  # type: ignore [assignment]
        return inst


class MetaObj(MetaCommon):  # noqa: D101
    def __new__(  # noqa: D102
        cls, name: str, bases: Tuple[Type, ...], dct: Dict[str, Any]
    ) -> "MetaCommon":
        return super().__new__(cls, name, bases, dct, Jac.make_obj)


class MetaWalker(MetaCommon):  # noqa: D101
    def __new__(  # noqa: D102
        cls, name: str, bases: Tuple[Type, ...], dct: Dict[str, Any]
    ) -> "MetaCommon":
        return super().__new__(cls, name, bases, dct, Jac.make_walker)


class MetaNode(MetaCommon):  # noqa: D101
    def __new__(  # noqa: D102
        cls, name: str, bases: Tuple[Type, ...], dct: Dict[str, Any]
    ) -> "MetaCommon":
        return super().__new__(cls, name, bases, dct, Jac.make_node)


class MetaEdge(MetaCommon):  # noqa: D101
    def __new__(  # noqa: D102
        cls, name: str, bases: Tuple[Type, ...], dct: Dict[str, Any]
    ) -> "MetaCommon":
        return super().__new__(cls, name, bases, dct, Jac.make_edge)


# ----------------------------------------------------------------------------
# Base classes.
# ----------------------------------------------------------------------------


class Obj(_ArchiTypeBase, metaclass=MetaObj):
    """Base class for all the jac object types."""

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Initialize Jac architype base."""


class Walker(_ArchiTypeBase, metaclass=MetaWalker):
    """Base class for all the jac walker types."""

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Initialize Jac architype base."""

    def spawn(self, node: "_ArchiTypeBase | Root") -> "Walker":
        """Spawn a new node from the walker."""
        return Jac.spawn_call(self, node)  # type: ignore [arg-type, return-value]

    def ignore(
        self,
        expr: """(
        Root
        | Node
        | Edge
        | list[Node | Root | Edge]
        | List[Node | Root | Edge]
        )""",
    ) -> bool:
        """Ignore statement."""
        return Jac.ignore(self, expr)  # type: ignore [arg-type]

    def visit(
        self,
        expr: """(
            Root
            | Node
            | Edge
            | list[Node | Root | Edge]
            | List[Node | Root | Edge]
        )""",
    ) -> bool:
        """Visit statement."""
        return Jac.visit_node(self, expr)  # type: ignore [arg-type]

    def disengage(self) -> None:
        """Disengage statement."""
        Jac.disengage(self)  # type: ignore [arg-type]


class Node(_ArchiTypeBase, metaclass=MetaNode):
    """Base class for all the jac node types."""

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Initialize Jac architype base."""

    def spawn(self, archi: _ArchiTypeBase) -> "Walker":
        """Spawn a new node from the walker."""
        return Jac.spawn_call(self, archi)  # type: ignore [arg-type, return-value]

    def connect(
        self,
        node: "Node | Root | List[Node | Root]",
        edge: "type[Edge] | Edge | None" = None,
        unidir: bool = False,
        conn_assign: tuple[tuple, tuple] | None = None,
        edges_only: bool = False,
    ) -> "List[Node | Root| Edge]":
        """Connect the current node to another node."""
        # TODO: The above edge type should be reviewed, as the bellow can also take None, Edge, type[Edge].
        ret = Jac.connect(
            left=self,  # type: ignore [arg-type]
            right=node,  # type: ignore [arg-type]
            edge_spec=Jac.build_edge(
                is_undirected=unidir, conn_type=edge, conn_assign=conn_assign  # type: ignore [arg-type]
            ),
            edges_only=edges_only,
        )
        return List(ret)  # type: ignore [arg-type]

    def disconnect(
        self,
        node: "Node | Root | List[Node | Root]",
        edge: "type[Edge] | None" = None,
        dir: EdgeDir = EdgeDir.OUT,
    ) -> bool:
        """Disconnect the current node from the graph."""
        filter_func = None
        if edge:
            filter_func = lambda edges: [  # noqa: E731
                ed for ed in edges if isinstance(ed, edge)
            ]
        return Jac.disconnect(self, node, dir=dir, filter_func=filter_func)  # type: ignore [arg-type]

    def refs(
        self,
        edge: "type[Edge] | None" = None,
        cond: "Callable[[Edge], bool] | None" = None,
        target: "Node | Root | List[Node|Root] | None" = None,
        dir: EdgeDir = EdgeDir.OUT,
        edges_only: bool = False,
    ) -> "List[Node | Root | Edge]":
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
        return List(ret)


class Edge(_ArchiTypeBase, metaclass=MetaEdge):
    """Base class for all the jac edge types."""

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Initialize Jac architype base."""

    def spawn(self, archi: _ArchiTypeBase) -> "Walker":
        """Spawn a new node from the walker."""
        return Jac.spawn_call(self, archi)  # type: ignore [arg-type, return-value]


class List(Generic[T], list[T]):
    """List with jac methods."""

    # Reuse the methods.
    connect = Node.connect
    disconnect = Node.disconnect
    refs = Node.refs

    def filter(
        self, ty: type[T] | None = None, fn: Callable[[T], bool] | None = None
    ) -> "List[T]":
        """Filter comprehension."""
        if ty and fn:
            return List(
                list(filter(lambda item: isinstance(item, ty) and fn(item), self))
            )
        if ty:
            return List(list(filter(lambda item: isinstance(item, ty), self)))
        if fn:
            return List(list(filter(fn, self)))
        return self

    def assign(self, attrs: tuple[str], values: tuple[Any]) -> "List[T]":
        """Assign Comprehension."""
        return List(Jac.assign_compr(self, (attrs, values)))


# ----------------------------------------------------------------------------
# Decorators.
# ----------------------------------------------------------------------------


def with_entry(func: Callable) -> Callable:
    """Mark a method as jac entry with this decorator."""
    setattr(func, "__jac_entry", True)  # noqa: B010
    return func


def with_exit(func: Callable) -> Callable:
    """Mark a method as jac exit with this decorator."""
    setattr(func, "__jac_exit", True)  # noqa: B010
    return func


# ----------------------------------------------------------------------------
# Functions.
# ----------------------------------------------------------------------------


def jac_import(
    target: str,
    lng: str | None = "jac",
    base_path: str | None = None,
    absorb: bool = False,
    cachable: bool = True,
    alias: str | None = None,
    override_name: str | None = None,
    items: dict[str, str | None] | None = None,
    reload_module: bool | None = False,
) -> tuple[ModuleType, ...]:
    """Import a module."""
    base_path = base_path or os.path.dirname(inspect.stack()[1].filename)
    return Jac.jac_import(
        target=target,
        lng=lng,
        base_path=base_path,
        absorb=absorb,
        cachable=cachable,
        mdl_alias=alias,
        override_name=override_name,
        items=items,
        reload_module=reload_module,
    )


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
    return Jac.has_instance_default(gen_func=gen)


# ----------------------------------------------------------------------------
# Builtin.
# ----------------------------------------------------------------------------

jac_test = Jac.create_test
static = ClassVar
jobj = Jac.get_object


# ----------------------------------------------------------------------------
# Root Node and Generic Edge.
# ----------------------------------------------------------------------------

Root._method_bounds = {
    "spawn": Node.spawn,
    "connect": Node.connect,
    "disconnect": Node.disconnect,
    "refs": Node.refs,
}

GenericEdge._method_bounds = {
    "spawn": Edge.spawn,
}

root = Jac.get_root()
root.load_method_bounds()


# Listen to context change and update the above global root here.
def _update_root() -> None:
    global root
    root = ExecutionContext.get_root()


ExecutionContext.on_ctx_change.append(lambda ctx: _update_root())
