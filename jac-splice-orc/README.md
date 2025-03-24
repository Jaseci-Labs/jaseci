# JAC Orchestrator (`jac-splice-orc`)

JAC Orchestrator (`jac-splice-orc`) is a system designed to dynamically import any Python module and deploy supported services (Jac-Cloud, MongoDB, Redis) on demand.

Supported services will have their respective yaml templates the can be overriden. It will spawn pods that's accesible to the whole cluster via FQDN.

Pytho module will be deployed as a Kubernetes Pod, and expose it as an independent gRPC service. This enables any Python module to be used as a microservice, providing flexibility and scalability in a cloud environment.

## Overview

Imagine having the ability to use any Python module as a remote service, seamlessly integrating it into your application without worrying about the underlying infrastructure. JAC Orchestrator allows you to dynamically deploy Python modules as microservices in a Kubernetes environment, exposing them via gRPC for remote execution.

On top of that, Jac Orchestrator also support automatic build up of supported services in just one API call.

This system abstracts away the complexities of remote execution, pod management, and inter-service communication, enabling developers to focus on building applications rather than managing infrastructure.

---

## Setup

### Prerequisites

Before you begin, ensure that you have the following installed and configured:

- **Kubernetes** (version 1.21 or later)
- **kubectl** command-line tool
- **Kubernetes Cluster**: Ensure you have access to a Kubernetes cluster (local or remote).

### Create Namespace
> kubectl create namespace your_namespace

### Complete [jac-orc.yaml](./jac_splice_orc/manifests/jac-orc.yaml) or [jac-orc-cluster-wide.yaml](./jac_splice_orc/manifests/jac-orc-cluster-wide.yaml)
- Uncomment and update ClusterRoleBinding's `subjects[0].namespace` to your_namespace
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: jac-orc
roleRef:
  kind: ClusterRole
  name: jac-orc
  apiGroup: rbac.authorization.k8s.io
subjects:
  - kind: ServiceAccount
    name: jac-orc
    # namespace: your_namespace
---

apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: jac-reloader
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: jac-reloader
subjects:
  - kind: ServiceAccount
    name: jac-reloader
    # namespace: littlex
```
- Update Secret's `stringData.MODULE` to include default modules. This should be JSON string and with the following format:
```python
# valid format
{
    # namespace
        "default": {

          # supported values: mongodb | redis | jac-cloud
          "redis": {

            # name of the service/library
            "testing-redis": {

                # deployment json
                "module": "redis",
                "version": "latest",
                "config": {
                  ...
                }
            }
        }
    }
    ...
}
```
### Apply [jac-orc.yaml](./jac_splice_orc/manifests/jac-orc.yaml) or [jac-orc-cluster-wide.yaml](./jac_splice_orc/manifests/jac-orc-cluster-wide.yaml)

> kubectl apply -f jac_splice_orc/manifests/jac-orc.yaml --namespace your_namespace

- This will spawn jac-orc pod and spawn default modules if specified
```log
INFO:     Started server process [987]
INFO:     Waiting for application startup.
2025-03-14 19:41:05,150 INFO Extracting redis namespaces...
2025-03-14 19:41:05,151 INFO Extracting default services/libraries...
2025-03-14 19:41:05,151 INFO Deploying testing-redis with {"name":"testing-redis","namespace":"default"}...
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## Add additional Service / Python Library
### Prerequisites

Make sure jac-orc service is accessible

### Dry Run
- This is to view manifests the will be applied on actual deployment. This also includes placeholders that you have overriden and their defaults.
##### **`REQUEST`**
> **POST** */deployment/dry_run*
```json
{
    "module": "mongodb",
    "config": {
        "name": "testing-db",
        "namespace": "testing"
    }
}
```
##### **`RESPONSE`**
```json
{
  "placeholders": {
    "password": {
      "default": "12345678",
      "current": "12345678"
    },
    "replicaset": {
      "default": 3,
      "current": 3
    },
    "username": {
      "default": "my-user",
      "current": "my-user"
    },
    "namespace": {
      "default": "default",
      "current": "testing"
    },
    "name": {
      "default": "jac-mongodb",
      "current": "testing-db"
    },
    "database": {
      "default": "jaseci",
      "current": "jaseci"
    }
  },
  "dependencies": {
    "custom_resource_definition.yaml": "{{raw custom_resource_definition.yaml with parsed placeholders}}",
    "operator.yaml": "{{raw operator.yaml with parsed placeholders}}"
  },
  "modules": {
    "mongodb.yaml": "{{raw mongodb.yaml with parsed placeholders}}"
  }
}
```

### Deploy
- Deploy target module with their config based on supported placeholders (see [dry_run](#dry-run) api).
##### **`REQUEST`**
> **POST** */deployment*
```json
{
    "module": "mongodb",
    "version": "latest",
    "config": {
        "name": "testing-db",
        "namespace": "testing"
    }
}
```
##### **`RESPONSE`**
```json
{
  "results": [
    "customresourcedefinition.apiextensions.k8s.io/mongodbcommunity.mongodbcommunity.mongodb.com created",
    "namespace/jac-orc created",
    "serviceaccount/jac-orc-mongodb-operator created",
    "clusterrole.rbac.authorization.k8s.io/jac-orc-mongodb-operator created",
    "clusterrolebinding.rbac.authorization.k8s.io/jac-orc-mongodb-operator created",
    "deployment.apps/jac-orc-mongodb-operator created",
    "namespace/testing created",
    "role.rbac.authorization.k8s.io/mongodb-database created",
    "rolebinding.rbac.authorization.k8s.io/mongodb-database created",
    "serviceaccount/mongodb-database created",
    "role.rbac.authorization.k8s.io/jac-orc-mongodb-operator created",
    "rolebinding.rbac.authorization.k8s.io/jac-orc-mongodb-operator created",
    "serviceaccount/jac-orc-mongodb-operator created",
    "mongodbcommunity.mongodbcommunity.mongodb.com/testing-db created",
    "secret/my-user-password created"
  ],
  "errors": []
}
```