import requests


def get_service_info(module_name: str) -> dict:
    """
    This function makes a request to the pod manager to create a pod and get
    the necessary service information, including the Ingress host and path.
    """
    pod_manager_url = (
        f"http://smartimport.apps.bcstechnology.com.au/create_pod/{module_name}"
    )

    response = requests.post(pod_manager_url)

    if response.status_code == 200:
        pod_info = response.json()
        print(f"Pod and Service Info: {pod_info}")
        return pod_info
    else:
        raise Exception(
            f"Failed to create pod: {response.status_code}, {response.text}"
        )


def run_module_via_pod_manager(module_name: str, method_name: str, args: list):
    """
    This function sends a request to the pod manager to run a module's method
    with the given arguments.
    """
    pod_manager_url = f"http://smartimport.apps.bcstechnology.com.au/run_module"

    # Pass module_name and method_name as query parameters, and args as the body
    params = {"module_name": module_name, "method_name": method_name}

    # Ensure args is included in the JSON payload
    data = {"args": args}

    response = requests.post(pod_manager_url, params=params, json=data)

    if response.status_code == 200:
        result = response.json().get("result")
        print(f"Result from module {module_name}: {result}")
    else:
        print(f"Error: {response.status_code}, {response.text}")


if __name__ == "__main__":
    module_name = "numpy"

    # # Get the pod and service information from the pod manager
    # pod_info = get_service_info(module_name)

    # # The method name and arguments for the gRPC call
    # method_name = "array"
    # args = [1, 2, 3]

    # # Send the request to the Pod Manager
    # run_module_via_pod_manager(module_name, method_name, args)
    from jaclang.settings import settings

    print(settings.modules_to_remote)
