import grpc
from grpc_local import module_service_pb2_grpc, module_service_pb2


def run_client(module_name: str, method_name: str, args: list):
    # Replace <pod-ip> with the actual IP or service name of the Kubernetes pod running the gRPC server
    channel = grpc.insecure_channel("<pod-ip>:50051")

    # Create a stub (client)
    stub = module_service_pb2_grpc.ModuleServiceStub(channel)

    # Create the request
    request = module_service_pb2.MethodRequest(
        method_name=method_name,
        args=[str(arg) for arg in args],  # Convert arguments to strings
    )

    # Call the remote method
    response = stub.ExecuteMethod(request)
    print(f"Result from gRPC server: {response.result}")


if __name__ == "__main__":
    module_name = "numpy"  # Example module
    method_name = "array"  # Example method from numpy
    args = [1, 2, 3]  # Example arguments for numpy.array

    run_client(module_name, method_name, args)
