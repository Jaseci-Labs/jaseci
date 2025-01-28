"""JAC Splice-Orchestrator Plugin."""

import json
import os
import time
import types
from typing import Optional, Union

from kubernetes import client, config
from jaclang.cli.cmdreg import cmd_registry
from jac_splice_orc.managers.proxy_manager import ModuleProxy
from jac_splice_orc.config.config_loader import ConfigLoader

import pluggy
import logging

logging.basicConfig(level=logging.INFO)

hookimpl = pluggy.HookimplMarker("jac")

# Initialize ConfigLoader
config_loader = ConfigLoader()


def try_incluster_or_local() -> bool:
    """
    Attempt to load in-cluster config if we're in a real K8s Pod
    (service account token present). If that fails, fallback
    to local kubeconfig. Returns True if in-cluster config loaded,
    False if local config loaded.
    """
    # Common check for in-cluster environment:
    # Usually: KUBERNETES_SERVICE_HOST is set, and
    # /var/run/secrets/kubernetes.io/serviceaccount/token exists
    token_file = "/var/run/secrets/kubernetes.io/serviceaccount/token"
    if os.getenv("KUBERNETES_SERVICE_HOST") and os.path.exists(token_file):
        logging.info("Attempting in-cluster config...")
        try:
            config.load_incluster_config()
            logging.info("Successfully loaded in-cluster config.")
            return True
        except config.ConfigException as e:
            logging.warning(f"Failed to load in-cluster config: {e}")
    # Otherwise, fallback to local:
    logging.info("Falling back to local kube config (not in-cluster).")
    try:
        config.load_kube_config()
        logging.info("Local kube config loaded successfully.")
        return False
    except config.ConfigException as e:
        logging.error(f"Failed to load any kube config: {e}")
        # No config at all
        return False


class SpliceOrcPlugin:
    """JAC Splice-Orchestrator Plugin."""

    @staticmethod
    def is_kind_cluster():
        """Detect if the cluster is a kind cluster."""
        try:
            contexts, current_context = config.list_kube_config_contexts()
            current_context_name = current_context["name"]
            if current_context_name.startswith("kind-"):
                logging.info("Detected kind cluster.")
                return True
            else:
                logging.info("Detected non-kind cluster.")
                return False
        except Exception as e:
            logging.error(f"Error detecting cluster type: {e}")
            return False

    @classmethod
    def create_namespace(cls, namespace_name):
        """Create a new namespace if it does not exist."""
        logging.info(f"Creating namespace '{namespace_name}'")

        # Attempt to load either in-cluster or local config
        # so we can call the K8s API
        in_cluster = try_incluster_or_local()

        v1 = client.CoreV1Api()
        # Check if the namespace exists
        namespaces = v1.list_namespace()
        if any(ns.metadata.name == namespace_name for ns in namespaces.items):
            logging.info(f"Namespace '{namespace_name}' already exists.")
        else:
            ns = client.V1Namespace(metadata=client.V1ObjectMeta(name=namespace_name))
            v1.create_namespace(ns)
            logging.info(f"Namespace '{namespace_name}' created.")

    @classmethod
    def create_service_account(cls, namespace):
        in_cluster = try_incluster_or_local()
        v1 = client.CoreV1Api()
        service_account_name = config_loader.get(
            "kubernetes", "service_account_name", default="jac-orc-sa"
        )

        # Check if the ServiceAccount already exists
        try:
            v1.read_namespaced_service_account(
                name=service_account_name, namespace=namespace
            )
            logging.info(
                f"ServiceAccount '{service_account_name}' already exists in namespace '{namespace}'."
            )
        except client.exceptions.ApiException as e:
            if e.status == 404:
                # Create the ServiceAccount
                sa = client.V1ServiceAccount(
                    metadata=client.V1ObjectMeta(name=service_account_name)
                )
                v1.create_namespaced_service_account(namespace=namespace, body=sa)
                logging.info(
                    f"ServiceAccount '{service_account_name}' created in namespace '{namespace}'."
                )
            else:
                logging.error(f"Error creating ServiceAccount: {e}")
                raise

        # Create the Role and RoleBinding
        cls.create_role_and_binding(namespace, service_account_name)

    @classmethod
    def create_role_and_binding(cls, namespace, service_account_name):
        in_cluster = try_incluster_or_local()
        rbac_api = client.RbacAuthorizationV1Api()

        role_name = "smartimport-role"
        role_binding_name = "smartimport-rolebinding"

        # Define the Role with updated permissions
        role = client.V1Role(
            metadata=client.V1ObjectMeta(name=role_name, namespace=namespace),
            rules=[
                # Permissions for pods and services
                client.V1PolicyRule(
                    api_groups=[""],
                    resources=["pods", "services", "configmaps", "roles"],
                    verbs=["get", "watch", "list", "create", "update", "delete"],
                ),
                # Permissions for deployments
                client.V1PolicyRule(
                    api_groups=["apps"],
                    resources=["deployments"],
                    verbs=["get", "watch", "list", "create", "update", "delete"],
                ),
            ],
        )
        try:
            rbac_api.read_namespaced_role(name=role_name, namespace=namespace)
            logging.info(
                f"Role '{role_name}' already exists in namespace '{namespace}'."
            )
        except client.exceptions.ApiException as e:
            if e.status == 404:
                # Create the Role
                rbac_api.create_namespaced_role(namespace=namespace, body=role)
                logging.info(f"Role '{role_name}' created in namespace '{namespace}'.")
            else:
                logging.error(f"Error creating Role: {e}")
                raise

        # Define the RoleBinding
        role_binding = client.V1RoleBinding(
            metadata=client.V1ObjectMeta(name=role_binding_name, namespace=namespace),
            subjects=[
                client.RbacV1Subject(
                    kind="ServiceAccount",
                    name=service_account_name,
                    namespace=namespace,
                )
            ],
            role_ref=client.V1RoleRef(
                kind="Role",
                name=role_name,
                api_group="rbac.authorization.k8s.io",
            ),
        )

        # Check if the RoleBinding exists
        try:
            rbac_api.read_namespaced_role_binding(
                name=role_binding_name, namespace=namespace
            )
            logging.info(
                f"RoleBinding '{role_binding_name}' already exists in namespace '{namespace}'."
            )
        except client.exceptions.ApiException as e:
            if e.status == 404:
                # Create the RoleBinding
                rbac_api.create_namespaced_role_binding(
                    namespace=namespace, body=role_binding
                )
                logging.info(
                    f"RoleBinding '{role_binding_name}' created in namespace '{namespace}'."
                )
            else:
                logging.error(f"Error creating RoleBinding: {e}")
                raise

    @classmethod
    def apply_pod_manager_yaml(cls, namespace):
        """Generate and apply the Pod Manager Deployment and Service."""
        in_cluster = try_incluster_or_local()

        # Read configuration
        kubernetes_config = config_loader.get("kubernetes")
        pod_manager_config = kubernetes_config["pod_manager"]
        service_account_name = kubernetes_config.get(
            "service_account_name", "jac-orc-sa"
        )
        deployment_name = pod_manager_config.get(
            "deployment_name", "pod-manager-deployment"
        )
        container_name = pod_manager_config.get("container_name", "pod-manager")
        image_name = pod_manager_config.get("image_name")
        container_port = pod_manager_config.get("container_port", 8000)
        env_vars = pod_manager_config.get("env_vars", {})
        resources = pod_manager_config.get("resources", {})
        service_name = pod_manager_config.get("service_name", "pod-manager-service")
        service_type = pod_manager_config.get("service_type", "LoadBalancer")
        if service_type == "NodePort":
            node_port = 30080
        else:
            node_port = None

        # Create the Deployment object
        apps_v1 = client.AppsV1Api()

        # Define container environment variables
        env_list = [
            client.V1EnvVar(name=key, value=str(value))
            for key, value in env_vars.items()
        ]

        # Define container resources
        resource_requirements = client.V1ResourceRequirements(
            limits=resources.get("limits"), requests=resources.get("requests")
        )

        # Define the container
        container = client.V1Container(
            name=container_name,
            image=image_name,
            ports=[client.V1ContainerPort(container_port=container_port)],
            env=env_list,
            resources=resource_requirements,
        )

        # Define the Pod template spec
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": container_name}),
            spec=client.V1PodSpec(
                containers=[container], service_account_name=service_account_name
            ),
        )

        # Define the Deployment spec
        spec = client.V1DeploymentSpec(
            replicas=1,
            selector=client.V1LabelSelector(match_labels={"app": container_name}),
            template=template,
        )

        # Define the Deployment
        deployment = client.V1Deployment(
            api_version="apps/v1",
            kind="Deployment",
            metadata=client.V1ObjectMeta(name=deployment_name, namespace=namespace),
            spec=spec,
        )

        # Create or update the Deployment
        try:
            apps_v1.read_namespaced_deployment(
                name=deployment_name, namespace=namespace
            )
            # Update the deployment if it exists
            apps_v1.patch_namespaced_deployment(
                name=deployment_name, namespace=namespace, body=deployment
            )
            logging.info(
                f"Updated Deployment '{deployment_name}' in namespace '{namespace}'"
            )
        except client.exceptions.ApiException as e:
            if e.status == 404:
                # Create the Deployment
                apps_v1.create_namespaced_deployment(
                    namespace=namespace, body=deployment
                )
                logging.info(
                    f"Created Deployment '{deployment_name}' in namespace '{namespace}'"
                )
            else:
                logging.error(f"Error creating/updating Deployment: {e}")
                raise

        # Define the service ports
        service_ports = [
            client.V1ServicePort(
                protocol="TCP",
                port=container_port,
                target_port=container_port,
            )
        ]

        if node_port:
            service_ports[0].node_port = node_port

        # Create the Service object
        v1 = client.CoreV1Api()

        service = client.V1Service(
            api_version="v1",
            kind="Service",
            metadata=client.V1ObjectMeta(name=service_name, namespace=namespace),
            spec=client.V1ServiceSpec(
                selector={"app": container_name},
                ports=service_ports,
                type=service_type,
            ),
        )

        # Create or update the Service
        try:
            v1.read_namespaced_service(name=service_name, namespace=namespace)
            # Update the service if it exists
            v1.patch_namespaced_service(
                name=service_name, namespace=namespace, body=service
            )
            logging.info(f"Updated Service '{service_name}' in namespace '{namespace}'")
        except client.exceptions.ApiException as e:
            if e.status == 404:
                # Create the Service
                v1.create_namespaced_service(namespace=namespace, body=service)
                logging.info(
                    f"Created Service '{service_name}' in namespace '{namespace}'"
                )
            else:
                logging.error(f"Error creating/updating Service: {e}")
                raise

    @classmethod
    def configure_pod_manager_url(cls, namespace):
        """
        Dynamically set the POD_MANAGER_URL:
          - If in-cluster: use 'pod-manager-service.{namespace}.svc.cluster.local:8000'
          - If local dev: use 'localhost:30080'
          - If 'LoadBalancer', call get_load_balancer_url() (optional).
        """
        in_cluster = try_incluster_or_local()

        service_name = config_loader.get(
            "kubernetes", "pod_manager", "service_name", default="pod-manager-service"
        )
        container_port = config_loader.get(
            "kubernetes", "pod_manager", "container_port", default=8000
        )
        service_type = config_loader.get(
            "kubernetes", "pod_manager", "service_type", default="NodePort"
        )

        if in_cluster:
            # In-cluster => use service DNS
            # If your Pod Manager is in the same namespace, short DNS name "pod-manager-service"
            # or full DNS "pod-manager-service.{namespace}.svc.cluster.local"
            pod_manager_url_local = (
                f"http://{service_name}.{namespace}.svc.cluster.local:{container_port}"
            )
            logging.info(f"In-cluster mode. Pod manager URL => {pod_manager_url_local}")
        else:
            # Local dev => typically NodePort
            if service_type == "NodePort":
                node_port = 30080
                pod_manager_url_local = f"http://localhost:{node_port}"
                logging.info(
                    f"Local dev mode. Pod manager URL => {pod_manager_url_local}"
                )
            else:
                # If user sets 'LoadBalancer', we can try get_load_balancer_url()
                logging.info(
                    "Service type=LoadBalancer, but we are not in-cluster. Might fail."
                )
                pod_manager_url_local = cls.get_load_balancer_url(namespace)
                if not pod_manager_url_local:
                    logging.error(
                        "Failed to retrieve LB URL, defaulting to localhost:30080"
                    )
                    pod_manager_url_local = "http://localhost:30080"

        # Update the config
        config_loader.set(["environment", "POD_MANAGER_URL"], pod_manager_url_local)
        config_loader.save_config()

        logging.info(f"Pod manager URL updated: {pod_manager_url_local}")

    @classmethod
    def get_load_balancer_url(cls, namespace, timeout=300, interval=5):
        """Retrieve the LoadBalancer service URL."""
        in_cluster = try_incluster_or_local()
        v1 = client.CoreV1Api()
        service_name = config_loader.get(
            "kubernetes", "pod_manager", "service_name", default="pod-manager-service"
        )
        start_time = time.time()
        while True:
            try:
                service = v1.read_namespaced_service(
                    name=service_name, namespace=namespace
                )
                ingress = service.status.load_balancer.ingress
                if ingress:
                    ip = ingress[0].ip
                    hostname = ingress[0].hostname
                    port = service.spec.ports[0].port
                    logging.info(f"LB ingress => ip: {ip}, host: {hostname}")
                    if ip:
                        return f"http://{ip}:{port}"
                    elif hostname:
                        return f"http://{hostname}:{port}"
                else:
                    logging.info(
                        "Waiting for external IP to be assigned (LoadBalancer)."
                    )
            except client.exceptions.ApiException as e:
                logging.error(f"Error retrieving LB URL: {e}")
                return None
            if (time.time() - start_time) > timeout:
                logging.error(
                    f"Timed out after {timeout} seconds waiting for external IP."
                )
                return None
            time.sleep(interval)

    @staticmethod
    @hookimpl
    def create_cmd() -> None:
        """Creating Jac CLI commands."""

        @cmd_registry.register
        def orc_initialize(namespace: str) -> None:
            """Initialize the Pod Manager and Kubernetes system.

            :param namespace: Kubernetes namespace to use.
            """
            # Use the provided namespace if given, else read from config
            if not namespace:
                namespace = config_loader.get(
                    "kubernetes", "namespace", default="jac-splice-orc"
                )
            else:
                # Update the namespace in the config
                config_loader.set(
                    ["kubernetes", "pod_manager", "env_vars", "NAMESPACE"], namespace
                )
                config_loader.set(["kubernetes", "namespace"], namespace)
                config_loader.save_config()

            logging.info(f"Initializing Pod Manager in namespace '{namespace}'")

            # Call the class methods to perform initialization
            SpliceOrcPlugin.create_namespace(namespace)
            SpliceOrcPlugin.create_service_account(namespace)
            SpliceOrcPlugin.apply_pod_manager_yaml(namespace)
            SpliceOrcPlugin.configure_pod_manager_url(namespace)

            logging.info("Initialization complete.")

    @staticmethod
    @hookimpl
    def jac_import(
        target: str,
        base_path: str,
        absorb: bool,
        cachable: bool,
        mdl_alias: Optional[str],
        override_name: Optional[str],
        lng: Optional[str],
        items: Optional[dict[str, Union[str, Optional[str]]]],
        reload_module: Optional[bool],
    ) -> tuple[types.ModuleType, ...]:
        """Core Import Process with Kubernetes Pod Integration."""
        from jaclang.runtimelib.importer import (
            ImportPathSpec,
            JacImporter,
            PythonImporter,
        )
        from jaclang.runtimelib.machine import JacMachine, JacProgram

        module_config_path = os.getenv("MODULE_CONFIG_PATH", "/cfg/module_config.json")
        try:
            logging.info(f"Loading from {module_config_path} for module_config...")
            with open(module_config_path, "r") as f:
                module_config = json.load(f)
        except Exception as e:
            logging.warning(
                f"No module_config found in config_map ({module_config_path}). "
                f"Defaulting to fallback file. Error: {e}"
            )
            module_config = config_loader.get("module_config", default={})
        if target in module_config and module_config[target]["load_type"] == "remote":
            pod_manager_url = config_loader.get("environment", "POD_MANAGER_URL")
            if not pod_manager_url:
                logging.error(
                    "POD_MANAGER_URL is not set. Please run 'jac orc_initialize'."
                )
                raise Exception("POD_MANAGER_URL is not set.")
            proxy = ModuleProxy(pod_manager_url)
            remote_module_proxy = proxy.get_module_proxy(
                module_name=target, module_config=module_config[target]
            )
            if items:
                imported_items = []
                for item_name, item_alias in items.items():
                    item = getattr(remote_module_proxy, item_name)
                    if item_alias:
                        item.__name__ = item_alias
                    imported_items.append(item)
                return tuple(imported_items)
            else:
                return (remote_module_proxy,)
        spec = ImportPathSpec(
            target,
            base_path,
            absorb,
            cachable,
            mdl_alias,
            override_name,
            lng,
            items,
        )

        jac_machine = JacMachine.get(base_path)
        if not jac_machine.jac_program:
            jac_machine.attach_program(
                JacProgram(mod_bundle=None, bytecode=None, sem_ir=None)
            )

        if lng == "py":
            import_result = PythonImporter(JacMachine.get()).run_import(spec)
        else:
            import_result = JacImporter(JacMachine.get()).run_import(
                spec, reload_module
            )

        return (
            (import_result.ret_mod,)
            if absorb or not items
            else tuple(import_result.ret_items)
        )
