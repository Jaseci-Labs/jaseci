import requests
import grpc
from grpc_local import module_service_pb2_grpc, module_service_pb2


def get_service_info(module_name: str) -> dict:
    """
    This function makes a request to the pod manager to create a pod and get
    the necessary service information, including the Ingress host and path.
    """
    pod_manager_url = f"http://127.0.0.1:8000/create_pod/{module_name}"

    response = requests.post(pod_manager_url)

    if response.status_code == 200:
        pod_info = response.json()
        print(f"Pod and Service Info: {pod_info}")
        return pod_info
    else:
        raise Exception(
            f"Failed to create pod: {response.status_code}, {response.text}"
        )


def run_client(ingress_host: str, ingress_path: str, method_name: str, args: list):
    """
    This function sets up a gRPC client that connects to the service exposed
    through Ingress and executes the specified method.

    Arguments:
        ingress_host: The host of the Ingress controller (e.g., "bcsaiassist.apps.bcstechnology.com.au").
        ingress_path: The path where the service is exposed via Ingress (e.g., "/api/numpy-grpc").
        method_name: The name of the method to execute on the gRPC server.
        args: A list of arguments to pass to the method.
    """
    # gRPC uses the host header for routing; hence we only use the host here
    credentials = grpc.ssl_channel_credentials()

    channel = grpc.insecure_channel(f"{ingress_host}:443")

    # Create the stub for the gRPC service
    stub = module_service_pb2_grpc.ModuleServiceStub(channel)

    # Construct the request with the method name and arguments
    request = module_service_pb2.MethodRequest(
        method_name=method_name,
        args=[str(arg) for arg in args],  # Convert arguments to string as needed
    )

    # Make the request and get the response
    response = stub.ExecuteMethod(request)

    print(f"Result from gRPC server: {response.result}")


if __name__ == "__main__":
    # The name of the module to import and run in the Kubernetes pod
    module_name = "numpy"

    # Get the pod and service information from the pod manager
    pod_info = get_service_info(module_name)

    # Extract the Ingress host and path
    ingress_host = pod_info["ingress_host"]
    ingress_path = pod_info["ingress_path"]

    # The method name and arguments for the gRPC call
    method_name = "array"
    args = [1, 2, 3]

    # Call the gRPC service through the Ingress
    run_client(ingress_host, ingress_path, method_name, args)
