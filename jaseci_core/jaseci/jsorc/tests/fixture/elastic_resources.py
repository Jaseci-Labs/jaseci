# List of kubernetes resources required by Elastic
ELASTIC_RESOURCES = {
    "Namespace": [],
    "CustomResourceDefinition": [
        "agents.agent.k8s.elastic.co",
        "apmservers.apm.k8s.elastic.co",
        "beats.beat.k8s.elastic.co",
        "elasticmapsservers.maps.k8s.elastic.co",
        "elasticsearchautoscalers.autoscaling.k8s.elastic.co",
        "elasticsearches.elasticsearch.k8s.elastic.co",
        "enterprisesearches.enterprisesearch.k8s.elastic.co",
        "kibanas.kibana.k8s.elastic.co",
        "stackconfigpolicies.stackconfigpolicy.k8s.elastic.co",
    ],
    "ServiceAccount": ["elastic-operator"],
    "Secret": ["elastic-webhook-server-cert"],
    "ConfigMap": ["elastic-operator"],
    "ClusterRole": [
        'elastic-operator-$j{ServiceAccount["elastic-operator"].metadata.namespace}',
        'elastic-operator-$j{ServiceAccount["elastic-operator"].metadata.namespace}-view',
        'elastic-operator-$j{ServiceAccount["elastic-operator"].metadata.namespace}-edit',
    ],
    "ClusterRoleBinding": [
        'elastic-operator-$j{ServiceAccount["elastic-operator"].metadata.namespace}'
    ],
    "Service": ["elastic-webhook-server"],
    "StatefulSet": ["elastic-operator"],
    "ValidatingWebhookConfiguration": ["elastic-webhook.k8s.elastic.co"],
    "Elasticsearch": ["jaseci"],
    "Kibana": ["jaseci"],
}
