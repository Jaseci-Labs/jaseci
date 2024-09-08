SUMMARIZATION_ACTION_CONFIG = {
    "module": "jac_nlp.summarization",
    "loaded_module": "jac_nlp.summarization.summarization",
    "local_mem_requirement": 2100,
    "remote": {
        "Service": {
            "kind": "Service",
            "apiVersion": "v1",
            "metadata": {"name": "bart-sum", "creationTimestamp": None},
            "spec": {
                "ports": [
                    {"name": "http", "protocol": "TCP", "port": 80, "targetPort": 80}
                ],
                "selector": {"pod": "bart-sum"},
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
                "name": "bart-sum-up",
                "creationTimestamp": None,
            },
            "data": {
                "prod_up": "uvicorn jac_nlp.summarization:serv_actions --host 0.0.0.0 --port 80"
            },
        },
        "Deployment": {
            "kind": "Deployment",
            "apiVersion": "apps/v1",
            "metadata": {"name": "bart-sum", "creationTimestamp": None},
            "spec": {
                "replicas": 1,
                "selector": {"matchLabels": {"pod": "bart-sum"}},
                "template": {
                    "metadata": {
                        "name": "bart-sum",
                        "creationTimestamp": None,
                        "labels": {"pod": "bart-sum"},
                    },
                    "spec": {
                        "volumes": [
                            {
                                "name": "prod-script",
                                "configMap": {
                                    "name": "bart-sum-up",
                                    "defaultMode": 420,
                                },
                            },
                            {
                                "name": "jac-nlp-volume",
                                "persistentVolumeClaim": {"claimName": "jac-nlp-pvc"},
                            },
                        ],
                        "containers": [
                            {
                                "name": "bart-sum",
                                "image": "jaseci/jac-nlp:1.4.0.18",
                                "command": ["bash", "-c", "source /script/prod_up"],
                                "ports": [{"containerPort": 80, "protocol": "TCP"}],
                                "resources": {
                                    "limits": {"memory": "3Gi"},
                                    "requests": {"memory": "3Gi"},
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
