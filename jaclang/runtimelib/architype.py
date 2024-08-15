"""Core constructs for Jac Language."""

from __future__ import annotations

import types
from dataclasses import dataclass, field
from typing import Any, Callable, Optional
from uuid import UUID, uuid4

from jaclang.compiler.constant import EdgeDir
from jaclang.runtimelib.utils import collect_node_connections


@dataclass(eq=False)
class ElementAnchor:
    """Element Anchor."""

    obj: Architype
    id: UUID = field(default_factory=uuid4)


@dataclass(eq=False)
class ObjectAnchor(ElementAnchor):
    """Object Anchor."""

    def spawn_call(self, walk: WalkerArchitype) -> WalkerArchitype:
        """Invoke data spatial call."""
        return walk.__jac__.spawn_call(self.obj)


@dataclass(eq=False)
class NodeAnchor(ObjectAnchor):
    """Node Anchor."""

    obj: NodeArchitype
    edges: list[EdgeArchitype] = field(default_factory=lambda: [])
    edge_ids: list[UUID] = field(default_factory=lambda: [])
    persistent: bool = False

    def __getstate__(self) -> dict:
        """Override getstate for pickle and shelve."""
        state = self.__dict__.copy()
        state.pop("obj")
        if self.edges and "edges" in state:
            edges = state.pop("edges")
            state["edge_ids"] = [e.__jac__.id for e in edges]

        return state

    def __setstate__(self, state: dict) -> None:
        """Override setstate for pickle and shelve."""
        self.__dict__.update(state)
        if "edge_ids" in state:
            self.edge_ids = state.pop("edge_ids")

    def populate_edges(self) -> None:
        """Populate edges from edge ids."""
        from jaclang.plugin.feature import JacFeature as Jac

        if len(self.edges) == 0 and len(self.edge_ids) > 0:
            for e_id in self.edge_ids:
                edge = Jac.context().get_obj(e_id)
                if edge is None:
                    raise ValueError(f"Edge with id {e_id} not found.")
                elif not isinstance(edge, EdgeArchitype):
                    raise ValueError(f"Object with id {e_id} is not an edge.")
                else:
                    self.edges.append(edge)
            self.edge_ids.clear()

    def connect_node(self, nd: NodeArchitype, edg: EdgeArchitype) -> NodeArchitype:
        """Connect a node with given edge."""
        edg.__jac__.attach(self.obj, nd)
        return self.obj

    def get_edges(
        self,
        dir: EdgeDir,
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
        target_obj: Optional[list[NodeArchitype]],
    ) -> list[EdgeArchitype]:
        """Get edges connected to this node."""
        self.populate_edges()

        edge_list: list[EdgeArchitype] = [*self.edges]
        ret_edges: list[EdgeArchitype] = []
        edge_list = filter_func(edge_list) if filter_func else edge_list
        for e in edge_list:
            if (
                e.__jac__.target
                and e.__jac__.source
                and (
                    dir in [EdgeDir.OUT, EdgeDir.ANY]
                    and self.obj == e.__jac__.source
                    and (not target_obj or e.__jac__.target in target_obj)
                )
                or (
                    dir in [EdgeDir.IN, EdgeDir.ANY]
                    and self.obj == e.__jac__.target
                    and (not target_obj or e.__jac__.source in target_obj)
                )
            ):
                ret_edges.append(e)
        return ret_edges

    def edges_to_nodes(
        self,
        dir: EdgeDir,
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
        target_obj: Optional[list[NodeArchitype]],
    ) -> list[NodeArchitype]:
        """Get set of nodes connected to this node."""
        self.populate_edges()
        for edge in self.edges:
            edge.populate_nodes()
        edge_list: list[EdgeArchitype] = [*self.edges]
        node_list: list[NodeArchitype] = []
        edge_list = filter_func(edge_list) if filter_func else edge_list
        for e in edge_list:
            if e.__jac__.target and e.__jac__.source:
                if (
                    dir in [EdgeDir.OUT, EdgeDir.ANY]
                    and self.obj == e.__jac__.source
                    and (not target_obj or e.__jac__.target in target_obj)
                ):
                    node_list.append(e.__jac__.target)
                if (
                    dir in [EdgeDir.IN, EdgeDir.ANY]
                    and self.obj == e.__jac__.target
                    and (not target_obj or e.__jac__.source in target_obj)
                ):
                    node_list.append(e.__jac__.source)
        return node_list

    def gen_dot(self, dot_file: Optional[str] = None) -> str:
        """Generate Dot file for visualizing nodes and edges."""
        visited_nodes: set[NodeAnchor] = set()
        connections: set[tuple[NodeArchitype, NodeArchitype, str]] = set()
        unique_node_id_dict = {}

        collect_node_connections(self, visited_nodes, connections)
        dot_content = 'digraph {\nnode [style="filled", shape="ellipse", fillcolor="invis", fontcolor="black"];\n'
        for idx, i in enumerate([nodes_.obj for nodes_ in visited_nodes]):
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


@dataclass(eq=False)
class EdgeAnchor(ObjectAnchor):
    """Edge Anchor."""

    obj: EdgeArchitype
    source: Optional[NodeArchitype] = None
    target: Optional[NodeArchitype] = None
    source_id: Optional[UUID] = None
    target_id: Optional[UUID] = None
    is_undirected: bool = False
    persistent: bool = False

    def __getstate__(self) -> dict:
        """Override getstate for pickle and shelve."""
        state = self.__dict__.copy()
        state.pop("obj")

        if self.source:
            state["source_id"] = self.source.__jac__.id
            state.pop("source")

        if self.target:
            state["target_id"] = self.target.__jac__.id
            state.pop("target")

        return state

    def __setstate__(self, state: dict) -> None:
        """Override setstate for pickle and shelve."""
        self.__dict__.update(state)

    def attach(
        self, src: NodeArchitype, trg: NodeArchitype, is_undirected: bool = False
    ) -> EdgeAnchor:
        """Attach edge to nodes."""
        self.source = src
        self.target = trg
        self.is_undirected = is_undirected
        src.__jac__.edges.append(self.obj)
        trg.__jac__.edges.append(self.obj)
        return self

    def detach(
        self, src: NodeArchitype, trg: NodeArchitype, is_undirected: bool = False
    ) -> None:
        """Detach edge from nodes."""
        self.is_undirected = is_undirected
        src.__jac__.edges.remove(self.obj)
        trg.__jac__.edges.remove(self.obj)
        self.source = None
        self.target = None
        del self

    def spawn_call(self, walk: WalkerArchitype) -> WalkerArchitype:
        """Invoke data spatial call."""
        if self.target:
            return walk.__jac__.spawn_call(self.target)
        else:
            raise ValueError("Edge has no target.")


@dataclass(eq=False)
class WalkerAnchor(ObjectAnchor):
    """Walker Anchor."""

    obj: WalkerArchitype
    path: list[Architype] = field(default_factory=lambda: [])
    next: list[Architype] = field(default_factory=lambda: [])
    ignores: list[Architype] = field(default_factory=lambda: [])
    disengaged: bool = False

    def visit_node(
        self,
        nds: (
            list[NodeArchitype | EdgeArchitype]
            | list[NodeArchitype]
            | list[EdgeArchitype]
            | NodeArchitype
            | EdgeArchitype
        ),
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
                    if i.__jac__.target:
                        self.next.append(i.__jac__.target)
                    else:
                        raise ValueError("Edge has no target.")
        return len(self.next) > before_len

    def ignore_node(
        self,
        nds: (
            list[NodeArchitype | EdgeArchitype]
            | list[NodeArchitype]
            | list[EdgeArchitype]
            | NodeArchitype
            | EdgeArchitype
        ),
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
                    if i.__jac__.target:
                        self.ignores.append(i.__jac__.target)
                    else:
                        raise ValueError("Edge has no target.")
        return len(self.ignores) > before_len

    def disengage_now(self) -> None:
        """Disengage walker from traversal."""
        self.disengaged = True

    def spawn_call(self, nd: Architype) -> WalkerArchitype:
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
                    return self.obj
            for i in self.obj._jac_entry_funcs_:
                if not i.trigger or isinstance(nd, i.trigger):
                    if i.func:
                        i.func(self.obj, nd)
                    else:
                        raise ValueError(f"No function {i.name} to call.")
                if self.disengaged:
                    return self.obj
            for i in self.obj._jac_exit_funcs_:
                if not i.trigger or isinstance(nd, i.trigger):
                    if i.func:
                        i.func(self.obj, nd)
                    else:
                        raise ValueError(f"No function {i.name} to call.")
                if self.disengaged:
                    return self.obj
            for i in nd._jac_exit_funcs_:
                if not i.trigger or isinstance(self.obj, i.trigger):
                    if i.func:
                        i.func(nd, self.obj)
                    else:
                        raise ValueError(f"No function {i.name} to call.")
                if self.disengaged:
                    return self.obj
        self.ignores = []
        return self.obj


class Architype:
    """Architype Protocol."""

    _jac_entry_funcs_: list[DSFunc]
    _jac_exit_funcs_: list[DSFunc]

    def __init__(self) -> None:
        """Create default architype."""
        self.__jac__: ObjectAnchor = ObjectAnchor(obj=self)

    def __hash__(self) -> int:
        """Override hash for architype."""
        return hash(self.__jac__.id)

    def __eq__(self, other: object) -> bool:
        """Override equality for architype."""
        if not isinstance(other, Architype):
            return False
        else:
            return self.__jac__.id == other.__jac__.id

    def __repr__(self) -> str:
        """Override repr for architype."""
        return f"{self.__class__.__name__}"

    def __getstate__(self) -> dict:
        """Override getstate for pickle and shelve."""
        raise NotImplementedError


class NodeArchitype(Architype):
    """Node Architype Protocol."""

    __jac__: NodeAnchor

    def __init__(self) -> None:
        """Create node architype."""
        from jaclang.plugin.feature import JacFeature as Jac

        self.__jac__: NodeAnchor = NodeAnchor(obj=self)
        Jac.context().save_obj(self, persistent=self.__jac__.persistent)

    def save(self) -> None:
        """Save the node to the memory/storage hierarchy."""
        from jaclang.plugin.feature import JacFeature as Jac

        self.__jac__.persistent = True
        Jac.context().save_obj(self, persistent=True)

    def __getstate__(self) -> dict:
        """Override getstate for pickle and shelve."""
        state = self.__dict__.copy()
        state["__jac__"] = self.__jac__.__getstate__()
        return state

    def __setstate__(self, state: dict) -> None:
        """Override setstate for pickle and shelve."""
        self.__dict__.update(state)
        self.__jac__ = NodeAnchor(obj=self)
        self.__jac__.__setstate__(state["__jac__"])


class EdgeArchitype(Architype):
    """Edge Architype Protocol."""

    __jac__: EdgeAnchor
    persistent: bool = False

    def __init__(self) -> None:
        """Create edge architype."""
        from jaclang.plugin.feature import JacFeature as Jac

        self.__jac__: EdgeAnchor = EdgeAnchor(obj=self)
        Jac.context().save_obj(self, persistent=self.persistent)

    def save(self) -> None:
        """Save the edge to the memory/storage hierarchy."""
        from jaclang.plugin.feature import JacFeature as Jac

        self.persistent = True
        Jac.context().save_obj(self, persistent=True)

    def __getstate__(self) -> dict:
        """Override getstate for pickle and shelve."""
        state = self.__dict__.copy()
        state["__jac__"] = self.__jac__.__getstate__()
        return state

    def __setstate__(self, state: dict) -> None:
        """Override setstate for pickle and shelve."""
        self.__dict__.update(state)
        self.__jac__ = EdgeAnchor(obj=self)
        self.__jac__.__setstate__(state["__jac__"])

    def populate_nodes(self) -> None:
        """Populate nodes for the edges from node ids."""
        from jaclang.plugin.feature import JacFeature as Jac

        if self.__jac__.source_id:
            obj = Jac.context().get_obj(self.__jac__.source_id)
            if obj is None:
                raise ValueError(f"Node with id {self.__jac__.source_id} not found.")
            elif not isinstance(obj, NodeArchitype):
                raise ValueError(
                    f"Object with id {self.__jac__.source_id} is not a node."
                )
            else:
                self.__jac__.source = obj
                self.__jac__.source_id = None
        if self.__jac__.target_id:
            obj = Jac.context().get_obj(self.__jac__.target_id)
            if obj is None:
                raise ValueError(f"Node with id {self.__jac__.target_id} not found.")
            elif not isinstance(obj, NodeArchitype):
                raise ValueError(
                    f"Object with id {self.__jac__.target_id} is not a node."
                )
            else:
                self.__jac__.target = obj
                self.__jac__.target_id = None


class WalkerArchitype(Architype):
    """Walker Architype Protocol."""

    __jac__: WalkerAnchor

    def __init__(self) -> None:
        """Create walker architype."""
        self.__jac__: WalkerAnchor = WalkerAnchor(obj=self)


class GenericEdge(EdgeArchitype):
    """Generic Root Node."""

    _jac_entry_funcs_ = []
    _jac_exit_funcs_ = []


class Root(NodeArchitype):
    """Generic Root Node."""

    _jac_entry_funcs_ = []
    _jac_exit_funcs_ = []
    reachable_nodes: list[NodeArchitype] = []
    connections: set[tuple[NodeArchitype, NodeArchitype, EdgeArchitype]] = set()

    def __init__(self) -> None:
        """Create root node."""
        super().__init__()
        self.__jac__.id = UUID(int=0)
        self.__jac__.persistent = True

    def reset(self) -> None:
        """Reset the root."""
        self.reachable_nodes = []
        self.connections = set()
        self.__jac__.edges = []


@dataclass(eq=False)
class DSFunc:
    """Data Spatial Function."""

    name: str
    trigger: type | types.UnionType | tuple[type | types.UnionType, ...] | None
    func: Callable[[Any, Any], Any] | None = None

    def resolve(self, cls: type) -> None:
        """Resolve the function."""
        self.func = getattr(cls, self.name)
