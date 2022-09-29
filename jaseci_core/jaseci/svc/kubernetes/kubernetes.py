from kubernetes import config
from kubernetes.client import ApiClient, CoreV1Api, AppsV1Api, RbacAuthorizationV1Api

from jaseci.svc import CommonService, ServiceState as Ss
from .common import KUBE_CONFIG


class KubernetesService(CommonService):
    def __init__(self, hook=None):
        super().__init__(__class__, hook)

    ###################################################
    #                     BUILDER                     #
    ###################################################

    def build(self, hook=None):
        configs = self.get_config(hook)
        enabled = configs.get("enabled", True)

        if enabled:
            self.quiet = configs.pop("quiet", False)
            self.app = Kube(configs.get("config"))
            self.state = Ss.RUNNING
        else:
            self.state = Ss.DISABLED

    ####################################################
    #                    OVERRIDDEN                    #
    ####################################################

    def get_config(self, hook) -> dict:
        return hook.build_config("KUBE_CONFIG", KUBE_CONFIG)


class Kube:
    def __init__(self, conf):
        config.load_incluster_config()
        self.client = ApiClient(conf)
        self.core = CoreV1Api(conf)
        self.api = AppsV1Api(self.client)
        self.auth = RbacAuthorizationV1Api(self.client)

        self.defaults()

    def call(self, namespace, conf):
        if conf["kind"].startswith("ClusterRole"):
            self.create_apis[conf["kind"]](body=conf)
        else:
            self.create_apis[conf["kind"]](namespace=namespace, body=conf)

    def defaults(self):
        self.create_apis = {
            "Service": self.core.create_namespaced_service,
            "Deployment": self.api.create_namespaced_deployment,
            "ConfigMap": self.core.create_namespaced_config_map,
            "ServiceAccount": self.core.create_namespaced_service_account,
            "ClusterRole": self.auth.create_cluster_role,
            "ClusterRoleBinding": self.auth.create_cluster_role_binding,
            "Secret": self.core.create_namespaced_secret,
            "PersistentVolumeClaim": self.core.create_namespaced_persistent_volume_claim,
            "DaemonSet": self.api.create_namespaced_daemon_set,
        }
