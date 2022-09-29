from prometheus_api_client import PrometheusConnect
from jaseci.svc import CommonService, ServiceState as Ss
from .common import PROMON_CONFIG, Cpu, Disk, Memory, Network


class PromotheusService(CommonService):
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
            self.app = PrometheusConnect(url=configs.get("url"), disable_ssl=True)
            self.cpu = Cpu(self.app)
            self.memory = Memory(self.app)
            self.network = Network(self.app)
            self.disk = Disk(self.app)
            self.state = Ss.RUNNING
        else:
            self.state = Ss.DISABLED

    ###################################################
    #                  COMMON UTILS                   #
    ###################################################

    def all_metrics(self) -> list:
        return self.app.all_metrics()

    def pods(self) -> dict:
        util = self.app.get_current_metric_value("kube_pod_info")
        res = {}
        for pod in util:
            info = pod["metric"]
            node = info["node"]
            pod = info["pod"]
            if res.get(node) is None:
                res[node] = set()
            res[node].add(pod)
        return res

    def info(self) -> dict:
        util = self.app.get_current_metric_value("kube_pod_info")
        res = {}
        for pod in util:
            pod_name = pod["metric"]["pod"]
            res[pod_name] = pod["metric"]

        cpu = self.cpu.utilization_per_pod_cores()
        for pod in util:
            pod_name = pod["metric"]["pod"]
            pod_cpu = cpu.get(pod_name, 0)
            res[pod_name]["cpu_utilization_cores"] = pod_cpu

        mem = self.memory.utilization_per_pod_bytes()
        for pod in util:
            pod_name = pod["metric"]["pod"]
            pod_mem = mem.get(pod_name, 0)
            res[pod_name]["mem_utilization_bytes"] = pod_mem

        recv = self.network.receive_per_pod_bytes()
        for pod in util:
            pod_name = pod["metric"]["pod"]
            pod_recv = recv.get(pod_name, 0)
            res[pod_name]["network_recv_bytes"] = pod_recv

        tran = self.network.transmit_per_pod_bytes()
        for pod in util:
            pod_name = pod["metric"]["pod"]
            pod_tran = tran.get(pod_name, 0)
            res[pod_name]["network_tran_bytes"] = pod_tran

        return res

    ####################################################
    #                    OVERRIDDEN                    #
    ####################################################

    def get_config(self, hook) -> dict:
        return hook.build_config("PROMON_CONFIG", PROMON_CONFIG)
