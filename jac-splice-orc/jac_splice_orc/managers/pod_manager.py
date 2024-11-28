"""This module provides a FastAPI-based API for managing Kubernetes pods."""

import logging
import os
import time

from typing import Any, List

from fastapi import Body, FastAPI, HTTPException, Query

import grpc

from grpc_local import module_service_pb2, module_service_pb2_grpc

from kubernetes import client, config

from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI()


class PodManager:
    """Manages Kubernetes pods and services for modules."""

    def __init__(self, namespace: str = "default") -> None:
        """Initialize Kubernetes client."""
        if os.getenv("TEST_ENV") == "true":
            logging.info("Running in test environment, skipping Kubernetes config.")
        else:
            try:
                config.load_incluster_config()
            except config.ConfigException:
                config.load_kube_config()
        self.v1 = client.CoreV1Api()
        self.namespace = os.getenv("NAMESPACE", namespace)

    def create_requirements_file(self, module_name: str, module_config: dict) -> str:
        """Generate a requirements.txt file based on the module configuration."""
        requirements_path = f"/app/requirements/{module_name}/requirements.txt"

        # Ensure the module directory exists
        os.makedirs(os.path.dirname(requirements_path), exist_ok=True)

        with open(requirements_path, "w") as f:
            dependencies = module_config.get("dependency", [])
            for dep in dependencies:
                f.write(f"{dep}\n")

        logging.info(
            f"Created requirements.txt for {module_name} at {requirements_path}"
        )
        return requirements_path

    def create_pod(self, module_name: str, module_config: dict) -> Any:
        """Create a pod and service for the given module."""
        image_name = os.getenv("IMAGE_NAME", "ashishmahendra/jac-splice-orc:0.1.8")

        pod_name = f"{module_name}-pod"
        service_name = f"{module_name}-service"
        logging.info(
            f"Creating pod {pod_name}...\n Image: {image_name}\n Service: {service_name}\n Namespace: {self.namespace}"
        )
        try:
            pod_info = self.v1.read_namespaced_pod(
                name=pod_name, namespace=self.namespace
            )
            if pod_info.status.phase == "Running":
                return {"message": f"Pod {pod_name} is already running."}
            else:
                raise HTTPException(
                    status_code=409,
                    detail=f"Pod {pod_name} exists but is not running.",
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
                                "image": image_name,
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
                                        "mountPath": f"/app/requirements/{module_name}",
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

                try:
                    existing_configmap = self.v1.read_namespaced_config_map(
                        name=f"{module_name}-requirements",
                        namespace=self.namespace
                    )
                    print(f"ConfigMap '{module_name}-requirements' already exists.")
                except client.exceptions.ApiException as e:
                    if e.status == 404: 
                        # Create the ConfigMap
                        print(f"ConfigMap '{module_name}-requirements' not found. Creating it...")
                        _ = self.v1.create_namespaced_config_map(
                            self.namespace,
                            body={
                                "metadata": {"name": f"{module_name}-requirements"},
                                "data": {
                                    "requirements.txt": open(requirements_file_path, "r").read()
                                },
                            },
                        )
                    else:
                        raise
                self.v1.create_namespaced_pod(self.namespace, body=pod_manifest)
                logging.info(f"Pod {pod_name} created.")
                self.wait_for_pod_ready(pod_name)

        # Create Service
        try:
            _ = self.v1.read_namespaced_service(
                name=service_name, namespace=self.namespace
            )
            logging.info(f"Service {service_name} already exists.")
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
                logging.info(f"Service {service_name} created.")

        return {"message": f"Pod {pod_name} and service {service_name} created."}

    def delete_pod(self, module_name: str) -> Any:
        """Delete the pod and service for the given module."""
        pod_name = f"{module_name}-pod"
        service_name = f"{module_name}-service"

        # Delete Pod
        try:
            self.v1.delete_namespaced_pod(name=pod_name, namespace=self.namespace)
            logging.info(f"Pod {pod_name} deleted.")
        except client.exceptions.ApiException:
            raise HTTPException(status_code=404, detail=f"Pod {pod_name} not found.")

        # Delete Service
        try:
            self.v1.delete_namespaced_service(
                name=service_name, namespace=self.namespace
            )
            logging.info(f"Service {service_name} deleted.")
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
                logging.info(
                    f"Pod {pod_name} is running with IP {pod_info.status.pod_ip}"
                )
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
        self,
        module_name: str,
        method_name: str,
        obj_id: str,
        args: list,
        kwargs: dict,
    ) -> Any:
        import json

        pod_name = f"{module_name}-pod"
        service_ip = self.get_pod_service_ip(module_name)

        self.wait_for_pod_ready(pod_name)

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
        max_retries = 5
        for _ in range(max_retries):
            try:
                response = stub.ExecuteMethod(request)
                if response.obj_id:
                    return {
                        "obj_id": response.obj_id,
                        "is_callable": response.is_callable,
                    }
                else:
                    return {"result": response.result}
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.UNAVAILABLE:
                    time.sleep(2)
                    continue
                else:
                    logging.error(f"gRPC error: {e.details()}")
                    raise HTTPException(
                        status_code=500, detail=f"gRPC error: {e.details()}"
                    )
        logging.error("gRPC server unavailable after retries")
        raise HTTPException(
            status_code=500, detail="gRPC server unavailable after retries"
        )


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
    """Run a module and return the result."""
    return pod_manager.forward_to_pod(
        module_name.replace("_", "-"), method_name, obj_id, request.args, request.kwargs
    )


@app.post("/create_pod/{module_name}")
def create_pod(module_name: str, module_config: dict = Body(...)) -> Any:
    """Create a pod and service for the given module and return the result."""
    return pod_manager.create_pod(module_name.replace("_", "-"), module_config)


@app.delete("/delete_pod/{module_name}")
def delete_pod(module_name: str) -> Any:
    """Delete the pod and service for the given module and return the result."""
    return pod_manager.delete_pod(module_name.replace("_", "-"))
