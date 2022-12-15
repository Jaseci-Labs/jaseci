USE_QA_ACTION_CONFIG = {
    "module": "jaseci_ai_kit.use_qa",
    "loaded_module": "jaseci_ai_kit.modules.use_qa.use_qa",
    "remote": {
        "Service": {
            "kind": "Service",
            "apiVersion": "v1",
            "metadata": {"name": "use-qa", "creationTimestamp": None},
            "spec": {
                "ports": [
                    {"name": "http", "protocol": "TCP", "port": 80, "targetPort": 80}
                ],
                "selector": {"pod": "use-qa"},
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
                "name": "use-qa-up",
                "creationTimestamp": None,
            },
            "data": {
                "prod_up": "uvicorn jaseci_ai_kit.use_qa:serv_actions --host 0.0.0.0 --port 80"
            },
        },
        "Deployment": {
            "kind": "Deployment",
            "apiVersion": "apps/v1",
            "metadata": {"name": "use-qa", "creationTimestamp": None},
            "spec": {
                "replicas": 1,
                "selector": {"matchLabels": {"pod": "use-qa"}},
                "template": {
                    "metadata": {
                        "name": "use-qa",
                        "creationTimestamp": None,
                        "labels": {"pod": "use-qa"},
                    },
                    "spec": {
                        "volumes": [
                            {
                                "name": "prod-script",
                                "configMap": {
                                    "name": "use-qa-up",
                                    "defaultMode": 420,
                                },
                            }
                        ],
                        "containers": [
                            {
                                "name": "use-qa",
                                "image": "jaseci/jaseci-ai:1.3.6.3",
                                "command": ["bash", "-c", "source script/prod_up"],
                                "ports": [{"containerPort": 80, "protocol": "TCP"}],
                                "resources": {
                                    "limits": {"memory": "3Gi"},
                                    "requests": {"memory": "3Gi"},
                                },
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
