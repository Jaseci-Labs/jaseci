POSTGRES_MANIFEST = {
    "Service": {
        "kind": "Service",
        "apiVersion": "v1",
        "metadata": {"name": "jaseci-db", "creationTimestamp": "None"},
        "spec": {
            "ports": [{"protocol": "TCP", "port": 5432, "targetPort": 5432}],
            "selector": {"pod": "jaseci-db"},
            "type": "ClusterIP",
            "sessionAffinity": "None",
            "internalTrafficPolicy": "Cluster",
        },
        "status": {"loadBalancer": {}},
    },
    "Secret": {
        "kind": "Secret",
        "apiVersion": "v1",
        "metadata": {"name": "jaseci-db-credentials", "creationTimestamp": "None"},
        "data": {"password": "bGlmZWxvZ2lmeWphc2VjaQ==", "user": "cG9zdGdyZXM="},
        "type": "Opaque",
    },
    "PersistentVolumeClaim": {
        "kind": "PersistentVolumeClaim",
        "apiVersion": "v1",
        "metadata": {"name": "jaseci-db-pvc", "creationTimestamp": "None"},
        "spec": {
            "accessModes": ["ReadWriteOnce"],
            "resources": {"requests": {"storage": "10Gi"}},
            "volumeMode": "Filesystem",
        },
        "status": {"phase": "Pending"},
    },
    "Deployment": {
        "kind": "Deployment",
        "apiVersion": "apps/v1",
        "metadata": {"name": "jaseci-db", "creationTimestamp": "None"},
        "spec": {
            "replicas": 1,
            "selector": {"matchLabels": {"pod": "jaseci-db"}},
            "template": {
                "metadata": {
                    "creationTimestamp": "None",
                    "labels": {"pod": "jaseci-db"},
                },
                "spec": {
                    "volumes": [
                        {
                            "name": "jaseci-db-volume",
                            "persistentVolumeClaim": {"claimName": "jaseci-db-pvc"},
                        }
                    ],
                    "containers": [
                        {
                            "name": "jaseci-db",
                            "image": "postgres:alpine",
                            "ports": [{"containerPort": 5432, "protocol": "TCP"}],
                            "env": [
                                {
                                    "name": "POSTGRES_USER",
                                    "valueFrom": {
                                        "secretKeyRef": {
                                            "name": "jaseci-db-credentials",
                                            "key": "user",
                                        }
                                    },
                                },
                                {
                                    "name": "POSTGRES_PASSWORD",
                                    "valueFrom": {
                                        "secretKeyRef": {
                                            "name": "jaseci-db-credentials",
                                            "key": "password",
                                        }
                                    },
                                },
                            ],
                            "resources": {},
                            "volumeMounts": [
                                {
                                    "name": "jaseci-db-volume",
                                    "mountPath": "/var/lib/postgresql/data",
                                    "subPath": "jaseci",
                                }
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
}
