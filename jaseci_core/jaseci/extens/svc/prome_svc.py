import time
from prometheus_api_client import PrometheusConnect
from jaseci.jsorc.jsorc import JsOrc


class MetricValue:
    node = None
    pod = None

    def __init__(self, _node: dict, _pod: dict):
        self.node = _node
        self.pod = _pod


@JsOrc.service(name="prome", config="PROME_CONFIG", manifest="PROME_MANIFEST")
class PrometheusService(JsOrc.CommonService):
    ###################################################
    #                     BUILDER                     #
    ###################################################

    def run(self):
        self.app = PrometheusConnect(url=self.config.get("url"), disable_ssl=True)
        self.ping()
        self.cpu = Cpu(self.app)
        self.memory = Memory(self.app)
        self.network = Network(self.app)
        self.disk = Disk(self.app)

    ###################################################
    #                  COMMON UTILS                   #
    ###################################################

    def ping(self) -> bool:
        prom = self.app
        response = prom._session.get(
            "{0}/".format(prom.url),
            verify=prom.ssl_verification,
            headers=prom.headers,
            timeout=2,
        )
        return response.ok

    def all_metrics(self) -> list:
        return self.app.all_metrics()

    def pods(self, namespace: str = "", exclude_prom: bool = False) -> dict:
        if namespace == "":
            util = self.app.get_current_metric_value("kube_pod_info")
        else:
            util = self.app.get_current_metric_value(
                f"kube_pod_info{{namespace='{namespace}'}}"
            )
        res = {}
        for pod in util:
            info = pod["metric"]
            node = info["node"]
            pod = info["pod"]
            if exclude_prom and "prometheus" in pod:
                continue
            if res.get(node) is None:
                res[node] = []
            res[node].append(pod)
        return res

    def node_info(
        self,
        namespace: str = "",
        exclude_prom: bool = False,
        timestamp: int = 0,
        duration: int = 0,
    ) -> dict:
        if namespace == "":
            util = self.app.get_current_metric_value("kube_node_info")
        else:
            util = self.app.get_current_metric_value(
                f"kube_node_info{{namespace='{namespace}'}}"
            )

        res = {}
        disk_read = self.disk.read()
        disk_write = self.disk.write()

        node_names = [nodes["metric"]["node"] for nodes in util]

        for node_name in node_names:
            res[node_name] = {}

        for node_name in node_names:
            res[node_name]["disk_read_bytes"] = disk_read.get(node_name, 0)

        for node_name in node_names:
            res[node_name]["disk_write_bytes"] = disk_write.get(node_name, 0)

        return res

    def pod_info(
        self,
        namespace: str = "",
        exclude_prom: bool = False,
        timestamp: int = 0,
        duration: int = 0,
    ) -> dict:
        if namespace == "":
            util = self.app.get_current_metric_value("kube_pod_info")
        else:
            util = self.app.get_current_metric_value(
                f"kube_pod_info{{namespace='{namespace}'}}"
            )

        res = {}

        for pod in util:
            pod_name = pod["metric"]["pod"]
            if exclude_prom and "prometheus" in pod_name:
                continue

        for pod in util:
            pod_name = pod["metric"]["pod"]
            if exclude_prom and "prometheus" in pod_name:
                continue
            # res[pod_name] = pod["metric"]
            res[pod_name] = {}

        if timestamp != 0 and duration != 0:
            cpu = self.cpu.utilization_per_pod_cores(ts=timestamp, duration=duration)
        else:
            cpu = self.cpu.utilization_per_pod_cores()
        for pod in util:
            pod_name = pod["metric"]["pod"]
            if exclude_prom and "prometheus" in pod_name:
                continue
            pod_cpu = cpu.get(pod_name, 0)

            res[pod_name]["cpu_utilization_cores"] = pod_cpu
        if timestamp != 0 and duration != 0:
            cpu = self.cpu.utilization_per_pod_cores(ts=timestamp, duration=duration)
        else:
            cpu = self.cpu.utilization_per_pod_cores()
        for pod in util:
            pod_name = pod["metric"]["pod"]
            if exclude_prom and "prometheus" in pod_name:
                continue
            pod_cpu = cpu.get(pod_name, 0)

            res[pod_name]["cpu_utilization_cores"] = pod_cpu

        mem = self.memory.utilization_per_pod_bytes()
        for pod in util:
            pod_name = pod["metric"]["pod"]
            pod_mem = mem.get(pod_name, 0)
            res[pod_name]["mem_utilization_bytes"] = pod_mem

        if timestamp != 0 and duration != 0:
            recv = self.network.receive_per_pod_bytes(ts=timestamp, duration=duration)
        else:
            recv = self.network.receive_per_pod_bytes()
        for pod in util:
            pod_name = pod["metric"]["pod"]
            if exclude_prom and "prometheus" in pod_name:
                continue
            pod_recv = recv.get(pod_name, 0)
            res[pod_name]["network_recv_bytes"] = pod_recv

        if timestamp != 0 and duration != 0:
            tran = self.network.transmit_per_pod_bytes(ts=timestamp, duration=duration)
        else:
            tran = self.network.transmit_per_pod_bytes()
        for pod in util:
            pod_name = pod["metric"]["pod"]
            if exclude_prom and "prometheus" in pod_name:
                continue
            pod_tran = tran.get(pod_name, 0)
            res[pod_name]["network_tran_bytes"] = pod_tran

        return res

    def info(
        self,
        namespace: str = "",
        exclude_prom: bool = False,
        timestamp: int = 0,
        duration: int = 0,
    ) -> MetricValue:
        node_value = self.node_info(
            namespace=namespace,
            exclude_prom=exclude_prom,
            timestamp=timestamp,
            duration=duration,
        )
        pod_value = self.pod_info(
            namespace=namespace,
            exclude_prom=exclude_prom,
            timestamp=timestamp,
            duration=duration,
        )
        return MetricValue(_node=node_value, _pod=pod_value)


class Info:
    def __init__(self, app):
        self.app = app


class Cpu(Info):
    def utilization_core(self) -> dict:
        util = self.app.get_current_metric_value(
            'sum(irate(node_cpu_seconds_total{mode!="idle"}[10m])) by (node)'
        )
        res = {}
        for node in util:
            node_name = node["metric"]["node"]
            node_util = float(node["value"][1])
            res[node_name] = node_util
        return res

    def utilization_percentage(self) -> dict:
        util = self.app.get_current_metric_value(
            '(sum(irate(node_cpu_seconds_total{mode!="idle"}[10m])) by '
            '(node)) / (sum(irate(node_cpu_seconds_total{mode!=""}[10m])) by '
            "(node)) * 100"
        )
        res = {}
        for node in util:
            node_name = node["metric"]["node"]
            node_util = float(node["value"][1])
            res[node_name] = node_util
        return res

    def utilization_per_pod_cores(self, ts=int(time.time()), duration=10) -> dict:
        query_str = f'sum(rate(container_cpu_usage_seconds_total{{pod!=""}}[{duration}s] @ {ts})) by (pod)'
        util = self.app.get_current_metric_value(query_str)
        res = {}
        for pod in util:
            pod_name = pod["metric"]["pod"]
            value = float(pod["value"][1])
            res[pod_name] = float(value)
        return res


class Memory(Info):
    def total_bytes(self) -> dict:
        util = self.app.get_current_metric_value(
            "sum(node_memory_MemTotal_bytes) by (node)"
        )
        res = {}
        for node in util:
            node_name = node["metric"]["node"]
            node_util = float(node["value"][1])
            res[node_name] = node_util
        return res

    def utilization_bytes(self) -> dict:
        util = self.app.get_current_metric_value(
            "sum(node_memory_Active_bytes) by (node)"
        )
        res = {}
        for node in util:
            node_name = node["metric"]["node"]
            node_util = float(node["value"][1])
            res[node_name] = node_util
        return res

    def utilization_percentage(self) -> dict:
        util = self.app.get_current_metric_value(
            "sum(node_memory_Active_bytes / node_memory_MemTotal_bytes * 100 ) by "
            "(node)"
        )
        res = {}
        for node in util:
            node_name = node["metric"]["node"]
            node_util = float(node["value"][1])
            res[node_name] = node_util
        return res

    def utilization_per_pod_bytes(self) -> dict:
        util = self.app.get_current_metric_value(
            'sum(container_memory_working_set_bytes{pod!=""}) by (pod)'
        )
        res = {}
        for pod in util:
            pod_name = pod["metric"]["pod"]
            value = float(pod["value"][1])
            res[pod_name] = float(value)
        return res


class Network(Info):
    def receive_bytes(self) -> dict:
        util = self.app.get_current_metric_value(
            "sum (rate (node_network_receive_bytes_total{}[10m])) by (node)"
        )
        res = {}
        for node in util:
            node_name = node["metric"]["node"]
            node_util = float(node["value"][1])
            res[node_name] = node_util
        return res

    def receive_per_pod_bytes(self, ts: int = int(time.time()), duration: int = 10):
        util = self.app.get_current_metric_value(
            f'sum (rate (container_network_receive_bytes_total{{pod!=""}}[{duration}s] @ {ts})) by (pod)'
        )
        res = {}
        for pod in util:
            pod_name = pod["metric"]["pod"]
            value = pod["value"][1]
            res[pod_name] = float(value)
        return res

    def transmit_bytes(self) -> dict:
        util = self.app.get_current_metric_value(
            "sum (rate (node_network_transmit_bytes_total{}[10m])) by (node)"
        )
        res = {}
        for node in util:
            node_name = node["metric"]["node"]
            node_util = float(node["value"][1])
            res[node_name] = node_util
        return res

    def transmit_per_pod_bytes(self, ts: int = int(time.time()), duration: int = 10):
        util = self.app.get_current_metric_value(
            f'sum (rate (container_network_transmit_bytes_total{{pod!=""}}[{duration}s] @ {ts})) by (pod)'
        )
        res = {}
        for pod in util:
            pod_name = pod["metric"]["pod"]
            value = pod["value"][1]
            res[pod_name] = float(value)
        return res


class Disk(Info):
    def total_bytes(self) -> dict:
        util = self.app.get_current_metric_value(
            'sum(avg (node_filesystem_size_bytes{mountpoint!="/boot", '
            'fstype!="tmpfs"}) without (mountpoint)) by (node)'
        )
        res = {}
        for node in util:
            node_name = node["metric"]["node"]
            node_util = float(node["value"][1])
            res[node_name] = node_util
        return res

    def free_bytes(self) -> dict:
        util = self.app.get_current_metric_value(
            'sum(avg (node_filesystem_free_bytes{mountpoint!="/boot", '
            'fstype!="tmpfs"}) without (mountpoint)) by (node)'
        )
        res = {}
        for node in util:
            node_name = node["metric"]["node"]
            node_util = float(node["value"][1])
            res[node_name] = node_util
        return res

    def read(self) -> dict:
        util = self.app.get_current_metric_value(
            "sum (rate (node_disk_read_bytes_total{}[10m])) by (node)"
        )
        res = {}
        for node in util:
            node_name = node["metric"]["node"]
            node_util = float(node["value"][1])
            res[node_name] = node_util
        return res

    def write(self) -> dict:
        util = self.app.get_current_metric_value(
            "sum (rate (node_disk_written_bytes_total{}[10m])) by (node)"
        )
        res = {}
        for node in util:
            node_name = node["metric"]["node"]
            node_util = float(node["value"][1])
            res[node_name] = node_util
        return res
