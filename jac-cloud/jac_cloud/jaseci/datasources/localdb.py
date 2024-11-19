"""Monty Implementations."""

from typing import Any

from montydb import MontyClient as _MontyClient, set_storage  # type: ignore[import-untyped]
from montydb.collection import MontyCollection as _MontyCollection  # type: ignore[import-untyped]
from montydb.database import MontyDatabase as _MontyDatabase  # type: ignore[import-untyped]

from pymongo import DeleteMany, DeleteOne, InsertOne, UpdateMany, UpdateOne
from pymongo.cursor import Cursor
from pymongo.results import BulkWriteResult, InsertManyResult, InsertOneResult


class MontyClientSession:
    """Monty Client Session."""

    def start_transaction(self) -> "MontyClientSession":
        """Start transaction."""
        return self

    def abort_transaction(self) -> None:
        """Abort transaction."""

    def commit_transaction(self) -> None:
        """Commit transaction."""

    def __enter__(self) -> "MontyClientSession":
        """Enter execution."""
        return self

    def __exit__(
        self, exc_type: Any, exc_val: Any, exc_tb: Any  # noqa: ANN401
    ) -> None:
        """Exit execution."""
        pass


class MontyCollection(_MontyCollection):
    """Monty Collection."""

    def __init__(self, col: _MontyCollection) -> None:
        """Override Init."""
        self.__dict__.update(col.__dict__)

    def create_indexes(self, *args, **kwargs: Any) -> None:  # noqa: ANN401, ANN002
        """Bypass Create Indexes."""
        pass

    def insert_one(
        self, document: dict, session: MontyClientSession | None = None
    ) -> InsertOneResult:
        """Override insert_one."""
        return super().insert_one(document)

    def insert_many(
        self,
        documents: list[dict],
        session: MontyClientSession | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> InsertManyResult:
        """Override insert_many."""
        return super().insert_many(documents, **kwargs)

    def find(
        self,
        filter: dict | None = None,
        projection: dict | None = None,
        session: MontyClientSession | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> Cursor:
        """Override find."""
        return super().find(filter, **kwargs)

    def find_one(
        self,
        filter: dict | None = None,
        projection: dict | None = None,
        session: MontyClientSession | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> Any | None:
        """Override find_one."""
        return super().find_one(filter, **kwargs)

    def count_documents(
        self,
        filter: dict,
        session: MontyClientSession | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> int:
        """Override count_documents."""
        return super().count_documents(filter, **kwargs)

    def bulk_write(
        self,
        ops: list[InsertOne | DeleteMany | DeleteOne | UpdateMany | UpdateOne],
        ordered: bool = True,
        session: MontyClientSession | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> BulkWriteResult:
        """Bulk write operations."""
        deleted_count = 0
        inserted_count = 0
        modified_count = 0

        for op in ops:
            match op:
                case InsertOne():
                    if self.insert_one(op._doc).inserted_id:
                        inserted_count += 1
                case DeleteMany():
                    deleted_count += self.delete_many(op._filter).deleted_count
                case DeleteOne():
                    deleted_count += self.delete_one(op._filter).deleted_count
                case UpdateMany():
                    modified_count += self.update_many(
                        op._filter, op._doc
                    ).modified_count
                case UpdateOne():
                    modified_count += self.update_one(
                        op._filter, op._doc
                    ).modified_count
                case _:
                    pass

        return BulkWriteResult(
            {
                "bulk_api_result": {},
                "deleted_count": deleted_count,
                "inserted_count": inserted_count,
                "matched_count": deleted_count + modified_count,
                "modified_count": modified_count,
                "upserted_count": 0,
                "upserted_ids": {},
            },
            True,
        )


class MontyDatabase(_MontyDatabase):
    """Monty Database."""

    def __init__(self, db: _MontyDatabase) -> None:
        """Override Init."""
        self.__dict__.update(db.__dict__)

    def get_collection(self, name: str) -> MontyCollection:
        """Get Collection."""
        return MontyCollection(super().get_collection(name))  # noqa: B009


class MontyClient(_MontyClient):
    """Monty Client."""

    def get_database(self, name: str) -> MontyDatabase:
        """Get local database."""
        return MontyDatabase(super().get_database(name))

    def start_session(self) -> MontyClientSession:
        """Start session."""
        return MontyClientSession()


__all__ = ["MontyClient", "set_storage"]
