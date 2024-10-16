"""This module provides a FastAPI-based API for managing Kubernetes pods."""

import os
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

    def __init__(self) -> None:
        """Initialize Kubernetes client."""
        try:
            config.load_incluster_config()
        except config.ConfigException:
            config.load_kube_config()
        self.v1 = client.CoreV1Api()

    def create_pod(self, module_name: str, module_config: dict) -> Any:
        """Create a pod and service for the given module."""
        print("Creating pod %s, with config: %s" % (module_name, module_config))
        image_name = os.getenv(
            "IMAGE_NAME", "ashishmahendra/jac-splice-orc:0.4.0"
        )  # Default image name

        pod_name = f"{module_name}-pod"
        service_name = f"{module_name}-service"
        try:
            pod_info = self.v1.read_namespaced_pod(name=pod_name, namespace="default")
            if pod_info.status.phase == "Running":
                return {"message": f"Pod {pod_name} is already running."}
            else:
                raise HTTPException(
                    status_code=409, detail=f"Pod {pod_name} exists but is not running."
                )
        except client.exceptions.ApiException as e:
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
                            }
                        ],
                        "restartPolicy": "Never",
                    },
                }
                self.v1.create_namespaced_pod(namespace="default", body=pod_manifest)
                print(f"Pod {pod_name} created.")
                self.wait_for_pod_ready(pod_name)

        # Create Service
        try:
            _ = self.v1.read_namespaced_service(name=service_name, namespace="default")
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
                self.v1.create_namespaced_service(
                    namespace="default", body=service_manifest
                )
                print(f"Service {service_name} created.")

        return {"message": f"Pod {pod_name} and service {service_name} created."}

    def delete_pod(self, module_name: str) -> Any:
        """Delete the pod and service for the given module."""
        pod_name = f"{module_name}-pod"
        service_name = f"{module_name}-service"

        # Delete Pod
        try:
            self.v1.delete_namespaced_pod(name=pod_name, namespace="default")
            print(f"Pod {pod_name} deleted.")
        except client.exceptions.ApiException:
            raise HTTPException(status_code=404, detail=f"Pod {pod_name} not found.")

        # Delete Service
        try:
            self.v1.delete_namespaced_service(name=service_name, namespace="default")
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
            pod_info = self.v1.read_namespaced_pod(name=pod_name, namespace="default")
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
                name=service_name, namespace="default"
            )
            return service_info.spec.cluster_ip
        except client.exceptions.ApiException:
            raise HTTPException(
                status_code=404, detail=f"Service for module {module_name} not found."
            )

    def forward_to_pod(self, service_ip: str, method_name: str, args: list) -> Any:
        """Forward the gRPC request to the pod service and return the result."""
        channel = grpc.insecure_channel(f"{service_ip}:50051")
        stub = module_service_pb2_grpc.ModuleServiceStub(channel)
        request = module_service_pb2.MethodRequest(
            method_name=method_name,
            args=[str(arg) for arg in args],
        )
        try:
            response = stub.ExecuteMethod(request)
            return response.result
        except grpc.RpcError as e:
            raise HTTPException(status_code=500, detail=f"gRPC error: {e.details()}")


pod_manager = PodManager()


class RunModuleRequest(BaseModel):
    """Request for running a module."""

    args: List[Any]


@app.post("/run_module")
async def run_module(
    module_name: str = Query(..., description="Name of the module"),
    method_name: str = Query(..., description="Name of the method"),
    request: RunModuleRequest = Body(..., description="Arguments for the method"),
) -> Any:
    """Run a module and return the result."""
    service_ip = pod_manager.get_pod_service_ip(module_name)

    # Forward the request to the corresponding pod via gRPC
    result = pod_manager.forward_to_pod(service_ip, method_name, request.args)

    return {"result": result}


@app.post("/create_pod/{module_name}")
def create_pod(module_name: str, module_config: dict = Body(...)) -> Any:
    """Create a pod and service for the given module and return the result."""
    return pod_manager.create_pod(module_name, module_config)


@app.delete("/delete_pod/{module_name}")
def delete_pod(module_name: str) -> Any:
    """Delete the pod and service for the given module and return the result."""
    return pod_manager.delete_pod(module_name)
