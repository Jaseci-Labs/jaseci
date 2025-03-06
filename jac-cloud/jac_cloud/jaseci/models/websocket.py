"""Jaseci Models."""

from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Generator, Mapping, cast

from bson import ObjectId

from ..datasources.collection import Collection as BaseCollection


@dataclass(kw_only=True)
class WebSocket:
    """WebSocket Base Model."""

    id: ObjectId = field(default_factory=ObjectId)
    name: str
    root_id: ObjectId
    walkers: list[str]
    nodes: list[str]
    expiration: datetime
    key: str

    class Collection(BaseCollection["WebSocket"]):
        """
        WebSocket collection interface.

        This interface is for WebSocket Credentials Management.
        You may override this if you wish to implement different structure
        """

        __collection__ = "websocket"
        __indexes__ = [
            {"keys": ["name"], "unique": True},
            {"keys": ["key"], "unique": True},
        ]

        @classmethod
        def __document__(cls, doc: Mapping[str, Any]) -> "WebSocket":
            """
            Return parsed WebSocket from document.

            This the default WebSocket parser after getting a single document.
            You may override this to specify how/which class it will be casted/based.
            """
            doc = cast(dict, doc)
            return WebSocket(id=doc.pop("_id"), **doc)

        @classmethod
        def find_by_root_id(
            cls, root_id: ObjectId
        ) -> Generator["WebSocket", None, None]:
            """Retrieve websocket via root_id."""
            return cls.find({"root_id": root_id})

        @classmethod
        def find_by_key(cls, key: str) -> "WebSocket | None":
            """Retrieve websocket via root_id."""
            return cls.find_one({"key": key})

    def __serialize__(self) -> dict:
        """Return serializable."""
        data = asdict(self)
        data["_id"] = data.pop("id")
        return data
