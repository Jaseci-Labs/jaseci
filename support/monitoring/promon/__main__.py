from numpy import double
from prometheus_api_client import PrometheusConnect

class Promon:
  def __init__(self, url: str):
    self.prom = PrometheusConnect(url = url, disable_ssl=True)
  def all_metrics(self)->list:
    return self.prom.all_metrics()
  def cpu_utilization_core(self)->dict:
    util = self.prom.get_current_metric_value("sum(irate(node_cpu_seconds_total{mode!=\"idle\"}[10m])) by (node)")
    res = {}
    for node in util:
      nodeName = node["metric"]["node"]
      nodeUtil = node["value"][1]
      res[nodeName] = nodeUtil
    return res
  
  def cpu_utilization_percentage(self)->dict:
    util = self.prom.get_current_metric_value("(sum(irate(node_cpu_seconds_total{mode!=\"idle\"}[10m])) by (node)) / (sum(irate(node_cpu_seconds_total{mode!=\"\"}[10m])) by (node)) * 100")
    res = {}
    for node in util:
      nodeName = node["metric"]["node"]
      nodeUtil = node["value"][1]
      res[nodeName] = nodeUtil
    return res

p = Promon("http://clarity31.eecs.umich.edu:8082")
print(p.cpu_utilization_percentage(), p.cpu_utilization_core())