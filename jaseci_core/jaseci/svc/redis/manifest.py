REDIS_MANIFEST = {
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
