"""Jaclang Runtimelib interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import IntEnum
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


_ANCHOR = TypeVar("_ANCHOR", "NodeAnchor", "EdgeAnchor", "WalkerAnchor", covariant=True)
_NODE_ANCHOR = TypeVar("_NODE_ANCHOR", bound="NodeAnchor")

_SERIALIZE = TypeVar("_SERIALIZE")
_DESERIALIZE = TypeVar("_DESERIALIZE")

#########################################################################################
#                                      ID / ACCESS                                      #
#########################################################################################


@dataclass(kw_only=True)
class JID(Generic[_ANCHOR], ABC):
    """Jaclang ID Interface."""

    id: Any
    type: Type[_ANCHOR]
    name: str


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

    anchors: dict[str, AccessLevel] = field(default_factory=dict)

    def check(self, anchor: str) -> AccessLevel:
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
class Anchor(Generic[_SERIALIZE], ABC):
    """Anchor Interface."""

    jid: JID[NodeAnchor] | JID[EdgeAnchor] | JID[WalkerAnchor]
    architype: "NodeArchitype" | "EdgeArchitype" | "WalkerArchitype"
    root: JID[NodeAnchor] | None
    access: Permission

    @abstractmethod
    def __serialize__(self) -> _SERIALIZE:
        """Override string representation."""

    @classmethod
    @abstractmethod
    def __deserialize__(cls: Type[_DESERIALIZE], data: _SERIALIZE) -> _DESERIALIZE:
        """Override string parsing."""


@dataclass(kw_only=True)
class NodeAnchor(Anchor[_SERIALIZE]):
    """NodeAnchor Interface."""

    jid: JID[NodeAnchor]
    architype: "NodeArchitype"
    edge_ids: Iterable[JID[EdgeAnchor]]


@dataclass(kw_only=True)
class EdgeAnchor(Anchor[_SERIALIZE]):
    """EdgeAnchor Interface."""

    jid: JID[EdgeAnchor]
    architype: "EdgeArchitype"
    source_id: JID[NodeAnchor]
    target_id: JID[NodeAnchor]


@dataclass(kw_only=True)
class WalkerAnchor(Anchor[_SERIALIZE]):
    """WalkerAnchor Interface."""

    jid: JID[WalkerAnchor]
    architype: "WalkerArchitype"


#########################################################################################
#                                       ARCHITYPES                                      #
#########################################################################################


class Architype(Generic[_SERIALIZE], ABC):
    """Architype Interface."""

    __jac__: NodeAnchor | EdgeAnchor | WalkerAnchor

    @abstractmethod
    def __serialize__(self) -> _SERIALIZE:
        """Override string representation."""

    @classmethod
    @abstractmethod
    def __deserialize__(cls: Type[_DESERIALIZE], data: _SERIALIZE) -> _DESERIALIZE:
        """Override string parsing."""


class NodeArchitype(Architype[_SERIALIZE]):
    """NodeArchitype Interface."""

    __jac__: NodeAnchor


class EdgeArchitype(Architype[_SERIALIZE]):
    """EdgeArchitype Interface."""

    __jac__: EdgeAnchor


class WalkerArchitype(Architype[_SERIALIZE]):
    """Walker Architype Interface."""

    __jac__: WalkerAnchor


@dataclass(kw_only=True)
class Root(NodeArchitype[_SERIALIZE]):
    """Default Root Architype."""


@dataclass(kw_only=True)
class GenericEdge(EdgeArchitype[_SERIALIZE]):
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
class Memory(Generic[_ANCHOR]):
    """Generic Memory Handler."""

    __mem__: dict[JID[_ANCHOR], _ANCHOR] = field(default_factory=dict)
    __gc__: set[JID[_ANCHOR]] = field(default_factory=set)

    def close(self) -> None:
        """Close memory handler."""
        self.__mem__.clear()
        self.__gc__.clear()

    def find(
        self,
        ids: JID[_ANCHOR] | Iterable[JID[_ANCHOR]],
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
        ids: JID[_ANCHOR] | Iterable[JID[_ANCHOR]],
        filter: Callable[[_ANCHOR], _ANCHOR] | None = None,
    ) -> _ANCHOR | None:
        """Find one anchor from memory by ids with filter."""
        return next(self.find(ids, filter), None)

    def find_by_id(self, id: JID[_ANCHOR]) -> _ANCHOR | None:
        """Find one by id."""
        return self.__mem__.get(id)

    def set(self, data: _ANCHOR) -> None:
        """Save anchor to memory."""
        self.__mem__[data.jid] = data

    def remove(self, ids: JID[_ANCHOR] | Iterable[JID[_ANCHOR]]) -> None:
        """Remove anchor/s from memory."""
        if not isinstance(ids, Iterable):
            ids = [ids]

        for id in ids:
            if self.__mem__.pop(id, None):
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
    def get_root() -> Root:
        """Get current root."""
