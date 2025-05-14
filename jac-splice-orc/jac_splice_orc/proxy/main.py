"""Jac Proxy Server."""

import sys
from concurrent import futures
from importlib import import_module
from pickle import dumps, loads
from typing import Any
from uuid import uuid4

import grpc

from grpc_health.v1 import health, health_pb2, health_pb2_grpc

from .grpc_local import module_service_pb2, module_service_pb2_grpc
from .utils import logger

memory: dict[str, Any] = {}


def is_primitive(value: Any) -> bool:
    """Check if value is primitive."""
    return isinstance(value, str | int | float | list | dict | bool)


class ModuleService(module_service_pb2_grpc.ModuleServiceServicer):
    """Module Service."""

    def __init__(self, module_name: str) -> None:
        """Override init."""
        logger.debug(f"Initializing ModuleService with module '{module_name}'")
        try:
            self.module = import_module(module_name.replace("-", "_"))
            logger.info(f"Module '{module_name}' imported successfully.")
        except Exception as e:
            logger.error(f"Failed to import module '{module_name}': {e}")
            raise e

    def get_attribute(self, request: Any, context: Any) -> Any:  # noqa: ANN401
        """Override execute."""
        try:
            module = memory[request.id] if request.id else self.module
            value = getattr(module, request.attribute)
            is_property = (
                1
                if isinstance(
                    getattr(module.__class__, request.attribute, None), property
                )
                else 2
            )

            if is_primitive(value):
                return module_service_pb2.ValueResponse(type=-1, bytes_value=dumps(value))  # type: ignore[attr-defined]

            id = uuid4().hex
            memory[id] = value

            return module_service_pb2.ValueResponse(  # type: ignore[attr-defined]
                type=is_property if callable(value) else 0, string_value=id
            )
        except Exception as e:
            logger.exception("Error during method get_attribute")
            context.abort(grpc.StatusCode.INTERNAL, str(e))

    def execute(self, request: Any, context: Any) -> Any:  # noqa: ANN401
        """Override execute."""
        try:
            args = [
                memory[arg.string_value] if arg.proxy else loads(arg.bytes_value)
                for arg in request.args
            ]
            kwargs = {
                key: (
                    memory[value.string_value]
                    if value.proxy
                    else loads(value.bytes_value)
                )
                for key, value in request.kwargs.items()
            }
            func = memory[request.id] if request.id else self.module

            if request.method:
                for m in request.method.split("."):
                    func = getattr(func, m)

            # allow throwing of error
            value = func(*args, **kwargs)  # type: ignore[operator]

            if is_primitive(value):
                return module_service_pb2.ValueResponse(type=-1, bytes_value=dumps(value))  # type: ignore[attr-defined]

            id = uuid4().hex
            memory[id] = value

            return module_service_pb2.ValueResponse(  # type: ignore[attr-defined]
                type=1 if callable(value) else 0, string_value=id
            )
        except Exception as e:
            logger.exception("Error during method execution")
            context.abort(grpc.StatusCode.INTERNAL, str(e))


def run() -> None:
    """Run server."""
    if len(sys.argv) < 2:
        print("Usage: python server.py <module_name>")
        sys.exit(1)

    module_name = sys.argv[-1]

    logger.info(f"Starting gRPC server for module '{module_name}'")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    module_service_pb2_grpc.add_ModuleServiceServicer_to_server(
        ModuleService(module_name), server
    )

    health_servicer = health.HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)

    health_servicer.set(
        service="ModuleService",
        status=health_pb2.HealthCheckResponse.SERVING,
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    logger.info("gRPC server started and listening on port 50051")
    server.wait_for_termination()
