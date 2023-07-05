DEMO_MOD_ACTION_CONFIG = {
    "module": "jac_nlp.demo_mod",
    "loaded_module": "jac_nlp.demo_mod.demo_mod",
    "local_mem_requirement": 100,
    "remote": {
        "Service": {
            "kind": "Service",
            "apiVersion": "v1",
            "metadata": {"name": "demo-mod", "creationTimestamp": None},
            "spec": {
                "ports": [
                    {"name": "http", "protocol": "TCP", "port": 80, "targetPort": 80}
                ],
                "selector": {"pod": "demo-mod"},
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
                "name": "demo-mod-up",
                "creationTimestamp": None,
            },
            "data": {
                "prod_up": "git clone -b action_policy https://github.com/Jaseci-Labs/jaseci.git; cd jaseci; cd jaseci_core; source install.sh; cd ../jaseci_ai_kit/jac_nlp; pip install -e .[demo_mod]; uvicorn jac_nlp.demo_mod:serv_actions --host 0.0.0.0 --port 80;"
                # "prod_up": "uvicorn jac_nlp.demo_mod:serv_actions --host 0.0.0.0 --port 80"
            },
        },
        "Deployment": {
            "kind": "Deployment",
            "apiVersion": "apps/v1",
            "metadata": {"name": "demo-mod", "creationTimestamp": None},
            "spec": {
                "replicas": 1,
                "selector": {"matchLabels": {"pod": "demo-mod"}},
                "template": {
                    "metadata": {
                        "name": "demo-mod",
                        "creationTimestamp": None,
                        "labels": {"pod": "demo-mod"},
                    },
                    "spec": {
                        "volumes": [
                            {
                                "name": "prod-script",
                                "configMap": {
                                    "name": "demo-mod-up",
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
                                "name": "demo-mod",
                                "image": "jaseci/jac-nlp:1.4.0.21",
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