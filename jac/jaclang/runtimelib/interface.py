"""Jaclang Runtimelib interfaces."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import IntEnum
from typing import ClassVar, Generic, Iterable, Type, TypeVar


_ID = TypeVar("_ID")
_ANCHOR = TypeVar("_ANCHOR", bound="Anchor")

_SERIALIZE = TypeVar("_SERIALIZE")
_DESERIALIZE = TypeVar("_DESERIALIZE")


@dataclass(kw_only=True)
class JID(Generic[_ID, _ANCHOR], ABC):
    """Jaclang ID Interface."""

    id: _ID
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


@dataclass(kw_only=True)
class Anchor(Generic[_SERIALIZE], ABC):
    """Anchor Interface."""

    jid: JID
    architype: "Architype"
    root: JID | None
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

    architype: "NodeArchitype"
    edge_ids: Iterable[JID]


@dataclass(kw_only=True)
class EdgeAnchor(Anchor[_SERIALIZE]):
    """EdgeAnchor Interface."""

    architype: "EdgeArchitype"
    source_id: JID
    target_id: JID


@dataclass(kw_only=True)
class WalkerAnchor(Anchor[_SERIALIZE]):
    """WalkerAnchor Interface."""

    architype: "WalkerArchitype"


class Architype(Generic[_SERIALIZE], ABC):
    """Architype Interface."""

    __jac__: ClassVar[Anchor]

    @abstractmethod
    def __serialize__(self) -> _SERIALIZE:
        """Override string representation."""

    @classmethod
    @abstractmethod
    def __deserialize__(cls: Type[_DESERIALIZE], data: _SERIALIZE) -> _DESERIALIZE:
        """Override string parsing."""


class NodeArchitype(Architype[_SERIALIZE]):
    """NodeArchitype Interface."""

    __jac__: ClassVar[NodeAnchor]


class EdgeArchitype(Architype[_SERIALIZE]):
    """EdgeArchitype Interface."""

    __jac__: ClassVar[EdgeAnchor]


class WalkerArchitype(Architype[_SERIALIZE]):
    """Walker Architype Interface."""

    __jac__: ClassVar[WalkerAnchor]


@dataclass(kw_only=True)
class Root(NodeArchitype[_SERIALIZE]):
    """Default Root Architype."""


@dataclass(kw_only=True)
class GenericEdge(EdgeArchitype[_SERIALIZE]):
    """Default Edge Architype."""
