"""Jaclang Runtimelib interfaces."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Iterable, Type, TypeVar

_ID = TypeVar("_ID")
_JID = TypeVar("_JID", bound="JID")
_REF_JID = TypeVar("_REF_JID", bound="JID")
_ANCHOR = TypeVar("_ANCHOR", bound="Anchor")
_NODE_ANCHOR = TypeVar("_NODE_ANCHOR", bound="NodeAnchor")
_EDGE_ANCHOR = TypeVar("_EDGE_ANCHOR", bound="EdgeAnchor")
_WALKER_ANCHOR = TypeVar("_WALKER_ANCHOR", bound="WalkerAnchor")
_ARCHITYPE = TypeVar("_ARCHITYPE", bound="Architype")
_NODE_ARCHITYPE = TypeVar("_NODE_ARCHITYPE", bound="NodeArchitype")
_EDGE_ARCHITYPE = TypeVar("_EDGE_ARCHITYPE", bound="EdgeArchitype")
_WALKER_ARCHITYPE = TypeVar("_WALKER_ARCHITYPE", bound="WalkerArchitype")

_BASE_ANCHOR = TypeVar("_BASE_ANCHOR", bound="Anchor")

_SERIALIZE = TypeVar("_SERIALIZE")
_DESERIALIZE = TypeVar("_DESERIALIZE")


@dataclass(kw_only=True)
class JID(Generic[_ID, _ANCHOR], ABC):
    """Jaclang ID Interface."""

    id: _ID
    type: Type[_ANCHOR]
    name: str

    @property
    @abstractmethod
    def anchor(self) -> _ANCHOR | None:
        """Get anchor by id and type."""


@dataclass(kw_only=True)
class Anchor(Generic[_JID, _ARCHITYPE, _SERIALIZE], ABC):
    """Anchor Interface."""

    jid: _JID
    architype: _ARCHITYPE

    @abstractmethod
    def __serialize__(self) -> _SERIALIZE:
        """Override string representation."""

    @classmethod
    @abstractmethod
    def __deserialize__(cls: Type[_DESERIALIZE], data: _SERIALIZE) -> _DESERIALIZE:
        """Override string parsing."""


@dataclass(kw_only=True)
class NodeAnchor(
    Generic[_JID, _REF_JID, _NODE_ARCHITYPE, _SERIALIZE],
    Anchor[_JID, "NodeArchitype", _SERIALIZE],
):
    """NodeAnchor Interface."""

    architype: _NODE_ARCHITYPE
    edge_ids: Iterable[_REF_JID]


@dataclass(kw_only=True)
class EdgeAnchor(
    Generic[_JID, _REF_JID, _EDGE_ARCHITYPE, _SERIALIZE],
    Anchor[_JID, "EdgeArchitype", _SERIALIZE],
):
    """EdgeAnchor Interface."""

    architype: _EDGE_ARCHITYPE
    source_id: _REF_JID
    target_id: _REF_JID


@dataclass(kw_only=True)
class WalkerAnchor(
    Generic[_JID, _WALKER_ARCHITYPE, _SERIALIZE],
    Anchor[_JID, "WalkerArchitype", _SERIALIZE],
):
    """WalkerAnchor Interface."""

    architype: _WALKER_ARCHITYPE


class Architype(Generic[_BASE_ANCHOR, _SERIALIZE], ABC):
    """Architype Interface."""

    __jac__: _BASE_ANCHOR

    @abstractmethod
    def __serialize__(self) -> _SERIALIZE:
        """Override string representation."""

    @classmethod
    @abstractmethod
    def __deserialize__(cls: Type[_DESERIALIZE], data: _SERIALIZE) -> _DESERIALIZE:
        """Override string parsing."""


class NodeArchitype(
    Generic[_NODE_ANCHOR, _SERIALIZE], Architype[NodeAnchor, _SERIALIZE]
):
    """NodeArchitype Interface."""

    __jac__: _NODE_ANCHOR


class EdgeArchitype(
    Generic[_EDGE_ANCHOR, _SERIALIZE], Architype[EdgeAnchor, _SERIALIZE]
):
    """EdgeArchitype Interface."""

    __jac__: _EDGE_ANCHOR


class WalkerArchitype(
    Generic[_WALKER_ANCHOR, _SERIALIZE], Architype[WalkerAnchor, _SERIALIZE]
):
    """Walker Architype Interface."""

    __jac__: _WALKER_ANCHOR


@dataclass(kw_only=True)
class Root(NodeArchitype[_NODE_ANCHOR, _SERIALIZE]):
    """Default Root Architype."""


@dataclass(kw_only=True)
class GenericEdge(EdgeArchitype[_EDGE_ANCHOR, _SERIALIZE]):
    """Default Edge Architype."""
