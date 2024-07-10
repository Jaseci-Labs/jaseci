"""Jaseci Redis."""

from os import getenv
from typing import Any, Optional, Union, cast

from jaclang.vendor.lark import logger

from orjson import dumps, loads

from redis import asyncio as aioredis
from redis.asyncio.client import Redis as _Redis


class Redis:
    """
    Base Memory interface.

    This interface use for connecting to redis.
    """

    ##########################################
    # ---------- Child Properties ---------- #
    ##########################################

    # Redis Hash Name
    __table__ = "common"

    ##########################################
    # ---------- Parent Properties --------- #
    ##########################################

    # Singleton redis client instance
    __redis__: Optional[_Redis] = None

    @staticmethod
    def get_rd() -> _Redis:
        """Return redis.Redis for Redis connection."""
        if not isinstance(Redis.__redis__, _Redis):
            Redis.__redis__ = aioredis.from_url(
                getenv("REDIS_HOST", "redis://localhost"),
                port=int(getenv("REDIS_PORT", "6379")),
                username=getenv("REDIS_USER"),
                password=getenv("REDIS_PASS"),
            )
        return Redis.__redis__

    @classmethod
    async def get(cls, key: str) -> Any:  # noqa: ANN401
        """Retrieve via key."""
        try:
            redis = cls.get_rd()
            return loads(cast(str, await redis.get(key)))
        except Exception:
            logger.exception(f"Error getting key {key}")
            return None

    @classmethod
    async def keys(cls) -> list[bytes]:
        """Return all available keys."""
        try:
            redis = cls.get_rd()
            return await redis.keys()
        except Exception:
            logger.exception("Error getting keys")
            return []

    @classmethod
    async def set(cls, key: str, data: Union[dict, bool]) -> bool:
        """Push key value pair."""
        try:
            redis = cls.get_rd()
            return bool(await redis.set(key, dumps(data)))
        except Exception:
            logger.exception(f"Error setting key {key} with data\n{data}")
            return False

    @classmethod
    async def delete(cls, key: str) -> bool:
        """Delete via key."""
        try:
            redis = cls.get_rd()
            return bool(await redis.delete(key))
        except Exception:
            logger.exception(f"Error deleting key {key}")
            return False

    @classmethod
    async def hget(cls, key: str) -> Any:  # noqa: ANN401
        """Retrieve via key from group."""
        try:
            redis = cls.get_rd()
            return loads(cast(str, await redis.hget(cls.__table__, key)))
        except Exception:
            logger.exception(f"Error getting key {key} from {cls.__table__}")

    @classmethod
    async def hkeys(cls) -> list[str]:
        """Retrieve all available keys from group."""
        try:
            redis = cls.get_rd()
            return await redis.hkeys(cls.__table__)
        except Exception:
            logger.exception(f"Error getting keys from {cls.__table__}")
            return []

    @classmethod
    async def hset(cls, key: str, data: Union[dict, bool]) -> bool:
        """Push key value pair to group."""
        try:
            redis = cls.get_rd()
            return bool(await redis.hset(cls.__table__, key, dumps(data).decode()))
        except Exception:
            logger.exception(
                f"Error setting key {key} from {cls.__table__} with data\n{data}"
            )
            return False

    @classmethod
    async def hdelete(cls, *keys: Any) -> bool:  # noqa: ANN401
        """Delete via key from group."""
        try:
            redis = cls.get_rd()
            return bool(await redis.hdel(cls.__table__, *keys))
        except Exception:
            logger.exception(f"Error deleting key {keys} from {cls.__table__}")
            return False


class CodeRedis(Redis):
    """Code Memory Interface.

    This interface is for Code Management such as Verification Code.
    You may override this if you wish to implement different structure
    """

    __table__ = "verification"


class TokenRedis(Redis):
    """Token Memory Interface.

    This interface is for Token Management.
    You may override this if you wish to implement different structure
    """

    __table__ = "token"
