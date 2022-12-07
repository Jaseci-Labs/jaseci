FAST_ENC_ACTION_CONFIG = {
    "module": "jaseci_ai_kit.fast_enc",
    "loaded_module": "jaseci_ai_kit.modules.fast_enc.fast_enc",
    "remote": {
        "Service": {
            "kind": "Service",
            "apiVersion": "v1",
            "metadata": {"name": "fast-enc", "creationTimestamp": None},
            "spec": {
                "ports": [
                    {"name": "http", "protocol": "TCP", "port": 80, "targetPort": 80}
                ],
                "selector": {"pod": "fast-enc"},
                "type": "ClusterIP",
                "sessionAffinity": "None",
                "internalTrafficPolicy": "Cluster",
            },
            "status": {"loadBalancer": {}},
        },
        "ConfigMap": {
            "kind": "ConfigMap",
            "apiVersion": "v1",
            "metadata": {
                "name": "fast-enc-up",
                "creationTimestamp": None,
            },
            "data": {
                "prod_up": "uvicorn jaseci_ai_kit.fast_enc:serv_actions --host 0.0.0.0 --port 80"
            },
        },
        "Deployment": {
            "kind": "Deployment",
            "apiVersion": "apps/v1",
            "metadata": {"name": "fast-enc", "creationTimestamp": None},
            "spec": {
                "replicas": 1,
                "selector": {"matchLabels": {"pod": "fast-enc"}},
                "template": {
                    "metadata": {
                        "name": "fast-enc",
                        "creationTimestamp": None,
                        "labels": {"pod": "fast-enc"},
                    },
                    "spec": {
                        "volumes": [
                            {
                                "name": "prod-script",
                                "configMap": {
                                    "name": "fast-enc-up",
                                    "defaultMode": 420,
                                },
                            }
                        ],
                        "containers": [
                            {
                                "name": "fast-enc",
                                "image": "jaseci/jaseci-ai:1.3.6.3",
                                "command": ["bash", "-c", "source script/prod_up"],
                                "ports": [{"containerPort": 80, "protocol": "TCP"}],
                                "resources": {"requests": {"memory": "3Gi"}},
                                "volumeMounts": [
                                    {"name": "prod-script", "mountPath": "/script"}
                                ],
                                "terminationMessagePath": "/dev/termination-log",
                                "terminationMessagePolicy": "File",
                                "imagePullPolicy": "IfNotPresent",
                            }
                        ],
                        "restartPolicy": "Always",
                        "terminationGracePeriodSeconds": 30,
                        "dnsPolicy": "ClusterFirst",
                        "securityContext": {},
                        "schedulerName": "default-scheduler",
                    },
                },
                "strategy": {
                    "type": "RollingUpdate",
                    "rollingUpdate": {"maxUnavailable": "25%", "maxSurge": "25%"},
                },
                "revisionHistoryLimit": 10,
                "progressDeadlineSeconds": 600,
            },
            "status": {},
        },
    },
}
