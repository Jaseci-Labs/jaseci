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
    __is_served__: bool | None = None

    @staticmethod
    def serve() -> None:
        """Tag Fastapi as served."""
        from jaclang.plugin.feature import JacFeature as Jac

        from ..core.architype import (
            EdgeArchitype,
            NodeArchitype,
            ObjectArchitype,
            Root,
            WalkerArchitype,
        )

        FastAPI.__is_served__ = True

        Jac.RootType = Root  # type: ignore[assignment]
        Jac.Obj = ObjectArchitype  # type: ignore[assignment]
        Jac.Node = NodeArchitype  # type: ignore[assignment]
        Jac.Edge = EdgeArchitype  # type: ignore[assignment]
        Jac.Walker = WalkerArchitype  # type: ignore[assignment]

    @staticmethod
    def is_served() -> bool:
        """Check if FastAPI is already served."""
        if FastAPI.__is_served__ is None:
            from jaclang.runtimelib.machine import JacMachine

            main = JacMachine.get().loaded_modules.get("__main__")
            if getattr(main, "FastAPI", None) is FastAPI:
                FastAPI.serve()
                return True
            else:
                FastAPI.__is_served__ = False

        return FastAPI.__is_served__

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
