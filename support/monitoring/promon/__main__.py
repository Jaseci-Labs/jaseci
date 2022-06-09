from prometheus_api_client import PrometheusConnect

prom = PrometheusConnect(url = "http://clarity31.eecs.umich.edu:8082", disable_ssl=True)

print(prom.all_metrics())

print(prom.get_current_metric_value("count(kube_node_info)"))