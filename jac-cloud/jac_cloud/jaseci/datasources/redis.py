"""Jaseci Redis."""

from os import getenv
from typing import Any, cast

from fakeredis import FakeRedis

from orjson import dumps, loads

from redis.asyncio.client import Redis as _AsyncRedis
from redis.backoff import ExponentialBackoff
from redis.client import Redis as _Redis
from redis.connection import ConnectionPool
from redis.exceptions import ConnectionError, TimeoutError
from redis.retry import Retry

from ..utils import logger


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
    __redis__: _Redis | None = None

    @staticmethod
    def get_rd() -> _Redis:
        """Return redis.Redis for Redis connection."""
        if Redis.__redis__ is None:
            if host := getenv("REDIS_HOST"):
                Redis.__redis__ = _Redis(
                    connection_pool=ConnectionPool.from_url(
                        host,
                        port=int(getenv("REDIS_PORT", "6379")),
                        username=getenv("REDIS_USER"),
                        password=getenv("REDIS_PASS"),
                    ),
                    retry=Retry(
                        ExponentialBackoff(
                            cap=int(getenv("REDIS_RETRY_BACKOFF_CAP", "10")),
                            base=int(getenv("REDIS_RETRY_BACKOFF_BASE", "1")),
                        ),
                        retries=int(getenv("REDIS_MAX_RETRY", "5")),
                    ),
                    retry_on_error=[ConnectionError, TimeoutError],
                )
            else:
                logger.info("REDIS_HOST is not available! Using FakeRedis...")
                Redis.__redis__ = FakeRedis()

        return Redis.__redis__

    @classmethod
    def get(cls, key: str) -> Any:  # noqa: ANN401
        """Retrieve via key."""
        try:
            redis = cls.get_rd()
            if res := redis.get(key):
                return loads(res)
            return None
        except Exception:
            logger.exception(f"Error getting key {key}")
            return None

    @classmethod
    def keys(cls) -> list[bytes]:
        """Return all available keys."""
        try:
            redis = cls.get_rd()
            return redis.keys()
        except Exception:
            logger.exception("Error getting keys")
            return []

    @classmethod
    def set(cls, key: str, data: dict | bool | float) -> bool:
        """Push key value pair."""
        try:
            redis = cls.get_rd()
            return bool(redis.set(key, dumps(data)))
        except Exception:
            logger.exception(f"Error setting key {key} with data\n{data}")
            return False

    @classmethod
    def delete(cls, key: str) -> bool:
        """Delete via key."""
        try:
            redis = cls.get_rd()
            return bool(redis.delete(key))
        except Exception:
            logger.exception(f"Error deleting key {key}")
            return False

    @classmethod
    def hget(cls, key: str) -> Any:  # noqa: ANN401
        """Retrieve via key from group."""
        try:
            redis = cls.get_rd()
            if res := redis.hget(cls.__table__, key):
                res = loads(res)
            return res
        except Exception:
            logger.exception(f"Error getting key {key} from {cls.__table__}")

    @classmethod
    def hkeys(cls) -> list[str]:
        """Retrieve all available keys from group."""
        try:
            redis = cls.get_rd()
            return redis.hkeys(cls.__table__)
        except Exception:
            logger.exception(f"Error getting keys from {cls.__table__}")
            return []

    @classmethod
    def hset(cls, key: str, data: dict | bool | float) -> bool:
        """Push key value pair to group."""
        try:
            redis = cls.get_rd()
            return bool(redis.hset(cls.__table__, key, dumps(data).decode()))
        except Exception:
            logger.exception(
                f"Error setting key {key} from {cls.__table__} with data\n{data}"
            )
            return False

    @classmethod
    def hsetnx(cls, key: str, data: dict | bool | float) -> bool:
        """Push key value pair to group."""
        try:
            redis = cls.get_rd()
            return cast(bool, redis.hsetnx(cls.__table__, key, dumps(data).decode()))
        except Exception:
            logger.exception(
                f"Error setting key {key} from {cls.__table__} with data\n{data}"
            )
            return False

    @classmethod
    def hdelete(cls, *keys: Any) -> bool:  # noqa: ANN401
        """Delete via key from group."""
        try:
            redis = cls.get_rd()
            return bool(redis.hdel(cls.__table__, *keys))
        except Exception:
            logger.exception(f"Error deleting key {keys} from {cls.__table__}")
            return False

    @classmethod
    def hdelete_rgx(cls, key: str) -> bool:
        """Delete via key pattern from group."""
        try:
            redis = cls.get_rd()
            for hkeys in redis.hscan_iter(cls.__table__, key):
                redis.hdel(cls.__table__, *hkeys)
            return True
        except Exception:
            logger.exception(f"Error deleting key {key} from {cls.__table__}")
            return False

    @classmethod
    def rpush(cls, key: str, *data: dict | bool | float) -> bool:
        """Push key value pair to group."""
        try:
            redis = cls.get_rd()
            return bool(redis.rpush(key, *(dumps(d).decode() for d in data)))
        except Exception:
            logger.exception(f"Error rpush key {key} with data\n{data}")
            return False

    @classmethod
    def lpop(cls, key: str, count: int | None = None) -> Any:  # noqa: ANN401
        """Retrieve via key from group."""
        try:
            redis = cls.get_rd()
            if res := redis.lpop(key, count):
                if isinstance(res, list):
                    res = [loads(r) for r in res]
                else:
                    res = loads(res)  # type: ignore[arg-type]
            return res
        except Exception:
            logger.exception(f"Error lpop key {key} with count {count}")


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


class WebhookRedis(Redis):
    """Webhook Memory Interface.

    This interface is for Token Management.
    You may override this if you wish to implement different structure
    """

    __table__ = "webhook"


class ScheduleRedis(Redis):
    """Schedule Memory Interface.

    This interface is for Schedule Management.
    You may override this if you wish to implement different structure
    """

    __table__ = "schedule"


class AsyncRedis:
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
    __redis__: _AsyncRedis | None = None

    @staticmethod
    def get_rd() -> _AsyncRedis:
        """Return redis.Redis for Redis connection."""
        if AsyncRedis.__redis__ is None:
            AsyncRedis.__redis__ = _AsyncRedis.from_url(
                getenv("REDIS_HOST", "redis://localhost"),
                port=int(getenv("REDIS_PORT", "6379")),
                username=getenv("REDIS_USER"),
                password=getenv("REDIS_PASS"),
            )
        return AsyncRedis.__redis__

    @classmethod
    async def get(cls, key: str) -> Any:  # noqa: ANN401
        """Retrieve via key."""
        try:
            redis = cls.get_rd()
            if res := await redis.get(key):
                return loads(res)
            return None
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
    async def set(cls, key: str, data: dict | bool | float) -> bool:
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
            if res := await redis.hget(cls.__table__, key):
                res = loads(res)
            return res
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
    async def hset(cls, key: str, data: dict | bool | float) -> bool:
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

    @classmethod
    async def hdelete_rgx(cls, key: str) -> bool:
        """Delete via key pattern from group."""
        try:
            redis = cls.get_rd()
            async for hkeys in redis.hscan_iter(cls.__table__, key):
                await redis.hdel(cls.__table__, *hkeys)
            return True
        except Exception:
            logger.exception(f"Error deleting key {key} from {cls.__table__}")
            return False


class AsyncCodeRedis(AsyncRedis):
    """Code Memory Interface.

    This interface is for Code Management such as Verification Code.
    You may override this if you wish to implement different structure
    """

    __table__ = "verification"


class AsyncTokenRedis(AsyncRedis):
    """Token Memory Interface.

    This interface is for Token Management.
    You may override this if you wish to implement different structure
    """

    __table__ = "token"
