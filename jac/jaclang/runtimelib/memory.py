"""Core constructs for Jac Language."""

from __future__ import annotations

from dataclasses import dataclass, field
from pickle import dumps
from shelve import Shelf, open
from typing import Callable, Generator, Iterable

from .architype import Anchor, JID, NodeAnchor, Root, _ANCHOR


@dataclass
class Memory:
    """Generic Memory Handler."""

    __mem__: dict[JID, Anchor] = field(default_factory=dict)
    __gc__: set[JID] = field(default_factory=set)

    def close(self) -> None:
        """Close memory handler."""
        self.__mem__.clear()
        self.__gc__.clear()

    def is_cached(self, id: JID) -> bool:
        """Check if id if already cached."""
        return id in self.__mem__

    def find(
        self,
        ids: JID[_ANCHOR] | Iterable[JID[_ANCHOR]],
        filter: Callable[[_ANCHOR], _ANCHOR] | None = None,
    ) -> Generator[_ANCHOR, None, None]:
        """Find anchors from memory by ids with filter."""
        if not isinstance(ids, Iterable):
            ids = [ids]

        return (
            anchor
            for id in ids
            if (anchor := self.__mem__.get(id))
            and isinstance(anchor, id.type)
            and (not filter or filter(anchor))
        )

    def find_one(
        self,
        ids: JID[_ANCHOR] | Iterable[JID[_ANCHOR]],
        filter: Callable[[_ANCHOR], _ANCHOR] | None = None,
    ) -> _ANCHOR | None:
        """Find one anchor from memory by ids with filter."""
        return next(self.find(ids, filter), None)

    def find_by_id(self, id: JID[_ANCHOR]) -> _ANCHOR | None:
        """Find one by id."""
        return (
            anchor
            if (anchor := self.__mem__.get(id)) and isinstance(anchor, id.type)
            else None
        )

    def set(self, id: JID[_ANCHOR], data: _ANCHOR) -> None:
        """Save anchor to memory."""
        self.__mem__[id] = data

    def remove(self, ids: JID | Iterable[JID]) -> None:
        """Remove anchor/s from memory."""
        if not isinstance(ids, Iterable):
            ids = [ids]

        for id in ids:
            self.__mem__.pop(id, None)
            self.__gc__.add(id)


@dataclass
class ShelfStorage(Memory):
    """Shelf Handler."""

    __shelf__: Shelf[Anchor] | None = None

    def __init__(self, session: str | None = None) -> None:
        """Initialize memory handler."""
        super().__init__()
        self.__shelf__ = open(session) if session else None  # noqa: SIM115

    def close(self) -> None:
        """Close memory handler."""
        if isinstance(self.__shelf__, Shelf):
            for jid in self.__gc__:
                self.__shelf__.pop(str(jid), None)
                self.__mem__.pop(jid, None)

            keys = set(self.__mem__.keys())

            # current memory
            self.sync_mem_to_db(keys)

            # additional after memory sync
            self.sync_mem_to_db(set(self.__mem__.keys() - keys))

            self.__shelf__.close()
        super().close()

    def sync_mem_to_db(self, keys: Iterable[JID]) -> None:
        """Manually sync memory to db."""
        from jaclang.plugin.feature import JacFeature as Jac

        if isinstance(self.__shelf__, Shelf):
            for key in keys:
                if (
                    (d := self.__mem__.get(key))
                    and d.persistent
                    and d.hash != hash(dumps(d))
                ):
                    _id = str(d.jid)
                    if p_d := self.__shelf__.get(_id):
                        if (
                            isinstance(p_d, NodeAnchor)
                            and isinstance(d, NodeAnchor)
                            and p_d.edges != d.edges
                            and Jac.check_connect_access(d)
                        ):
                            if not d.edges and not isinstance(d.architype, Root):
                                self.__shelf__.pop(_id, None)
                                continue
                            p_d.edges = d.edges

                        if hash(dumps(p_d.architype)) != hash(
                            dumps(d.architype)
                        ) and Jac.check_write_access(d):
                            p_d.architype = d.architype

                        if hash(dumps(p_d.access)) != hash(
                            dumps(d.access)
                        ) and Jac.check_write_access(d):
                            p_d.access = d.access

                        self.__shelf__[_id] = p_d
                    elif not (
                        isinstance(d, NodeAnchor)
                        and not isinstance(d.architype, Root)
                        and not d.edges
                    ):
                        self.__shelf__[_id] = d

    def find(
        self,
        ids: JID[_ANCHOR] | Iterable[JID[_ANCHOR]],
        filter: Callable[[_ANCHOR], _ANCHOR] | None = None,
    ) -> Generator[_ANCHOR, None, None]:
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
                    anchor = self.__mem__[id] = _anchor
                    anchor.architype.__jac__ = anchor
                if (
                    anchor
                    and isinstance(anchor, id.type)
                    and (not filter or filter(anchor))
                ):
                    yield anchor
        else:
            yield from super().find(ids, filter)

    def find_by_id(self, id: JID[_ANCHOR]) -> _ANCHOR | None:
        """Find one by id."""
        data = super().find_by_id(id)

        if (
            not data
            and isinstance(self.__shelf__, Shelf)
            and (_data := self.__shelf__.get(str(id)))
            and isinstance(_data, id.type)
        ):
            data = self.__mem__[id] = _data
            data.architype.__jac__ = data

        return data
