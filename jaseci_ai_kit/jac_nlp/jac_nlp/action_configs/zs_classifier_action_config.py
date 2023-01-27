ZS_CLASSIFIER_ACTION_CONFIG = {
    "module": "jac_nlp.zs_classifier",
    "loaded_module": "jac_nlp.zs_classifier.zs_classifier",
    "remote": {
        "Service": {
            "kind": "Service",
            "apiVersion": "v1",
            "metadata": {"name": "zs-classifier", "creationTimestamp": None},
            "spec": {
                "ports": [
                    {"name": "http", "protocol": "TCP", "port": 80, "targetPort": 80}
                ],
                "selector": {"pod": "zs-classifier"},
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
                "name": "zs-classifier-up",
                "creationTimestamp": None,
            },
            "data": {
                "prod_up": "uvicorn jac_nlp.zs_classifier:serv_actions --host 0.0.0.0 --port 80"
            },
        },
        "Deployment": {
            "kind": "Deployment",
            "apiVersion": "apps/v1",
            "metadata": {"name": "zs-classifier", "creationTimestamp": None},
            "spec": {
                "replicas": 1,
                "selector": {"matchLabels": {"pod": "zs-classifier"}},
                "template": {
                    "metadata": {
                        "name": "zs-classifier",
                        "creationTimestamp": None,
                        "labels": {"pod": "zs-classifier"},
                    },
                    "spec": {
                        "volumes": [
                            {
                                "name": "prod-script",
                                "configMap": {
                                    "name": "zs-classifier-up",
                                    "defaultMode": 420,
                                },
                            }
                        ],
                        "containers": [
                            {
                                "name": "zs-classifier",
                                "image": "jaseci/jac-nlp:1.4.0.6",
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
