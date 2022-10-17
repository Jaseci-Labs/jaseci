from prometheus_api_client import PrometheusConnect


class Promon:
    def __init__(self, url: str):
        self.prom = PrometheusConnect(url=url, disable_ssl=True)

    def all_metrics(self) -> list:
        return self.prom.all_metrics()

    def cpu_utilization_core(self) -> dict:
        util = self.prom.get_current_metric_value(
            'sum(irate(node_cpu_seconds_total{mode!="idle"}[10m])) by (node)'
        )
        res = {}
        for node in util:
            node_name = node["metric"]["node"]
            node_util = float(node["value"][1])
            res[node_name] = node_util
        return res

    def cpu_utilization_percentage(self) -> dict:
        util = self.prom.get_current_metric_value(
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

    def cpu_utilization_per_pod_cores(self) -> dict:
        util = self.prom.get_current_metric_value(
            'sum(irate(container_cpu_usage_seconds_total{pod!=""}[10m])) by (pod)'
        )
        res = {}
        for pod in util:
            pod_name = pod["metric"]["pod"]
            value = float(pod["value"][1])
            res[pod_name] = float(value)
        return res

    def mem_total_bytes(self) -> dict:
        util = self.prom.get_current_metric_value(
            "sum(node_memory_MemTotal_bytes) by (node)"
        )
        res = {}
        for node in util:
            node_name = node["metric"]["node"]
            node_util = float(node["value"][1])
            res[node_name] = node_util
        return res

    def mem_utilization_bytes(self) -> dict:
        util = self.prom.get_current_metric_value(
            "sum(node_memory_Active_bytes) by (node)"
        )
        res = {}
        for node in util:
            node_name = node["metric"]["node"]
            node_util = float(node["value"][1])
            res[node_name] = node_util
        return res

    def mem_utilization_percentage(self) -> dict:
        util = self.prom.get_current_metric_value(
            "sum(node_memory_Active_bytes / node_memory_MemTotal_bytes * 100 ) by "
            "(node)"
        )
        res = {}
        for node in util:
            node_name = node["metric"]["node"]
            node_util = float(node["value"][1])
            res[node_name] = node_util
        return res

    def mem_utilization_per_pod_bytes(self) -> dict:
        util = self.prom.get_current_metric_value(
            'sum(container_memory_working_set_bytes{pod!=""}) by (pod)'
        )
        res = {}
        for pod in util:
            pod_name = pod["metric"]["pod"]
            value = float(pod["value"][1])
            res[pod_name] = float(value)
        return res

    def node_pods(self) -> dict:
        util = self.prom.get_current_metric_value("kube_pod_info")
        res = {}
        for pod in util:
            info = pod["metric"]
            node = info["node"]
            pod = info["pod"]
            if res.get(node) is None:
                res[node] = set()
            res[node].add(pod)
        return res

    def network_receive_bytes(self) -> dict:
        util = self.prom.get_current_metric_value(
            "sum (rate (node_network_receive_bytes_total{}[10m])) by (node)"
        )
        res = {}
        for node in util:
            node_name = node["metric"]["node"]
            node_util = float(node["value"][1])
            res[node_name] = node_util
        return res

    def network_receive_per_pod_bytes(self):
        util = self.prom.get_current_metric_value(
            'sum (rate (container_network_receive_bytes_total{pod!=""}[10m])) by (pod)'
        )
        res = {}
        for pod in util:
            pod_name = pod["metric"]["pod"]
            value = pod["value"][1]
            res[pod_name] = float(value)
        return res

    def network_transmit_bytes(self) -> dict:
        util = self.prom.get_current_metric_value(
            "sum (rate (node_network_transmit_bytes_total{}[10m])) by (node)"
        )
        res = {}
        for node in util:
            node_name = node["metric"]["node"]
            node_util = float(node["value"][1])
            res[node_name] = node_util
        return res

    def network_transmit_per_pod_bytes(self):
        util = self.prom.get_current_metric_value(
            'sum (rate (container_network_transmit_bytes_total{pod!=""}[10m])) by (pod)'
        )
        res = {}
        for pod in util:
            pod_name = pod["metric"]["pod"]
            value = pod["value"][1]
            res[pod_name] = float(value)
        return res

    def disk_total_bytes(self) -> dict:
        util = self.prom.get_current_metric_value(
            'sum(avg (node_filesystem_size_bytes{mountpoint!="/boot", '
            'fstype!="tmpfs"}) without (mountpoint)) by (node)'
        )
        res = {}
        for node in util:
            node_name = node["metric"]["node"]
            node_util = float(node["value"][1])
            res[node_name] = node_util
        return res

    def disk_free_bytes(self) -> dict:
        util = self.prom.get_current_metric_value(
            'sum(avg (node_filesystem_free_bytes{mountpoint!="/boot", '
            'fstype!="tmpfs"}) without (mountpoint)) by (node)'
        )
        res = {}
        for node in util:
            node_name = node["metric"]["node"]
            node_util = float(node["value"][1])
            res[node_name] = node_util
        return res

    def pod_info(self) -> dict:
        util = self.prom.get_current_metric_value("kube_pod_info")
        res = {}
        for pod in util:
            pod_name = pod["metric"]["pod"]
            res[pod_name] = pod["metric"]

        cpu = self.cpu_utilization_per_pod_cores()
        for pod in util:
            pod_name = pod["metric"]["pod"]
            pod_cpu = cpu.get(pod_name, 0)
            res[pod_name]["cpu_utilization_cores"] = pod_cpu

        mem = self.mem_utilization_per_pod_bytes()
        for pod in util:
            pod_name = pod["metric"]["pod"]
            pod_mem = mem.get(pod_name, 0)
            res[pod_name]["mem_utilization_bytes"] = pod_mem

        recv = self.network_receive_per_pod_bytes()
        for pod in util:
            pod_name = pod["metric"]["pod"]
            pod_recv = recv.get(pod_name, 0)
            res[pod_name]["network_recv_bytes"] = pod_recv

        tran = self.network_transmit_per_pod_bytes()
        for pod in util:
            pod_name = pod["metric"]["pod"]
            pod_tran = tran.get(pod_name, 0)
            res[pod_name]["network_tran_bytes"] = pod_tran

        return res
