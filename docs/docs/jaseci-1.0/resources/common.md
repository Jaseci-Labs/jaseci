---
sidebar_position: 1
---

# Common

## Interacting with Kubernetes

### Common Jaseci Kubernetes commands

**Start pods**

```
kubectl apply -f scripts/jaseci.yml
```

**Stop Jaseci Kubernetes**
```
kubectl delete -f scripts/jaseci.yaml
```

**Delete and remove all kubernetes resources**
```
kubectl delete daemonsets,replicasets,services,deployments,pods,rc --all
```

**Port forward from running pod**
```
kubectl port-forward REPLACE_WITH_NAME_OF_POD 8888:80
```

**See all running pods**
```
kubectl get pod
```
