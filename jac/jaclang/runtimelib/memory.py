"""Core constructs for Jac Language."""

from __future__ import annotations

from dataclasses import dataclass, field
from pickle import dumps
from shelve import Shelf, open
from typing import Callable, Generator, Generic, Iterable, Mapping, TypeVar, TypeAlias
from uuid import UUID

from .implementation import (
    Anchor,
    EdgeAnchor,
    JID,
    NodeAnchor,
    Root,
    WalkerAnchor,
    _ANCHORS,
)
from .interface import Memory


@dataclass
class ShelfStorage(Memory[JID, Anchor]):
    """Shelf Handler."""

    __shelf__: Shelf[Anchor] | None = None

    def __init__(self, session: str | None = None) -> None:
        """Initialize memory handler."""
        self.__mem__ = {}
        self.__gc__ = set()
        self.__shelf__ = open(session) if session else None  # noqa: SIM115

    def close(self) -> None:
        """Close memory handler."""
        if isinstance(self.__shelf__, Shelf):
            from jaclang.plugin.feature import JacFeature as Jac

            for jid in self.__gc__:
                self.__shelf__.pop(str(jid), None)
                self.__mem__.pop(jid, None)

            for d in self.__mem__.values():
                if d.persistent and d.hash != hash(dumps(d)):
                    _id = str(d.id)
                    if p_d := self.__shelf__.get(_id):
                        if (
                            isinstance(p_d, NodeAnchor)
                            and isinstance(d, NodeAnchor)
                            and p_d.edges != d.edges
                            and Jac.check_connect_access(d)
                        ):
                            if not d.edges:
                                self.__shelf__.pop(_id, None)
                                continue
                            p_d.edges = d.edges

                        if Jac.check_write_access(d):
                            if hash(dumps(p_d.access)) != hash(dumps(d.access)):
                                p_d.access = d.access
                            if hash(dumps(p_d.architype)) != hash(dumps(d.architype)):
                                p_d.architype = d.architype

                        self.__shelf__[_id] = p_d
                    elif not (
                        isinstance(d, NodeAnchor)
                        and not isinstance(d.architype, Root)
                        and not d.edges
                    ):
                        self.__shelf__[_id] = d

            self.__shelf__.close()
        self.__mem__.clear()
        self.__gc__.clear()

    def find(
        self,
        ids: JID[_ANCHORS] | Iterable[JID[_ANCHORS]],
        filter: Callable[[_ANCHORS], _ANCHORS] | None = None,
    ) -> Generator[_ANCHORS, None, None]:
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
                if (
                    anchor
                    and isinstance(anchor, id.type)
                    and (not filter or filter(anchor))
                ):
                    yield anchor
        else:
            for id in ids:
                if (
                    (anchor := self.__mem__.get(id))
                    and isinstance(anchor, id.type)
                    and (not filter or filter(anchor))
                ):
                    yield anchor

    def find_by_id(self, id: JID[_ANCHORS]) -> _ANCHORS | None:
        """Find one by id."""
        if (data := self.__mem__.get(id)) and isinstance(data, id.type):
            return data

        if (
            isinstance(self.__shelf__, Shelf)
            and (data := self.__shelf__.get(str(id)))
            and isinstance(data, id.type)
        ):
            self.__mem__[id] = data
            return data

        return None
