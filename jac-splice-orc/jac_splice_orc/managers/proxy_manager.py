"""Module for proxying requests to pod manager and remote objects."""

import base64
import json
from typing import Any, Callable, Dict, List, Optional, Union, cast

import numpy as np

import requests

Primitive = Union[str, int, float, bool]
JSONable = Union[Primitive, List[Any], Dict[str, Any]]


class PodManagerProxy:
    """Proxy for interacting with the pod manager service."""

    def __init__(self, pod_manager_url: str) -> None:
        """Initialize the pod manager proxy.

        Args:
            pod_manager_url: URL of the pod manager service
        """
        self.pod_manager_url = pod_manager_url

    def create_pod(
        self, module_name: str, module_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send a request to the pod manager to create the pod and service.

        Args:
            module_name: Name of the module
            module_config: Configuration for the module

        Returns:
            Response from the pod manager

        Raises:
            Exception: If the pod creation fails
        """
        response = requests.post(
            f"{self.pod_manager_url}/create_pod/{module_name}", json=module_config
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to create pod: {response.text}")

    def delete_pod(self, module_name: str) -> Dict[str, Any]:  # noqa: ANN401
        """Send a request to the pod manager to delete the pod and service.

        Args:
            module_name: Name of the module

        Returns:
            Response from the pod manager

        Raises:
            Exception: If the pod deletion fails
        """
        response = requests.delete(f"{self.pod_manager_url}/delete_pod/{module_name}")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to delete pod: {response.text}")

    def run_module(
        self,
        module_name: str,
        method_name: str,
        obj_id: Optional[str],
        args: List[Any],
        kwargs: Dict[str, Any],  # noqa: ANN401
    ) -> Dict[str, Any]:  # noqa: ANN401
        """Run a method on a module.

        Args:
            module_name: Name of the module
            method_name: Name of the method to run
            obj_id: ID of the object to run the method on
            args: Positional arguments for the method
            kwargs: Keyword arguments for the method

        Returns:
            Response from the module

        Raises:
            Exception: If the module execution fails
        """

        def serialize_arg(
            arg: Any,  # noqa: ANN401
        ) -> Dict[str, Any]:  # noqa: ANN401
            """Serialize an argument for transmission to the pod manager.

            Args:
                arg: Argument to serialize

            Returns:
                Serialized argument

            Raises:
                Exception: If the argument type is not supported
            """
            if isinstance(arg, (int, float, str, bool)):
                return {"type": "primitive", "value": arg}
            elif isinstance(arg, np.generic):
                return {"type": "primitive", "value": arg.item()}
            elif isinstance(arg, tuple):
                return {"type": "json", "value": list(arg)}
            elif isinstance(arg, (list, dict)):
                return {"type": "json", "value": cast(JSONable, arg)}
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
    """Proxy for interacting with modules."""

    def __init__(self, pod_manager_url: str) -> None:
        """Initialize the module proxy.

        Args:
            pod_manager_url: URL of the pod manager service
        """
        self.pod_manager = PodManagerProxy(pod_manager_url)

    def get_module_proxy(
        self, module_name: str, module_config: Dict[str, Any]
    ) -> "RemoteObjectProxy":
        """Create a proxy object for the module running in the pod.

        Args:
            module_name: Name of the module
            module_config: Configuration for the module

        Returns:
            Proxy object for the module
        """
        self.pod_manager.create_pod(module_name, module_config)
        return RemoteObjectProxy(module_name, self.pod_manager)


class RemoteObjectProxy:
    """Proxy for interacting with remote objects."""

    def __init__(
        self,
        module_name: str,
        pod_manager: PodManagerProxy,
        obj_id: Optional[str] = None,
    ) -> None:
        """Initialize the remote object proxy.

        Args:
            module_name: Name of the module
            pod_manager: Pod manager proxy
            obj_id: ID of the object (None for module-level)
        """
        self.module_name = module_name
        self.pod_manager = pod_manager
        self.obj_id = obj_id  # None for module-level

    def __getattr__(self, method_name: str) -> Callable[
        ...,
        Union[Dict[str, Any], List[Any], str, float, int, bool, "RemoteObjectProxy"],
    ]:
        """Get a method from the remote object.

        Args:
            method_name: Name of the method

        Returns:
            Function that calls the remote method
        """

        def method(*args: Any, **kwargs: Any) -> Union[  # noqa: ANN401
            Dict[str, Any],  # noqa: ANN401
            List[Any],  # noqa: ANN401
            str,
            float,
            int,
            bool,
            "RemoteObjectProxy",
        ]:
            """Call the remote method.

            Args:
                *args: Positional arguments for the method
                **kwargs: Keyword arguments for the method

            Returns:
                Result of the method call

            Raises:
                Exception: If the result type is unknown
            """
            result = self.pod_manager.run_module(
                self.module_name,
                method_name,
                obj_id=self.obj_id,
                args=list(args),
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
                if result_data["type"] == "primitive" or result_data["type"] == "json":
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

    def __call__(self, *args: Any, **kwargs: Any) -> Union[  # noqa: ANN401
        Dict[str, Any],  # noqa: ANN401
        List[Any],  # noqa: ANN401
        str,
        float,
        int,
        bool,
        "RemoteObjectProxy",
    ]:
        """Call the remote object as a function.

        Args:
            *args: Positional arguments for the call
            **kwargs: Keyword arguments for the call

        Returns:
            Result of the call
        """
        return self.__getattr__("__call__")(*args, **kwargs)
