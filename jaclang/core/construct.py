"""Core constructs for Jac Language."""

from __future__ import annotations

import shelve
import unittest
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Callable, Optional
from uuid import UUID, uuid4

from jaclang.compiler.constant import EdgeDir
from jaclang.core.utils import collect_node_connections
from jaclang.plugin.spec import DSFunc


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
        return walk._jac_.spawn_call(self.obj)


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
            state["edge_ids"] = [e._jac_.id for e in edges]

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
        edg._jac_.attach(self.obj, nd)
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
                e._jac_.target
                and e._jac_.source
                and (
                    dir in [EdgeDir.OUT, EdgeDir.ANY]
                    and self.obj == e._jac_.source
                    and (not target_obj or e._jac_.target in target_obj)
                )
                or (
                    dir in [EdgeDir.IN, EdgeDir.ANY]
                    and self.obj == e._jac_.target
                    and (not target_obj or e._jac_.source in target_obj)
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
            if e._jac_.target and e._jac_.source:
                if (
                    dir in [EdgeDir.OUT, EdgeDir.ANY]
                    and self.obj == e._jac_.source
                    and (not target_obj or e._jac_.target in target_obj)
                ):
                    node_list.append(e._jac_.target)
                if (
                    dir in [EdgeDir.IN, EdgeDir.ANY]
                    and self.obj == e._jac_.target
                    and (not target_obj or e._jac_.source in target_obj)
                ):
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
    source_id: Optional[UUID] = None
    target_id: Optional[UUID] = None
    is_undirected: bool = False
    persistent: bool = False

    def __getstate__(self) -> dict:
        """Override getstate for pickle and shelve."""
        state = self.__dict__.copy()
        state.pop("obj")

        if self.source:
            state["source_id"] = self.source._jac_.id
            state.pop("source")

        if self.target:
            state["target_id"] = self.target._jac_.id
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
        src._jac_.edges.append(self.obj)
        trg._jac_.edges.append(self.obj)
        return self

    def detach(
        self, src: NodeArchitype, trg: NodeArchitype, is_undirected: bool = False
    ) -> None:
        """Detach edge from nodes."""
        self.is_undirected = is_undirected
        src._jac_.edges.remove(self.obj)
        trg._jac_.edges.remove(self.obj)
        self.source = None
        self.target = None
        del self

    def spawn_call(self, walk: WalkerArchitype) -> WalkerArchitype:
        """Invoke data spatial call."""
        if self.target:
            return walk._jac_.spawn_call(self.target)
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
                    if i._jac_.target:
                        self.next.append(i._jac_.target)
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
                    if i._jac_.target:
                        self.ignores.append(i._jac_.target)
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
        self._jac_: ObjectAnchor = ObjectAnchor(obj=self)

    def __hash__(self) -> int:
        """Override hash for architype."""
        return hash(self._jac_.id)

    def __eq__(self, other: object) -> bool:
        """Override equality for architype."""
        if not isinstance(other, Architype):
            return False
        else:
            return self._jac_.id == other._jac_.id

    def __repr__(self) -> str:
        """Override repr for architype."""
        return f"{self.__class__.__name__}"

    def __getstate__(self) -> dict:
        """Override getstate for pickle and shelve."""
        raise NotImplementedError


class NodeArchitype(Architype):
    """Node Architype Protocol."""

    _jac_: NodeAnchor

    def __init__(self) -> None:
        """Create node architype."""
        from jaclang.plugin.feature import JacFeature as Jac

        self._jac_: NodeAnchor = NodeAnchor(obj=self)
        Jac.context().save_obj(self, persistent=self._jac_.persistent)

    def save(self) -> None:
        """Save the node to the memory/storage hierarchy."""
        from jaclang.plugin.feature import JacFeature as Jac

        self._jac_.persistent = True
        Jac.context().save_obj(self, persistent=True)

    def __getstate__(self) -> dict:
        """Override getstate for pickle and shelve."""
        state = self.__dict__.copy()
        state["_jac_"] = self._jac_.__getstate__()
        return state

    def __setstate__(self, state: dict) -> None:
        """Override setstate for pickle and shelve."""
        self.__dict__.update(state)
        self._jac_ = NodeAnchor(obj=self)
        self._jac_.__setstate__(state["_jac_"])


class EdgeArchitype(Architype):
    """Edge Architype Protocol."""

    _jac_: EdgeAnchor
    persistent: bool = False

    def __init__(self) -> None:
        """Create edge architype."""
        from jaclang.plugin.feature import JacFeature as Jac

        self._jac_: EdgeAnchor = EdgeAnchor(obj=self)
        Jac.context().save_obj(self, persistent=self.persistent)

    def save(self) -> None:
        """Save the edge to the memory/storage hierarchy."""
        from jaclang.plugin.feature import JacFeature as Jac

        self.persistent = True
        Jac.context().save_obj(self, persistent=True)

    def __getstate__(self) -> dict:
        """Override getstate for pickle and shelve."""
        state = self.__dict__.copy()
        state["_jac_"] = self._jac_.__getstate__()
        return state

    def __setstate__(self, state: dict) -> None:
        """Override setstate for pickle and shelve."""
        self.__dict__.update(state)
        self._jac_ = EdgeAnchor(obj=self)
        self._jac_.__setstate__(state["_jac_"])

    def populate_nodes(self) -> None:
        """Populate nodes for the edges from node ids."""
        from jaclang.plugin.feature import JacFeature as Jac

        if self._jac_.source_id:
            obj = Jac.context().get_obj(self._jac_.source_id)
            if obj is None:
                raise ValueError(f"Node with id {self._jac_.source_id} not found.")
            elif not isinstance(obj, NodeArchitype):
                raise ValueError(
                    f"Object with id {self._jac_.source_id} is not a node."
                )
            else:
                self._jac_.source = obj
                self._jac_.source_id = None
        if self._jac_.target_id:
            obj = Jac.context().get_obj(self._jac_.target_id)
            if obj is None:
                raise ValueError(f"Node with id {self._jac_.target_id} not found.")
            elif not isinstance(obj, NodeArchitype):
                raise ValueError(
                    f"Object with id {self._jac_.target_id} is not a node."
                )
            else:
                self._jac_.target = obj
                self._jac_.target_id = None


class WalkerArchitype(Architype):
    """Walker Architype Protocol."""

    _jac_: WalkerAnchor

    def __init__(self) -> None:
        """Create walker architype."""
        self._jac_: WalkerAnchor = WalkerAnchor(obj=self)


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
        self._jac_.id = UUID(int=0)
        self._jac_.persistent = True

    def reset(self) -> None:
        """Reset the root."""
        self.reachable_nodes = []
        self.connections = set()
        self._jac_.edges = []


class Memory:
    """Memory module interface."""

    mem: dict[UUID, Architype] = {}
    save_obj_list: dict[UUID, Architype] = {}

    def __init__(self) -> None:
        """init."""
        pass

    def get_obj(self, obj_id: UUID) -> Architype | None:
        """Get object from memory."""
        return self.get_obj_from_store(obj_id)

    def get_obj_from_store(self, obj_id: UUID) -> Architype | None:
        """Get object from the underlying store."""
        ret = self.mem.get(obj_id)
        return ret

    def has_obj(self, obj_id: UUID) -> bool:
        """Check if the object exists."""
        return self.has_obj_in_store(obj_id)

    def has_obj_in_store(self, obj_id: UUID) -> bool:
        """Check if the object exists in the underlying store."""
        return obj_id in self.mem

    def save_obj(self, item: Architype, persistent: bool) -> None:
        """Save object."""
        self.mem[item._jac_.id] = item
        if persistent:
            # TODO: check if it needs to be saved, i.e. dirty or not
            self.save_obj_list[item._jac_.id] = item

    def commit(self) -> None:
        """Commit changes to persistent storage, if applicable."""
        pass

    def close(self) -> None:
        """Close any connection, if applicable."""
        self.mem.clear()


class ShelveStorage(Memory):
    """Shelve storage for jaclang runtime object."""

    storage: shelve.Shelf | None = None

    def __init__(self, session: str = "") -> None:
        """Init shelve storage."""
        super().__init__()
        if session:
            self.connect(session)

    def get_obj_from_store(self, obj_id: UUID) -> Architype | None:
        """Get object from the underlying store."""
        obj = super().get_obj_from_store(obj_id)
        if obj is None and self.storage:
            obj = self.storage.get(str(obj_id))
            if obj is not None:
                self.mem[obj_id] = obj

        return obj

    def has_obj_in_store(self, obj_id: UUID | str) -> bool:
        """Check if the object exists in the underlying store."""
        return obj_id in self.mem or (
            str(obj_id) in self.storage if self.storage else False
        )

    def commit(self) -> None:
        """Commit changes to persistent storage."""
        if self.storage is not None:
            for obj_id, obj in self.save_obj_list.items():
                self.storage[str(obj_id)] = obj
        self.save_obj_list.clear()

    def connect(self, session: str) -> None:
        """Connect to storage."""
        self.session = session
        self.storage = shelve.open(session)

    def close(self) -> None:
        """Close the storage."""
        super().close()
        self.commit()
        if self.storage:
            self.storage.close()
        self.storage = None


class ExecutionContext:
    """Default Execution Context implementation."""

    mem: Optional[Memory]
    root: Optional[Root]

    def __init__(self) -> None:
        """Create execution context."""
        super().__init__()
        self.mem = ShelveStorage()
        self.root = None

    def init_memory(self, session: str = "") -> None:
        """Initialize memory."""
        if session:
            self.mem = ShelveStorage(session)
        else:
            self.mem = Memory()

    def get_root(self) -> Root:
        """Get the root object."""
        if self.mem is None:
            raise ValueError("Memory not initialized")

        if not self.root:
            root = self.mem.get_obj(UUID(int=0))
            if root is None:
                self.root = Root()
                self.mem.save_obj(self.root, persistent=self.root._jac_.persistent)
            elif not isinstance(root, Root):
                raise ValueError(f"Invalid root object: {root}")
            else:
                self.root = root
        return self.root

    def get_obj(self, obj_id: UUID) -> Architype | None:
        """Get object from memory."""
        if self.mem is None:
            raise ValueError("Memory not initialized")

        return self.mem.get_obj(obj_id)

    def save_obj(self, item: Architype, persistent: bool) -> None:
        """Save object to memory."""
        if self.mem is None:
            raise ValueError("Memory not initialized")

        self.mem.save_obj(item, persistent)

    def reset(self) -> None:
        """Reset the execution context."""
        if self.mem:
            self.mem.close()
        self.mem = None
        self.root = None


exec_context: ContextVar[ExecutionContext | None] = ContextVar(
    "ExecutionContext", default=None
)


class JacTestResult(unittest.TextTestResult):
    """Jac test result class."""

    def __init__(
        self,
        stream,  # noqa
        descriptions,  # noqa
        verbosity: int,
        max_failures: Optional[int] = None,
    ) -> None:
        """Initialize FailFastTestResult object."""
        super().__init__(stream, descriptions, verbosity)  # noqa
        self.failures_count = JacTestCheck.failcount
        self.max_failures = max_failures

    def addFailure(self, test, err) -> None:  # noqa
        """Count failures and stop."""
        super().addFailure(test, err)
        self.failures_count += 1
        if self.max_failures is not None and self.failures_count >= self.max_failures:
            self.stop()

    def stop(self) -> None:
        """Stop the test execution."""
        self.shouldStop = True


class JacTextTestRunner(unittest.TextTestRunner):
    """Jac test runner class."""

    def __init__(self, max_failures: Optional[int] = None, **kwargs) -> None:  # noqa
        """Initialize JacTextTestRunner object."""
        self.max_failures = max_failures
        super().__init__(**kwargs)

    def _makeResult(self) -> JacTestResult:  # noqa
        """Override the method to return an instance of JacTestResult."""
        return JacTestResult(
            self.stream,
            self.descriptions,
            self.verbosity,
            max_failures=self.max_failures,
        )


class JacTestCheck:
    """Jac Testing and Checking."""

    test_case = unittest.TestCase()
    test_suite = unittest.TestSuite()
    breaker = False
    failcount = 0

    @staticmethod
    def reset() -> None:
        """Clear the test suite."""
        JacTestCheck.test_case = unittest.TestCase()
        JacTestCheck.test_suite = unittest.TestSuite()

    @staticmethod
    def run_test(xit: bool, maxfail: int | None, verbose: bool) -> None:
        """Run the test suite."""
        verb = 2 if verbose else 1
        runner = JacTextTestRunner(max_failures=maxfail, failfast=xit, verbosity=verb)
        result = runner.run(JacTestCheck.test_suite)
        if result.wasSuccessful():
            print("Passed successfully.")
        else:
            fails = len(result.failures)
            JacTestCheck.failcount += fails
            JacTestCheck.breaker = (
                (JacTestCheck.failcount >= maxfail) if maxfail else True
            )

    @staticmethod
    def add_test(test_fun: Callable) -> None:
        """Create a new test."""
        JacTestCheck.test_suite.addTest(unittest.FunctionTestCase(test_fun))

    def __getattr__(self, name: str) -> object:
        """Make convenient check.Equal(...) etc."""
        return getattr(JacTestCheck.test_case, name)
