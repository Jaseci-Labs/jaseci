"""JAC Splice-Orchestrator Plugin."""

import os
import time
import types
from typing import Optional, Union

from kubernetes import client, config, utils

from jac_splice_orc.managers.proxy_manager import ModuleProxy

import pluggy


hookimpl = pluggy.HookimplMarker("jac")


# def create_namespace(namespace_name):
#     try:
#         # Load Kubernetes configuration
#         config.load_kube_config()
#         v1 = client.CoreV1Api()

#         # Check if the namespace already exists
#         namespaces = v1.list_namespace()
#         existing_namespaces = [ns.metadata.name for ns in namespaces.items]
#         if namespace_name in existing_namespaces:
#             print(f"Namespace '{namespace_name}' already exists.")
#         else:
#             # Create the namespace
#             namespace_body = client.V1Namespace(
#                 metadata=client.V1ObjectMeta(name=namespace_name)
#             )
#             v1.create_namespace(namespace_body)
#             print(f"Namespace '{namespace_name}' created successfully.")
#     except client.exceptions.ApiException as e:
#         print(f"Error creating namespace: {e}")


# def get_loadbalancer_url(service_name, namespace):
#     try:
#         config.load_kube_config()
#         v1 = client.CoreV1Api()
#         service = v1.read_namespaced_service(name=service_name, namespace=namespace)
#         ingress = service.status.load_balancer.ingress
#         if ingress:
#             ip = ingress[0].ip
#             hostname = ingress[0].hostname
#             if ip:
#                 return ip
#             elif hostname:
#                 return hostname
#         return None
#     except client.exceptions.ApiException as e:
#         print(f"Error retrieving LoadBalancer URL: {e}")
#         return None


class SpliceOrcPlugin:
    """JAC Splice-Orchestrator Plugin."""

    def __init__(self):
        """Constructor for SpliceOrcPlugin."""
        namespace = "jac-splice-orc"
        self.create_namespace(namespace)
        self.create_service_account(namespace)
        self.apply_pod_manager_yaml(namespace)
        self.configure_pod_manager_url(namespace)

    def create_namespace(self, namespace_name):
        try:
            config.load_kube_config()
        except config.ConfigException:
            config.load_incluster_config()
        v1 = client.CoreV1Api()

        # Check if the namespace exists
        namespaces = v1.list_namespace()
        if any(ns.metadata.name == namespace_name for ns in namespaces.items):
            print(f"Namespace '{namespace_name}' already exists.")
        else:
            ns = client.V1Namespace(metadata=client.V1ObjectMeta(name=namespace_name))
            v1.create_namespace(ns)
            print(f"Namespace '{namespace_name}' created.")

    def create_service_account(self, namespace):
        v1 = client.CoreV1Api()
        service_account_name = "smartimportsa"

        # Check if the ServiceAccount already exists
        try:
            v1.read_namespaced_service_account(
                name=service_account_name, namespace=namespace
            )
            print(
                f"ServiceAccount '{service_account_name}' already exists in namespace '{namespace}'."
            )
        except client.exceptions.ApiException as e:
            if e.status == 404:
                # Create the ServiceAccount
                sa = client.V1ServiceAccount(
                    metadata=client.V1ObjectMeta(name=service_account_name)
                )
                v1.create_namespaced_service_account(namespace=namespace, body=sa)
                print(
                    f"ServiceAccount '{service_account_name}' created in namespace '{namespace}'."
                )
            else:
                print(f"Error creating ServiceAccount: {e}")
                raise

        # Create the Role and RoleBinding
        self.create_role_and_binding(namespace, service_account_name)

    def create_role_and_binding(self, namespace, service_account_name):
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
                    resources=[
                        "pods",
                        "services",
                        "configmaps",
                    ],  # Added 'configmaps' here
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

        # Rest of the method remains the same...
        # Check if the Role exists and create it if it doesn't
        try:
            rbac_api.read_namespaced_role(name=role_name, namespace=namespace)
            print(f"Role '{role_name}' already exists in namespace '{namespace}'.")
        except client.exceptions.ApiException as e:
            if e.status == 404:
                # Create the Role
                rbac_api.create_namespaced_role(namespace=namespace, body=role)
                print(f"Role '{role_name}' created in namespace '{namespace}'.")
            else:
                print(f"Error creating Role: {e}")
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
            print(
                f"RoleBinding '{role_binding_name}' already exists in namespace '{namespace}'."
            )
        except client.exceptions.ApiException as e:
            if e.status == 404:
                # Create the RoleBinding
                rbac_api.create_namespaced_role_binding(
                    namespace=namespace, body=role_binding
                )
                print(
                    f"RoleBinding '{role_binding_name}' created in namespace '{namespace}'."
                )
            else:
                print(f"Error creating RoleBinding: {e}")
                raise

    def apply_pod_manager_yaml(self, namespace):
        try:
            config.load_kube_config()
        except config.ConfigException:
            config.load_incluster_config()

        k8s_client = client.ApiClient()
        yaml_file = os.path.join(
            os.path.dirname(__file__), "..", "managers", "pod_manager_deployment.yml"
        )
        yaml_file = os.path.abspath(yaml_file)

        print(f"Applying {yaml_file} in namespace {namespace}")

        try:
            utils.create_from_yaml(k8s_client, yaml_file, namespace=namespace)
            print(f"Successfully applied {yaml_file}")
        except utils.FailToCreateError as failure:
            for err in failure.api_exceptions:
                if err.status == 409:
                    print(f"Resource already exists: {err.reason}")
                else:
                    print(f"Error creating resource: {err}")
                    raise
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise

    def configure_pod_manager_url(self, namespace):
        service_name = "pod-manager-service"
        url = self.get_loadbalancer_url(service_name, namespace)
        if url:
            pod_manager_url = f"http://{url}"
            # Directly set the pod_manager_url in settings
            from jaclang import settings

            settings.pod_manager_url = pod_manager_url
            print(f"Set settings.pod_manager_url to {pod_manager_url}")
        else:
            print("Failed to retrieve the pod_manager_url.")

    def get_loadbalancer_url(self, service_name, namespace):
        try:
            config.load_kube_config()
        except config.ConfigException:
            config.load_incluster_config()

        v1 = client.CoreV1Api()
        try:
            service = v1.read_namespaced_service(name=service_name, namespace=namespace)
            ingress = service.status.load_balancer.ingress
            if ingress:
                ip = ingress[0].ip
                hostname = ingress[0].hostname
                print(f"ip: {ip}, host: {hostname}")
                if ip:
                    return ip
                elif hostname:
                    return hostname
            return None
        except client.exceptions.ApiException as e:
            print(f"Error retrieving LoadBalancer URL: {e}")
            return None

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
        from jaclang.settings import settings

        if (
            target in settings.module_config
            and settings.module_config[target]["load_type"] == "remote"
        ):
            proxy = ModuleProxy(settings.pod_manager_url)
            print(f"Loading Kubernetes Pod Integration")
            remote_module_proxy = proxy.get_module_proxy(
                module_name=target, module_config=settings.module_config[target]
            )
            print(f"Loading remote module {remote_module_proxy}")
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
            jac_machine.attach_program(JacProgram(mod_bundle=None, bytecode=None))

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
