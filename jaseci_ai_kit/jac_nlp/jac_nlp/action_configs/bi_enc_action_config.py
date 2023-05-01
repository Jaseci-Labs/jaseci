BI_ENC_ACTION_CONFIG = {
    "module": "jac_nlp.bi_enc",
    "loaded_module": "jac_nlp.bi_enc.bi_enc",
    "local_mem_requirement": 333.92,
    "remote": {
        "Service": {
            "kind": "Service",
            "apiVersion": "v1",
            "metadata": {"name": "bi-enc", "creationTimestamp": None},
            "spec": {
                "ports": [
                    {"name": "http", "protocol": "TCP", "port": 80, "targetPort": 80}
                ],
                "selector": {"pod": "bi-enc"},
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
                "name": "bi-enc-up",
                "creationTimestamp": None,
            },
            "data": {
                "prod_up": "uvicorn jac_nlp.bi_enc:serv_actions --host 0.0.0.0 --port 80"
            },
        },
        "Deployment": {
            "kind": "Deployment",
            "apiVersion": "apps/v1",
            "metadata": {"name": "bi-enc", "creationTimestamp": None},
            "spec": {
                "replicas": 1,
                "selector": {"matchLabels": {"pod": "bi-enc"}},
                "template": {
                    "metadata": {
                        "name": "bi-enc",
                        "creationTimestamp": None,
                        "labels": {"pod": "bi-enc"},
                    },
                    "spec": {
                        "volumes": [
                            {
                                "name": "prod-script",
                                "configMap": {"name": "bi-enc-up", "defaultMode": 420},
                            },
                            {
                                "name": "jac-nlp-volume",
                                "persistentVolumeClaim": {"claimName": "jac-nlp-pvc"},
                            },
                        ],
                        "containers": [
                            {
                                "name": "bi-enc",
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
