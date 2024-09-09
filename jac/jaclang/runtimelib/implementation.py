"""Jaclang Runtimelib Implementation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Type
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


@dataclass(kw_only=True)
class JID(_JID[UUID, _ANCHOR]):
    """Jaclang Default JID."""

    id: UUID = field(default_factory=uuid4)
    type: Type[_ANCHOR]
    name: str = ""

    @property
    def anchor(self) -> _ANCHOR | None:
        """Get anchor by id and type."""
        return None

    def __repr__(self) -> str:
        """Override string representation."""
        return f"{self.type.__class__.__name__[:1].lower()}:{self.name}:{self.id}"

    def __str__(self) -> str:
        """Override string parsing."""
        return f"{self.type.__class__.__name__[:1].lower()}:{self.name}:{self.id}"


@dataclass(kw_only=True)
class NodeAnchor(
    _NodeAnchor[JID["NodeAnchor"], JID["EdgeAnchor"], "NodeArchitype", dict]
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
    _EdgeAnchor[JID["EdgeAnchor"], JID["NodeAnchor"], "EdgeArchitype", dict]
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
class WalkerAnchor(_WalkerAnchor[JID["WalkerAnchor"], "WalkerArchitype", dict]):
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
