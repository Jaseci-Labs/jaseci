"""Memory abstraction for jaseci plugin."""

from dataclasses import dataclass, field
from typing import Any, AsyncGenerator, Callable, Generator, Type

from bson import ObjectId

from jaclang.runtimelib.architype import MANUAL_SAVE


from motor.motor_asyncio import AsyncIOMotorClientSession

from pymongo import DeleteMany, DeleteOne, InsertOne, UpdateMany, UpdateOne

from .architype import (
    Anchor,
    AnchorType,
    EdgeAnchor,
    NodeAnchor,
    WalkerAnchor,
)
from ..jaseci.datasources import Collection
from ..jaseci.utils import logger

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
        ids: IDS,
        filter: Callable[[Anchor], Anchor] | None = None,
        session: AsyncIOMotorClientSession | None = None,
    ) -> AsyncGenerator[Anchor, None]:
        """Find anchors from datasource by ids with filter."""
        if not isinstance(ids, list):
            ids = [ids]

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
                "_id": {"$in": [id for id in ids if id not in self.__mem__]},
            },
            session=session or self.__session__,
        ):
            self.__mem__[anchor.id] = anchor

        for id in ids:
            if (_anchor := self.__mem__.get(id)) and (not filter or filter(_anchor)):
                yield _anchor

    async def find_one(  # type: ignore[override]
        self,
        type: AnchorType,
        ids: IDS,
        filter: Callable[[Anchor], Anchor] | None = None,
        session: AsyncIOMotorClientSession | None = None,
    ) -> Anchor | None:
        """Find one anchor from memory by ids with filter."""
        return await anext(self.find(type, ids, filter, session), None)

    def remove(self, data: Anchor | list[Anchor]) -> None:
        """Remove anchor/s from datasource."""
        super().remove(data)

    async def sync(self, session: AsyncIOMotorClientSession) -> None:
        """Sync memory to database."""
        operations: dict[
            AnchorType,
            list[InsertOne[Any] | DeleteMany | DeleteOne | UpdateMany | UpdateOne],
        ] = {
            AnchorType.node: [],
            AnchorType.edge: [],
            AnchorType.walker: [],
            AnchorType.generic: [],  # ignored
        }

        del_node_ids = []
        del_edge_ids = []
        del_walker_ids = []
        for anchor in self.__gc__:
            match anchor.type:
                case AnchorType.node:
                    del_node_ids.append(anchor.id)
                case AnchorType.edge:
                    del_edge_ids.append(anchor.id)
                case AnchorType.walker:
                    del_walker_ids.append(anchor.id)
                case _:
                    pass

        if del_node_ids:
            operations[AnchorType.node].append(
                DeleteMany({"_id": {"$in": del_node_ids}})
            )
        if del_edge_ids:
            operations[AnchorType.edge].append(
                DeleteMany({"_id": {"$in": del_edge_ids}})
            )
        if del_walker_ids:
            operations[AnchorType.walker].append(
                DeleteMany({"_id": {"$in": del_walker_ids}})
            )

        if not MANUAL_SAVE:
            for anchor in self.__mem__.values():
                if anchor.architype and anchor.persistent:
                    if not anchor.connected:
                        anchor.connected = True
                        anchor.sync_hash()
                        operations[anchor.type].append(InsertOne(anchor.serialize()))
                    elif anchor.current_access_level > 0 and (
                        changes := await anchor.pull_changes(False)
                    ):
                        operations[anchor.type] += changes

        if node_operation := operations[AnchorType.node]:
            await NodeAnchor.Collection.bulk_write(node_operation, session)
        if edge_operation := operations[AnchorType.edge]:
            await EdgeAnchor.Collection.bulk_write(edge_operation, session)
        if walker_operation := operations[AnchorType.walker]:
            await WalkerAnchor.Collection.bulk_write(walker_operation, session)

    async def close(self) -> None:  # type: ignore[override]
        """Close memory handler."""
        if self.__session__:
            await self.sync(self.__session__)
        else:
            async with await Collection.get_session() as session:
                async with session.start_transaction():
                    try:
                        await self.sync(session)
                        await session.commit_transaction()
                    except Exception:
                        await session.abort_transaction()
                        logger.exception("Error syncing memory to database!")
                        raise

        super().close()
