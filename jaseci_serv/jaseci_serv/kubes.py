################################################
#                  KUBERNETES                  #
################################################

REDIS_KUBE = {
    "Service": [
        {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {"name": "jaseci-redis"},
            "spec": {
                "selector": {"pod": "jaseci-redis"},
                "ports": [{"protocol": "TCP", "port": 6379, "targetPort": 6379}],
            },
        }
    ],
    "Deployment": [
        {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {"name": "jaseci-redis"},
            "spec": {
                "replicas": 1,
                "selector": {"matchLabels": {"pod": "jaseci-redis"}},
                "template": {
                    "metadata": {"labels": {"pod": "jaseci-redis"}},
                    "spec": {
                        "containers": [
                            {
                                "name": "jaseci-redis-master",
                                "image": "redis",
                                "imagePullPolicy": "IfNotPresent",
                                "command": ["redis-server", "/redis-master/redis.conf"],
                                "resources": {"limits": {"cpu": "0.2"}},
                                "ports": [{"containerPort": 6379}],
                                "volumeMounts": [
                                    {"mountPath": "/redis-master-data", "name": "data"},
                                    {"mountPath": "/redis-master", "name": "config"},
                                ],
                            }
                        ],
                        "volumes": [
                            {"name": "data", "emptyDir": {}},
                            {
                                "name": "config",
                                "configMap": {
                                    "name": "jaseci-redis-config",
                                    "items": [
                                        {"key": "redis-config", "path": "redis.conf"}
                                    ],
                                },
                            },
                        ],
                    },
                },
            },
        }
    ],
    "ConfigMap": [
        {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {"name": "jaseci-redis-config"},
            "data": {
                "redis-config": "maxmemory 1000mb\nmaxmemory-policy allkeys-lru\n"
            },
        }
    ],
}


PROMON_KUBE = {
    "ServiceAccount": [
        {
            "apiVersion": "v1",
            "kind": "ServiceAccount",
            "metadata": {
                "labels": {
                    "helm.sh/chart": "kube-state-metrics-4.13.0",
                    "app.kubernetes.io/managed-by": "Helm",
                    "app.kubernetes.io/component": "metrics",
                    "app.kubernetes.io/part-of": "kube-state-metrics",
                    "app.kubernetes.io/name": "kube-state-metrics",
                    "app.kubernetes.io/instance": "jaseci-prometheus",
                    "app.kubernetes.io/version": "2.5.0",
                },
                "name": "jaseci-prometheus-kube-state-metrics",
                "namespace": "default",
            },
            "imagePullSecrets": [],
        },
        {
            "apiVersion": "v1",
            "kind": "ServiceAccount",
            "metadata": {
                "labels": {
                    "component": "alertmanager",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                },
                "name": "jaseci-prometheus-alertmanager",
                "namespace": "default",
                "annotations": {},
            },
        },
        {
            "apiVersion": "v1",
            "kind": "ServiceAccount",
            "metadata": {
                "labels": {
                    "component": "node-exporter",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                },
                "name": "jaseci-prometheus-node-exporter",
                "namespace": "default",
                "annotations": {},
            },
        },
        {
            "apiVersion": "v1",
            "kind": "ServiceAccount",
            "metadata": {
                "labels": {
                    "component": "pushgateway",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                },
                "name": "jaseci-prometheus-pushgateway",
                "namespace": "default",
                "annotations": {},
            },
        },
        {
            "apiVersion": "v1",
            "kind": "ServiceAccount",
            "metadata": {
                "labels": {
                    "component": "server",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                },
                "name": "jaseci-prometheus-server",
                "namespace": "default",
                "annotations": {},
            },
        },
    ],
    "ConfigMap": [
        {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {
                "labels": {
                    "component": "alertmanager",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                },
                "name": "jaseci-prometheus-alertmanager",
                "namespace": "default",
            },
            "data": {
                "allow-snippet-annotations": "false",
                "alertmanager.yml": "global: {}\nreceivers:\n- name: default-receiver\nroute:\n  group_interval: 5m\n  group_wait: 10s\n  receiver: default-receiver\n  repeat_interval: 3h\n",
            },
        },
        {
            "apiVersion": "v1",
            "kind": "ConfigMap",
            "metadata": {
                "labels": {
                    "component": "server",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                },
                "name": "jaseci-prometheus-server",
                "namespace": "default",
            },
            "data": {
                "allow-snippet-annotations": "false",
                "alerting_rules.yml": "{}\n",
                "alerts": "{}\n",
                "prometheus.yml": 'global:\n  evaluation_interval: 1m\n  scrape_interval: 1m\n  scrape_timeout: 10s\nrule_files:\n- /etc/config/recording_rules.yml\n- /etc/config/alerting_rules.yml\n- /etc/config/rules\n- /etc/config/alerts\nscrape_configs:\n- job_name: prometheus\n  static_configs:\n  - targets:\n    - localhost:9090\n- bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token\n  job_name: kubernetes-apiservers\n  kubernetes_sd_configs:\n  - role: endpoints\n  relabel_configs:\n  - action: keep\n    regex: default;kubernetes;https\n    source_labels:\n    - __meta_kubernetes_namespace\n    - __meta_kubernetes_service_name\n    - __meta_kubernetes_endpoint_port_name\n  scheme: https\n  tls_config:\n    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt\n    insecure_skip_verify: true\n- bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token\n  job_name: kubernetes-nodes\n  kubernetes_sd_configs:\n  - role: node\n  relabel_configs:\n  - action: labelmap\n    regex: __meta_kubernetes_node_label_(.+)\n  - replacement: kubernetes.default.svc:443\n    target_label: __address__\n  - regex: (.+)\n    replacement: /api/v1/nodes/$1/proxy/metrics\n    source_labels:\n    - __meta_kubernetes_node_name\n    target_label: __metrics_path__\n  scheme: https\n  tls_config:\n    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt\n    insecure_skip_verify: true\n- bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token\n  job_name: kubernetes-nodes-cadvisor\n  kubernetes_sd_configs:\n  - role: node\n  relabel_configs:\n  - action: labelmap\n    regex: __meta_kubernetes_node_label_(.+)\n  - replacement: kubernetes.default.svc:443\n    target_label: __address__\n  - regex: (.+)\n    replacement: /api/v1/nodes/$1/proxy/metrics/cadvisor\n    source_labels:\n    - __meta_kubernetes_node_name\n    target_label: __metrics_path__\n  scheme: https\n  tls_config:\n    ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt\n    insecure_skip_verify: true\n- honor_labels: true\n  job_name: kubernetes-service-endpoints\n  kubernetes_sd_configs:\n  - role: endpoints\n  relabel_configs:\n  - action: keep\n    regex: true\n    source_labels:\n    - __meta_kubernetes_service_annotation_prometheus_io_scrape\n  - action: drop\n    regex: true\n    source_labels:\n    - __meta_kubernetes_service_annotation_prometheus_io_scrape_slow\n  - action: replace\n    regex: (https?)\n    source_labels:\n    - __meta_kubernetes_service_annotation_prometheus_io_scheme\n    target_label: __scheme__\n  - action: replace\n    regex: (.+)\n    source_labels:\n    - __meta_kubernetes_service_annotation_prometheus_io_path\n    target_label: __metrics_path__\n  - action: replace\n    regex: (.+?)(?::\\d+)?;(\\d+)\n    replacement: $1:$2\n    source_labels:\n    - __address__\n    - __meta_kubernetes_service_annotation_prometheus_io_port\n    target_label: __address__\n  - action: labelmap\n    regex: __meta_kubernetes_service_annotation_prometheus_io_param_(.+)\n    replacement: __param_$1\n  - action: labelmap\n    regex: __meta_kubernetes_service_label_(.+)\n  - action: replace\n    source_labels:\n    - __meta_kubernetes_namespace\n    target_label: namespace\n  - action: replace\n    source_labels:\n    - __meta_kubernetes_service_name\n    target_label: service\n  - action: replace\n    source_labels:\n    - __meta_kubernetes_pod_node_name\n    target_label: node\n- honor_labels: true\n  job_name: kubernetes-service-endpoints-slow\n  kubernetes_sd_configs:\n  - role: endpoints\n  relabel_configs:\n  - action: keep\n    regex: true\n    source_labels:\n    - __meta_kubernetes_service_annotation_prometheus_io_scrape_slow\n  - action: replace\n    regex: (https?)\n    source_labels:\n    - __meta_kubernetes_service_annotation_prometheus_io_scheme\n    target_label: __scheme__\n  - action: replace\n    regex: (.+)\n    source_labels:\n    - __meta_kubernetes_service_annotation_prometheus_io_path\n    target_label: __metrics_path__\n  - action: replace\n    regex: (.+?)(?::\\d+)?;(\\d+)\n    replacement: $1:$2\n    source_labels:\n    - __address__\n    - __meta_kubernetes_service_annotation_prometheus_io_port\n    target_label: __address__\n  - action: labelmap\n    regex: __meta_kubernetes_service_annotation_prometheus_io_param_(.+)\n    replacement: __param_$1\n  - action: labelmap\n    regex: __meta_kubernetes_service_label_(.+)\n  - action: replace\n    source_labels:\n    - __meta_kubernetes_namespace\n    target_label: namespace\n  - action: replace\n    source_labels:\n    - __meta_kubernetes_service_name\n    target_label: service\n  - action: replace\n    source_labels:\n    - __meta_kubernetes_pod_node_name\n    target_label: node\n  scrape_interval: 5m\n  scrape_timeout: 30s\n- honor_labels: true\n  job_name: prometheus-pushgateway\n  kubernetes_sd_configs:\n  - role: service\n  relabel_configs:\n  - action: keep\n    regex: pushgateway\n    source_labels:\n    - __meta_kubernetes_service_annotation_prometheus_io_probe\n- honor_labels: true\n  job_name: kubernetes-services\n  kubernetes_sd_configs:\n  - role: service\n  metrics_path: /probe\n  params:\n    module:\n    - http_2xx\n  relabel_configs:\n  - action: keep\n    regex: true\n    source_labels:\n    - __meta_kubernetes_service_annotation_prometheus_io_probe\n  - source_labels:\n    - __address__\n    target_label: __param_target\n  - replacement: blackbox\n    target_label: __address__\n  - source_labels:\n    - __param_target\n    target_label: instance\n  - action: labelmap\n    regex: __meta_kubernetes_service_label_(.+)\n  - source_labels:\n    - __meta_kubernetes_namespace\n    target_label: namespace\n  - source_labels:\n    - __meta_kubernetes_service_name\n    target_label: service\n- honor_labels: true\n  job_name: kubernetes-pods\n  kubernetes_sd_configs:\n  - role: pod\n  relabel_configs:\n  - action: keep\n    regex: true\n    source_labels:\n    - __meta_kubernetes_pod_annotation_prometheus_io_scrape\n  - action: drop\n    regex: true\n    source_labels:\n    - __meta_kubernetes_pod_annotation_prometheus_io_scrape_slow\n  - action: replace\n    regex: (https?)\n    source_labels:\n    - __meta_kubernetes_pod_annotation_prometheus_io_scheme\n    target_label: __scheme__\n  - action: replace\n    regex: (.+)\n    source_labels:\n    - __meta_kubernetes_pod_annotation_prometheus_io_path\n    target_label: __metrics_path__\n  - action: replace\n    regex: (.+?)(?::\\d+)?;(\\d+)\n    replacement: $1:$2\n    source_labels:\n    - __address__\n    - __meta_kubernetes_pod_annotation_prometheus_io_port\n    target_label: __address__\n  - action: labelmap\n    regex: __meta_kubernetes_pod_annotation_prometheus_io_param_(.+)\n    replacement: __param_$1\n  - action: labelmap\n    regex: __meta_kubernetes_pod_label_(.+)\n  - action: replace\n    source_labels:\n    - __meta_kubernetes_namespace\n    target_label: namespace\n  - action: replace\n    source_labels:\n    - __meta_kubernetes_pod_name\n    target_label: pod\n  - action: drop\n    regex: Pending|Succeeded|Failed|Completed\n    source_labels:\n    - __meta_kubernetes_pod_phase\n- honor_labels: true\n  job_name: kubernetes-pods-slow\n  kubernetes_sd_configs:\n  - role: pod\n  relabel_configs:\n  - action: keep\n    regex: true\n    source_labels:\n    - __meta_kubernetes_pod_annotation_prometheus_io_scrape_slow\n  - action: replace\n    regex: (https?)\n    source_labels:\n    - __meta_kubernetes_pod_annotation_prometheus_io_scheme\n    target_label: __scheme__\n  - action: replace\n    regex: (.+)\n    source_labels:\n    - __meta_kubernetes_pod_annotation_prometheus_io_path\n    target_label: __metrics_path__\n  - action: replace\n    regex: (.+?)(?::\\d+)?;(\\d+)\n    replacement: $1:$2\n    source_labels:\n    - __address__\n    - __meta_kubernetes_pod_annotation_prometheus_io_port\n    target_label: __address__\n  - action: labelmap\n    regex: __meta_kubernetes_pod_annotation_prometheus_io_param_(.+)\n    replacement: __param_$1\n  - action: labelmap\n    regex: __meta_kubernetes_pod_label_(.+)\n  - action: replace\n    source_labels:\n    - __meta_kubernetes_namespace\n    target_label: namespace\n  - action: replace\n    source_labels:\n    - __meta_kubernetes_pod_name\n    target_label: pod\n  - action: drop\n    regex: Pending|Succeeded|Failed|Completed\n    source_labels:\n    - __meta_kubernetes_pod_phase\n  scrape_interval: 5m\n  scrape_timeout: 30s\nalerting:\n  alertmanagers:\n  - kubernetes_sd_configs:\n      - role: pod\n    tls_config:\n      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt\n    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token\n    relabel_configs:\n    - source_labels: [__meta_kubernetes_namespace]\n      regex: default\n      action: keep\n    - source_labels: [__meta_kubernetes_pod_label_app]\n      regex: prometheus\n      action: keep\n    - source_labels: [__meta_kubernetes_pod_label_component]\n      regex: alertmanager\n      action: keep\n    - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_probe]\n      regex: .*\n      action: keep\n    - source_labels: [__meta_kubernetes_pod_container_port_number]\n      regex: "9093"\n      action: keep\n',
                "recording_rules.yml": "{}\n",
                "rules": "{}\n",
            },
        },
    ],
    "PersistentVolumeClaim": [
        {
            "apiVersion": "v1",
            "kind": "PersistentVolumeClaim",
            "metadata": {
                "labels": {
                    "component": "alertmanager",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                },
                "name": "jaseci-prometheus-alertmanager",
                "namespace": "default",
            },
            "spec": {
                "accessModes": ["ReadWriteOnce"],
                "resources": {"requests": {"storage": "2Gi"}},
            },
        },
        {
            "apiVersion": "v1",
            "kind": "PersistentVolumeClaim",
            "metadata": {
                "labels": {
                    "component": "server",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                },
                "name": "jaseci-prometheus-server",
                "namespace": "default",
            },
            "spec": {
                "accessModes": ["ReadWriteOnce"],
                "resources": {"requests": {"storage": "8Gi"}},
            },
        },
    ],
    "ClusterRole": [
        {
            "apiVersion": "rbac.authorization.k8s.io/v1",
            "kind": "ClusterRole",
            "metadata": {
                "labels": {
                    "helm.sh/chart": "kube-state-metrics-4.13.0",
                    "app.kubernetes.io/managed-by": "Helm",
                    "app.kubernetes.io/component": "metrics",
                    "app.kubernetes.io/part-of": "kube-state-metrics",
                    "app.kubernetes.io/name": "kube-state-metrics",
                    "app.kubernetes.io/instance": "jaseci-prometheus",
                    "app.kubernetes.io/version": "2.5.0",
                },
                "name": "jaseci-prometheus-kube-state-metrics",
            },
            "rules": [
                {
                    "apiGroups": ["certificates.k8s.io"],
                    "resources": ["certificatesigningrequests"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": [""],
                    "resources": ["configmaps"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": ["batch"],
                    "resources": ["cronjobs"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": ["extensions", "apps"],
                    "resources": ["daemonsets"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": ["extensions", "apps"],
                    "resources": ["deployments"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": [""],
                    "resources": ["endpoints"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": ["autoscaling"],
                    "resources": ["horizontalpodautoscalers"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": ["extensions", "networking.k8s.io"],
                    "resources": ["ingresses"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": ["batch"],
                    "resources": ["jobs"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": [""],
                    "resources": ["limitranges"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": ["admissionregistration.k8s.io"],
                    "resources": ["mutatingwebhookconfigurations"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": [""],
                    "resources": ["namespaces"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": ["networking.k8s.io"],
                    "resources": ["networkpolicies"],
                    "verbs": ["list", "watch"],
                },
                {"apiGroups": [""], "resources": ["nodes"], "verbs": ["list", "watch"]},
                {
                    "apiGroups": [""],
                    "resources": ["persistentvolumeclaims"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": [""],
                    "resources": ["persistentvolumes"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": ["policy"],
                    "resources": ["poddisruptionbudgets"],
                    "verbs": ["list", "watch"],
                },
                {"apiGroups": [""], "resources": ["pods"], "verbs": ["list", "watch"]},
                {
                    "apiGroups": ["extensions", "apps"],
                    "resources": ["replicasets"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": [""],
                    "resources": ["replicationcontrollers"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": [""],
                    "resources": ["resourcequotas"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": [""],
                    "resources": ["secrets"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": [""],
                    "resources": ["services"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": ["apps"],
                    "resources": ["statefulsets"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": ["storage.k8s.io"],
                    "resources": ["storageclasses"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": ["admissionregistration.k8s.io"],
                    "resources": ["validatingwebhookconfigurations"],
                    "verbs": ["list", "watch"],
                },
                {
                    "apiGroups": ["storage.k8s.io"],
                    "resources": ["volumeattachments"],
                    "verbs": ["list", "watch"],
                },
            ],
        },
        {
            "apiVersion": "rbac.authorization.k8s.io/v1",
            "kind": "ClusterRole",
            "metadata": {
                "labels": {
                    "component": "alertmanager",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                },
                "name": "jaseci-prometheus-alertmanager",
            },
            "rules": [],
        },
        {
            "apiVersion": "rbac.authorization.k8s.io/v1",
            "kind": "ClusterRole",
            "metadata": {
                "labels": {
                    "component": "pushgateway",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                },
                "name": "jaseci-prometheus-pushgateway",
            },
            "rules": [],
        },
        {
            "apiVersion": "rbac.authorization.k8s.io/v1",
            "kind": "ClusterRole",
            "metadata": {
                "labels": {
                    "component": "server",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                },
                "name": "jaseci-prometheus-server",
            },
            "rules": [
                {
                    "apiGroups": [""],
                    "resources": [
                        "nodes",
                        "nodes/proxy",
                        "nodes/metrics",
                        "services",
                        "endpoints",
                        "pods",
                        "ingresses",
                        "configmaps",
                    ],
                    "verbs": ["get", "list", "watch"],
                },
                {
                    "apiGroups": ["extensions", "networking.k8s.io"],
                    "resources": ["ingresses/status", "ingresses"],
                    "verbs": ["get", "list", "watch"],
                },
                {"nonResourceURLs": ["/metrics"], "verbs": ["get"]},
            ],
        },
    ],
    "ClusterRoleBinding": [
        {
            "apiVersion": "rbac.authorization.k8s.io/v1",
            "kind": "ClusterRoleBinding",
            "metadata": {
                "labels": {
                    "helm.sh/chart": "kube-state-metrics-4.13.0",
                    "app.kubernetes.io/managed-by": "Helm",
                    "app.kubernetes.io/component": "metrics",
                    "app.kubernetes.io/part-of": "kube-state-metrics",
                    "app.kubernetes.io/name": "kube-state-metrics",
                    "app.kubernetes.io/instance": "jaseci-prometheus",
                    "app.kubernetes.io/version": "2.5.0",
                },
                "name": "jaseci-prometheus-kube-state-metrics",
            },
            "roleRef": {
                "apiGroup": "rbac.authorization.k8s.io",
                "kind": "ClusterRole",
                "name": "jaseci-prometheus-kube-state-metrics",
            },
            "subjects": [
                {
                    "kind": "ServiceAccount",
                    "name": "jaseci-prometheus-kube-state-metrics",
                    "namespace": "default",
                }
            ],
        },
        {
            "apiVersion": "rbac.authorization.k8s.io/v1",
            "kind": "ClusterRoleBinding",
            "metadata": {
                "labels": {
                    "component": "alertmanager",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                },
                "name": "jaseci-prometheus-alertmanager",
            },
            "subjects": [
                {
                    "kind": "ServiceAccount",
                    "name": "jaseci-prometheus-alertmanager",
                    "namespace": "default",
                }
            ],
            "roleRef": {
                "apiGroup": "rbac.authorization.k8s.io",
                "kind": "ClusterRole",
                "name": "jaseci-prometheus-alertmanager",
            },
        },
        {
            "apiVersion": "rbac.authorization.k8s.io/v1",
            "kind": "ClusterRoleBinding",
            "metadata": {
                "labels": {
                    "component": "pushgateway",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                },
                "name": "jaseci-prometheus-pushgateway",
            },
            "subjects": [
                {
                    "kind": "ServiceAccount",
                    "name": "jaseci-prometheus-pushgateway",
                    "namespace": "default",
                }
            ],
            "roleRef": {
                "apiGroup": "rbac.authorization.k8s.io",
                "kind": "ClusterRole",
                "name": "jaseci-prometheus-pushgateway",
            },
        },
        {
            "apiVersion": "rbac.authorization.k8s.io/v1",
            "kind": "ClusterRoleBinding",
            "metadata": {
                "labels": {
                    "component": "server",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                },
                "name": "jaseci-prometheus-server",
            },
            "subjects": [
                {
                    "kind": "ServiceAccount",
                    "name": "jaseci-prometheus-server",
                    "namespace": "default",
                }
            ],
            "roleRef": {
                "apiGroup": "rbac.authorization.k8s.io",
                "kind": "ClusterRole",
                "name": "jaseci-prometheus-server",
            },
        },
    ],
    "Service": [
        {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "name": "jaseci-prometheus-kube-state-metrics",
                "namespace": "default",
                "labels": {
                    "helm.sh/chart": "kube-state-metrics-4.13.0",
                    "app.kubernetes.io/managed-by": "Helm",
                    "app.kubernetes.io/component": "metrics",
                    "app.kubernetes.io/part-of": "kube-state-metrics",
                    "app.kubernetes.io/name": "kube-state-metrics",
                    "app.kubernetes.io/instance": "jaseci-prometheus",
                    "app.kubernetes.io/version": "2.5.0",
                },
                "annotations": {"prometheus.io/scrape": "true"},
            },
            "spec": {
                "type": "ClusterIP",
                "ports": [
                    {
                        "name": "http",
                        "protocol": "TCP",
                        "port": 8080,
                        "targetPort": 8080,
                    }
                ],
                "selector": {
                    "app.kubernetes.io/name": "kube-state-metrics",
                    "app.kubernetes.io/instance": "jaseci-prometheus",
                },
            },
        },
        {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "labels": {
                    "component": "alertmanager",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                },
                "name": "jaseci-prometheus-alertmanager",
                "namespace": "default",
            },
            "spec": {
                "ports": [
                    {"name": "http", "port": 80, "protocol": "TCP", "targetPort": 9093}
                ],
                "selector": {
                    "component": "alertmanager",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                },
                "sessionAffinity": "None",
                "type": "ClusterIP",
            },
        },
        {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "annotations": {"prometheus.io/scrape": "true"},
                "labels": {
                    "component": "node-exporter",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                },
                "name": "jaseci-prometheus-node-exporter",
                "namespace": "default",
            },
            "spec": {
                "ports": [
                    {
                        "name": "metrics",
                        "port": 9100,
                        "protocol": "TCP",
                        "targetPort": 9100,
                    }
                ],
                "selector": {
                    "component": "node-exporter",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                },
                "type": "ClusterIP",
            },
        },
        {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "annotations": {"prometheus.io/probe": "pushgateway"},
                "labels": {
                    "component": "pushgateway",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                },
                "name": "jaseci-prometheus-pushgateway",
                "namespace": "default",
            },
            "spec": {
                "ports": [
                    {
                        "name": "http",
                        "port": 9091,
                        "protocol": "TCP",
                        "targetPort": 9091,
                    }
                ],
                "selector": {
                    "component": "pushgateway",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                },
                "type": "ClusterIP",
            },
        },
        {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {
                "labels": {
                    "component": "server",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                },
                "name": "jaseci-prometheus-server",
                "namespace": "default",
            },
            "spec": {
                "ports": [
                    {
                        "name": "http",
                        "port": 9090,
                        "protocol": "TCP",
                        "targetPort": 9090,
                    }
                ],
                "selector": {
                    "component": "server",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                },
                "sessionAffinity": "None",
                "type": "ClusterIP",
            },
        },
    ],
    "DaemonSet": [
        {
            "apiVersion": "apps/v1",
            "kind": "DaemonSet",
            "metadata": {
                "labels": {
                    "component": "node-exporter",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                },
                "name": "jaseci-prometheus-node-exporter",
                "namespace": "default",
            },
            "spec": {
                "selector": {
                    "matchLabels": {
                        "component": "node-exporter",
                        "app": "prometheus",
                        "release": "jaseci-prometheus",
                    }
                },
                "updateStrategy": {"type": "RollingUpdate"},
                "template": {
                    "metadata": {
                        "labels": {
                            "component": "node-exporter",
                            "app": "prometheus",
                            "release": "jaseci-prometheus",
                            "chart": "prometheus-15.10.5",
                            "heritage": "Helm",
                        }
                    },
                    "spec": {
                        "serviceAccountName": "jaseci-prometheus-node-exporter",
                        "containers": [
                            {
                                "name": "prometheus-node-exporter",
                                "image": "quay.io/prometheus/node-exporter:v1.3.1",
                                "imagePullPolicy": "IfNotPresent",
                                "args": [
                                    "--path.procfs=/host/proc",
                                    "--path.sysfs=/host/sys",
                                    "--path.rootfs=/host/root",
                                    "--web.listen-address=:9100",
                                ],
                                "ports": [
                                    {
                                        "name": "metrics",
                                        "containerPort": 9100,
                                        "hostPort": 9100,
                                    }
                                ],
                                "resources": {},
                                "securityContext": {"allowPrivilegeEscalation": False},
                                "volumeMounts": [
                                    {
                                        "name": "proc",
                                        "mountPath": "/host/proc",
                                        "readOnly": True,
                                    },
                                    {
                                        "name": "sys",
                                        "mountPath": "/host/sys",
                                        "readOnly": True,
                                    },
                                    {
                                        "name": "root",
                                        "mountPath": "/host/root",
                                        "mountPropagation": "HostToContainer",
                                        "readOnly": True,
                                    },
                                ],
                            }
                        ],
                        "hostNetwork": True,
                        "hostPID": True,
                        "securityContext": {
                            "fsGroup": 65534,
                            "runAsGroup": 65534,
                            "runAsNonRoot": True,
                            "runAsUser": 65534,
                        },
                        "volumes": [
                            {"name": "proc", "hostPath": {"path": "/proc"}},
                            {"name": "sys", "hostPath": {"path": "/sys"}},
                            {"name": "root", "hostPath": {"path": "/"}},
                        ],
                    },
                },
            },
        }
    ],
    "Deployment": [
        {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": "jaseci-prometheus-kube-state-metrics",
                "namespace": "default",
                "labels": {
                    "helm.sh/chart": "kube-state-metrics-4.13.0",
                    "app.kubernetes.io/managed-by": "Helm",
                    "app.kubernetes.io/component": "metrics",
                    "app.kubernetes.io/part-of": "kube-state-metrics",
                    "app.kubernetes.io/name": "kube-state-metrics",
                    "app.kubernetes.io/instance": "jaseci-prometheus",
                    "app.kubernetes.io/version": "2.5.0",
                },
            },
            "spec": {
                "selector": {
                    "matchLabels": {
                        "app.kubernetes.io/name": "kube-state-metrics",
                        "app.kubernetes.io/instance": "jaseci-prometheus",
                    }
                },
                "replicas": 1,
                "template": {
                    "metadata": {
                        "labels": {
                            "helm.sh/chart": "kube-state-metrics-4.13.0",
                            "app.kubernetes.io/managed-by": "Helm",
                            "app.kubernetes.io/component": "metrics",
                            "app.kubernetes.io/part-of": "kube-state-metrics",
                            "app.kubernetes.io/name": "kube-state-metrics",
                            "app.kubernetes.io/instance": "jaseci-prometheus",
                            "app.kubernetes.io/version": "2.5.0",
                        }
                    },
                    "spec": {
                        "hostNetwork": False,
                        "serviceAccountName": "jaseci-prometheus-kube-state-metrics",
                        "securityContext": {
                            "fsGroup": 65534,
                            "runAsGroup": 65534,
                            "runAsUser": 65534,
                        },
                        "containers": [
                            {
                                "name": "kube-state-metrics",
                                "args": [
                                    "--port=8080",
                                    "--resources=certificatesigningrequests,configmaps,cronjobs,daemonsets,deployments,endpoints,horizontalpodautoscalers,ingresses,jobs,limitranges,mutatingwebhookconfigurations,namespaces,networkpolicies,nodes,persistentvolumeclaims,persistentvolumes,poddisruptionbudgets,pods,replicasets,replicationcontrollers,resourcequotas,secrets,services,statefulsets,storageclasses,validatingwebhookconfigurations,volumeattachments",
                                    "--telemetry-port=8081",
                                ],
                                "imagePullPolicy": "IfNotPresent",
                                "image": "registry.k8s.io/kube-state-metrics/kube-state-metrics:v2.5.0",
                                "ports": [{"containerPort": 8080, "name": "http"}],
                                "livenessProbe": {
                                    "httpGet": {"path": "/healthz", "port": 8080},
                                    "initialDelaySeconds": 5,
                                    "timeoutSeconds": 5,
                                },
                                "readinessProbe": {
                                    "httpGet": {"path": "/", "port": 8080},
                                    "initialDelaySeconds": 5,
                                    "timeoutSeconds": 5,
                                },
                            }
                        ],
                    },
                },
            },
        },
        {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "labels": {
                    "component": "alertmanager",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                },
                "name": "jaseci-prometheus-alertmanager",
                "namespace": "default",
            },
            "spec": {
                "selector": {
                    "matchLabels": {
                        "component": "alertmanager",
                        "app": "prometheus",
                        "release": "jaseci-prometheus",
                    }
                },
                "replicas": 1,
                "template": {
                    "metadata": {
                        "labels": {
                            "component": "alertmanager",
                            "app": "prometheus",
                            "release": "jaseci-prometheus",
                            "chart": "prometheus-15.10.5",
                            "heritage": "Helm",
                        }
                    },
                    "spec": {
                        "serviceAccountName": "jaseci-prometheus-alertmanager",
                        "containers": [
                            {
                                "name": "prometheus-alertmanager",
                                "image": "quay.io/prometheus/alertmanager:v0.24.0",
                                "imagePullPolicy": "IfNotPresent",
                                "securityContext": {},
                                "env": [
                                    {
                                        "name": "POD_IP",
                                        "valueFrom": {
                                            "fieldRef": {
                                                "apiVersion": "v1",
                                                "fieldPath": "status.podIP",
                                            }
                                        },
                                    }
                                ],
                                "args": [
                                    "--config.file=/etc/config/alertmanager.yml",
                                    "--storage.path=/data",
                                    "--cluster.listen-address=",
                                    "--web.external-url=http://localhost:9093",
                                ],
                                "ports": [{"containerPort": 9093}],
                                "readinessProbe": {
                                    "httpGet": {"path": "/-/ready", "port": 9093},
                                    "initialDelaySeconds": 30,
                                    "timeoutSeconds": 30,
                                },
                                "resources": {},
                                "volumeMounts": [
                                    {
                                        "name": "config-volume",
                                        "mountPath": "/etc/config",
                                    },
                                    {
                                        "name": "storage-volume",
                                        "mountPath": "/data",
                                        "subPath": "",
                                    },
                                ],
                            },
                            {
                                "name": "prometheus-alertmanager-configmap-reload",
                                "image": "jimmidyson/configmap-reload:v0.5.0",
                                "imagePullPolicy": "IfNotPresent",
                                "securityContext": {},
                                "args": [
                                    "--volume-dir=/etc/config",
                                    "--webhook-url=http://127.0.0.1:9093/-/reload",
                                ],
                                "resources": {},
                                "volumeMounts": [
                                    {
                                        "name": "config-volume",
                                        "mountPath": "/etc/config",
                                        "readOnly": True,
                                    }
                                ],
                            },
                        ],
                        "securityContext": {
                            "fsGroup": 65534,
                            "runAsGroup": 65534,
                            "runAsNonRoot": True,
                            "runAsUser": 65534,
                        },
                        "volumes": [
                            {
                                "name": "config-volume",
                                "configMap": {"name": "jaseci-prometheus-alertmanager"},
                            },
                            {
                                "name": "storage-volume",
                                "persistentVolumeClaim": {
                                    "claimName": "jaseci-prometheus-alertmanager"
                                },
                            },
                        ],
                    },
                },
            },
        },
        {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "labels": {
                    "component": "pushgateway",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                },
                "name": "jaseci-prometheus-pushgateway",
                "namespace": "default",
            },
            "spec": {
                "selector": {
                    "matchLabels": {
                        "component": "pushgateway",
                        "app": "prometheus",
                        "release": "jaseci-prometheus",
                    }
                },
                "replicas": 1,
                "template": {
                    "metadata": {
                        "labels": {
                            "component": "pushgateway",
                            "app": "prometheus",
                            "release": "jaseci-prometheus",
                            "chart": "prometheus-15.10.5",
                            "heritage": "Helm",
                        }
                    },
                    "spec": {
                        "serviceAccountName": "jaseci-prometheus-pushgateway",
                        "containers": [
                            {
                                "name": "prometheus-pushgateway",
                                "image": "prom/pushgateway:v1.4.3",
                                "imagePullPolicy": "IfNotPresent",
                                "securityContext": {},
                                "args": None,
                                "ports": [{"containerPort": 9091}],
                                "livenessProbe": {
                                    "httpGet": {"path": "/-/healthy", "port": 9091},
                                    "initialDelaySeconds": 10,
                                    "timeoutSeconds": 10,
                                },
                                "readinessProbe": {
                                    "httpGet": {"path": "/-/ready", "port": 9091},
                                    "initialDelaySeconds": 10,
                                    "timeoutSeconds": 10,
                                },
                                "resources": {},
                            }
                        ],
                        "securityContext": {"runAsNonRoot": True, "runAsUser": 65534},
                    },
                },
            },
        },
        {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "labels": {
                    "component": "server",
                    "app": "prometheus",
                    "release": "jaseci-prometheus",
                    "chart": "prometheus-15.10.5",
                    "heritage": "Helm",
                    "pod": "jaseci-prometheus-server",
                },
                "name": "jaseci-prometheus-server",
                "namespace": "default",
            },
            "spec": {
                "selector": {
                    "matchLabels": {
                        "component": "server",
                        "app": "prometheus",
                        "release": "jaseci-prometheus",
                    }
                },
                "replicas": 1,
                "template": {
                    "metadata": {
                        "labels": {
                            "component": "server",
                            "app": "prometheus",
                            "release": "jaseci-prometheus",
                            "chart": "prometheus-15.10.5",
                            "heritage": "Helm",
                            "pod": "jaseci-prometheus-server",
                        }
                    },
                    "spec": {
                        "enableServiceLinks": True,
                        "serviceAccountName": "jaseci-prometheus-server",
                        "containers": [
                            {
                                "name": "prometheus-server-configmap-reload",
                                "image": "jimmidyson/configmap-reload:v0.5.0",
                                "imagePullPolicy": "IfNotPresent",
                                "securityContext": {},
                                "args": [
                                    "--volume-dir=/etc/config",
                                    "--webhook-url=http://127.0.0.1:9090/-/reload",
                                ],
                                "resources": {},
                                "volumeMounts": [
                                    {
                                        "name": "config-volume",
                                        "mountPath": "/etc/config",
                                        "readOnly": True,
                                    }
                                ],
                            },
                            {
                                "name": "prometheus-server",
                                "image": "quay.io/prometheus/prometheus:v2.36.2",
                                "imagePullPolicy": "IfNotPresent",
                                "securityContext": {},
                                "args": [
                                    "--storage.tsdb.retention.time=15d",
                                    "--config.file=/etc/config/prometheus.yml",
                                    "--storage.tsdb.path=/data",
                                    "--web.console.libraries=/etc/prometheus/console_libraries",
                                    "--web.console.templates=/etc/prometheus/consoles",
                                    "--web.enable-lifecycle",
                                ],
                                "ports": [{"containerPort": 9090}],
                                "readinessProbe": {
                                    "httpGet": {
                                        "path": "/-/ready",
                                        "port": 9090,
                                        "scheme": "HTTP",
                                    },
                                    "initialDelaySeconds": 30,
                                    "periodSeconds": 5,
                                    "timeoutSeconds": 4,
                                    "failureThreshold": 3,
                                    "successThreshold": 1,
                                },
                                "livenessProbe": {
                                    "httpGet": {
                                        "path": "/-/healthy",
                                        "port": 9090,
                                        "scheme": "HTTP",
                                    },
                                    "initialDelaySeconds": 30,
                                    "periodSeconds": 15,
                                    "timeoutSeconds": 10,
                                    "failureThreshold": 3,
                                    "successThreshold": 1,
                                },
                                "resources": {},
                                "volumeMounts": [
                                    {
                                        "name": "config-volume",
                                        "mountPath": "/etc/config",
                                    },
                                    {
                                        "name": "storage-volume",
                                        "mountPath": "/data",
                                        "subPath": "",
                                    },
                                ],
                            },
                        ],
                        "hostNetwork": False,
                        "dnsPolicy": "ClusterFirst",
                        "securityContext": {
                            "fsGroup": 65534,
                            "runAsGroup": 65534,
                            "runAsNonRoot": True,
                            "runAsUser": 65534,
                        },
                        "terminationGracePeriodSeconds": 300,
                        "volumes": [
                            {
                                "name": "config-volume",
                                "configMap": {"name": "jaseci-prometheus-server"},
                            },
                            {
                                "name": "storage-volume",
                                "persistentVolumeClaim": {
                                    "claimName": "jaseci-prometheus-server"
                                },
                            },
                        ],
                    },
                },
            },
        },
    ],
}
