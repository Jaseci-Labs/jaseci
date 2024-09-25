"""Core constructs for Jac Language."""

from __future__ import annotations

from dataclasses import dataclass
from pickle import dumps
from shelve import Shelf, open
from typing import Callable, Generator, Iterable, TypeVar

from .implementation import Anchor, JID, NodeAnchor, Root
from .interface import Memory

ID = TypeVar("ID")


@dataclass
class ShelfStorage(Memory[JID[Anchor], Anchor]):
    """Shelf Handler."""

    __shelf__: Shelf[Anchor] | None = None

    def __init__(self, session: str | None = None) -> None:
        """Initialize memory handler."""
        super().__init__()
        self.__shelf__ = open(session) if session else None  # noqa: SIM115

    def close(self) -> None:
        """Close memory handler."""
        if isinstance(self.__shelf__, Shelf):
            from jaclang.plugin.feature import JacFeature as Jac

            for jid in self.__gc__:
                self.__shelf__.pop(str(jid), None)
                self.__mem__.pop(jid, None)

            for jid, anchor in self.__mem__.items():
                if anchor.persistent and anchor.hash != hash(dumps(anchor)):
                    _jid = str(jid)
                    if p_d := self.__shelf__.get(_jid):
                        if (
                            isinstance(p_d, NodeAnchor)
                            and isinstance(anchor, NodeAnchor)
                            and p_d.edge_ids != anchor.edge_ids
                            and Jac.check_connect_access(anchor)
                        ):
                            if not anchor.edge_ids:
                                self.__shelf__.pop(_jid, None)
                                continue
                            p_d.edge_ids = anchor.edge_ids

                        if Jac.check_write_access(anchor):
                            if hash(dumps(p_d.access)) != hash(dumps(anchor.access)):
                                p_d.access = anchor.access
                            if hash(dumps(anchor.architype)) != hash(
                                dumps(anchor.architype)
                            ):
                                p_d.architype = anchor.architype

                        self.__shelf__[_jid] = p_d
                    elif not (
                        isinstance(anchor, NodeAnchor)
                        and not isinstance(anchor.architype, Root)
                        and not anchor.edge_ids
                    ):
                        self.__shelf__[_jid] = anchor

            self.__shelf__.close()
        super().close()

    def find(
        self,
        ids: JID[Anchor] | Iterable[JID[Anchor]],
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

    def find_by_id(self, id: JID[Anchor]) -> Anchor | None:
        """Find one by id."""
        data = super().find_by_id(id)

        if (
            not data
            and isinstance(self.__shelf__, Shelf)
            and (data := self.__shelf__.get(str(id)))
        ):
            self.__mem__[id] = data

        return data
