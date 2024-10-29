import requests


class PodManagerProxy:
    def __init__(self, pod_manager_url: str):
        print(f"Initializing PodManagerProxy with URL: {pod_manager_url}")
        self.pod_manager_url = pod_manager_url

    def create_pod(self, module_name: str, module_config: dict):
        """Send a request to the pod manager to create the pod and service."""
        import json

        print(
            f"Creating Pod: {module_name} with module_config: {json.dumps(module_config, indent=4)}"
        )
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

    def run_module(
        self, module_name: str, method_name: str, obj_id: str, args: list, kwargs: dict
    ):
        """Send a request to the pod manager to run a module's method."""
        payload = {"args": args, "kwargs": kwargs}
        params = {
            "module_name": module_name,
            "method_name": method_name,
            "obj_id": obj_id,
        }
        response = requests.post(
            f"{self.pod_manager_url}/run_module",
            params=params,
            json=payload,
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to run module: {response.text}")


class ModuleProxy:
    def __init__(self, pod_manager_url: str):
        self.pod_manager = PodManagerProxy(pod_manager_url)

    def get_module_proxy(self, module_name, module_config):
        """Creates a proxy object for the module running in the pod."""
        self.pod_manager.create_pod(module_name, module_config)
        print(f"Created proxy for module: {module_name}")
        return RemoteObjectProxy(module_name, self.pod_manager)


class RemoteObjectProxy:
    def __init__(self, module_name, pod_manager, obj_id=None):
        self.module_name = module_name
        self.pod_manager = pod_manager
        self.obj_id = obj_id  # None for module-level

    def __getattr__(self, method_name):
        def method(*args, **kwargs):
            result = self.pod_manager.run_module(
                self.module_name,
                method_name,
                obj_id=self.obj_id,
                args=args,
                kwargs=kwargs,
            )

            if "obj_id" in result:
                return RemoteObjectProxy(
                    self.module_name, self.pod_manager, obj_id=result["obj_id"]
                )
            else:
                import json

                return json.loads(result["result"])

        return method

    def __call__(self, *args, **kwargs):
        return self.__getattr__("__call__")(*args, **kwargs)
