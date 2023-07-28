BI_NER_ACTION_CONFIG = {
    "module": "jac_nlp.bi_ner",
    "loaded_module": "jac_nlp.bi_ner.bi_ner",
    "remote": {
        "Service": {
            "kind": "Service",
            "apiVersion": "v1",
            "metadata": {"name": "bi-ner", "creationTimestamp": None},
            "spec": {
                "ports": [
                    {"name": "http", "protocol": "TCP", "port": 80, "targetPort": 80}
                ],
                "selector": {"pod": "bi-ner"},
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
                "name": "bi-ner-up",
                "creationTimestamp": None,
            },
            "data": {
                "prod_up": "uvicorn jac_nlp.bi_ner:serv_actions --host 0.0.0.0 --port 80"
            },
        },
        "Deployment": {
            "kind": "Deployment",
            "apiVersion": "apps/v1",
            "metadata": {"name": "bi-ner", "creationTimestamp": None},
            "spec": {
                "replicas": 1,
                "selector": {"matchLabels": {"pod": "bi-ner"}},
                "template": {
                    "metadata": {
                        "name": "bi-ner",
                        "creationTimestamp": None,
                        "labels": {"pod": "bi-ner"},
                    },
                    "spec": {
                        "volumes": [
                            {
                                "name": "prod-script",
                                "configMap": {"name": "bi-ner-up", "defaultMode": 420},
                            }
                        ],
                        "containers": [
                            {
                                "name": "bi-ner",
                                "image": "jaseci/jac-nlp:latest",
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
