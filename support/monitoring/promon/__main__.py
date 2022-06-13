from numpy import double
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
            nodeName = node["metric"]["node"]
            nodeUtil = node["value"][1]
            res[nodeName] = nodeUtil
        return res

    def cpu_utilization_percentage(self) -> dict:
        util = self.prom.get_current_metric_value(
            '(sum(irate(node_cpu_seconds_total{mode!="idle"}[10m])) by (node)) / (sum(irate(node_cpu_seconds_total{mode!=""}[10m])) by (node)) * 100'
        )
        res = {}
        for node in util:
            nodeName = node["metric"]["node"]
            nodeUtil = node["value"][1]
            res[nodeName] = nodeUtil
        return res
    
    def cpu_utilization_per_pod_cores(self)->dict :
      util = self.prom.get_current_metric_value('sum(irate(container_cpu_usage_seconds_total{pod!=\"\"}[10m])) by (pod)')
      res = {}
      for pod in util:
        podName = pod['metric']['pod']
        value = pod["value"][1]
        res[podName] = float(value)
      return res

    def mem_total_bytes(self) -> dict:
        util = self.prom.get_current_metric_value(
            "sum(node_memory_MemTotal_bytes) by (node)"
        )
        res = {}
        for node in util:
            nodeName = node["metric"]["node"]
            nodeUtil = node["value"][1]
            res[nodeName] = nodeUtil
        return res

    def mem_utilization_bytes(self) -> dict:
        util = self.prom.get_current_metric_value(
            "sum(node_memory_Active_bytes) by (node)"
        )
        res = {}
        for node in util:
            nodeName = node["metric"]["node"]
            nodeUtil = node["value"][1]
            res[nodeName] = nodeUtil
        return res

    def mem_utilization_percentage(self) -> dict:
        util = self.prom.get_current_metric_value(
            "sum(node_memory_Active_bytes / node_memory_MemTotal_bytes * 100 ) by (node)"
        )
        res = {}
        for node in util:
            nodeName = node["metric"]["node"]
            nodeUtil = node["value"][1]
            res[nodeName] = nodeUtil
        return res

    def node_pods(self) -> list:
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


p = Promon("http://clarity31.eecs.umich.edu:8082")
print(p.cpu_utilization_per_pod_cores())
