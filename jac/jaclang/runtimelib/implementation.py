"""Jaclang Runtimelib Implementation."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Generic, Type
from uuid import UUID, uuid4

from .interface import (
    Anchor,
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
class JID(Generic[_ANCHOR], _JID[UUID, Anchor]):
    """Jaclang Default JID."""

    id: UUID = field(default_factory=uuid4)
    type: Type[_ANCHOR]
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
class NodeAnchor(
    _NodeAnchor[JID["NodeAnchor"], JID["EdgeAnchor"], "NodeArchitype", dict], AnchorMeta
):
    """NodeAnchor Interface."""

    jid = field(default_factory=lambda: JID(type=NodeAnchor))
    edge_ids = field(default_factory=set)

    def __serialize__(self) -> dict:
        """Override string representation."""
        return {}

    @classmethod
    def __deserialize__(cls, data: dict) -> NodeAnchor:
        """Override string parsing."""
        return object.__new__(NodeAnchor)


@dataclass(kw_only=True)
class EdgeAnchor(
    _EdgeAnchor[JID["EdgeAnchor"], JID["NodeAnchor"], "EdgeArchitype", dict], AnchorMeta
):
    """NodeAnchor Interface."""

    jid = field(default_factory=lambda: JID(type=EdgeAnchor))

    def __serialize__(self) -> dict:
        """Override string representation."""
        return {}

    @classmethod
    def __deserialize__(cls, data: dict) -> EdgeAnchor:
        """Override string parsing."""
        return object.__new__(EdgeAnchor)


@dataclass(kw_only=True)
class WalkerAnchor(
    _WalkerAnchor[JID["WalkerAnchor"], "WalkerArchitype", dict], AnchorMeta
):
    """NodeAnchor Interface."""

    jid = field(default_factory=lambda: JID(type=WalkerAnchor))

    def __serialize__(self) -> dict:
        """Override string representation."""
        return {}

    @classmethod
    def __deserialize__(cls, data: dict) -> WalkerAnchor:
        """Override string parsing."""
        return object.__new__(WalkerAnchor)


class NodeArchitype(_NodeArchitype[NodeAnchor, dict]):
    """NodeArchitype Interface."""


class EdgeArchitype(_EdgeArchitype[EdgeAnchor, dict]):
    """EdgeArchitype Interface."""


class WalkerArchitype(_WalkerArchitype[WalkerAnchor, dict]):
    """Walker Architype Interface."""


@dataclass(kw_only=True)
class Root(_Root[NodeAnchor, dict]):
    """Default Root Architype."""


@dataclass(kw_only=True)
class GenericEdge(_GenericEdge[EdgeAnchor, dict]):
    """Default Root Architype."""
