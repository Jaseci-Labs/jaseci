---
side_bar_position: 5
---

# Starting Jaseci Services

We have put together a demo that you can run to verify that Jaseci works on your system. If for some reason this does not work we recommend that you recheck the previous installation steps for your Operating System.

## Before continuing

**Note**: Jaseci depends on Kubernetes to be up and running on your system. We assume that all the installation steps were successful. You can find a cheat sheet of Kubernetes resources here: <a href="/docs/resources/common">Kubernetes Cheat Sheet</a>.

### Steps to start Jaseci Services

1. Open the repo folder for Jaseci in a terminal
2. Stand up the Kubernetes pods by running the following command:
```
kubectl apply -f scripts/jaseci.yaml
```
3. After executing the above command, run the following command to check that the Jaseci Pods are running.
```
kubectl get pod
```
4. If it says “Creating Container” (or similar) wait a bit and run the run the command to check the status of the pods again. We want to make sure that the Pods are in a Ready/ Running state before continuing.
5. Next run the following command to run the Jaseci tests to verify that your installation works:
```
./scripts/script_sync_code_kube_test
```
Running the above demo script will run the Jaseci tests and output the results to your terminal. If the demo runs successfully you can move onto the next sections to start writing Jac code.

6. Port forward Jaseci pods for access to the API locally:
```
kubectl port-forward <jaseci pod name> 8888:80
```
This will forward the port 80 on the Jaseci pod to port 8888 on localhost. This allows you to access the API on:
```
http://localhost:8888
```
