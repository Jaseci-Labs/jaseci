TFM_NER_ACTION_CONFIG = {
    "module": "jac_nlp.tfm_ner",
    "loaded_module": "jac_nlp.tfm_ner.tfm_ner",
    "local_mem_requirement": 1014.12,
    "remote": {
        "Service": {
            "kind": "Service",
            "apiVersion": "v1",
            "metadata": {"name": "tfm-ner", "creationTimestamp": None},
            "spec": {
                "ports": [
                    {"name": "http", "protocol": "TCP", "port": 80, "targetPort": 80}
                ],
                "selector": {"pod": "tfm-ner"},
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
                "name": "tfm-ner-up",
                "creationTimestamp": None,
            },
            "data": {
                "prod_up": "uvicorn jac_nlp.tfm_ner:serv_actions --host 0.0.0.0 --port 80"
            },
        },
        "Deployment": {
            "kind": "Deployment",
            "apiVersion": "apps/v1",
            "metadata": {"name": "tfm-ner", "creationTimestamp": None},
            "spec": {
                "replicas": 1,
                "selector": {"matchLabels": {"pod": "tfm-ner"}},
                "template": {
                    "metadata": {
                        "name": "tfm-ner",
                        "creationTimestamp": None,
                        "labels": {"pod": "tfm-ner"},
                    },
                    "spec": {
                        "volumes": [
                            {
                                "name": "prod-script",
                                "configMap": {"name": "tfm-ner-up", "defaultMode": 420},
                            },
                            {
                                "name": "jac-nlp-volume",
                                "persistentVolumeClaim": {"claimName": "jac-nlp-pvc"},
                            },
                        ],
                        "containers": [
                            {
                                "name": "tfm-ner",
                                "image": "jaseci/jac-nlp:1.4.0.18",
                                "command": ["bash", "-c", "source /script/prod_up"],
                                "ports": [{"containerPort": 80, "protocol": "TCP"}],
                                "resources": {
                                    "limits": {"memory": "2Gi"},
                                    "requests": {"memory": "2Gi"},
                                },
                                "volumeMounts": [
                                    {"name": "prod-script", "mountPath": "/script"},
                                    {
                                        "name": "jac-nlp-volume",
                                        "mountPath": "/root/.jaseci/models/",
                                    },
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
