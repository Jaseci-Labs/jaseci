# server.py

import grpc
from concurrent import futures
import importlib
import threading
import uuid
from grpc_local import module_service_pb2_grpc
from grpc_local import module_service_pb2
import logging
import traceback

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


class ObjectRegistry:
    """Thread-safe registry for storing objects with unique IDs."""

    def __init__(self):
        self.lock = threading.Lock()
        self.objects = {}
        logging.debug("ObjectRegistry initialized.")

    def add(self, obj):
        obj_id = str(uuid.uuid4())
        with self.lock:
            self.objects[obj_id] = obj
            logging.debug(f"Object added with ID {obj_id}: {obj}")
        return obj_id

    def get(self, obj_id):
        with self.lock:
            obj = self.objects.get(obj_id)
            logging.debug(f"Object retrieved with ID {obj_id}: {obj}")
            return obj

    def remove(self, obj_id):
        with self.lock:
            if obj_id in self.objects:
                del self.objects[obj_id]
                logging.debug(f"Object with ID {obj_id} removed.")


object_registry = ObjectRegistry()


class ModuleService(module_service_pb2_grpc.ModuleServiceServicer):
    def __init__(self, module_name):
        logging.debug(f"Initializing ModuleService with module '{module_name}'")
        try:
            self.module = importlib.import_module(module_name.replace("-", "_"))
            logging.info(f"Module '{module_name}' imported successfully.")
        except Exception as e:
            logging.error(f"Failed to import module '{module_name}': {e}")
            traceback.print_exc()
            raise e

    def ExecuteMethod(self, request, context):
        try:
            logging.debug(f"Received ExecuteMethod request: {request}")
            if request.obj_id:
                # Method call on an object instance
                obj = object_registry.get(request.obj_id)
                if obj is None:
                    error_msg = f"Object with ID {request.obj_id} not found"
                    logging.error(error_msg)
                    raise Exception(error_msg)
            else:
                # Method call on the module
                obj = self.module
                logging.debug(
                    f"Using module '{self.module.__name__}' for method execution."
                )

            # Get the attribute or method
            attr = getattr(obj, request.method_name, None)
            if attr is None:
                error_msg = f"Attribute '{request.method_name}' not found in '{obj}'"
                logging.error(error_msg)
                raise AttributeError(error_msg)

            logging.debug(f"Executing method '{request.method_name}' on '{obj}'")

            # Deserialize arguments
            import json

            def deserialize_arg(arg):
                import numpy as np
                import base64

                if arg["type"] == "primitive":
                    return arg["value"]
                elif arg["type"] == "json":
                    return arg["value"]
                elif arg["type"] == "ndarray":
                    data_bytes = base64.b64decode(arg["data"])
                    array = np.frombuffer(data_bytes, dtype=arg["dtype"])
                    array = array.reshape(arg["shape"])
                    return array
                elif arg["type"] == "ndarray_list":
                    value = arg["value"]
                    return np.array(value, dtype=object)
                elif arg["type"] == "object":
                    obj = object_registry.get(arg["obj_id"])
                    if obj is None:
                        raise Exception(f"Object with ID {arg['obj_id']} not found")
                    return obj
                else:
                    raise Exception(f"Unknown argument type: {arg.get('type')}")

            args = [deserialize_arg(json.loads(arg)) for arg in request.args]
            kwargs = {
                key: deserialize_arg(json.loads(value))
                for key, value in request.kwargs.items()
            }

            logging.debug(
                f"Arguments after deserialization: args={args}, kwargs={kwargs}"
            )

            if callable(attr):
                result = attr(*args, **kwargs)
            else:
                result = attr

            logging.debug(f"Execution result: {result}")

            def serialize_result(res):
                import numpy as np
                import base64

                if isinstance(res, (int, float, str, bool)):
                    logging.debug(f"Serializing primitive: {res}")
                    return {"type": "primitive", "value": res}
                elif isinstance(res, (np.integer, np.floating)):
                    logging.debug(f"Serializing NumPy scalar: {res}")
                    return {"type": "primitive", "value": res.item()}
                elif isinstance(res, (list, dict, tuple)):
                    logging.debug(f"Serializing JSON serializable object: {res}")
                    return {"type": "json", "value": res}
                elif isinstance(res, np.ndarray):
                    logging.debug(
                        f"Serializing ndarray with dtype: {res.dtype}, shape: {res.shape}"
                    )
                    if res.dtype.kind == "O":
                        logging.debug(
                            "Array has dtype 'object'; converting to list with 'ndarray_list' type."
                        )
                        return {"type": "ndarray_list", "value": res.tolist()}
                    else:
                        data_bytes = res.tobytes()
                        data_b64 = base64.b64encode(data_bytes).decode("utf-8")
                        return {
                            "type": "ndarray",
                            "data": data_b64,
                            "dtype": str(res.dtype),
                            "shape": res.shape,
                        }
                else:
                    logging.debug(f"Serializing object instance: {res}")
                    obj_id = object_registry.add(res)
                    return {"type": "object", "obj_id": obj_id}

            serialized_result = serialize_result(result)
            response = module_service_pb2.MethodResponse(
                result=json.dumps(serialized_result), is_callable=callable(result)
            )
            logging.debug(f"Returning serialized result: {response}")
            return response
        except Exception as e:
            error_msg = f"Error during method execution: {str(e)}"
            logging.error(error_msg)
            traceback.print_exc()
            context.set_details(error_msg)
            context.set_code(grpc.StatusCode.INTERNAL)
            return module_service_pb2.MethodResponse()


def serve(module_name):
    logging.info(f"Starting gRPC server for module '{module_name}'")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    module_service_pb2_grpc.add_ModuleServiceServicer_to_server(
        ModuleService(module_name), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    logging.info("gRPC server started and listening on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python server.py <module_name>")
        sys.exit(1)

    module_name = sys.argv[1]
    try:
        serve(module_name)
    except Exception as e:
        logging.error(f"Server failed to start: {e}")
        traceback.print_exc()
        sys.exit(1)
