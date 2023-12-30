"""Core constructs for Jac Language."""
from __future__ import annotations

import types
from dataclasses import dataclass, field
from typing import Any, Callable, Optional


from jaclang.compiler.constant import EdgeDir


@dataclass(eq=False)
class Architype:
    """Architype Protocol."""

    _jac_: ObjectAnchor
    _jac_entry_funcs_: list[DSFunc]
    _jac_exit_funcs_: list[DSFunc]


@dataclass(eq=False)
class NodeArchitype(Architype):
    """Node Architype Protocol."""

    _jac_: NodeAnchor


@dataclass(eq=False)
class EdgeArchitype(Architype):
    """Edge Architype Protocol."""

    _jac_: EdgeAnchor


@dataclass(eq=False)
class WalkerArchitype(Architype):
    """Walker Architype Protocol."""

    _jac_: WalkerAnchor


@dataclass(eq=False)
class Root(NodeArchitype):
    """Generic Root Node."""

    _jac_: NodeAnchor

    def __init__(self) -> None:
        """Create default root node."""
        self._jac_ = NodeAnchor(obj=self)
        self._jac_entry_funcs_ = []
        self._jac_exit_funcs_ = []


@dataclass(eq=False)
class GenericEdge(EdgeArchitype):
    """Generic Root Node."""

    _jac_: EdgeAnchor

    def __init__(self) -> None:
        """Create default root node."""
        self._jac_ = EdgeAnchor(obj=self)
        self._jac_entry_funcs_ = []
        self._jac_exit_funcs_ = []


@dataclass(eq=False)
class DSFunc:
    """Data Spatial Function."""

    name: str
    trigger: type | types.UnionType | tuple[type | types.UnionType, ...] | None
    func: Callable[[Any, Any], Any] | None = None

    def resolve(self, cls: type) -> None:
        """Resolve the function."""
        self.func = getattr(cls, self.name)


@dataclass(eq=False)
class ElementAnchor:
    """Element Anchor."""

    obj: Architype


@dataclass(eq=False)
class ObjectAnchor(ElementAnchor):
    """Object Anchor."""

    def spawn_call(self, walk: WalkerArchitype) -> None:
        """Invoke data spatial call."""
        walk._jac_.spawn_call(self.obj)


@dataclass(eq=False)
class NodeAnchor(ObjectAnchor):
    """Node Anchor."""

    obj: NodeArchitype
    edges: dict[EdgeDir, list[EdgeArchitype]] = field(
        default_factory=lambda: {EdgeDir.IN: [], EdgeDir.OUT: []}
    )

    def connect_node(self, nd: NodeArchitype, edg: EdgeArchitype) -> NodeArchitype:
        """Connect a node with given edge."""
        edg._jac_.attach(self.obj, nd)
        return self.obj

    def edges_to_nodes(
        self, dir: EdgeDir, filter_type: Optional[type]
    ) -> list[NodeArchitype]:
        """Get set of nodes connected to this node."""
        ret_nodes: list[NodeArchitype] = []
        if dir in [EdgeDir.OUT]:
            for i in self.edges[EdgeDir.OUT]:
                if i._jac_.target and (
                    not filter_type or isinstance(i._jac_.target, filter_type)
                ):
                    ret_nodes.append(i._jac_.target)
        elif dir in [EdgeDir.IN]:
            for i in self.edges[EdgeDir.IN]:
                if i._jac_.source and (
                    not filter_type or isinstance(i._jac_.source, filter_type)
                ):
                    ret_nodes.append(i._jac_.source)
        return ret_nodes


@dataclass(eq=False)
class EdgeAnchor(ObjectAnchor):
    """Edge Anchor."""

    obj: EdgeArchitype
    source: Optional[NodeArchitype] = None
    target: Optional[NodeArchitype] = None
    dir: Optional[EdgeDir] = None

    def apply_dir(self, dir: EdgeDir) -> EdgeAnchor:
        """Apply direction to edge."""
        self.dir = dir
        return self

    def attach(self, src: NodeArchitype, trg: NodeArchitype) -> EdgeAnchor:
        """Attach edge to nodes."""
        if self.dir == EdgeDir.IN:
            self.source = trg
            self.target = src
            self.source._jac_.edges[EdgeDir.IN].append(self.obj)
            self.target._jac_.edges[EdgeDir.OUT].append(self.obj)
        else:
            self.source = src
            self.target = trg
            self.source._jac_.edges[EdgeDir.OUT].append(self.obj)
            self.target._jac_.edges[EdgeDir.IN].append(self.obj)
        return self

    def spawn_call(self, walk: WalkerArchitype) -> None:
        """Invoke data spatial call."""
        if self.target:
            walk._jac_.spawn_call(self.target)


@dataclass(eq=False)
class WalkerAnchor(ObjectAnchor):
    """Walker Anchor."""

    obj: WalkerArchitype
    path: list[NodeArchitype] = field(default_factory=lambda: [])
    next: list[NodeArchitype] = field(default_factory=lambda: [])
    ignores: list[NodeArchitype] = field(default_factory=lambda: [])
    disengaged: bool = False

    def visit_node(
        self,
        nds: list[NodeArchitype | EdgeArchitype] | NodeArchitype | EdgeArchitype,
    ) -> bool:
        """Walker visits node."""
        nd_list: list[NodeArchitype | EdgeArchitype]
        if not isinstance(nds, list):
            nd_list = [nds]
        else:
            nd_list = list(nds)
        before_len = len(self.next)
        for i in nd_list:
            if i not in self.ignores:
                if isinstance(i, NodeArchitype):
                    self.next.append(i)
                elif isinstance(i, EdgeArchitype):
                    if i._jac_.target:
                        self.next.append(i._jac_.target)
                    else:
                        raise ValueError("Edge has no target.")
        return len(self.next) > before_len

    def ignore_node(
        self,
        nds: list[NodeArchitype | EdgeArchitype] | NodeArchitype | EdgeArchitype,
    ) -> bool:
        """Walker ignores node."""
        nd_list: list[NodeArchitype | EdgeArchitype]
        if not isinstance(nds, list):
            nd_list = [nds]
        else:
            nd_list = list(nds)
        before_len = len(self.ignores)
        for i in nd_list:
            if i not in self.ignores:
                if isinstance(i, NodeArchitype):
                    self.ignores.append(i)
                elif isinstance(i, EdgeArchitype):
                    if i._jac_.target:
                        self.ignores.append(i._jac_.target)
                    else:
                        raise ValueError("Edge has no target.")
        return len(self.ignores) > before_len

    def disengage_now(self) -> None:
        """Disengage walker from traversal."""
        self.disengaged = True

    def spawn_call(self, nd: Architype) -> None:
        """Invoke data spatial call."""
        self.path = []
        self.next = [nd]
        while len(self.next):
            nd = self.next.pop(0)
            for i in nd._jac_entry_funcs_:
                if not i.trigger or isinstance(self.obj, i.trigger):
                    if i.func:
                        i.func(nd, self.obj)
                    else:
                        raise ValueError(f"No function {i.name} to call.")
                if self.disengaged:
                    return
            for i in self.obj._jac_entry_funcs_:
                if not i.trigger or isinstance(nd, i.trigger):
                    if i.func:
                        i.func(self.obj, nd)
                    else:
                        raise ValueError(f"No function {i.name} to call.")
                if self.disengaged:
                    return
            for i in self.obj._jac_exit_funcs_:
                if not i.trigger or isinstance(nd, i.trigger):
                    if i.func:
                        i.func(self.obj, nd)
                    else:
                        raise ValueError(f"No function {i.name} to call.")
                if self.disengaged:
                    return
            for i in nd._jac_exit_funcs_:
                if not i.trigger or isinstance(self.obj, i.trigger):
                    if i.func:
                        i.func(nd, self.obj)
                    else:
                        raise ValueError(f"No function {i.name} to call.")
                if self.disengaged:
                    return
        self.ignores = []


root = Root()
