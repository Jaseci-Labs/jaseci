"""Jaclang Implementations."""

from __future__ import annotations

from dataclasses import dataclass
from re import IGNORECASE, compile
from typing import Type, TypeVar
from uuid import UUID, uuid4

from ..interfaces import (
    BaseJID,
    BaseEdgeAnchor,
    BaseNodeAnchor,
    BaseObjectAnchor,
    BaseWalkerAnchor,
    _ANCHORS,
)


JID_REGEX = compile(
    r"^(n|e|w):([^:]*):([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$",
    IGNORECASE,
)

_JID = TypeVar("_JID", bound="JID")


@dataclass(kw_only=True)
class JID(BaseJID[_ANCHORS]):
    """Jaclang ID Implementation."""

    id: UUID

    def __init__(
        self,
        id: str | UUID | None = None,
        type: Type[_ANCHORS] | None = None,
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
                        case _:
                            self.type = WalkerAnchor  # type: ignore [assignment]
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


@dataclass(kw_only=True)
class NodeAnchor(BaseNodeAnchor["NodeAnchor"]):
    """NodeAnchor Implementation."""

    jid: JID["NodeAnchor"]
    architype: "NodeArchitype"
    edge_ids: list[JID["EdgeAnchor"]]

    def __serialize__(self) -> NodeAnchor:
        """Override string representation."""
        return self


@dataclass(kw_only=True)
class EdgeAnchor(BaseEdgeAnchor["EdgeAnchor"]):
    """EdgeAnchor Implementation."""

    jid: JID["EdgeAnchor"]
    architype: "EdgeArchitype"
    source_id: JID[NodeAnchor]
    target_id: JID[NodeAnchor]

    def __serialize__(self) -> EdgeAnchor:
        """Override string representation."""
        return self


@dataclass(kw_only=True)
class WalkerAnchor(BaseWalkerAnchor["WalkerAnchor"]):
    """WalkerAnchor Implementation."""

    jid: JID["WalkerAnchor"]
    architype: "WalkerArchitype"

    def __serialize__(self) -> EdgeAnchor:
        """Override string representation."""
        return self
