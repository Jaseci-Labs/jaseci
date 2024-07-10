"""Collection Abstract."""

from os import getenv
from typing import (
    Any,
    AsyncGenerator,
    Generic,
    Iterable,
    Mapping,
    Optional,
    TypeVar,
    Union,
    cast,
)

from bson import ObjectId

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorClientSession,
    AsyncIOMotorCollection,
    AsyncIOMotorCursor,
    AsyncIOMotorDatabase,
)

from pymongo import DeleteMany, DeleteOne, IndexModel, InsertOne, UpdateMany, UpdateOne
from pymongo.server_api import ServerApi

from .utils import logger

T = TypeVar("T")


class Collection(Generic[T]):
    """
    Base collection interface.

    This interface use for connecting to mongodb.
    """

    ##########################################
    # ---------- Child Properties ---------- #
    ##########################################

    # Collection Name
    __collection__: Optional[str] = None
    # Singleton Collection Instance
    __collection_obj__: Optional[AsyncIOMotorCollection] = None

    # Custom Index Declaration
    __indexes__: list[dict] = []
    __default_indexes__: list[dict] = []

    # Transient Field List
    __excluded__: list = []
    # Converted Mapping of Transient Fields
    __excluded_obj__: Optional[Mapping[str, Any]] = None

    ##########################################
    # ---------- Parent Properties --------- #
    ##########################################

    # Singleton client instance
    __client__: Optional[AsyncIOMotorClient] = None
    # Singleton database instance
    __database__: Optional[AsyncIOMotorDatabase] = None

    @staticmethod
    async def apply_indexes() -> None:
        """Apply Indexes."""
        queue: list[type[Collection]] = Collection.__subclasses__()
        while queue:
            cls = queue.pop(-1)

            if scls := cls.__subclasses__():
                queue.extend(scls)

            if cls.__collection__ is None:
                continue

            if cls.__excluded__:
                excl_obj = {}
                for excl in cls.__excluded__:
                    excl_obj[excl] = False
                cls.__excluded_obj__ = excl_obj

            idxs = []
            if cls.__default_indexes__:
                for idx in cls.__default_indexes__:
                    idxs.append(IndexModel(**idx))

            if cls.__indexes__:
                for idx in cls.__indexes__:
                    idxs.append(IndexModel(**idx))

            if idxs:
                await cls.collection().create_indexes(idxs)

    @classmethod
    def __document__(cls, doc: Mapping[str, Any]) -> T:
        """
        Return parsed version of document.

        This the default parser after getting a single document.
        You may override this to specify how/which class it will be casted/based.
        """
        return cast(T, doc)

    @classmethod
    async def __documents__(cls, docs: AsyncIOMotorCursor) -> AsyncGenerator[T, None]:
        """
        Return parsed version of multiple documents.

        This the default parser after getting a list of documents.
        You may override this to specify how/which class it will be casted/based.
        """
        return (cls.__document__(doc) async for doc in docs)

    @staticmethod
    def get_client() -> AsyncIOMotorClient:
        """Return pymongo.database.Database for mongodb connection."""
        if not isinstance(Collection.__client__, AsyncIOMotorClient):
            Collection.__client__ = AsyncIOMotorClient(
                getenv(
                    "DATABASE_HOST",
                    "mongodb://localhost/?retryWrites=true&w=majority",
                ),
                server_api=ServerApi("1"),
            )

        return Collection.__client__

    @staticmethod
    async def get_session() -> AsyncIOMotorClientSession:
        """Return pymongo.client_session.ClientSession used for mongodb transactional operations."""
        return await Collection.get_client().start_session()

    @staticmethod
    def get_database() -> AsyncIOMotorDatabase:
        """Return pymongo.database.Database for database connection based from current client connection."""
        if not isinstance(Collection.__database__, AsyncIOMotorDatabase):
            Collection.__database__ = Collection.get_client().get_database(
                getenv("DATABASE_NAME", "jaclang")
            )

        return Collection.__database__

    @staticmethod
    def get_collection(collection: str) -> AsyncIOMotorCollection:
        """Return pymongo.collection.Collection for collection connection based from current database connection."""
        return Collection.get_database().get_collection(collection)

    @classmethod
    def collection(cls) -> AsyncIOMotorCollection:
        """Return pymongo.collection.Collection for collection connection based from attribute of it's child class."""
        if not isinstance(cls.__collection_obj__, AsyncIOMotorCollection):
            cls.__collection_obj__ = cls.get_collection(
                getattr(cls, "__collection__", None) or cls.__name__.lower()
            )

        return cls.__collection_obj__

    @classmethod
    async def insert_one(
        cls,
        doc: dict,
        session: Optional[AsyncIOMotorClientSession] = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> Optional[ObjectId]:
        """Insert single document and return the inserted id."""
        try:
            ops = await cls.collection().insert_one(doc, session=session, **kwargs)
            return ops.inserted_id
        except Exception:
            if session:
                raise
            logger.exception(f"Error inserting doc:\n{doc}")
        return None

    @classmethod
    async def insert_many(
        cls,
        docs: list[dict],
        session: Optional[AsyncIOMotorClientSession] = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> list[ObjectId]:
        """Insert multiple documents and return the inserted ids."""
        try:
            ops = await cls.collection().insert_many(docs, session=session, **kwargs)
            return ops.inserted_ids
        except Exception:
            if session:
                raise
            logger.exception(f"Error inserting docs:\n{docs}")
        return []

    @classmethod
    async def update_one(
        cls,
        filter: dict,
        update: dict,
        session: Optional[AsyncIOMotorClientSession] = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> int:
        """Update single document and return if it's modified or not."""
        try:
            ops = await cls.collection().update_one(
                filter, update, session=session, **kwargs
            )
            return ops.modified_count
        except Exception:
            if session:
                raise
            logger.exception(f"Error updating doc:\n{filter}\n{update}")
        return 0

    @classmethod
    async def update_many(
        cls,
        filter: dict,
        update: dict,
        session: Optional[AsyncIOMotorClientSession] = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> int:
        """Update multiple documents and return how many docs are modified."""
        try:
            ops = await cls.collection().update_many(
                filter, update, session=session, **kwargs
            )
            return ops.modified_count
        except Exception:
            if session:
                raise
            logger.exception(f"Error updating doc:\n{filter}\n{update}")
        return 0

    @classmethod
    async def update_by_id(
        cls,
        id: Union[str, ObjectId],
        update: dict,
        session: Optional[AsyncIOMotorClientSession] = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> int:
        """Update single document via ID and return if it's modified or not."""
        return await cls.update_one({"_id": ObjectId(id)}, update, session, **kwargs)

    @classmethod
    async def find(
        cls,
        filter: Optional[Mapping[str, Any]] = None,
        projection: Optional[Union[Mapping[str, Any], Iterable[str]]] = None,
        session: Optional[AsyncIOMotorClientSession] = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> AsyncGenerator[T, None]:
        """Retrieve multiple documents."""
        if projection is None:
            projection = cls.__excluded_obj__

        docs = cls.collection().find(filter, projection, session=session, **kwargs)
        return await cls.__documents__(docs)

    @classmethod
    async def find_one(
        cls,
        filter: Optional[Mapping[str, Any]] = None,
        projection: Optional[Union[Mapping[str, Any], Iterable[str]]] = None,
        session: Optional[AsyncIOMotorClientSession] = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> Optional[T]:
        """Retrieve single document from db."""
        if projection is None:
            projection = cls.__excluded_obj__

        if ops := await cls.collection().find_one(
            filter, projection, session=session, **kwargs
        ):
            return cls.__document__(ops)
        return cast(Optional[T], ops)

    @classmethod
    async def find_by_id(
        cls,
        id: Union[str, ObjectId],
        projection: Optional[Union[Mapping[str, Any], Iterable[str]]] = None,
        session: Optional[AsyncIOMotorClientSession] = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> Optional[T]:
        """Retrieve single document via ID."""
        return await cls.find_one(
            {"_id": ObjectId(id)}, projection, session=session, **kwargs
        )

    @classmethod
    async def delete(
        cls,
        filter: dict,
        session: Optional[AsyncIOMotorClientSession] = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> int:
        """Delete document/s via filter and return how many documents are deleted."""
        try:
            ops = await cls.collection().delete_many(filter, session=session, **kwargs)
            return ops.deleted_count
        except Exception:
            if session:
                raise
            logger.exception(f"Error delete with filter:\n{filter}")
        return 0

    @classmethod
    async def delete_one(
        cls,
        filter: dict,
        session: Optional[AsyncIOMotorClientSession] = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> int:
        """Delete single document via filter and return if it's deleted or not."""
        try:
            ops = await cls.collection().delete_one(filter, session=session, **kwargs)
            return ops.deleted_count
        except Exception:
            if session:
                raise
            logger.exception(f"Error delete one with filter:\n{filter}")
        return 0

    @classmethod
    async def delete_by_id(
        cls,
        id: Union[str, ObjectId],
        session: Optional[AsyncIOMotorClientSession] = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> int:
        """Delete single document via ID and return if it's deleted or not."""
        return await cls.delete_one({"_id": ObjectId(id)}, session, **kwargs)

    @classmethod
    async def bulk_write(
        cls,
        ops: list[Union[InsertOne, DeleteMany, DeleteOne, UpdateMany, UpdateOne]],
        session: Optional[AsyncIOMotorClientSession] = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> dict:
        """Bulk write operations."""
        try:
            _ops = await cls.collection().bulk_write(ops, session=session, **kwargs)
            return _ops.bulk_api_result
        except Exception:
            if session:
                raise
            logger.exception(f"Error bulk write:\n{ops}")
        return {}
