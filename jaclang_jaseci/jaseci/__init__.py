"""Jaseci FastAPI."""

from contextlib import asynccontextmanager
from os import getenv
from typing import Any, AsyncGenerator

from fastapi import FastAPI as _FaststAPI

from uvicorn import run as _run

from .utils import Emailer


class FastAPI:
    """FastAPI Handler."""

    __app__ = None
    __is_enabled__: bool = False

    @staticmethod
    def enable() -> None:
        """Tag Fastapi as enabled."""
        from jaclang.plugin.feature import JacFeature as Jac

        from ..core.architype import (
            EdgeArchitype,
            NodeArchitype,
            ObjectArchitype,
            Root,
            WalkerArchitype,
        )

        FastAPI.__is_enabled__ = True

        Jac.RootType = Root  # type: ignore[assignment]
        Jac.Obj = ObjectArchitype  # type: ignore[assignment]
        Jac.Node = NodeArchitype  # type: ignore[assignment]
        Jac.Edge = EdgeArchitype  # type: ignore[assignment]
        Jac.Walker = WalkerArchitype  # type: ignore[assignment]

    @staticmethod
    def is_enabled() -> bool:
        """Check if FastAPI is already enabled."""
        return FastAPI.__is_enabled__

    @classmethod
    def get(cls) -> _FaststAPI:
        """Get or Create new instance of FastAPI."""
        if not isinstance(cls.__app__, _FaststAPI):

            @asynccontextmanager
            async def lifespan(app: _FaststAPI) -> AsyncGenerator[None, _FaststAPI]:
                from .datasources import Collection

                Collection.apply_indexes()
                yield

            cls.__app__ = _FaststAPI(lifespan=lifespan)

            from .routers import healthz_router, sso_router, user_router
            from ..plugin.jaseci import walker_router

            for router in [healthz_router, sso_router, user_router, walker_router]:
                cls.__app__.include_router(router)

        return cls.__app__

    @classmethod
    def start(
        cls,
        host: str | None = None,
        port: int | None = None,
        emailer: type[Emailer] | None = None,
        **kwargs: Any  # noqa ANN401
    ) -> None:
        """Run FastAPI Handler via Uvicorn."""
        if emailer:
            emailer.start()

        _run(
            cls.get(),
            host=host or getenv("HOST") or "0.0.0.0",
            port=port or int(getenv("PORT", "8000")),
            **kwargs
        )
