"""Jaclang Runtimelib Implementation."""

from __future__ import annotations

from dataclasses import dataclass, field
from logging import getLogger
from typing import ClassVar, TypeAlias
from uuid import UUID, uuid4

from .interface import (
    EdgeAnchor as _EdgeAnchor,
    EdgeArchitype as _EdgeArchitype,
    JID as _JID,
    NodeAnchor as _NodeAnchor,
    NodeArchitype as _NodeArchitype,
    Permission,
    WalkerAnchor as _WalkerAnchor,
    WalkerArchitype as _WalkerArchitype,
    _ANCHOR,
)

Anchor: TypeAlias = "NodeAnchor" | "EdgeAnchor" | "WalkerAnchor"
Architype: TypeAlias = "NodeArchitype" | "EdgeArchitype" | "WalkerArchitype"
logger = getLogger(__name__)


@dataclass(kw_only=True)
class JID(_JID[UUID, _ANCHOR]):
    """Jaclang Default JID."""

    id: UUID = field(default_factory=uuid4)
    name: str = ""

    def __repr__(self) -> str:
        """Override string representation."""
        return f"{self.type.__class__.__name__[:1].lower()}:{self.name}:{self.id}"

    def __str__(self) -> str:
        """Override string parsing."""
        return f"{self.type.__class__.__name__[:1].lower()}:{self.name}:{self.id}"


@dataclass(kw_only=True)
class NodeAnchor(_NodeAnchor["NodeAnchor"]):
    """NodeAnchor Interface."""

    jid: JID[NodeAnchor] = field(default_factory=lambda: JID(type=NodeAnchor))
    architype: "NodeArchitype"
    root: JID["NodeAnchor"] | None = None
    access: Permission = field(default_factory=Permission)
    persistent: bool = False
    hash: int = 0

    edge_ids: set[JID[EdgeAnchor]] = field(default_factory=set)

    def __serialize__(self) -> NodeAnchor:
        """Override serialization."""
        return self

    @classmethod
    def __deserialize__(cls, data: NodeAnchor) -> NodeAnchor:
        """Override deserialization."""
        return data


@dataclass(kw_only=True)
class EdgeAnchor(_EdgeAnchor["EdgeAnchor"]):
    """NodeAnchor Interface."""

    jid: JID[EdgeAnchor] = field(default_factory=lambda: JID(type=EdgeAnchor))
    architype: "EdgeArchitype"
    root: JID["NodeAnchor"] | None = None
    access: Permission = field(default_factory=Permission)
    persistent: bool = False
    hash: int = 0

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
class WalkerAnchor(_WalkerAnchor["WalkerAnchor"]):
    """NodeAnchor Interface."""

    jid: JID[WalkerAnchor] = field(default_factory=lambda: JID(type=WalkerAnchor))
    architype: "WalkerArchitype"
    root: JID["NodeAnchor"] | None = None
    access: Permission = field(default_factory=Permission)
    persistent: bool = False
    hash: int = 0

    def __serialize__(self) -> WalkerAnchor:
        """Override serialization."""
        return self

    @classmethod
    def __deserialize__(cls, data: WalkerAnchor) -> WalkerAnchor:
        """Override deserialization."""
        return data


class NodeArchitype(_NodeArchitype["NodeArchitype"]):
    """NodeArchitype Interface."""

    __jac__: ClassVar[NodeAnchor]

    def __serialize__(self) -> NodeArchitype:
        """Override serialization."""
        return self

    @classmethod
    def __deserialize__(cls, data: NodeArchitype) -> NodeArchitype:
        """Override deserialization."""
        return data


class EdgeArchitype(_EdgeArchitype["EdgeArchitype"]):
    """EdgeArchitype Interface."""

    __jac__: ClassVar[EdgeAnchor]

    def __serialize__(self) -> EdgeArchitype:
        """Override serialization."""
        return self

    @classmethod
    def __deserialize__(cls, data: EdgeArchitype) -> EdgeArchitype:
        """Override deserialization."""
        return data


class WalkerArchitype(_WalkerArchitype["WalkerArchitype"]):
    """Walker Architype Interface."""

    __jac__: ClassVar[WalkerAnchor]

    def __serialize__(self) -> WalkerArchitype:
        """Override serialization."""
        return self

    @classmethod
    def __deserialize__(cls, data: WalkerArchitype) -> WalkerArchitype:
        """Override deserialization."""
        return data


@dataclass(kw_only=True)
class Root(NodeArchitype):
    """Default Root Architype."""


@dataclass(kw_only=True)
class GenericEdge(EdgeArchitype):
    """Default Edge Architype."""
