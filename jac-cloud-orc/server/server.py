import grpc
from concurrent import futures
import importlib
from grpc_local import module_service_pb2_grpc
from grpc_local import module_service_pb2


class ModuleService(module_service_pb2_grpc.ModuleServiceServicer):
    def __init__(self, module_name):
        self.module = importlib.import_module(module_name)

    def ExecuteMethod(self, request, context):
        try:
            # Get the method from the module
            method = getattr(self.module, request.method_name)

            # Wrap args in a list if the method is 'numpy.array'
            if request.method_name == "array" and hasattr(self.module, "array"):
                args = [request.args]  # numpy expects a list of arguments
            else:
                args = request.args  # Regular case: no need to wrap

            # Call the method with the provided arguments
            result = method(*args)

            # Return the result as a string
            return module_service_pb2.MethodResponse(result=str(result))
        except Exception as e:
            # Handle any errors during method execution
            context.set_details(f"gRPC error: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return module_service_pb2.MethodResponse(result=f"Error: {str(e)}")


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

    # Take module name from command-line argument
    module_name = sys.argv[1]
    serve(module_name)
