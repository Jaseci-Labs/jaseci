from jaseci.svc import KubernetesService as Ks
from jaseci_serv.configs import KUBE_CONFIG


class KubernetesService(Ks):
    def build_config(self, hook) -> dict:
        return hook.service_glob("KUBE_CONFIG", KUBE_CONFIG)
