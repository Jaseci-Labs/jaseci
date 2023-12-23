"""Core constructs for Jac Language."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional


from jaclang.compiler.constant import EdgeDir


class Architype:
    """Architype Protocol."""

    _jac_: ObjectAnchor

    def __call__(self, target: Architype) -> None:
        """Call the architype's data spatial behavior."""
        if callable(self._jac_):
            return self._jac_(target)


@dataclass(eq=False)
class DSFunc:
    """Data Spatial Function."""

    name: str
    trigger: type | tuple[type, ...] | None
    func: Callable[[Any, Any], Any] | None = None

    def resolve(self, cls: type) -> None:
        """Resolve the function."""
        self.func = getattr(cls, self.name)


class RootTypeHook:
    """Abstract Root Node."""


@dataclass(eq=False)
class Root(RootTypeHook):
    """Generic Root Node."""

    _jac_: NodeAnchor | None = None

    def __post_init__(self) -> None:
        """Create default root node."""
        self._jac_ = NodeAnchor(obj=self, ds_entry_funcs=[], ds_exit_funcs=[])


@dataclass(eq=False)
class ElementAnchor:
    """Element Anchor."""

    obj: object


@dataclass(eq=False)
class ObjectAnchor(ElementAnchor):
    """Object Anchor."""

    ds_entry_funcs: list[DSFunc]
    ds_exit_funcs: list[DSFunc]


@dataclass(eq=False)
class NodeAnchor(ObjectAnchor):
    """Node Anchor."""

    edges: dict[EdgeDir, list[EdgeAnchor]] = field(
        default_factory=lambda: {EdgeDir.IN: [], EdgeDir.OUT: []}
    )

    def connect_node(self, nd: NodeAnchor, edg: EdgeAnchor) -> NodeAnchor:
        """Connect a node with given edge."""
        edg.attach(self, nd)
        return self

    def edges_to_nodes(self, dir: EdgeDir) -> list[NodeAnchor]:
        """Get set of nodes connected to this node."""
        ret_nodes: list[NodeAnchor] = []
        if dir in [EdgeDir.OUT, EdgeDir.ANY]:
            for i in self.edges[EdgeDir.OUT]:
                if i.target:
                    ret_nodes.append(i.target)
        elif dir in [EdgeDir.IN, EdgeDir.ANY]:
            for i in self.edges[EdgeDir.IN]:
                if i.source:
                    ret_nodes.append(i.source)
        return ret_nodes

    def __call__(self, walk: WalkerAnchor) -> None:
        """Invoke data spatial call."""
        walk(self)


@dataclass(eq=False)
class EdgeAnchor(ObjectAnchor):
    """Edge Anchor."""

    source: Optional[NodeAnchor] = None
    target: Optional[NodeAnchor] = None
    dir: Optional[EdgeDir] = None

    def apply_dir(self, dir: EdgeDir) -> EdgeAnchor:
        """Apply direction to edge."""
        self.dir = dir
        return self

    def attach(self, src: NodeAnchor, trg: NodeAnchor) -> EdgeAnchor:
        """Attach edge to nodes."""
        if self.dir == EdgeDir.IN:
            self.source = trg
            self.target = src
            self.source.edges[EdgeDir.IN].append(self)
            self.target.edges[EdgeDir.OUT].append(self)
        else:
            self.source = src
            self.target = trg
            self.source.edges[EdgeDir.OUT].append(self)
            self.target.edges[EdgeDir.IN].append(self)
        return self

    def __call__(self, walk: WalkerAnchor) -> None:
        """Invoke data spatial call."""
        if self.target:
            walk(self.target)


@dataclass(eq=False)
class WalkerAnchor(ObjectAnchor):
    """Walker Anchor."""

    path: list[NodeAnchor] = field(default_factory=lambda: [])
    next: list[NodeAnchor] = field(default_factory=lambda: [])
    ignores: list[NodeAnchor] = field(default_factory=lambda: [])
    disengaged: bool = False

    def visit_node(
        self, nds: list[NodeAnchor] | list[EdgeAnchor] | NodeAnchor | EdgeAnchor
    ) -> bool:
        """Walker visits node."""
        nd_list: list[NodeAnchor | EdgeAnchor]
        if not isinstance(nds, list):
            nd_list = [nds]
        else:
            nd_list = list(nds)
        before_len = len(self.next)
        for i in nd_list:
            if i not in self.ignores:
                if isinstance(i, NodeAnchor):
                    self.next.append(i)
                elif isinstance(i, EdgeAnchor):
                    if i.target:
                        self.next.append(i.target)
                    else:
                        raise ValueError("Edge has no target.")
        return len(self.next) > before_len

    def ignore_node(
        self, nds: list[NodeAnchor] | list[EdgeAnchor] | NodeAnchor | EdgeAnchor
    ) -> bool:
        """Walker ignores node."""
        nd_list: list[NodeAnchor | EdgeAnchor]
        if not isinstance(nds, list):
            nd_list = [nds]
        else:
            nd_list = list(nds)
        before_len = len(self.ignores)
        for i in nd_list:
            if i not in self.ignores:
                if isinstance(i, NodeAnchor):
                    self.ignores.append(i)
                elif isinstance(i, EdgeAnchor):
                    if i.target:
                        self.ignores.append(i.target)
                    else:
                        raise ValueError("Edge has no target.")
        return len(self.ignores) > before_len

    def disengage_now(self) -> None:
        """Disengage walker from traversal."""
        self.disengaged = True

    def __call__(self, nd: NodeAnchor) -> None:
        """Invoke data spatial call."""
        self.path = []
        self.next = [nd]
        while len(self.next):
            nd = self.next.pop(0)
            for i in nd.ds_entry_funcs:
                if not i.trigger or isinstance(self.obj, i.trigger):
                    if i.func:
                        i.func(nd.obj, self)
                    else:
                        raise ValueError(f"No function {i.name} to call.")
                if self.disengaged:
                    return
            for i in self.ds_entry_funcs:
                if not i.trigger or isinstance(nd.obj, i.trigger):
                    if i.func:
                        i.func(self.obj, nd)
                    else:
                        raise ValueError(f"No function {i.name} to call.")
                if self.disengaged:
                    return
            for i in self.ds_exit_funcs:
                if not i.trigger or isinstance(nd.obj, i.trigger):
                    if i.func:
                        i.func(self.obj, nd)
                    else:
                        raise ValueError(f"No function {i.name} to call.")
                if self.disengaged:
                    return
            for i in nd.ds_exit_funcs:
                if not i.trigger or isinstance(self.obj, i.trigger):
                    if i.func:
                        i.func(nd.obj, self)
                    else:
                        raise ValueError(f"No function {i.name} to call.")
                if self.disengaged:
                    return
            self.path.append(nd)
        self.ignores = []


root = Root()
