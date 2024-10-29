# server.py

import grpc
from concurrent import futures
import importlib
import threading
import uuid
from grpc_local import module_service_pb2_grpc
from grpc_local import module_service_pb2


class ObjectRegistry:
    """Thread-safe registry for storing objects with unique IDs."""

    def __init__(self):
        self.lock = threading.Lock()
        self.objects = {}

    def add(self, obj):
        obj_id = str(uuid.uuid4())
        with self.lock:
            self.objects[obj_id] = obj
        return obj_id

    def get(self, obj_id):
        with self.lock:
            return self.objects.get(obj_id)

    def remove(self, obj_id):
        with self.lock:
            if obj_id in self.objects:
                del self.objects[obj_id]


object_registry = ObjectRegistry()


class ModuleService(module_service_pb2_grpc.ModuleServiceServicer):
    def __init__(self, module_name):
        self.module = importlib.import_module(module_name)

    def ExecuteMethod(self, request, context):
        try:
            if request.obj_id:
                # Method call on an object instance
                obj = object_registry.get(request.obj_id)
                if obj is None:
                    raise Exception(f"Object with ID {request.obj_id} not found")
            else:
                # Method call on the module
                obj = self.module

            # Get the attribute or method
            attr = getattr(obj, request.method_name)

            # Prepare arguments
            import json

            args = [json.loads(arg) for arg in request.args]
            kwargs = {key: json.loads(value) for key, value in request.kwargs.items()}

            # Execute the method or access the attribute
            if callable(attr):
                result = attr(*args, **kwargs)
            else:
                result = attr

            # If the result is an object, assign an ID
            if isinstance(result, (int, float, str, bool, list, dict, tuple)):
                return module_service_pb2.MethodResponse(
                    result=json.dumps(result), is_callable=callable(result)
                )
            else:
                # Handle object instances
                result_id = object_registry.add(result)
                return module_service_pb2.MethodResponse(
                    obj_id=result_id, is_callable=callable(result)
                )
        except Exception as e:
            context.set_details(f"Error: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return module_service_pb2.MethodResponse()


def serve(module_name):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    module_service_pb2_grpc.add_ModuleServiceServicer_to_server(
        ModuleService(module_name), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python server.py <module_name>")
        sys.exit(1)

    module_name = sys.argv[1]
    serve(module_name)
