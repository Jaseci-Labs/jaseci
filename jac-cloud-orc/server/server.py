import grpc
from concurrent import futures
import importlib
from grpc_local import module_service_pb2_grpc
from grpc_local import module_service_pb2


class ModuleService(module_service_pb2_grpc.ModuleServiceServicer):
    def __init__(self, module_name):
        self.module = importlib.import_module(module_name)

    def ExecuteMethod(self, request, context):
        method = getattr(self.module, request.method_name)
        result = method(*request.args)
        return module_service_pb2.MethodResponse(result=str(result))


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
    sys.argv[1]
    serve(sys.argv[1])
