"""Core constructs for Jac Language."""

from __future__ import annotations

# import shelve
import types
import unittest
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Union


from jaclang.compiler.constant import EdgeDir
from jaclang.core.utils import collect_node_connections


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
    edges: list[EdgeArchitype] = field(default_factory=lambda: [])

    def connect_node(self, nd: NodeArchitype, edg: EdgeArchitype) -> NodeArchitype:
        """Connect a node with given edge."""
        edg._jac_.attach(self.obj, nd)
        return self.obj

    def get_edges(
        self,
        dir: EdgeDir,
        filter_type: Optional[type],
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
    ) -> list[EdgeArchitype]:
        """Get edges connected to this node."""
        edge_list: list[EdgeArchitype] = [*self.edges]
        ret_edges: list[EdgeArchitype] = []
        if filter_type:
            edge_list = [e for e in edge_list if isinstance(e, filter_type)]
        edge_list = filter_func(edge_list) if filter_func else edge_list
        for e in edge_list:
            if (
                e._jac_.target
                and e._jac_.source
                and (dir in [EdgeDir.OUT, EdgeDir.ANY] and self.obj == e._jac_.source)
                or (dir in [EdgeDir.IN, EdgeDir.ANY] and self.obj == e._jac_.target)
            ):
                ret_edges.append(e)
        return ret_edges

    def edges_to_nodes(
        self,
        dir: EdgeDir,
        filter_type: Optional[type],
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
    ) -> list[NodeArchitype]:
        """Get set of nodes connected to this node."""
        edge_list: list[EdgeArchitype] = [*self.edges]
        node_list: list[NodeArchitype] = []
        if filter_type:
            edge_list = [e for e in edge_list if isinstance(e, filter_type)]
        edge_list = filter_func(edge_list) if filter_func else edge_list
        for e in edge_list:
            if e._jac_.target and e._jac_.source:
                if dir in [EdgeDir.OUT, EdgeDir.ANY] and self.obj == e._jac_.source:
                    node_list.append(e._jac_.target)
                if dir in [EdgeDir.IN, EdgeDir.ANY] and self.obj == e._jac_.target:
                    node_list.append(e._jac_.source)
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
    is_undirected: bool = False

    def attach(
        self, src: NodeArchitype, trg: NodeArchitype, is_undirected: bool = False
    ) -> EdgeAnchor:
        """Attach edge to nodes."""
        self.source = src
        self.target = trg
        self.is_undirected = is_undirected
        src._jac_.edges.append(self.obj)
        trg._jac_.edges.append(self.obj)
        return self

    def detach(
        self, src: NodeArchitype, trg: NodeArchitype, is_undirected: bool = False
    ) -> EdgeAnchor:
        """Detach edge from nodes."""
        self.source = src  # TODO: Delete me, don't keep attached
        self.target = trg  # TODO: Delete me, don't keep attached
        self.is_undirected = is_undirected
        src._jac_.edges.remove(self.obj)
        trg._jac_.edges.remove(self.obj)
        return self

    def spawn_call(self, walk: WalkerArchitype) -> None:
        """Invoke data spatial call."""
        if self.target:
            walk._jac_.spawn_call(self.target)


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


class Architype:
    """Architype Protocol."""

    _jac_entry_funcs_: list[DSFunc]
    _jac_exit_funcs_: list[DSFunc]

    def __init__(self) -> None:
        """Create default architype."""
        self._jac_: ObjectAnchor = ObjectAnchor(obj=self)


class NodeArchitype(Architype):
    """Node Architype Protocol."""

    def __init__(self) -> None:
        """Create node architype."""
        self._jac_: NodeAnchor = NodeAnchor(obj=self)


class EdgeArchitype(Architype):
    """Edge Architype Protocol."""

    def __init__(self) -> None:
        """Create edge architype."""
        self._jac_: EdgeAnchor = EdgeAnchor(obj=self)


class WalkerArchitype(Architype):
    """Walker Architype Protocol."""

    def __init__(self) -> None:
        """Create walker architype."""
        self._jac_: WalkerAnchor = WalkerAnchor(obj=self)


class Root(NodeArchitype):
    """Generic Root Node."""

    _jac_entry_funcs_ = []
    _jac_exit_funcs_ = []
    reachable_nodes: list[NodeArchitype] = []
    connections: set[tuple[NodeArchitype, NodeArchitype, EdgeArchitype]] = set()

    def reset(self) -> None:
        """Reset the root."""
        self.reachable_nodes = []
        self.connections = set()
        self._jac_.edges = []


class GenericEdge(EdgeArchitype):
    """Generic Root Node."""

    _jac_entry_funcs_ = []
    _jac_exit_funcs_ = []


@dataclass(eq=False)
class DSFunc:
    """Data Spatial Function."""

    name: str
    trigger: type | types.UnionType | tuple[type | types.UnionType, ...] | None
    func: Callable[[Any, Any], Any] | None = None

    def resolve(self, cls: type) -> None:
        """Resolve the function."""
        self.func = getattr(cls, self.name)


class JacTestCheck:
    """Jac Testing and Checking."""

    test_case = unittest.TestCase()
    test_suite = unittest.TestSuite()

    @staticmethod
    def reset() -> None:
        """Clear the test suite."""
        JacTestCheck.test_case = unittest.TestCase()
        JacTestCheck.test_suite = unittest.TestSuite()

    @staticmethod
    def run_test() -> None:
        """Run the test suite."""
        unittest.TextTestRunner().run(JacTestCheck.test_suite)

    @staticmethod
    def add_test(test_fun: Callable) -> None:
        """Create a new test."""
        JacTestCheck.test_suite.addTest(unittest.FunctionTestCase(test_fun))

    def __getattr__(self, name: str) -> Union[bool, Any]:
        """Make convenient check.Equal(...) etc."""
        return getattr(JacTestCheck.test_case, "assert" + name)


root = Root()
