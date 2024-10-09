import requests


class PodManagerProxy:
    def __init__(self, pod_manager_url: str):
        self.pod_manager_url = pod_manager_url

    def create_pod(self, module_name: str, module_config: dict):
        """Send a request to the pod manager to create the pod and service."""
        response = requests.post(
            f"{self.pod_manager_url}/create_pod/{module_name}", json=module_config
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to create pod: {response.text}")

    def delete_pod(self, module_name: str):
        """Send a request to the pod manager to delete the pod and service."""
        response = requests.delete(f"{self.pod_manager_url}/delete_pod/{module_name}")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to delete pod: {response.text}")

    def run_module(self, module_name: str, method_name: str, args: list):
        """Send a request to the pod manager to run a module's method."""
        response = requests.post(
            f"{self.pod_manager_url}/run_module",
            params={"module_name": module_name, "method_name": method_name},
            json={"args": args},
        )
        if response.status_code == 200:
            return response.json().get("result")
        else:
            raise Exception(f"Failed to run module: {response.text}")


class ModuleProxy:
    def __init__(self, pod_manager_url: str):
        self.pod_manager = PodManagerProxy(pod_manager_url)

    def get_module_proxy(self, module_name, module_config):
        """Creates a proxy object for the module running in the pod."""
        self.pod_manager.create_pod(module_name, module_config)

        class ModuleRemoteProxy:
            def __init__(self, module_name, pod_manager):
                self.module_name = module_name
                self.pod_manager = pod_manager

            def __getattr__(self, method_name):
                def method(*args, **kwargs):
                    return self.pod_manager.run_module(
                        self.module_name, method_name, list(args)
                    )

                return method

        return ModuleRemoteProxy(module_name, self.pod_manager)


module_config = {
    "lib_mem_size_req": "150MB",
    "lib_cpu_req": "600m",
    "dependency": ["numpy", "mkl"],
    "load_type": "remote",
}

# Example usage
if __name__ == "__main__":
    pod_manager_url = (
        "http://smartimport.apps.bcstechnology.com.au"  # Pod Manager service URL
    )
    proxy = ModuleProxy(pod_manager_url)
    numpy_proxy = proxy.get_module_proxy("numpy", module_config)

    # Call methods of the numpy module remotely
    result = numpy_proxy.array(1, 2, 3)
    print(f"Result: {result}")
