"""This module provides a FastAPI-based API for managing Kubernetes pods."""

from contextlib import asynccontextmanager
from os import getenv
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from orjson import dumps, loads

from .routers.deployment import Deployment, deployment, router
from .utils import logger

MODULES = getenv("MODULES", "{}")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, FastAPI]:
    """Process FastAPI life cycle."""
    if MODULES:
        try:
            namespaces: dict[
                str,  # Namespace
                dict[
                    str,  # Module
                    dict[str, dict],  # Service / Python Library - Deployment Config
                ],
            ] = loads(MODULES.encode())
            for namespace, modules in namespaces.items():
                logger.info(f"Extracting modules from `{namespace}` namespace ...")
                for module, deployments in modules.items():
                    logger.info(
                        f"Extracting deployments from `{module}` with `{namespace}` namespace ..."
                    )
                    for service, _deployment in deployments.items():
                        _deployment = {
                            "module": module,
                            "version": _deployment.get("version", "latest"),
                            "config": {
                                **_deployment.get("config", {}),
                                "name": service,
                                "namespace": namespace,
                            },
                        }
                        logger.info(
                            f"Deploying {service} with {dumps(_deployment).decode()} ..."
                        )
                        deployment(Deployment(**_deployment))

        except Exception:
            logger.exception(
                f"MODULES environment variable is not in valid format!\n{MODULES}"
            )
    yield


app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)
app.include_router(router)
