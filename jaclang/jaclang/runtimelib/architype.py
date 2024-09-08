"""Core constructs for Jac Language."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields, is_dataclass
from enum import IntEnum
from logging import getLogger
from pickle import dumps
from types import UnionType
from typing import Any, Callable, ClassVar, Iterable, Optional, TypeVar
from uuid import UUID, uuid4

from jaclang.compiler.constant import EdgeDir
from jaclang.runtimelib.utils import collect_node_connections

logger = getLogger(__name__)

TARCH = TypeVar("TARCH", bound="Architype")
TANCH = TypeVar("TANCH", bound="Anchor")


class AccessLevel(IntEnum):
    """Access level enum."""

    NO_ACCESS = -1
    READ = 0
    CONNECT = 1
    WRITE = 2

    @staticmethod
    def cast(val: int | str | AccessLevel) -> AccessLevel:
        """Cast access level."""
        match val:
            case int():
                return AccessLevel(val)
            case str():
                return AccessLevel[val]
            case _:
                return val


@dataclass
class Access:
    """Access Structure."""

    anchors: dict[str, AccessLevel] = field(default_factory=dict)

    def check(self, anchor: str) -> AccessLevel:
        """Validate access."""
        return self.anchors.get(anchor, AccessLevel.NO_ACCESS)


@dataclass
class Permission:
    """Anchor Access Handler."""

    all: AccessLevel = AccessLevel.NO_ACCESS
    roots: Access = field(default_factory=Access)


@dataclass
class AnchorReport:
    """Report Handler."""

    id: str
    context: dict[str, Any]


@dataclass(eq=False, repr=False, kw_only=True)
class Anchor:
    """Object Anchor."""

    architype: Architype
    id: UUID = field(default_factory=uuid4)
    root: Optional[UUID] = None
    access: Permission = field(default_factory=Permission)
    persistent: bool = False
    hash: int = 0

    ##########################################################################
    #                             ACCESS CONTROL: TODO: Make Base Type       #
    ##########################################################################

    def allow_root(
        self, root_id: UUID, level: AccessLevel | int | str = AccessLevel.READ
    ) -> None:
        """Allow all access from target root graph to current Architype."""
        level = AccessLevel.cast(level)
        access = self.access.roots

        _root_id = str(root_id)
        if level != access.anchors.get(_root_id, AccessLevel.NO_ACCESS):
            access.anchors[_root_id] = level

    def disallow_root(
        self, root_id: UUID, level: AccessLevel | int | str = AccessLevel.READ
    ) -> None:
        """Disallow all access from target root graph to current Architype."""
        level = AccessLevel.cast(level)
        access = self.access.roots

        access.anchors.pop(str(root_id), None)

    def unrestrict(self, level: AccessLevel | int | str = AccessLevel.READ) -> None:
        """Allow everyone to access current Architype."""
        level = AccessLevel.cast(level)
        if level != self.access.all:
            self.access.all = level

    def restrict(self) -> None:
        """Disallow others to access current Architype."""
        if self.access.all > AccessLevel.NO_ACCESS:
            self.access.all = AccessLevel.NO_ACCESS

    def has_read_access(self, to: Anchor) -> bool:
        """Read Access Validation."""
        if not (access_level := self.access_level(to) > AccessLevel.NO_ACCESS):
            logger.info(
                f"Current root doesn't have read access to {to.__class__.__name__}[{to.id}]"
            )
        return access_level

    def has_connect_access(self, to: Anchor) -> bool:
        """Write Access Validation."""
        if not (access_level := self.access_level(to) > AccessLevel.READ):
            logger.info(
                f"Current root doesn't have connect access to {to.__class__.__name__}[{to.id}]"
            )
        return access_level

    def has_write_access(self, to: Anchor) -> bool:
        """Write Access Validation."""
        if not (access_level := self.access_level(to) > AccessLevel.CONNECT):
            logger.info(
                f"Current root doesn't have write access to {to.__class__.__name__}[{to.id}]"
            )
        return access_level

    def access_level(self, to: Anchor) -> AccessLevel:
        """Access validation."""
        if not to.persistent:
            return AccessLevel.WRITE

        from jaclang.plugin.feature import JacFeature as Jac

        jctx = Jac.get_context()

        jroot = jctx.root

        # if current root is system_root
        # if current root id is equal to target anchor's root id
        # if current root is the target anchor
        if jroot == jctx.system_root or jroot.id == to.root or jroot == to:
            return AccessLevel.WRITE

        access_level = AccessLevel.NO_ACCESS

        # if target anchor have set access.all
        if (to_access := to.access).all > AccessLevel.NO_ACCESS:
            access_level = to_access.all

        # if target anchor's root have set allowed roots
        # if current root is allowed to the whole graph of target anchor's root
        if to.root and isinstance(to_root := jctx.mem.find_one(to.root), Anchor):
            if to_root.access.all > access_level:
                access_level = to_root.access.all

            level = to_root.access.roots.check(str(jroot.id))
            if level > AccessLevel.NO_ACCESS and access_level == AccessLevel.NO_ACCESS:
                access_level = level

        # if target anchor have set allowed roots
        # if current root is allowed to target anchor
        level = to_access.roots.check(str(jroot.id))
        if level > AccessLevel.NO_ACCESS and access_level == AccessLevel.NO_ACCESS:
            access_level = level

        return access_level

    # ---------------------------------------------------------------------- #

    def save(self) -> None:
        """Save Anchor."""
        from jaclang.plugin.feature import JacFeature as Jac

        jctx = Jac.get_context()

        self.persistent = True
        self.root = jctx.root.id

        jctx.mem.set(self.id, self)

    def destroy(self) -> None:
        """Destroy Anchor."""
        from jaclang.plugin.feature import JacFeature as Jac

        jctx = Jac.get_context()

        if jctx.root.has_write_access(self):
            jctx.mem.remove(self.id)

    def is_populated(self) -> bool:
        """Check if state."""
        return "architype" in self.__dict__

    def make_stub(self: TANCH) -> TANCH:
        """Return unsynced copy of anchor."""
        if self.is_populated():
            unloaded = object.__new__(self.__class__)
            unloaded.id = self.id
            return unloaded
        return self

    def populate(self) -> None:
        """Retrieve the Architype from db and return."""
        from jaclang.plugin.feature import JacFeature as Jac

        jsrc = Jac.get_context().mem

        if anchor := jsrc.find_by_id(self.id):
            self.__dict__.update(anchor.__dict__)

    def __getattr__(self, name: str) -> object:
        """Trigger load if detects unloaded state."""
        if not self.is_populated():
            self.populate()

            if not self.is_populated():
                raise ValueError(
                    f"{self.__class__.__name__} [{self.id}] is not a valid reference!"
                )

            return getattr(self, name)

        raise AttributeError(
            f"'{self.__class__.__name__}' object has not attribute '{name}'"
        )

    def __getstate__(self) -> dict[str, Any]:  # NOTE: May be better type hinting
        """Serialize Anchor."""
        if self.is_populated():
            unlinked = object.__new__(self.architype.__class__)
            unlinked.__dict__.update(self.architype.__dict__)
            unlinked.__dict__.pop("__jac__", None)

            return {
                "id": self.id,
                "architype": unlinked,
                "root": self.root,
                "access": self.access,
                "persistent": self.persistent,
            }
        else:
            return {"id": self.id}

    def __setstate__(self, state: dict[str, Any]) -> None:
        """Deserialize Anchor."""
        self.__dict__.update(state)

        if self.is_populated() and self.architype:
            self.architype.__jac__ = self
            self.hash = hash(dumps(self))

    def __repr__(self) -> str:
        """Override representation."""
        if self.is_populated():
            attrs = ""
            for f in fields(self):
                if f.name in self.__dict__:
                    attrs += f"{f.name}={self.__dict__[f.name]}, "
            attrs = attrs[:-2]
        else:
            attrs = f"id={self.id}"

        return f"{self.__class__.__name__}({attrs})"

    def report(self) -> AnchorReport:
        """Report Anchor."""
        return AnchorReport(
            id=self.id.hex,
            context=(
                asdict(self.architype)
                if is_dataclass(self.architype) and not isinstance(self.architype, type)
                else {}
            ),
        )

    def __hash__(self) -> int:
        """Override hash for anchor."""
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        """Override equal implementation."""
        if isinstance(other, Anchor):
            return self.__class__ is other.__class__ and self.id == other.id

        return False


@dataclass(eq=False, repr=False, kw_only=True)
class NodeAnchor(Anchor):
    """Node Anchor."""

    architype: NodeArchitype
    edges: list[EdgeAnchor]

    def get_edges(
        self,
        dir: EdgeDir,
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
        target_obj: Optional[list[NodeArchitype]],
    ) -> list[EdgeArchitype]:
        """Get edges connected to this node."""
        from jaclang.plugin.feature import JacFeature as Jac

        root = Jac.get_root().__jac__
        ret_edges: list[EdgeArchitype] = []
        for anchor in self.edges:
            if (
                (source := anchor.source)
                and (target := anchor.target)
                and (not filter_func or filter_func([anchor.architype]))
                and source.architype
                and target.architype
            ):
                if (
                    dir in [EdgeDir.OUT, EdgeDir.ANY]
                    and self == source
                    and (not target_obj or target.architype in target_obj)
                    and root.has_read_access(target)
                ):
                    ret_edges.append(anchor.architype)
                if (
                    dir in [EdgeDir.IN, EdgeDir.ANY]
                    and self == target
                    and (not target_obj or source.architype in target_obj)
                    and root.has_read_access(source)
                ):
                    ret_edges.append(anchor.architype)
        return ret_edges

    def edges_to_nodes(
        self,
        dir: EdgeDir,
        filter_func: Optional[Callable[[list[EdgeArchitype]], list[EdgeArchitype]]],
        target_obj: Optional[list[NodeArchitype]],
    ) -> list[NodeArchitype]:
        """Get set of nodes connected to this node."""
        from jaclang.plugin.feature import JacFeature as Jac

        root = Jac.get_root().__jac__
        ret_edges: list[NodeArchitype] = []
        for anchor in self.edges:
            if (
                (source := anchor.source)
                and (target := anchor.target)
                and (not filter_func or filter_func([anchor.architype]))
                and source.architype
                and target.architype
            ):
                if (
                    dir in [EdgeDir.OUT, EdgeDir.ANY]
                    and self == source
                    and (not target_obj or target.architype in target_obj)
                    and root.has_read_access(target)
                ):
                    ret_edges.append(target.architype)
                if (
                    dir in [EdgeDir.IN, EdgeDir.ANY]
                    and self == target
                    and (not target_obj or source.architype in target_obj)
                    and root.has_read_access(source)
                ):
                    ret_edges.append(source.architype)
        return ret_edges

    def remove_edge(self, edge: EdgeAnchor) -> None:
        """Remove reference without checking sync status."""
        for idx, ed in enumerate(self.edges):
            if ed.id == edge.id:
                self.edges.pop(idx)
                break

    def gen_dot(self, dot_file: Optional[str] = None) -> str:
        """Generate Dot file for visualizing nodes and edges."""
        visited_nodes: set[NodeAnchor] = set()
        connections: set[tuple[NodeArchitype, NodeArchitype, str]] = set()
        unique_node_id_dict = {}

        collect_node_connections(self, visited_nodes, connections)
        dot_content = 'digraph {\nnode [style="filled", shape="ellipse", fillcolor="invis", fontcolor="black"];\n'
        for idx, i in enumerate([nodes_.architype for nodes_ in visited_nodes]):
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

    def spawn_call(self, walk: WalkerAnchor) -> WalkerArchitype:
        """Invoke data spatial call."""
        return walk.spawn_call(self)

    def destroy(self) -> None:
        """Destroy Anchor."""
        from jaclang.plugin.feature import JacFeature as Jac

        jctx = Jac.get_context()

        if jctx.root.has_write_access(self):
            for edge in self.edges:
                edge.destroy()

            jctx.mem.remove(self.id)

    def __getstate__(self) -> dict[str, object]:
        """Serialize Node Anchor."""
        state = super().__getstate__()

        if self.is_populated():
            state["edges"] = [edge.make_stub() for edge in self.edges]

        return state


@dataclass(eq=False, repr=False, kw_only=True)
class EdgeAnchor(Anchor):
    """Edge Anchor."""

    architype: EdgeArchitype
    source: NodeAnchor
    target: NodeAnchor
    is_undirected: bool

    def __post_init__(self) -> None:
        """Populate edge to source and target."""
        self.source.edges.append(self)
        self.target.edges.append(self)

    def detach(self) -> None:
        """Detach edge from nodes."""
        self.source.remove_edge(self)
        self.target.remove_edge(self)

    def spawn_call(self, walk: WalkerAnchor) -> WalkerArchitype:
        """Invoke data spatial call."""
        return walk.spawn_call(self.target)

    def destroy(self) -> None:
        """Destroy Anchor."""
        from jaclang.plugin.feature import JacFeature as Jac

        jctx = Jac.get_context()

        if jctx.root.has_write_access(self):
            self.detach()
            jctx.mem.remove(self.id)

    def __getstate__(self) -> dict[str, object]:
        """Serialize Node Anchor."""
        state = super().__getstate__()

        if self.is_populated():
            state.update(
                {
                    "source": self.source.make_stub(),
                    "target": self.target.make_stub(),
                    "is_undirected": self.is_undirected,
                }
            )

        return state


@dataclass(eq=False, repr=False, kw_only=True)
class WalkerAnchor(Anchor):
    """Walker Anchor."""

    architype: WalkerArchitype
    path: list[Anchor] = field(default_factory=list)
    next: list[Anchor] = field(default_factory=list)
    ignores: list[Anchor] = field(default_factory=list)
    disengaged: bool = False

    def visit_node(self, anchors: Iterable[NodeAnchor | EdgeAnchor]) -> bool:
        """Walker visits node."""
        before_len = len(self.next)
        for anchor in anchors:
            if anchor not in self.ignores:
                if isinstance(anchor, NodeAnchor):
                    self.next.append(anchor)
                elif isinstance(anchor, EdgeAnchor):
                    if target := anchor.target:
                        self.next.append(target)
                    else:
                        raise ValueError("Edge has no target.")
        return len(self.next) > before_len

    def ignore_node(self, anchors: Iterable[NodeAnchor | EdgeAnchor]) -> bool:
        """Walker ignores node."""
        before_len = len(self.ignores)
        for anchor in anchors:
            if anchor not in self.ignores:
                if isinstance(anchor, NodeAnchor):
                    self.ignores.append(anchor)
                elif isinstance(anchor, EdgeAnchor):
                    if target := anchor.target:
                        self.ignores.append(target)
                    else:
                        raise ValueError("Edge has no target.")
        return len(self.ignores) > before_len

    def disengage_now(self) -> None:
        """Disengage walker from traversal."""
        self.disengaged = True

    def spawn_call(self, node: Anchor) -> WalkerArchitype:
        """Invoke data spatial call."""
        if walker := self.architype:
            self.path = []
            self.next = [node]
            while len(self.next):
                if current_node := self.next.pop(0).architype:
                    for i in current_node._jac_entry_funcs_:
                        if not i.trigger or isinstance(walker, i.trigger):
                            if i.func:
                                i.func(current_node, walker)
                            else:
                                raise ValueError(f"No function {i.name} to call.")
                        if self.disengaged:
                            return walker
                    for i in walker._jac_entry_funcs_:
                        if not i.trigger or isinstance(current_node, i.trigger):
                            if i.func:
                                i.func(walker, current_node)
                            else:
                                raise ValueError(f"No function {i.name} to call.")
                        if self.disengaged:
                            return walker
                    for i in walker._jac_exit_funcs_:
                        if not i.trigger or isinstance(current_node, i.trigger):
                            if i.func:
                                i.func(walker, current_node)
                            else:
                                raise ValueError(f"No function {i.name} to call.")
                        if self.disengaged:
                            return walker
                    for i in current_node._jac_exit_funcs_:
                        if not i.trigger or isinstance(walker, i.trigger):
                            if i.func:
                                i.func(current_node, walker)
                            else:
                                raise ValueError(f"No function {i.name} to call.")
                        if self.disengaged:
                            return walker
            self.ignores = []
            return walker
        raise Exception(f"Invalid Reference {self.id}")


class Architype:
    """Architype Protocol."""

    _jac_entry_funcs_: ClassVar[list[DSFunc]]
    _jac_exit_funcs_: ClassVar[list[DSFunc]]

    def __init__(self) -> None:
        """Create default architype."""
        self.__jac__ = Anchor(architype=self)

    def __repr__(self) -> str:
        """Override repr for architype."""
        return f"{self.__class__.__name__}"


class NodeArchitype(Architype):
    """Node Architype Protocol."""

    __jac__: NodeAnchor

    def __init__(self) -> None:
        """Create node architype."""
        self.__jac__ = NodeAnchor(architype=self, edges=[])


class EdgeArchitype(Architype):
    """Edge Architype Protocol."""

    __jac__: EdgeAnchor

    def __attach__(
        self,
        source: NodeAnchor,
        target: NodeAnchor,
        is_undirected: bool,
    ) -> None:
        """Attach EdgeAnchor properly."""
        self.__jac__ = EdgeAnchor(
            architype=self, source=source, target=target, is_undirected=is_undirected
        )


class WalkerArchitype(Architype):
    """Walker Architype Protocol."""

    __jac__: WalkerAnchor

    def __init__(self) -> None:
        """Create walker architype."""
        self.__jac__ = WalkerAnchor(architype=self)


@dataclass(eq=False)
class GenericEdge(EdgeArchitype):
    """Generic Root Node."""

    _jac_entry_funcs_: ClassVar[list[DSFunc]] = []
    _jac_exit_funcs_: ClassVar[list[DSFunc]] = []


@dataclass(eq=False)
class Root(NodeArchitype):
    """Generic Root Node."""

    _jac_entry_funcs_: ClassVar[list[DSFunc]] = []
    _jac_exit_funcs_: ClassVar[list[DSFunc]] = []

    def __init__(self) -> None:
        """Create root node."""
        self.__jac__ = NodeAnchor(architype=self, persistent=True, edges=[])


@dataclass(eq=False)
class DSFunc:
    """Data Spatial Function."""

    name: str
    trigger: type | UnionType | tuple[type | UnionType, ...] | None
    func: Callable[[Any, Any], Any] | None = None

    def resolve(self, cls: type) -> None:
        """Resolve the function."""
        self.func = getattr(cls, self.name)
