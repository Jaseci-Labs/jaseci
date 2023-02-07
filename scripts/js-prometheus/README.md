## Set up a Prometheus for Jaseci System

To set up a Promethues system for Jaseci, please run
```bash
kubectl delete -f jaseci-prometheus.yaml
```

This command is equivalent to running
```bash
helm install jaseci-prometheus prometheus-community/prometheus
```

## Test Prometheus

You need to set up port forwarding with
```bash
kubectl port-forward \<Jaseci Prometheus pod name\> 8000:9090
```
Then open `http://localhost:8000`. If you see the Prometheus WebUI, it means that you have set up the databse correctly.

The Prometheus instance installed with the given yaml file also comes with node exporter. You can test it with `sum(node_cpu_seconds_total) by (node)`, you should see all your nodes in the result list. Also, you can run `sum(container_cpu_usage_seconds_total) by (pod)`, you should see all your pods there.
