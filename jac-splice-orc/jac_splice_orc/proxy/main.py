"""Jac Proxy Server."""

import sys
import traceback
from concurrent import futures
from importlib import import_module
from pickle import dumps, loads
from typing import Any

import grpc

from grpc_health.v1 import health, health_pb2, health_pb2_grpc

from .grpc_local import module_service_pb2, module_service_pb2_grpc
from .utils import logger


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

    def execute(self, request: Any, context: Any) -> Any:  # noqa: ANN401
        """Override execute."""
        try:
            module = self.module
            for name in request.method_name.split("."):
                module = getattr(module, name)

            if callable(module):
                result = module(*loads(request.args), **loads(request.kwargs))
            else:
                request = module

            return module_service_pb2.MethodResponse(  # type: ignore[attr-defined]
                result=dumps(result), is_callable=callable(result)
            )
        except Exception as e:
            error_msg = f"Error during method execution: {str(e)}"
            logger.error(error_msg)
            traceback.print_exc()
            context.set_details(error_msg)
            context.set_code(grpc.StatusCode.INTERNAL)
            return module_service_pb2.MethodResponse()  # type: ignore[attr-defined]


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
