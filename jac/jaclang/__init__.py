"""The Jac Programming Language."""

import inspect
import os
from abc import abstractmethod as abstract
from dataclasses import dataclass, field as dc_field
from types import ModuleType
from typing import (
    Any,
    Callable,
    ClassVar,
    Generic,
    Type,
    TypeGuard,
    TypeVar,
    cast,
    override,
)

from jaclang.runtimelib.architype import (
    Architype,
    EdgeArchitype,
    GenericEdge as GenericEdgeArchitype,
    NodeArchitype,
    Root as RootArchitype,
    WalkerArchitype,
)
from jaclang.runtimelib.plugin.builtin import dotgen, jid, jobj  # noqa: F401
from jaclang.runtimelib.plugin.feature import EdgeDir, JacFeature as Jac, plugin_manager


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
    "obj",
    "node",
    "walker",
    "edge",
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


T = TypeVar("T")
S = TypeVar("S")  # S is a subtype of T.

# ----------------------------------------------------------------------------
# Base classes.
# ----------------------------------------------------------------------------


class Obj(Architype):
    """Base class for all the jac object types."""


class Walker(WalkerArchitype):
    """Base class for all the jac walker types."""

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


class Node(NodeArchitype):
    """Base class for all the jac node types."""

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


class Edge(EdgeArchitype):
    """Base class for all the jac edge types."""

    def spawn(self, archi: Walker) -> "Walker":
        """Spawn a new node from the walker."""
        return Jac.spawn_call(self, archi)  # type: ignore [arg-type, return-value]


# ----------------------------------------------------------------------------
# Internal decorators.
# ----------------------------------------------------------------------------


# This function is needed to mark the Root class is Root after apply the Jac.make_architype otherwise
# the instance of Root will be Any and it'll generate warnings.
def _root_factory(cls: Type["Root"]) -> Type["Root"]:
    """Create a new root class."""
    cls = dataclass(eq=False)(cls)  # type: ignore [arg-type, assignment]
    cls = Jac.make_architype(cls, RootArchitype, on_entry=[], on_exit=[])  # type: ignore [assignment, attr-defined]
    return cls


# This function is needed to mark the Root class is Root after apply the Jac.make_architype otherwise
# the instance of Root will be Any and it'll generate warnings.
def _generic_edge_factory(cls: Type["GenericEdge"]) -> Type["GenericEdge"]:
    """Create a new root class."""
    cls = dataclass(eq=False)(cls)  # type: ignore [arg-type, assignment]
    cls = Jac.make_architype(  # type: ignore [assignment, attr-defined]
        cls,
        GenericEdgeArchitype,
        on_entry=[],
        on_exit=[],
    )
    return cls


def _architype_factory(cls: Type[T], base: Type[S]) -> Type[S]:
    """Create a new architype class."""
    on_entry, on_exit = [], []
    for func in cls.__dict__.values():
        if hasattr(func, "__jac_entry"):
            on_entry.append(Jac.DSFunc(func.__name__, func))
        if hasattr(func, "__jac_exit"):
            on_exit.append(Jac.DSFunc(func.__name__, func))
    cls = dataclass(eq=False)(cls)  # type: ignore [arg-type, assignment]
    cls = Jac.make_architype(cls, base, on_entry, on_exit)  # type: ignore [assignment, attr-defined]
    return cls  # type: ignore [return-value]


@_root_factory
class Root(Node):
    """Base class for jac root type."""


@_generic_edge_factory
class GenericEdge(Edge):
    """Base class for jac root type."""


# ----------------------------------------------------------------------------
# JacList.
# ----------------------------------------------------------------------------


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


def obj(cls: Type[T]) -> Type[Obj]:
    """Decorator to mark a class as jac object."""
    return _architype_factory(cls, Obj)


def node(cls: Type[T]) -> Type[Node]:
    """Decorator to mark a class as jac node."""
    return _architype_factory(cls, Node)


def walker(cls: Type[T]) -> Type[Walker]:
    """Decorator to mark a class as jac walker."""
    return _architype_factory(cls, Walker)


def edge(cls: Type[T]) -> Type[Edge]:
    """Decorator to mark a class as jac edge."""
    return _architype_factory(cls, Edge)


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
