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
            modules: dict[
                str,  # Module
                dict[
                    str,  # Namespace
                    dict[str, dict],  # Service / Python Library - Deployment Config
                ],
            ] = loads(MODULES.encode())
            for module, namespaces in modules.items():
                logger.info(f"Extracting {module} namespaces ...")
                for namespace, names in namespaces.items():
                    logger.info(f"Extracting {namespace} services/libraries ...")
                    for service, config in names.items():
                        config = {
                            **config,
                            "name": service,
                            "namespace": namespace,
                        }

                        logger.info(
                            f"Deploying {service} with {dumps(config).decode()} ..."
                        )
                        deployment(Deployment(module=module, config=config))

        except Exception:
            logger.exception(
                f"MODULES environment variable is not in valid format!\n{MODULES}"
            )
    yield


app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)
app.include_router(router)
