"""Memory abstraction for jaseci plugin."""

from dataclasses import dataclass, field
from os import getenv
from typing import AsyncGenerator, Callable, Generator, Type

from bson import ObjectId

from jaclang.runtimelib.architype import MANUAL_SAVE


from motor.motor_asyncio import AsyncIOMotorClientSession

from pymongo import InsertOne

from .architype import (
    Anchor,
    AnchorType,
    BulkWrite,
    EdgeAnchor,
    NodeAnchor,
    Root,
    WalkerAnchor,
)
from ..jaseci.datasources import Collection

DISABLE_AUTO_CLEANUP = getenv("DISABLE_AUTO_CLEANUP") == "true"
IDS = ObjectId | list[ObjectId]


@dataclass
class Memory:
    """Generic Memory Handler."""

    __mem__: dict[ObjectId, Anchor] = field(default_factory=dict)
    __gc__: set[Anchor] = field(default_factory=set)

    def close(self) -> None:
        """Close memory handler."""
        self.__mem__.clear()
        self.__gc__.clear()

    def find(
        self, ids: IDS, filter: Callable[[Anchor], Anchor] | None = None
    ) -> Generator[Anchor, None, None]:
        """Find anchors from memory by ids with filter."""
        if not isinstance(ids, list):
            ids = [ids]

        return (
            anchor
            for id in ids
            if (anchor := self.__mem__.get(id)) and (not filter or filter(anchor))
        )

    def find_one(
        self,
        ids: IDS,
        filter: Callable[[Anchor], Anchor] | None = None,
    ) -> Anchor | None:
        """Find one anchor from memory by ids with filter."""
        return next(self.find(ids, filter), None)

    def set(self, data: Anchor | list[Anchor]) -> None:
        """Save anchor/s to memory."""
        if isinstance(data, list):
            for d in data:
                if d not in self.__gc__:
                    self.__mem__[d.id] = d
        elif data not in self.__gc__:
            self.__mem__[data.id] = data

    def remove(self, data: Anchor | list[Anchor]) -> None:
        """Remove anchor/s from memory."""
        if isinstance(data, list):
            for d in data:
                self.__mem__.pop(d.id, None)
                self.__gc__.add(d)
        else:
            self.__mem__.pop(data.id, None)
            self.__gc__.add(data)


@dataclass
class MongoDB(Memory):
    """Shelf Handler."""

    __session__: AsyncIOMotorClientSession | None = None

    async def find(  # type: ignore[override]
        self,
        type: AnchorType,
        anchors: Anchor | list[Anchor],
        filter: Callable[[Anchor], Anchor] | None = None,
        session: AsyncIOMotorClientSession | None = None,
    ) -> AsyncGenerator[Anchor, None]:
        """Find anchors from datasource by ids with filter."""
        if not isinstance(anchors, list):
            anchors = [anchors]

        base_anchor: Type[Anchor] = Anchor
        match type:
            case AnchorType.node:
                base_anchor = NodeAnchor
            case AnchorType.edge:
                base_anchor = EdgeAnchor
            case AnchorType.walker:
                base_anchor = WalkerAnchor
            case _:
                pass

        async for anchor in await base_anchor.Collection.find(
            {
                "_id": {
                    "$in": [
                        anchor.id
                        for anchor in anchors
                        if anchor.id not in self.__mem__ and anchor not in self.__gc__
                    ]
                },
            },
            session=session or self.__session__,
        ):
            self.__mem__[anchor.id] = anchor

        for anchor in anchors:
            if (
                anchor not in self.__gc__
                and (_anchor := self.__mem__.get(anchor.id))
                and (not filter or filter(_anchor))
            ):
                yield _anchor

    async def find_one(  # type: ignore[override]
        self,
        type: AnchorType,
        anchors: Anchor | list[Anchor],
        filter: Callable[[Anchor], Anchor] | None = None,
        session: AsyncIOMotorClientSession | None = None,
    ) -> Anchor | None:
        """Find one anchor from memory by ids with filter."""
        return await anext(self.find(type, anchors, filter, session), None)

    def get_bulk_write(self) -> BulkWrite:
        """Sync memory to database."""
        bulk_write = BulkWrite()

        for anchor in self.__gc__:
            if anchor.state.deleted is False:
                match anchor.type:
                    case AnchorType.node:
                        bulk_write.del_node(anchor.id)
                    case AnchorType.edge:
                        bulk_write.del_edge(anchor.id)
                    case AnchorType.walker:
                        bulk_write.del_walker(anchor.id)
                    case _:
                        pass

        if not MANUAL_SAVE:
            for anchor in self.__mem__.values():
                if anchor.architype and anchor.state.persistent:
                    if not anchor.state.connected:
                        anchor.state.connected = True
                        anchor.sync_hash()
                        bulk_write.operations[anchor.type].append(
                            InsertOne(anchor.serialize())
                        )
                    elif anchor.state.current_access_level > 0:
                        if (
                            not DISABLE_AUTO_CLEANUP
                            and isinstance(anchor, NodeAnchor)
                            and not isinstance(anchor.architype, Root)
                            and not anchor.edges
                        ):
                            bulk_write.del_node(anchor.id)
                        else:
                            anchor.update(bulk_write)

        return bulk_write

    async def close(self) -> None:  # type: ignore[override]
        """Close memory handler."""
        bulk_write = self.get_bulk_write()

        if bulk_write.has_operations:
            if session := self.__session__:
                await bulk_write.execute(session)
            else:
                async with await Collection.get_session() as session:
                    async with session.start_transaction():
                        await bulk_write.execute(session)

        super().close()
