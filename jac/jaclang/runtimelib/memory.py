"""Core constructs for Jac Language."""

from __future__ import annotations

from dataclasses import dataclass, field
from pickle import dumps
from shelve import Shelf, open
from typing import Callable, Generator, Generic, Iterable, TypeVar

from .implementation import EdgeAnchor, JID, NodeAnchor, WalkerAnchor, _ANCHOR

ID = TypeVar("ID")


@dataclass
class Memory(Generic[ID, _ANCHOR]):
    """Generic Memory Handler."""

    __mem__: dict[ID, _ANCHOR] = field(default_factory=dict)
    __gc__: set[_ANCHOR] = field(default_factory=set)

    def close(self) -> None:
        """Close memory handler."""
        self.__mem__.clear()
        self.__gc__.clear()

    def find(
        self,
        ids: ID | Iterable[ID],
        filter: Callable[[_ANCHOR], _ANCHOR] | None = None,
    ) -> Generator[_ANCHOR, None, None]:
        """Find anchors from memory by ids with filter."""
        if not isinstance(ids, Iterable):
            ids = [ids]

        return (
            anchor
            for id in ids
            if (anchor := self.__mem__.get(id)) and (not filter or filter(anchor))
        )

    def find_one(
        self,
        ids: ID | Iterable[ID],
        filter: Callable[[_ANCHOR], _ANCHOR] | None = None,
    ) -> _ANCHOR | None:
        """Find one anchor from memory by ids with filter."""
        return next(self.find(ids, filter), None)

    def find_by_id(self, id: ID) -> _ANCHOR | None:
        """Find one by id."""
        return self.__mem__.get(id)

    def set(self, id: ID, data: _ANCHOR) -> None:
        """Save anchor to memory."""
        self.__mem__[id] = data

    def remove(self, ids: ID | Iterable[ID]) -> None:
        """Remove anchor/s from memory."""
        if not isinstance(ids, Iterable):
            ids = [ids]

        for id in ids:
            if anchor := self.__mem__.pop(id, None):
                self.__gc__.add(anchor)


@dataclass
class ShelfStorage(Memory[JID, EdgeAnchor | NodeAnchor | WalkerAnchor]):
    """Shelf Handler."""

    __shelf__: Shelf[EdgeAnchor | NodeAnchor | WalkerAnchor] | None = None

    def __init__(self, session: str | None = None) -> None:
        """Initialize memory handler."""
        super().__init__()
        self.__shelf__ = open(session) if session else None  # noqa: SIM115

    def close(self) -> None:
        """Close memory handler."""
        if isinstance(self.__shelf__, Shelf):
            from jaclang.plugin.feature import JacFeature as Jac

            root = Jac.get_root().__jac__

            for anchor in self.__gc__:
                self.__shelf__.pop(str(anchor.jid), None)
                self.__mem__.pop(anchor.jid, None)

            for anchor in self.__mem__.values():
                if anchor.persistent and anchor.hash != hash(dumps(anchor)):
                    jid = str(anchor.jid)
                    if source_anchor := self.__shelf__.get(jid):
                        if (
                            isinstance(source_anchor, NodeAnchor)
                            and isinstance(anchor, NodeAnchor)
                            and source_anchor.edge_ids != anchor.edge_ids
                            and root.has_connect_access(anchor)
                        ):
                            if not anchor.edges:
                                self.__shelf__.pop(jid, None)
                                continue
                            source_anchor.edges = anchor.edges

                        if root.has_write_access(anchor):
                            if hash(dumps(source_anchor.access)) != hash(
                                dumps(anchor.access)
                            ):
                                source_anchor.access = anchor.access
                            if hash(dumps(anchor.architype)) != hash(
                                dumps(anchor.architype)
                            ):
                                source_anchor.architype = anchor.architype

                        self.__shelf__[jid] = source_anchor
                    elif not (
                        isinstance(anchor, NodeAnchor)
                        and not isinstance(anchor.architype, Root)
                        and not anchor.edges
                    ):
                        self.__shelf__[jid] = anchor

            self.__shelf__.close()
        super().close()

    def find(
        self,
        ids: JID | Iterable[JID],
        filter: Callable[[Anchor], Anchor] | None = None,
    ) -> Generator[Anchor, None, None]:
        """Find anchors from datasource by ids with filter."""
        if not isinstance(ids, Iterable):
            ids = [ids]

        if isinstance(self.__shelf__, Shelf):
            for id in ids:
                anchor = self.__mem__.get(id)

                if (
                    not anchor
                    and id not in self.__gc__
                    and (_anchor := self.__shelf__.get(str(id)))
                ):
                    self.__mem__[id] = anchor = _anchor
                if anchor and (not filter or filter(anchor)):
                    yield anchor
        else:
            yield from super().find(ids, filter)

    def find_by_id(self, id: JID) -> Anchor | None:
        """Find one by id."""
        data = super().find_by_id(id)

        if (
            not data
            and isinstance(self.__shelf__, Shelf)
            and (data := self.__shelf__.get(str(id)))
        ):
            self.__mem__[id] = data

        return data
