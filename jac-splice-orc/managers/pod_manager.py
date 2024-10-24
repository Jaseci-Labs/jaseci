"""This module provides a FastAPI-based API for managing Kubernetes pods."""

import os
import subprocess
import time

from typing import Any, List

from fastapi import Body, FastAPI, HTTPException, Query

import grpc

from grpc_local import module_service_pb2, module_service_pb2_grpc

from kubernetes import client, config

from pydantic import BaseModel


app = FastAPI()


class PodManager:
    """Manages Kubernetes pods and services for modules."""

    def __init__(self, namespace: str = "default") -> None:
        """Initialize Kubernetes client."""
        if os.getenv("TEST_ENV") == "true":
            print("Running in test environment, skipping Kubernetes config.")
        else:
            try:
                config.load_incluster_config()
            except config.ConfigException:
                config.load_kube_config()
        self.v1 = client.CoreV1Api()
        self.namespace = namespace

    def get_loadbalancer_url(service_name, namespace):
        try:

            # Fetch the external IP or hostname using kubectl
            result_ip = subprocess.run(
                [
                    "kubectl",
                    "get",
                    "svc",
                    service_name,
                    "-n",
                    namespace,
                    "-o",
                    "jsonpath={.status.loadBalancer.ingress[0].ip}",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            result_hostname = subprocess.run(
                [
                    "kubectl",
                    "get",
                    "svc",
                    service_name,
                    "-n",
                    namespace,
                    "-o",
                    "jsonpath={.status.loadBalancer.ingress[0].hostname}",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            # If the result contains an IP, return it
            if result_ip.stdout:
                return result_ip.stdout.strip()

            # If the result contains a hostname, return it
            if result_hostname.stdout:
                return result_hostname.stdout.strip()

            return "No LoadBalancer URL found (external IP or hostname missing)."

        except subprocess.CalledProcessError as e:
            return f"Error executing kubectl command: {e}"

    def create_namespace(namespace_name):
        try:
            # Run the kubectl command to create a namespace
            result = subprocess.run(
                ["kubectl", "create", "namespace", namespace_name],
                capture_output=True,
                text=True,
                check=True,
            )

            # Return success message if the namespace is created successfully
            return f"Namespace '{namespace_name}' created successfully."

        except subprocess.CalledProcessError as e:
            # If there's an error, return the error message
            return f"Error creating namespace: {e.stderr}"

    def create_requirements_file(self, module_name: str, module_config: dict) -> str:
        """Generate a requirements.txt file based on the module configuration."""
        requirements_path = f"/app/{module_name}/requirements.txt"

        # Ensure the module directory exists
        os.makedirs(os.path.dirname(requirements_path), exist_ok=True)

        with open(requirements_path, "w") as f:
            dependencies = module_config.get("dependency", [])
            for dep in dependencies:
                f.write(f"{dep}\n")

        print(f"Created requirements.txt for {module_name} at {requirements_path}")
        return requirements_path

    def create_pod(self, module_name: str, module_config: dict) -> Any:
        """Create a pod and service for the given module."""
        print("Creating pod %s, with config: %s" % (module_name, module_config))
        image_name = os.getenv(
            "IMAGE_NAME", "ashishmahendra/jac-splice-orc:0.1.0"
        )  # Default image name

        pod_name = f"{module_name}-pod"
        service_name = f"{module_name}-service"
        try:
            pod_info = self.v1.read_namespaced_pod(
                name=pod_name, namespace=self.namespace
            )
            if pod_info.status.phase == "Running":
                return {"message": f"Pod {pod_name} is already running."}
            else:
                raise HTTPException(
                    status_code=409, detail=f"Pod {pod_name} exists but is not running."
                )
        except client.exceptions.ApiException as e:
            requirements_file_path = self.create_requirements_file(
                module_name, module_config
            )
            if e.status == 404:
                # Pod does not exist, so create it
                pod_manifest = {
                    "apiVersion": "v1",
                    "kind": "Pod",
                    "metadata": {
                        "name": pod_name,
                        "labels": {"app": pod_name},
                    },
                    "spec": {
                        "containers": [
                            {
                                "name": "module-container",
                                "image": f"{image_name}",
                                "env": [{"name": "MODULE_NAME", "value": module_name}],
                                "ports": [{"containerPort": 50051}],
                                "resources": {
                                    "requests": {
                                        "cpu": module_config["lib_cpu_req"],
                                        "memory": module_config["lib_mem_size_req"],
                                    },
                                    "limits": {
                                        "cpu": module_config["lib_cpu_req"],
                                        "memory": module_config["lib_mem_size_req"],
                                    },
                                },
                                "volumeMounts": [
                                    {
                                        "name": "requirements-volume",
                                        "mountPath": f"/app/{module_name}",
                                    }
                                ],
                            }
                        ],
                        "volumes": [
                            {
                                "name": "requirements-volume",
                                "configMap": {"name": f"{module_name}-requirements"},
                            }
                        ],
                        "restartPolicy": "Never",
                    },
                }
                import json

                print(json.dumps(pod_manifest, indent=4))
                _ = self.v1.create_namespaced_config_map(
                    self.namespace,
                    body={  # Create a ConfigMap for requirements
                        "metadata": {"name": f"{module_name}-requirements"},
                        "data": {
                            "requirements.txt": open(requirements_file_path, "r").read()
                        },  # Read requirements.txt into ConfigMap
                    },
                )
                self.v1.create_namespaced_pod(self.namespace, body=pod_manifest)
                print(f"Pod {pod_name} created.")
                self.wait_for_pod_ready(pod_name)

        # Create Service
        try:

            _ = self.v1.read_namespaced_service(
                name=service_name, namespace=self.namespace
            )
            print(f"Service {service_name} already exists.")

        except client.exceptions.ApiException as e:
            if e.status == 404:
                service_manifest = {
                    "apiVersion": "v1",
                    "kind": "Service",
                    "metadata": {"name": service_name},
                    "spec": {
                        "selector": {"app": pod_name},
                        "ports": [
                            {"protocol": "TCP", "port": 50051, "targetPort": 50051}
                        ],
                        "type": "ClusterIP",
                    },
                }
                self.v1.create_namespaced_service(self.namespace, body=service_manifest)
                print(f"Service {service_name} created.")

        return {"message": f"Pod {pod_name} and service {service_name} created."}

    def delete_pod(self, module_name: str) -> Any:
        """Delete the pod and service for the given module."""
        pod_name = f"{module_name}-pod"
        service_name = f"{module_name}-service"

        # Delete Pod
        try:
            self.v1.delete_namespaced_pod(name=pod_name, namespace=self.namespace)
            print(f"Pod {pod_name} deleted.")
        except client.exceptions.ApiException:
            raise HTTPException(status_code=404, detail=f"Pod {pod_name} not found.")

        # Delete Service
        try:
            self.v1.delete_namespaced_service(
                name=service_name, namespace=self.namespace
            )
            print(f"Service {service_name} deleted.")
        except client.exceptions.ApiException:
            raise HTTPException(
                status_code=404, detail=f"Service {service_name} not found."
            )

        return {"message": f"Pod {pod_name} and service {service_name} deleted."}

    def wait_for_pod_ready(self, pod_name: str) -> None:
        """Wait until the pod is ready."""
        max_retries = 30
        retries = 0
        while retries < max_retries:
            pod_info = self.v1.read_namespaced_pod(
                name=pod_name, namespace=self.namespace
            )
            if pod_info.status.phase == "Running":
                print(f"Pod {pod_name} is running with IP {pod_info.status.pod_ip}")
                return
            retries += 1
            time.sleep(2)
        raise Exception(f"Timeout: Pod {pod_name} failed to reach 'Running' state.")

    def get_pod_service_ip(self, module_name: str) -> str:
        """Look up the service IP for the pod corresponding to the module."""
        service_name = f"{module_name}-service"
        try:
            service_info = self.v1.read_namespaced_service(
                name=service_name, namespace=self.namespace
            )
            return service_info.spec.cluster_ip
        except client.exceptions.ApiException:
            raise HTTPException(
                status_code=404, detail=f"Service for module {module_name} not found."
            )

    def forward_to_pod(
        self, service_ip: str, method_name: str, obj_id: str, args: list, kwargs: dict
    ) -> Any:
        import json

        serialized_args = [json.dumps(arg) for arg in args]
        serialized_kwargs = {key: json.dumps(value) for key, value in kwargs.items()}
        channel = grpc.insecure_channel(f"{service_ip}:50051")
        stub = module_service_pb2_grpc.ModuleServiceStub(channel)
        request = module_service_pb2.MethodRequest(
            obj_id=obj_id,
            method_name=method_name,
            args=serialized_args,
            kwargs=serialized_kwargs,
        )
        try:
            response = stub.ExecuteMethod(request)
            if response.obj_id:
                return {"obj_id": response.obj_id, "is_callable": response.is_callable}
            else:
                return {"result": response.result}
        except grpc.RpcError as e:
            raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")


pod_manager = PodManager()


class RunModuleRequest(BaseModel):
    """Request for running a module."""

    args: List[Any] = []
    kwargs: dict[str, Any] = {}


@app.post("/run_module")
async def run_module(
    module_name: str = Query(..., description="Name of the module"),
    method_name: str = Query(..., description="Name of the method"),
    obj_id: str = Query(None, description="Object ID"),
    request: RunModuleRequest = Body(
        ..., description="Arguments and keyword arguments"
    ),
):
    service_ip = pod_manager.get_pod_service_ip(module_name)
    result = pod_manager.forward_to_pod(
        service_ip, method_name, obj_id, request.args, request.kwargs
    )
    return result


@app.post("/create_pod/{module_name}")
def create_pod(module_name: str, module_config: dict = Body(...)) -> Any:
    """Create a pod and service for the given module and return the result."""
    return pod_manager.create_pod(module_name, module_config)


@app.delete("/delete_pod/{module_name}")
def delete_pod(module_name: str) -> Any:
    """Delete the pod and service for the given module and return the result."""
    return pod_manager.delete_pod(module_name)


@app.get("/get_loadbalancer_url")
def fetch_loadbalancer_url(service_name: str, namespace: str):
    return {
        "loadbalancer_url": pod_manager.get_loadbalancer_url(service_name, namespace)
    }


@app.post("/create_namespace")
def create_new_namespace(namespace_name: str):
    return {"message": pod_manager.create_namespace(namespace_name)}
