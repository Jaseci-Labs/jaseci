import grpc
from grpc import module_service_pb2_grpc


class ModuleProxy:
    @staticmethod
    def get_module_proxy(pod_name, module_name):
        # Establish gRPC connection with the pod
        channel = grpc.insecure_channel(f"{pod_name}:50051")
        stub = module_service_pb2_grpc.ModuleServiceStub(channel)

        class ModuleRemoteProxy:
            def __getattr__(self, name):
                def method(*args, **kwargs):
                    # Send gRPC request to the pod
                    return stub.execute_method(name, *args, **kwargs)

                return method

        return ModuleRemoteProxy()
