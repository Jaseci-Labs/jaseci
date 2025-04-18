"""Jaseci FastAPI."""

from contextlib import asynccontextmanager
from os import getenv
from traceback import format_exception
from typing import Any, AsyncGenerator

from anyio import create_task_group

from fastapi import FastAPI as _FaststAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from uvicorn import run as _run

from .utils import Emailer, logger, populate_yaml_specs


class FastAPI:
    """FastAPI Handler."""

    __app__ = None
    __is_enabled__: bool = False

    @staticmethod
    def enable() -> None:
        """Tag Fastapi as enabled."""
        from jaclang.runtimelib.feature import JacFeature

        FastAPI.__is_enabled__ = True
        JacFeature.setup()

    @staticmethod
    def is_enabled() -> bool:
        """Check if FastAPI is already enabled."""
        return FastAPI.__is_enabled__

    @classmethod
    def get(cls) -> _FaststAPI:
        """Get or Create new instance of FastAPI."""
        if not isinstance(cls.__app__, _FaststAPI):
            from .routers import healthz_router, sso_router, user_router, webhook_router
            from ..plugin.implementation import (
                WEBSOCKET_MANAGER,
                walker_router,
                webhook_walker_router,
                websocket_router,
            )

            @asynccontextmanager
            async def lifespan(app: _FaststAPI) -> AsyncGenerator[None, _FaststAPI]:
                from .datasources import Collection

                Collection.apply_indexes()

                async with create_task_group() as task_group:
                    await WEBSOCKET_MANAGER.open_broadcaster(task_group)

                    yield

                    await WEBSOCKET_MANAGER.close_broadcaster(task_group)

            cls.__app__ = _FaststAPI(lifespan=lifespan)

            cls.__app__.add_middleware(
                CORSMiddleware,
                allow_origins=getenv("ALLOW_ORIGINS", "*").split(","),
                allow_credentials=True,
                allow_methods=getenv("ALLOW_METHODS", "*").split(","),
                allow_headers=getenv("ALLOW_HEADERS", "*").split(","),
            )

            populate_yaml_specs(cls.__app__)

            for router in [
                healthz_router,
                sso_router,
                user_router,
                webhook_router,
                walker_router,
                webhook_walker_router,
                websocket_router,
            ]:
                cls.__app__.include_router(router)

            @cls.__app__.exception_handler(Exception)
            async def uncatched_exception_handler(
                request: Request, exc: Exception
            ) -> ORJSONResponse:
                """Catched uncatched exceptions."""
                response = {"errors": format_exception(exc)}

                log: dict[str, Any] = {"request_url": str(request.url)}
                log["extra_fields"] = list(log.keys())
                logger.error(
                    f"Call from to {log["request_url"]} returns unexpected errors: {response["errors"]}",
                    extra=log,
                )

                return ORJSONResponse(response, status_code=500)

        return cls.__app__

    @classmethod
    def start(
        cls,
        host: str | None = None,
        port: int | None = None,
        emailer: type[Emailer] | None = None,
        **kwargs: Any,  # noqa ANN401
    ) -> None:
        """Run FastAPI Handler via Uvicorn."""
        if emailer:
            emailer.start()

        _run(
            cls.get(),
            host=host or getenv("HOST") or "0.0.0.0",
            port=port or int(getenv("PORT", "8000")),
            **kwargs,
        )
