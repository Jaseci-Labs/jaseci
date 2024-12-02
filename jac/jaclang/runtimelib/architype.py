"""Core constructs for Jac Language."""

from __future__ import annotations

import inspect
from dataclasses import asdict, dataclass, field, is_dataclass
from enum import IntEnum
from functools import cached_property
from logging import getLogger
from re import IGNORECASE, compile
from types import UnionType
from typing import Any, Callable, ClassVar, Generic, Optional, Type, TypeVar
from uuid import UUID, uuid4

logger = getLogger(__name__)


JID_REGEX = compile(
    r"^(n|e|w|o):([^:]*):([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$",
    IGNORECASE,
)
_ANCHOR = TypeVar("_ANCHOR", bound="Anchor")


@dataclass(kw_only=True)
class JID(Generic[_ANCHOR]):
    """Jaclang ID Interface."""

    id: Any
    type: Type[_ANCHOR]
    name: str

    @cached_property
    def __cached_repr__(self) -> str:
        """Cached string representation."""
        return f"{self.type.__name__[:1].lower()}:{self.name}:{self.id}"

    @cached_property
    def anchor(self) -> _ANCHOR | None:
        """Get architype."""
        from jaclang.plugin.feature import JacFeature

        return JacFeature.get_context().mem.find_by_id(self)

    def __repr__(self) -> str:
        """Override string representation."""
        return self.__cached_repr__

    def __str__(self) -> str:
        """Override string parsing."""
        return self.__cached_repr__

    def __hash__(self) -> int:
        """Return default hasher."""
        return hash(self.__cached_repr__)


@dataclass(kw_only=True)
class JacLangJID(JID[_ANCHOR]):
    """Jaclang ID Implementation."""

    def __init__(
        self,
        id: str | UUID | None = None,
        type: Type[_ANCHOR] | None = None,
        name: str = "",
    ) -> None:
        """Override JID initializer."""
        match id:
            case str():
                if matched := JID_REGEX.search(id):
                    self.id = UUID(matched.group(3))
                    self.name = matched.group(2)
                    # currently no way to base hinting on string regex!
                    match matched.group(1).lower():
                        case "n":
                            self.type = NodeAnchor  # type: ignore [assignment]
                        case "e":
                            self.type = EdgeAnchor  # type: ignore [assignment]
                        case "w":
                            self.type = WalkerAnchor  # type: ignore [assignment]
                        case _:
                            self.type = ObjectAnchor  # type: ignore [assignment]
                    return
                raise ValueError("Not a valid JID format!")
            case UUID():
                self.id = id
            case None:
                self.id = uuid4()
            case _:
                raise ValueError("Not a valid id for JID!")

        if type is None:
            raise ValueError("Type is required from non string JID!")
        self.type = type
        self.name = name

    def __getstate__(self) -> str:
        """Override getstate."""
        return self.__cached_repr__

    def __setstate__(self, state: str) -> None:
        """Override setstate."""
        self.__init__(state)  # type: ignore[misc]

    def __hash__(self) -> int:
        """Return default hasher."""
        return hash(self.__cached_repr__)


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

    anchors: dict[JID, AccessLevel] = field(default_factory=dict)

    def check(self, id: JID) -> AccessLevel:
        """Validate access."""
        return self.anchors.get(id, AccessLevel.NO_ACCESS)


@dataclass
class Permission:
    """Anchor Access Handler."""

    all: AccessLevel = AccessLevel.NO_ACCESS
    roots: Access = field(default_factory=Access)


@dataclass
class AnchorReport:
    """Report Handler."""

    id: JID
    context: dict[str, Any]


@dataclass(eq=False, kw_only=True)
class Anchor:
    """Object Anchor."""

    architype: Architype
    id: Any = field(default_factory=uuid4)
    root: Optional[JID[NodeAnchor]] = None
    access: Permission = field(default_factory=Permission)
    persistent: bool = False
    hash: int = 0

    @cached_property
    def jid(self: _ANCHOR) -> JID[_ANCHOR]:
        """Get JID representation."""
        jid = JacLangJID[_ANCHOR](
            self.id,
            self.__class__,
            (
                ""
                if isinstance(self.architype, (GenericEdge, Root))
                else self.architype.__class__.__name__
            ),
        )
        jid.anchor = self

        return jid

    def report(self) -> AnchorReport:
        """Report Anchor."""
        return AnchorReport(
            id=self.jid,
            context=(
                asdict(self.architype)
                if is_dataclass(self.architype) and not isinstance(self.architype, type)
                else {}
            ),
        )

    def __hash__(self) -> int:
        """Override hash for anchor."""
        return hash(self.jid)

    def __eq__(self, value: object) -> bool:
        """Override __eq__."""
        if isinstance(value, Anchor):
            return value.jid == self.jid
        return False


@dataclass(eq=False, kw_only=True)
class NodeAnchor(Anchor):
    """Node Anchor."""

    architype: NodeArchitype
    edges: list[JID["EdgeAnchor"]]


@dataclass(eq=False, kw_only=True)
class EdgeAnchor(Anchor):
    """Edge Anchor."""

    architype: EdgeArchitype
    source: JID["NodeAnchor"]
    target: JID["NodeAnchor"]
    is_undirected: bool


@dataclass(eq=False, kw_only=True)
class WalkerAnchor(Anchor):
    """Walker Anchor."""

    architype: WalkerArchitype
    path: list[Anchor] = field(default_factory=list)
    next: list[Anchor] = field(default_factory=list)
    ignores: list[Anchor] = field(default_factory=list)
    disengaged: bool = False


@dataclass(eq=False, kw_only=True)
class ObjectAnchor(Anchor):
    """Object Anchor."""

    architype: ObjectArchitype


class Architype:
    """Architype Protocol."""

    _jac_entry_funcs_: ClassVar[list[DSFunc]]
    _jac_exit_funcs_: ClassVar[list[DSFunc]]

    def __repr__(self) -> str:
        """Override repr for architype."""
        return f"{self.__class__.__name__}"

    @cached_property
    def __jac__(self) -> Anchor:
        """Build anchor reference."""
        return Anchor(architype=self)


class NodeArchitype(Architype):
    """Node Architype Protocol."""

    @cached_property
    def __jac__(self) -> NodeAnchor:
        """Build anchor reference."""
        return NodeAnchor(architype=self, edges=[])


class EdgeArchitype(Architype):
    """Edge Architype Protocol."""

    __jac__: EdgeAnchor


class WalkerArchitype(Architype):
    """Walker Architype Protocol."""

    @cached_property
    def __jac__(self) -> WalkerAnchor:
        """Build anchor reference."""
        return WalkerAnchor(architype=self)


class ObjectArchitype(Architype):
    """Walker Architype Protocol."""

    @cached_property
    def __jac__(self) -> ObjectAnchor:
        """Build anchor reference."""
        return ObjectAnchor(architype=self)


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

    @cached_property
    def __jac__(self) -> NodeAnchor:
        """Build anchor reference."""
        return NodeAnchor(architype=self, persistent=True, edges=[])


@dataclass(eq=False)
class DSFunc:
    """Data Spatial Function."""

    name: str
    func: Callable[[Any, Any], Any] | None = None

    def resolve(self, cls: type) -> None:
        """Resolve the function."""
        self.func = getattr(cls, self.name)

    def get_funcparam_annotations(
        self, func: Callable[[Any, Any], Any] | None
    ) -> type | UnionType | tuple[type | UnionType, ...] | None:
        """Get function parameter annotations."""
        if not func:
            return None
        annotation = (
            inspect.signature(func, eval_str=True).parameters["_jac_here_"].annotation
        )
        return annotation if annotation != inspect._empty else None
