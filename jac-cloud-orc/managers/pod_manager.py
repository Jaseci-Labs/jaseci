from fastapi import FastAPI
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import time

app = FastAPI()


class JacPodManager:
    def __init__(self, module_name: str):
        self.module_name = module_name
        self.pod_name = f"{module_name}-pod"
        self.service_name = f"{module_name}-service"
        self.ingress_name = "smartimport-ingress"
        self.namespace = "default"

    def create_pod(self):
        """Create a Kubernetes pod, service, and ingress to dynamically import and run a module."""
        try:
            # Load Kubernetes config (for in-cluster use)
            config.load_incluster_config()
            v1 = client.CoreV1Api()

            # Check if the pod already exists
            try:
                pod_info = v1.read_namespaced_pod(
                    name=self.pod_name, namespace=self.namespace
                )
                if pod_info.status.phase == "Running":
                    pod_ip = pod_info.status.pod_ip
                    print(f"Pod {self.pod_name} is already running with IP {pod_ip}")
                else:
                    raise Exception(f"Pod {self.pod_name} exists but is not running.")
            except ApiException as e:
                if e.status == 404:
                    # If the pod does not exist, create it
                    pod_manifest = {
                        "apiVersion": "v1",
                        "kind": "Pod",
                        "metadata": {
                            "name": self.pod_name,
                            "labels": {"app": self.pod_name},
                        },
                        "spec": {
                            "containers": [
                                {
                                    "name": "module-container",
                                    "image": "ashishmahendra/jac-cloud-orc:latest",
                                    "env": [
                                        {
                                            "name": "MODULE_NAME",
                                            "value": self.module_name,
                                        }
                                    ],
                                    "ports": [{"containerPort": 50051}],
                                }
                            ],
                            "restartPolicy": "Never",
                        },
                    }

                    # Create the pod in Kubernetes
                    v1.create_namespaced_pod(
                        namespace=self.namespace, body=pod_manifest
                    )
                    print(
                        f"Pod {self.pod_name} created. Waiting for pod to be ready..."
                    )

                    # Wait for the pod to be in 'Running' state and get its IP
                    max_retries = 30  # Timeout after 30 retries (~1 minute)
                    retries = 0
                    while retries < max_retries:
                        pod_info = v1.read_namespaced_pod(
                            name=self.pod_name, namespace=self.namespace
                        )
                        if pod_info.status.phase == "Running":
                            pod_ip = pod_info.status.pod_ip
                            print(f"Pod {self.pod_name} is running with IP {pod_ip}")
                            break
                        time.sleep(2)
                        retries += 1
                    else:
                        raise Exception(
                            f"Timeout: Pod {self.pod_name} failed to reach 'Running' state."
                        )

            # Check if the service already exists
            try:
                service_info = v1.read_namespaced_service(
                    name=self.service_name, namespace=self.namespace
                )
                service_ip = service_info.spec.cluster_ip
                print(
                    f"Service {self.service_name} already exists with IP {service_ip}"
                )
            except ApiException as e:
                if e.status == 404:
                    # If the service does not exist, create it
                    service_manifest = {
                        "apiVersion": "v1",
                        "kind": "Service",
                        "metadata": {"name": self.service_name},
                        "spec": {
                            "selector": {
                                "app": self.pod_name
                            },  # Assumes the pod has this label
                            "ports": [
                                {
                                    "protocol": "TCP",
                                    "port": 50051,  # Service port
                                    "targetPort": 50051,  # Target container port
                                }
                            ],
                            "type": "ClusterIP",  # Use ClusterIP, as Ingress will handle external access
                        },
                    }

                    # Create the service in Kubernetes
                    v1.create_namespaced_service(
                        namespace=self.namespace, body=service_manifest
                    )
                    print(f"Service {self.service_name} created to expose the pod.")
                    service_info = v1.read_namespaced_service(
                        name=self.service_name, namespace=self.namespace
                    )
                    service_ip = service_info.spec.cluster_ip

            networking_v1 = client.NetworkingV1Api()
            try:
                ingress_info = networking_v1.read_namespaced_ingress(
                    name=self.ingress_name, namespace=self.namespace
                )
                print(
                    f"Ingress {self.ingress_name} already exists. Updating with new path..."
                )

                # Check if path already exists, if not, add the path
                existing_paths = ingress_info.spec.rules[0].http.paths
                path_exists = any(
                    path.backend.service.name == self.service_name
                    for path in existing_paths
                )

                if not path_exists:
                    new_path = {
                        "path": f"/api/{self.module_name}-grpc",
                        "pathType": "Prefix",
                        "backend": {
                            "service": {
                                "name": self.service_name,
                                "port": {"number": 50051},
                            }
                        },
                    }
                    ingress_info.spec.rules[0].http.paths.append(new_path)
                    networking_v1.replace_namespaced_ingress(
                        name=self.ingress_name,
                        namespace=self.namespace,
                        body=ingress_info,
                    )
                    print(
                        f"Added path /api/{self.module_name}-grpc to Ingress {self.ingress_name}."
                    )
            except ApiException as e:
                if e.status == 404:
                    # If the ingress does not exist, create it
                    ingress_manifest = {
                        "apiVersion": "networking.k8s.io/v1",
                        "kind": "Ingress",
                        "metadata": {
                            "name": self.ingress_name,
                            "annotations": {
                                "nginx.ingress.kubernetes.io/backend-protocol": "GRPC",  # Enable gRPC in Ingress
                            },
                        },
                        "spec": {
                            "rules": [
                                {
                                    "host": "smartimport.apps.bcstechnology.com.au",
                                    "http": {
                                        "paths": [
                                            {
                                                "path": f"/api/{self.module_name}-grpc",
                                                "pathType": "Prefix",
                                                "backend": {
                                                    "service": {
                                                        "name": self.service_name,
                                                        "port": {"number": 50051},
                                                    }
                                                },
                                            }
                                        ]
                                    },
                                }
                            ],
                        },
                    }

                    # Create the Ingress in Kubernetes
                    networking_v1.create_namespaced_ingress(
                        namespace=self.namespace, body=ingress_manifest
                    )
                    print(
                        f"Ingress {self.ingress_name} created with path /api/{self.module_name}-grpc."
                    )

            # Return pod, service, and ingress details
            return {
                "pod_ip": pod_ip,
                "service_ip": service_ip,
                "ingress_host": f"smartimport.apps.bcstechnology.com.au",
                "ingress_path": f"/api/{self.module_name}-grpc",
            }

        except ApiException as e:
            print(f"Kubernetes API Error: {e.status} {e.reason}")
            print(f"Details: {e.body}")
            raise Exception(f"Failed to create pod, service, and ingress: {e.reason}")

        except Exception as e:
            print(f"General Error: {str(e)}")
            raise Exception(f"Failed to create pod, service, and ingress: {str(e)}")

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


@app.get("/")
def health():
    return "I'm healthy."
