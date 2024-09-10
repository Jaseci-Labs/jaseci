"""Jaclang Runtimelib Implementation."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from uuid import UUID, uuid4

from .interface import (
    EdgeAnchor as _EdgeAnchor,
    EdgeArchitype as _EdgeArchitype,
    GenericEdge as _GenericEdge,
    JID as _JID,
    NodeAnchor as _NodeAnchor,
    NodeArchitype as _NodeArchitype,
    Root as _Root,
    WalkerAnchor as _WalkerAnchor,
    WalkerArchitype as _WalkerArchitype,
    _ANCHOR,
)


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


@dataclass(kw_only=True)
class JID(_JID[UUID, _ANCHOR]):
    """Jaclang Default JID."""

    id: UUID = field(default_factory=uuid4)
    name: str = ""

    @property
    def anchor(self) -> _ANCHOR | None:
        """Get anchor by id and type."""
        from jaclang.plugin.feature import JacFeature as Jac

        return Jac.get_context().mem.find_by_id(self)

    def __repr__(self) -> str:
        """Override string representation."""
        return f"{self.type.__class__.__name__[:1].lower()}:{self.name}:{self.id}"

    def __str__(self) -> str:
        """Override string parsing."""
        return f"{self.type.__class__.__name__[:1].lower()}:{self.name}:{self.id}"


@dataclass(kw_only=True)
class AnchorMeta:
    """Anchor persistence metadata."""

    root: JID["NodeAnchor"] | None = None
    access: Permission = field(default_factory=Permission)
    persistent: bool = False
    hash: int = 0


@dataclass(kw_only=True)
class NodeAnchor(_NodeAnchor["NodeAnchor"], AnchorMeta):
    """NodeAnchor Interface."""

    jid: JID[NodeAnchor] = field(default_factory=lambda: JID(type=NodeAnchor))
    architype: "NodeArchitype"
    edge_ids: set[JID[EdgeAnchor]] = field(default_factory=set)

    def __serialize__(self) -> NodeAnchor:
        """Override serialization."""
        return self

    @classmethod
    def __deserialize__(cls, data: NodeAnchor) -> NodeAnchor:
        """Override deserialization."""
        return data


@dataclass(kw_only=True)
class EdgeAnchor(_EdgeAnchor["EdgeAnchor"], AnchorMeta):
    """NodeAnchor Interface."""

    jid: JID[EdgeAnchor] = field(default_factory=lambda: JID(type=EdgeAnchor))
    architype: "EdgeArchitype"
    source_id: JID[NodeAnchor]
    target_id: JID[NodeAnchor]

    def __serialize__(self) -> EdgeAnchor:
        """Override serialization."""
        return self

    @classmethod
    def __deserialize__(cls, data: EdgeAnchor) -> EdgeAnchor:
        """Override deserialization."""
        return data


@dataclass(kw_only=True)
class WalkerAnchor(_WalkerAnchor["WalkerAnchor"], AnchorMeta):
    """NodeAnchor Interface."""

    jid: JID[WalkerAnchor] = field(default_factory=lambda: JID(type=WalkerAnchor))
    architype: "WalkerArchitype"

    def __serialize__(self) -> WalkerAnchor:
        """Override serialization."""
        return self

    @classmethod
    def __deserialize__(cls, data: WalkerAnchor) -> WalkerAnchor:
        """Override deserialization."""
        return data


class NodeArchitype(_NodeArchitype["NodeArchitype"]):
    """NodeArchitype Interface."""

    __jac__: NodeAnchor

    def __serialize__(self) -> NodeArchitype:
        """Override serialization."""
        return self

    @classmethod
    def __deserialize__(cls, data: NodeArchitype) -> NodeArchitype:
        """Override deserialization."""
        return data


class EdgeArchitype(_EdgeArchitype["EdgeArchitype"]):
    """EdgeArchitype Interface."""

    __jac__: EdgeAnchor

    def __serialize__(self) -> EdgeArchitype:
        """Override serialization."""
        return self

    @classmethod
    def __deserialize__(cls, data: EdgeArchitype) -> EdgeArchitype:
        """Override deserialization."""
        return data


class WalkerArchitype(_WalkerArchitype["WalkerArchitype"]):
    """Walker Architype Interface."""

    __jac__: WalkerAnchor

    def __serialize__(self) -> WalkerArchitype:
        """Override serialization."""
        return self

    @classmethod
    def __deserialize__(cls, data: WalkerArchitype) -> WalkerArchitype:
        """Override deserialization."""
        return data


@dataclass(kw_only=True)
class Root(_Root["Root"]):
    """Default Root Architype."""

    __jac__: NodeAnchor

    def __serialize__(self) -> Root:
        """Override serialization."""
        return self

    @classmethod
    def __deserialize__(cls, data: Root) -> Root:
        """Override deserialization."""
        return data


@dataclass(kw_only=True)
class GenericEdge(_GenericEdge["GenericEdge"]):
    """Default Edge Architype."""

    __jac__: EdgeAnchor

    def __serialize__(self) -> GenericEdge:
        """Override serialization."""
        return self

    @classmethod
    def __deserialize__(cls, data: GenericEdge) -> GenericEdge:
        """Override deserialization."""
        return data
