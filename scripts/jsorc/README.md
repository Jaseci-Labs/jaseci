## JSORC Infrasturcture
This folder contains the many files related to the JSORC infrastructure.

### Run JSORC tests
There are two categories of JSORC tests. One that requires Kuberenetes environment and one that doesn't.

#### Non-kubernetes Tests
These tests operate just like any other tests in `jaseci_serv`. A full `pytest` run will include these tests.

#### Kuberentes-dependent Tests
These tests require the test process to be in a kuberentes cluster environment.
To run these tests, use `jsorc_test.yaml`. Here are the steps:

1. We need to first mount the source code and test into the kubernetes pods. `jsorc_test.yaml` already has the neccessary configuration to do that in `wsl`. Run the following to set up the volume mount in `wsl`
```bash
mkdir /mnt/wsl/jaseci
sudo mount --bind PATH_TO_YOUR_JASECI_REPO /mnt/wsl/jaseci
```

Note that these commands need to be run every time `wsl` restartes.

2.  If you on a native linux environment instead of `wsl`, update the following block in `jsorc_test.yaml` with the path to your jaseci repo.
```yaml
- name: host-mount
  hostPath:
    path: /run/desktop/mnt/host/wsl/jaseci
    type: Directory
```

3. Apply the yaml to deploy the test container.
```bash
kubectl apply -f jsorc_test.yaml
```
This will launch a pod that will execute all the tests in the `JsorcAPIKubeTest` test suite and exit after completion.
Check the pod logs for the test results.

### TODO

- [ ] Automate this in a github action workflow