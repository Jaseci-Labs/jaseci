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
    TypeGuard,
    TypeVar,
    cast,
    override,
)

from jaclang.plugin.builtin import dotgen, jid, jobj  # noqa: F401
from jaclang.plugin.default import JacFeatureImpl
from jaclang.plugin.feature import JacFeature as Jac, plugin_manager
from jaclang.plugin.spec import EdgeDir

__all__ = [
    # Jac types.
    "Obj",
    "Walker",
    "Node",
    "Edge",
    "JacList",
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
S = TypeVar("S")  # S is a subtype of T.

# ----------------------------------------------------------------------------
# Meta classes.
# ----------------------------------------------------------------------------


# Since the meta class of the architypes are changine the base class to it's
# suitable archi type, If a class doesn't have a parent class (ie. by default
# inherit from object) __bases__ will be immutable. So we need to use a dummy
# parent class to make it mutable.
#
# Reference: https://stackoverflow.com/a/9639512/10846399
#
class _ArchiTypeBase:

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """Initialize Jac architype base."""


class JacMeta(ABCMeta):
    """Common metaclass for Jac types."""

    def __new__(  # noqa: D102
        cls,
        name: str,
        bases: Tuple[Type, ...],
        dct: Dict[str, Any],
    ) -> "JacMeta":

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
        inst = inst._MAKE_FN(on_entry, on_exit)(inst)  # type: ignore [assignment, attr-defined]
        return inst


# ----------------------------------------------------------------------------
# Base classes.
# ----------------------------------------------------------------------------


class Obj(_ArchiTypeBase, metaclass=JacMeta):
    """Base class for all the jac object types."""

    _MAKE_FN = Jac.make_obj


class Walker(_ArchiTypeBase, metaclass=JacMeta):
    """Base class for all the jac walker types."""

    _MAKE_FN = Jac.make_walker

    def spawn(self, node: "Node | Root") -> "Walker":
        """Spawn a new node from the walker."""
        return Jac.spawn_call(self, node)  # type: ignore [arg-type, return-value]

    def ignore(
        self,
        expr: """(
        Root
        | Node
        | Edge
        | list[Node | Root | Edge]
        | JacList[Node | Root | Edge]
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
            | JacList[Node | Root | Edge]
        )""",
    ) -> bool:
        """Visit statement."""
        return Jac.visit_node(self, expr)  # type: ignore [arg-type]

    def disengage(self) -> None:
        """Disengage statement."""
        Jac.disengage(self)  # type: ignore [arg-type]


class Node(_ArchiTypeBase, metaclass=JacMeta):
    """Base class for all the jac node types."""

    _MAKE_FN = Jac.make_node

    def spawn(self, archi: Walker) -> "Walker":
        """Spawn a new node from the walker."""
        return Jac.spawn_call(self, archi)  # type: ignore [arg-type, return-value]

    def connect(
        self,
        node: "Node | Root | JacList[Node | Root]",
        edge: "type[Edge] | Edge | None" = None,
        undir: bool = False,
        conn_assign: tuple[tuple, tuple] | None = None,
        edges_only: bool = False,
    ) -> "JacList[Node | Root| Edge]":
        """Connect the current node to another node."""
        # TODO: The above edge type should be reviewed, as the bellow can also take None, Edge, type[Edge].
        ret = Jac.connect(
            left=self,  # type: ignore [arg-type]
            right=node,  # type: ignore [arg-type]
            edge_spec=Jac.build_edge(
                is_undirected=undir, conn_type=edge, conn_assign=conn_assign  # type: ignore [arg-type]
            ),
            edges_only=edges_only,
        )
        return JacList(ret)  # type: ignore [arg-type]

    def disconnect(
        self,
        node: "Node | Root | JacList[Node | Root]",
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
        target: "Node | Root | JacList[Node|Root] | None" = None,
        dir: EdgeDir = EdgeDir.OUT,
        edges_only: bool = False,
    ) -> "JacList[Node | Root | Edge]":
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
        return JacList(ret)


class Root(_ArchiTypeBase, metaclass=JacMeta):
    """Base class for jac root type."""

    _MAKE_FN = Jac.make_root

    def spawn(self, archi: Walker) -> "Walker":
        """Spawn a new node from the walker."""
        return Jac.spawn_call(self, archi)  # type: ignore [arg-type, return-value]

    def connect(
        self,
        node: "Node | Root | JacList[Node | Root]",
        edge: "type[Edge] | Edge | None" = None,
        undir: bool = False,
        conn_assign: tuple[tuple, tuple] | None = None,
        edges_only: bool = False,
    ) -> "JacList[Node | Root| Edge]":
        """Connect the current node to another node."""
        # TODO: The above edge type should be reviewed, as the bellow can also take None, Edge, type[Edge].
        ret = Jac.connect(
            left=self,  # type: ignore [arg-type]
            right=node,  # type: ignore [arg-type]
            edge_spec=Jac.build_edge(
                is_undirected=undir, conn_type=edge, conn_assign=conn_assign  # type: ignore [arg-type]
            ),
            edges_only=edges_only,
        )
        return JacList(ret)  # type: ignore [arg-type]

    def disconnect(
        self,
        node: "Node | Root | JacList[Node | Root]",
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
        target: "Node | Root | JacList[Node|Root] | None" = None,
        dir: EdgeDir = EdgeDir.OUT,
        edges_only: bool = False,
    ) -> "JacList[Node | Root | Edge]":
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
        return JacList(ret)


class Edge(_ArchiTypeBase, metaclass=JacMeta):
    """Base class for all the jac edge types."""

    _MAKE_FN = Jac.make_edge

    def spawn(self, archi: Walker) -> "Walker":
        """Spawn a new node from the walker."""
        return Jac.spawn_call(self, archi)  # type: ignore [arg-type, return-value]


class GenericEdge(_ArchiTypeBase, metaclass=JacMeta):
    """Base class for jac root type."""

    _MAKE_FN = Jac.make_generic_edge

    def spawn(self, archi: Walker) -> "Walker":
        """Spawn a new node from the walker."""
        return Jac.spawn_call(self, archi)  # type: ignore [arg-type, return-value]


class JacList(Generic[T], list[T]):
    """List with jac methods."""

    # Reuse the methods.
    connect = Node.connect
    disconnect = Node.disconnect
    refs = Node.refs

    def filter(
        self,
        ty: Type[S] | None = None,
        fn: Callable[[T | S], TypeGuard[S]] | None = None,
    ) -> "JacList[S]":
        """Filter comprehension."""
        if ty and fn:
            return JacList([item for item in self if isinstance(item, ty) and fn(item)])
        if ty:
            return JacList([item for item in self if isinstance(item, ty)])
        if fn:
            return JacList(list(filter(fn, self)))
        return cast(JacList[S], self)

    def assign(self, attrs: tuple[str], values: tuple[Any]) -> "JacList[T]":
        """Assign Comprehension."""
        return JacList(Jac.assign_compr(self, (attrs, values)))


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
    value: T = None,  # type: ignore [assignment]
    gen: Callable[[], T] | None = None,
    postinit: bool = False,
) -> T:
    """Set the default value to jac architype dataclass."""
    if postinit:
        return dc_field(init=False)
    gen = gen or (lambda: value)  # noqa: E731
    return Jac.has_instance_default(gen_func=gen)  # type: ignore


# ----------------------------------------------------------------------------
# Builtin.
# ----------------------------------------------------------------------------

jac_test = Jac.create_test
static = ClassVar


def root() -> Root:
    """Get Root."""
    return cast(Root, Jac.get_root())
