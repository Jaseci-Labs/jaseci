CL_SUMMER_ACTION_CONFIG = {
    "module": "jaseci_ai_kit.cl_summer",
    "loaded_module": "jaseci_ai_kit.modules.cl_summer.cl_summer",
    "remote": {
        "Service": {
            "kind": "Service",
            "apiVersion": "v1",
            "metadata": {"name": "cl-summer", "creationTimestamp": None},
            "spec": {
                "ports": [
                    {"name": "http", "protocol": "TCP", "port": 80, "targetPort": 80}
                ],
                "selector": {"pod": "cl-summer"},
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
                "name": "cl-summer-up",
                "creationTimestamp": None,
            },
            "data": {
                "prod_up": "uvicorn jaseci_ai_kit.cl_summer:serv_actions --host 0.0.0.0 --port 80"
            },
        },
        "Deployment": {
            "kind": "Deployment",
            "apiVersion": "apps/v1",
            "metadata": {"name": "cl-summer", "creationTimestamp": None},
            "spec": {
                "replicas": 1,
                "selector": {"matchLabels": {"pod": "cl-summer"}},
                "template": {
                    "metadata": {
                        "name": "cl-summer",
                        "creationTimestamp": None,
                        "labels": {"pod": "cl-summer"},
                    },
                    "spec": {
                        "volumes": [
                            {
                                "name": "prod-script",
                                "configMap": {
                                    "name": "cl-summer-up",
                                    "defaultMode": 420,
                                },
                            }
                        ],
                        "containers": [
                            {
                                "name": "cl-summer",
                                "image": "jaseci/jaseci-ai:1.3.6.3",
                                "command": ["bash", "-c", "source script/prod_up"],
                                "ports": [{"containerPort": 80, "protocol": "TCP"}],
                                "resources": {
                                    "limits": {"memory": "2Gi"},
                                    "requests": {"memory": "2Gi"},
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
