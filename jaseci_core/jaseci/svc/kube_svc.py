from jaseci import JsOrc

from kubernetes import config as kubernetes_config
from kubernetes.client import ApiClient, CoreV1Api, AppsV1Api, RbacAuthorizationV1Api
from kubernetes.client.rest import ApiException

from jaseci.utils.utils import logger


@JsOrc.service(name="kube", config="KUBE_CONFIG")
class KubeService(JsOrc.CommonService):
    ###################################################
    #                     BUILDER                     #
    ###################################################

    def run(self):
        self._in_cluster = self.config.get("in_cluster", True)
        if self._in_cluster:
            kubernetes_config.load_incluster_config()
        else:
            kubernetes_config.load_kube_config()

        self.namespace = self.config.get("namespace", "default")
        config = self.config.get("config")

        self.app = ApiClient(config)
        self.core = CoreV1Api(config)
        self.api = AppsV1Api(self.app)
        self.auth = RbacAuthorizationV1Api(self.app)

        self.ping()
        self.defaults()

    def defaults(self):
        self.create_apis = {
            "Service": self.core.create_namespaced_service,
            "Deployment": self.api.create_namespaced_deployment,
            "ConfigMap": self.core.create_namespaced_config_map,
            "ServiceAccount": self.core.create_namespaced_service_account,
            "ClusterRole": self.auth.create_cluster_role,
            "ClusterRoleBinding": self.auth.create_cluster_role_binding,
            "Secret": self.core.create_namespaced_secret,
            "PersistentVolumeClaim": (
                self.core.create_namespaced_persistent_volume_claim
            ),
            "DaemonSet": self.api.create_namespaced_daemon_set,
        }
        self.patch_apis = {
            "Service": self.core.patch_namespaced_service,
            "Deployment": self.api.patch_namespaced_deployment,
            "ConfigMap": self.core.patch_namespaced_config_map,
            "ServiceAccount": self.core.patch_namespaced_service_account,
            "ClusterRole": self.auth.patch_cluster_role,
            "ClusterRoleBinding": self.auth.patch_cluster_role_binding,
            "Secret": self.core.patch_namespaced_secret,
            "PersistentVolumeClaim": (
                self.core.patch_namespaced_persistent_volume_claim
            ),
            "DaemonSet": self.api.patch_namespaced_daemon_set,
        }
        self.delete_apis = {
            "Service": self.core.delete_namespaced_service,
            "Deployment": self.api.delete_namespaced_deployment,
            "ConfigMap": self.core.delete_namespaced_config_map,
            "ServiceAccount": self.core.delete_namespaced_service_account,
            "ClusterRole": self.auth.delete_cluster_role,
            "ClusterRoleBinding": self.auth.delete_cluster_role_binding,
            "Secret": self.core.delete_namespaced_secret,
            "PersistentVolumeClaim": (
                self.core.delete_namespaced_persistent_volume_claim
            ),
            "DaemonSet": self.api.delete_namespaced_daemon_set,
        }
        self.read_apis = {
            "Service": self.core.read_namespaced_service,
            "Endpoints": self.core.read_namespaced_endpoints,
            "Deployment": self.api.read_namespaced_deployment,
            "ConfigMap": self.core.read_namespaced_config_map,
            "ServiceAccount": self.core.read_namespaced_service_account,
            "ClusterRole": self.auth.read_cluster_role,
            "ClusterRoleBinding": self.auth.read_cluster_role_binding,
            "Secret": self.core.read_namespaced_secret,
            "PersistentVolumeClaim": self.core.read_namespaced_persistent_volume_claim,
            "DaemonSet": self.api.read_namespaced_daemon_set,
        }

    ###################################################
    #                     COMMONS                     #
    ###################################################

    def ping(self):
        res = self.app.call_api("/readyz", "GET")
        return res[1] == 200

    def in_cluster(self):
        """
        Check if JSORC/Jaseci is running in a kubernetes cluster
        """
        try:
            return self._in_cluster and self.ping()
        except ApiException as e:
            logger.info(f"Kubernetes cluster environment check failed: {e}")
            return False

    def create(
        self,
        kind: str,
        name: str,
        conf: dict,
        namespace: str = None,
        log_pref: str = "",
    ):
        namespace = namespace or self.namespace
        try:
            logger.info(
                f"{log_pref} Creating {kind} for `{name}` with namespace `{namespace}`"
            )
            if kind.startswith("ClusterRole"):
                self.create_apis[kind](body=conf)
            else:
                self.create_apis[kind](namespace=namespace, body=conf)
        except ApiException as e:
            logger.error(
                f"{log_pref} Error creating {kind} for `{name}` with namespace `{namespace}` -- {e}"
            )

    def patch(
        self,
        kind: str,
        name: str,
        conf: dict,
        namespace: str = None,
        log_pref: str = "",
    ):
        namespace = namespace or self.namespace
        try:
            logger.info(
                f"{log_pref} Patching {kind} for `{name}` with namespace `{namespace}`"
            )
            if kind.startswith("ClusterRole"):
                self.patch_apis[kind](name=name, body=conf)
            else:
                self.patch_apis[kind](name=name, namespace=namespace, body=conf)
        except ApiException as e:
            logger.error(
                f"{log_pref} Error patching {kind} for `{name}` with namespace `{namespace}` -- {e}"
            )

    def read(self, kind: str, name: str, namespace: str = None, log_pref: str = ""):
        namespace = namespace or self.namespace
        try:
            logger.info(
                f"{log_pref} Retrieving {kind} for `{name}` with namespace `{namespace}`"
            )
            if kind.startswith("ClusterRole"):
                return self.read_apis[kind](name=name)
            else:
                return self.read_apis[kind](name=name, namespace=namespace)
        except ApiException as e:
            logger.error(
                f"{log_pref} Error retrieving {kind} for `{name}` with namespace `{namespace}` -- {e}"
            )
            return e

    def delete(self, kind: str, name: str, namespace: str = None, log_pref: str = ""):
        namespace = namespace or self.namespace
        try:
            logger.info(
                f"{log_pref} Deleting {kind} for `{name}` with namespace `{namespace}`"
            )
            if kind.startswith("ClusterRole"):
                return self.delete_apis[kind](name=name)
            else:
                return self.delete_apis[kind](name=name, namespace=namespace)
        except ApiException as e:
            logger.error(
                f"{log_pref} Error deleting {kind} for `{name}` with namespace `{namespace}` -- {e}"
            )
            return e

    def is_pod_running(self, name: str, namespace: str = None):
        namespace = namespace or self.namespace
        try:
            return (
                self.core.list_namespaced_pod(
                    namespace=namespace, label_selector=f"pod={name}"
                )
                .items[0]
                .status.phase
                == "Running"
            )
        except Exception:
            return False

    def terminate_jaseci(self, name: str, namespace: str = None):
        namespace = namespace or self.namespace
        try:
            for item in self.core.list_namespaced_pod(
                namespace=namespace, label_selector=f"pod={name}"
            ).items:
                self.core.delete_namespaced_pod(item["name"], namespace)
        except Exception:
            raise Exception("Force termination to restart the pod!")
