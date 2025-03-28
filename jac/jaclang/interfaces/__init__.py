"""Jaclang interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import IntEnum
from pickle import dumps as pdumps
from types import UnionType
from typing import (
    Any,
    Callable,
    Generator,
    Generic,
    Iterable,
    Type,
    TypeVar,
)

_JID = TypeVar("_JID", bound="BaseJID")
_ANCHOR = TypeVar("_ANCHOR", bound="BaseAnchor")
_ANCHORS = TypeVar(
    "_ANCHORS",
    "BaseNodeAnchor",
    "BaseEdgeAnchor",
    "BaseWalkerAnchor",
    "BaseObjectAnchor",
    covariant=True,
)
_NODE_ANCHOR = TypeVar("_NODE_ANCHOR", bound="BaseNodeAnchor")
_SERIALIZE = TypeVar("_SERIALIZE")
_DESERIALIZE = TypeVar("_DESERIALIZE")

#########################################################################################
#                                      ID / ACCESS                                      #
#########################################################################################


@dataclass(kw_only=True)
class BaseJID(Generic[_ANCHORS], ABC):
    """Jaclang ID Interface."""

    id: Any
    type: Type[_ANCHORS]
    name: str

    def __repr__(self) -> str:
        """Override string representation."""
        return f"{self.type.__class__.__name__[:1].lower()}:{self.name}:{self.id}"

    def __str__(self) -> str:
        """Override string parsing."""
        return f"{self.type.__class__.__name__[:1].lower()}:{self.name}:{self.id}"

    def __hash__(self) -> int:
        """Return default hasher."""
        return hash(pdumps(self))


class AccessLevel(IntEnum):
    """Access level enum."""

    NO_ACCESS = -1
    READ = 0
    CONNECT = 1
    WRITE = 2

    @staticmethod
    def cast(val: int | str | "AccessLevel") -> "AccessLevel":
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

    anchors: dict[
        BaseJID[BaseNodeAnchor]
        | BaseJID[BaseEdgeAnchor]
        | BaseJID[BaseWalkerAnchor]
        | BaseJID[BaseObjectAnchor],
        AccessLevel,
    ] = field(default_factory=dict)

    def check(
        self,
        anchor: (
            BaseJID[BaseNodeAnchor]
            | BaseJID[BaseEdgeAnchor]
            | BaseJID[BaseWalkerAnchor]
            | BaseJID[BaseObjectAnchor]
        ),
    ) -> AccessLevel:
        """Validate access."""
        return self.anchors.get(anchor, AccessLevel.NO_ACCESS)


@dataclass
class Permission:
    """Anchor Access Handler."""

    all: AccessLevel = AccessLevel.NO_ACCESS
    roots: Access = field(default_factory=Access)


#########################################################################################
#                                        ANCHORS                                        #
#########################################################################################


@dataclass(kw_only=True)
class BaseAnchor(Generic[_SERIALIZE], ABC):
    """Anchor Interface."""

    jid: (
        BaseJID[BaseNodeAnchor]
        | BaseJID[BaseEdgeAnchor]
        | BaseJID[BaseWalkerAnchor]
        | BaseJID[BaseObjectAnchor]
    )
    architype: "BaseNodeArchitype | BaseEdgeArchitype | BaseWalkerArchitype | BaseObjectArchitype"
    root: BaseJID[BaseNodeAnchor] | None
    access: Permission

    @abstractmethod
    def __serialize__(self) -> _SERIALIZE:
        """Override string representation."""


@dataclass(kw_only=True)
class BaseNodeAnchor(BaseAnchor[_SERIALIZE]):
    """NodeAnchor Interface."""

    jid: BaseJID[BaseNodeAnchor]
    architype: "BaseNodeArchitype"
    edge_ids: Iterable[BaseJID[BaseEdgeAnchor]]


@dataclass(kw_only=True)
class BaseEdgeAnchor(BaseAnchor[_SERIALIZE]):
    """EdgeAnchor Interface."""

    jid: BaseJID[BaseEdgeAnchor]
    architype: "BaseEdgeArchitype"
    source_id: BaseJID[BaseNodeAnchor]
    target_id: BaseJID[BaseNodeAnchor]


@dataclass(kw_only=True)
class BaseWalkerAnchor(BaseAnchor[_SERIALIZE]):
    """WalkerAnchor Interface."""

    jid: BaseJID[BaseWalkerAnchor]
    architype: "BaseWalkerArchitype"


@dataclass(kw_only=True)
class BaseObjectAnchor(BaseAnchor[_SERIALIZE]):
    """ObjectAnchor Interface."""

    jid: BaseJID[BaseObjectAnchor]
    architype: "BaseObjectArchitype"


#########################################################################################
#                                       ARCHITYPES                                      #
#########################################################################################


class BaseArchitype(Generic[_SERIALIZE], ABC):
    """Architype Interface."""

    __jac_ref__: (
        BaseNodeAnchor | BaseEdgeAnchor | BaseWalkerAnchor | BaseObjectAnchor | None
    )

    @property
    @abstractmethod
    def __jac__(
        self,
    ) -> BaseNodeAnchor | BaseEdgeAnchor | BaseWalkerAnchor | BaseObjectAnchor:
        """Get or generate anchor."""

    @abstractmethod
    def __serialize__(self) -> _SERIALIZE:
        """Override string representation."""

    @classmethod
    @abstractmethod
    def __deserialize__(cls: Type[_DESERIALIZE], data: _SERIALIZE) -> _DESERIALIZE:
        """Override string parsing."""


class BaseNodeArchitype(BaseArchitype[_SERIALIZE]):
    """NodeArchitype Interface."""

    __jac_ref__: BaseNodeAnchor | None

    @property
    @abstractmethod
    def __jac__(
        self,
    ) -> BaseNodeAnchor:
        """Get or generate NodeAnchor."""


class BaseEdgeArchitype(BaseArchitype[_SERIALIZE]):
    """EdgeArchitype Interface."""

    __jac_ref__: BaseEdgeAnchor | None

    @property
    @abstractmethod
    def __jac__(
        self,
    ) -> BaseEdgeAnchor:
        """Get or generate EdgeAnchor."""


class BaseWalkerArchitype(BaseArchitype[_SERIALIZE]):
    """Walker Architype Interface."""

    __jac_ref__: BaseWalkerAnchor | None

    @property
    @abstractmethod
    def __jac__(
        self,
    ) -> BaseWalkerAnchor:
        """Get or generate WalkerAnchor."""


class BaseObjectArchitype(BaseArchitype[_SERIALIZE]):
    """Walker Architype Interface."""

    __jac_ref__: BaseObjectAnchor | None

    @property
    @abstractmethod
    def __jac__(
        self,
    ) -> BaseObjectAnchor:
        """Get or generate ObjectAnchor."""


@dataclass(kw_only=True)
class Root(BaseNodeArchitype[_SERIALIZE]):
    """Default Root Architype."""


@dataclass(kw_only=True)
class GenericEdge(BaseEdgeArchitype[_SERIALIZE]):
    """Default Edge Architype."""


@dataclass(eq=False)
class DSFunc:
    """Data Spatial Function."""

    name: str
    trigger: type | UnionType | tuple[type | UnionType, ...] | None
    func: Callable[[Any, Any], Any] | None = None

    def resolve(self, cls: type) -> None:
        """Resolve the function."""
        self.func = getattr(cls, self.name)


#########################################################################################
#                                   MEMORY INTERFACES                                   #
#########################################################################################


@dataclass
class Memory(Generic[_JID, _ANCHOR]):
    """Generic Memory Handler."""

    __mem__: dict[_JID, _ANCHOR] = field(default_factory=dict)
    __gc__: set[_JID] = field(default_factory=set)

    def close(self) -> None:
        """Close memory handler."""
        self.__mem__.clear()
        self.__gc__.clear()

    def find(
        self,
        ids: _JID | Iterable[_JID],
        filter: Callable[[_ANCHOR], _ANCHOR] | None = None,
    ) -> Generator[_ANCHOR, None, None]:
        """Find anchors from memory by ids with filter."""
        if not isinstance(ids, Iterable):
            ids = [ids]

        for id in ids:
            if (
                (anchor := self.__mem__.get(id))
                and isinstance(anchor, id.type)
                and (not filter or filter(anchor))
            ):
                yield anchor

    def find_one(
        self,
        ids: _JID | Iterable[_JID],
        filter: Callable[[_ANCHOR], _ANCHOR] | None = None,
    ) -> _ANCHOR | None:
        """Find one anchor from memory by ids with filter."""
        return next(self.find(ids, filter), None)

    def find_by_id(self, id: _JID) -> _ANCHOR | None:
        """Find one by id."""
        if (anchor := self.__mem__.get(id)) and isinstance(anchor, id.type):
            return anchor
        return None

    def set(self, id: _JID, data: _ANCHOR) -> None:
        """Save anchor to memory."""
        self.__mem__[id] = data

    def remove(self, ids: _JID | Iterable[_JID]) -> None:
        """Remove anchor/s from memory."""
        if not isinstance(ids, Iterable):
            ids = [ids]

        for id in ids:
            self.__mem__.pop(id, None)
            self.__gc__.add(id)


#########################################################################################
#                                        CONTEXT                                        #
#########################################################################################


class ExecutionContext(Generic[_NODE_ANCHOR], ABC):
    """Execution Context."""

    mem: Memory
    reports: list[Any]
    system_root: _NODE_ANCHOR
    root: _NODE_ANCHOR
    entry_node: _NODE_ANCHOR

    @abstractmethod
    def init_anchor(
        self,
        anchor_jid: str | None,
        default: _NODE_ANCHOR,
    ) -> _NODE_ANCHOR:
        """Load initial anchors."""

    def set_entry_node(self, entry_node: str | None) -> None:
        """Override entry."""
        self.entry_node = self.init_anchor(entry_node, self.root)

    @abstractmethod
    def close(self) -> None:
        """Close current ExecutionContext."""

    @staticmethod
    @abstractmethod
    def create(
        session: str | None = None,
        root: str | None = None,
        auto_close: bool = True,
    ) -> ExecutionContext:
        """Create ExecutionContext."""

    @staticmethod
    @abstractmethod
    def get() -> ExecutionContext:
        """Get current ExecutionContext."""

    @staticmethod
    @abstractmethod
    def get_root() -> BaseNodeArchitype:
        """Get current root."""
