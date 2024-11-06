import requests
import json
import numpy as np
import base64


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

    def run_module(self, module_name, method_name, obj_id, args, kwargs):
        # Serialize arguments
        def serialize_arg(arg):
            if isinstance(arg, (int, float, str, bool)):
                return {"type": "primitive", "value": arg}
            elif isinstance(arg, np.generic):
                return {"type": "primitive", "value": arg.item()}
            elif isinstance(arg, (list, dict, tuple)):
                return {"type": "json", "value": arg}
            elif isinstance(arg, np.ndarray):
                if arg.ndim == 0:
                    # Zero-dimensional array (NumPy scalar)
                    return {"type": "primitive", "value": arg.item()}
                elif arg.dtype.kind == "O":
                    return {"type": "ndarray_list", "value": arg.tolist()}
                else:
                    data_bytes = arg.tobytes()
                    data_b64 = base64.b64encode(data_bytes).decode("utf-8")
                    return {
                        "type": "ndarray",
                        "data": data_b64,
                        "dtype": arg.dtype.str,
                        "shape": arg.shape,
                    }
            elif isinstance(arg, RemoteObjectProxy):
                return {"type": "object", "obj_id": arg.obj_id}
            else:
                raise Exception(f"Unsupported argument type: {type(arg)}")

        serialized_args = [serialize_arg(arg) for arg in args]
        serialized_kwargs = {key: serialize_arg(value) for key, value in kwargs.items()}

        request_data = {
            "args": serialized_args,
            "kwargs": serialized_kwargs,
        }

        response = requests.post(
            f"{self.pod_manager_url}/run_module",
            params={
                "module_name": module_name,
                "method_name": method_name,
                "obj_id": obj_id,
            },
            json=request_data,
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
                result_data = result.get("result")
                if isinstance(result_data, str):
                    result_data = json.loads(result_data)

                # Deserialize the result based on its type
                if result_data["type"] == "primitive":
                    return result_data["value"]
                elif result_data["type"] == "json":
                    return result_data["value"]
                elif result_data["type"] == "ndarray":
                    data_bytes = base64.b64decode(result_data["data"])
                    array = np.frombuffer(data_bytes, dtype=result_data["dtype"])
                    array = array.reshape(result_data["shape"])
                    return array
                elif result_data["type"] == "ndarray_list":
                    value = result_data["value"]
                    return np.array(value, dtype=object)
                elif result_data["type"] == "object":
                    return RemoteObjectProxy(
                        self.module_name, self.pod_manager, obj_id=result_data["obj_id"]
                    )
                else:
                    raise Exception("Unknown result type received from server")

        return method

    def __call__(self, *args, **kwargs):
        return self.__getattr__("__call__")(*args, **kwargs)
