from fastapi import FastAPI
from kubernetes import client, config
import time

app = FastAPI()


class JacPodManager:
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.pod_name = f"{module_name}-pod"
        self.namespace = "default"

    def create_pod(self):
        """Create a Kubernetes pod to dynamically import and run a module."""
        # Load Kubernetes config
        config.load_incluster_config()

        v1 = client.CoreV1Api()

        # Define the pod spec
        pod_manifest = {
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {"name": self.pod_name},
            "spec": {
                "containers": [
                    {
                        "name": "module-container",
                        "image": "ashishmahendra/jac-cloud-orc:latest",
                        "env": [{"name": "MODULE_NAME", "value": self.module_name}],
                        "ports": [{"containerPort": 50051}],
                    }
                ],
                "restartPolicy": "Never",
            },
        }

        # Create the pod in Kubernetes
        v1.create_namespaced_pod(namespace=self.namespace, body=pod_manifest)
        print(f"Pod {self.pod_name} created. Waiting for pod to be ready...")

        # Wait for the pod to be in 'Running' state and get its IP
        while True:
            pod_info = v1.read_namespaced_pod(
                name=self.pod_name, namespace=self.namespace
            )
            if pod_info.status.phase == "Running":
                pod_ip = pod_info.status.pod_ip
                print(f"Pod {self.pod_name} is running with IP {pod_ip}")
                return {"message": f"Pod {self.pod_name} created", "pod_ip": pod_ip}
            time.sleep(2)

    def delete_pod(self):
        """Delete the Kubernetes pod."""
        config.load_kube_config()
        v1 = client.CoreV1Api()
        v1.delete_namespaced_pod(name=self.pod_name, namespace=self.namespace)
        return {"message": f"Pod {self.pod_name} deleted."}


@app.post("/create_pod/{module_name}")
def create_pod(module_name: str):
    manager = JacPodManager(module_name=module_name)
    return manager.create_pod()


@app.delete("/delete_pod/{module_name}")
def delete_pod(module_name: str):
    manager = JacPodManager(module_name=module_name)
    return manager.delete_pod()
