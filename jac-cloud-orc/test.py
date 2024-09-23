import requests
import grpc
from grpc_local import module_service_pb2_grpc, module_service_pb2


def get_pod_ip(module_name: str) -> str:
    pod_manager_url = f"http://127.0.0.1:8000/create_pod/{module_name}"

    response = requests.post(pod_manager_url)

    if response.status_code == 200:
        pod_info = response.json()
        return pod_info["pod_ip"]
    else:
        raise Exception(
            f"Failed to create pod: {response.status_code}, {response.text}"
        )


def run_client(pod_ip: str, method_name: str, args: list):
    channel = grpc.insecure_channel(f"{pod_ip}:50051")

    stub = module_service_pb2_grpc.ModuleServiceStub(channel)

    request = module_service_pb2.MethodRequest(
        method_name=method_name,
        args=[str(arg) for arg in args],
    )

    response = stub.ExecuteMethod(request)
    print(f"Result from gRPC server: {response.result}")


if __name__ == "__main__":

    module_name = "numpy"
    pod_ip = get_pod_ip(module_name)

    method_name = "array"
    args = [1, 2, 3]
    run_client(pod_ip, method_name, args)
