## Usage Documentation for jac-cloud Deployment

### Overview
The `jac-cloud` deployment provides a Kubernetes-based system for running JAC applications using the `jac-splice-orc` plugin. This setup includes:
1. A Docker image with necessary dependencies.
2. A Kubernetes configuration for creating required resources like namespaces, service accounts, roles, and bindings.
3. Dynamic configuration through environment variables and ConfigMaps.

---

### Prerequisites
1. **Kubernetes Cluster**: Ensure you have access to a Kubernetes cluster.
2. **kubectl**: Install the Kubernetes command-line tool.
3. **Docker**: Build and push the `jac-cloud` Docker image if necessary.
4. **Namespace**: The target namespace should be created before deploying resources.
5. **OpenAI API Key**: Add your OpenAI API key in base64 format for secret management.

---

### Directory Structure
```
jac-cloud/
├── scripts/
│   ├── Dockerfile
│   ├── init_jac_cloud.sh
│   ├── jac-cloud.yml
│   ├── module-config.yml
```

---

### Step-by-Step Guide

#### 1. Build and Push the Docker Image
Build the `jac-cloud` Docker image using the `Dockerfile` in the `scripts` directory.

```bash
docker build -t your-dockerhub-username/jac-cloud:latest -f jac-cloud/scripts/Dockerfile .
docker push your-dockerhub-username/jac-cloud:latest
```

Update the `image` field in `jac-cloud.yml` with your Docker image path.

---
#### 2. Apply the ConfigMap for Dynamic Configuration
Apply the `module-config.yml` file to configure module-specific settings:

```bash
kubectl apply -f jac-cloud/scripts/module-config.yml
```
This will:
- Create the `littlex` namespace.

---

#### 3. Apply Namespace and Resources
Run the following command to  apply the Kubernetes resources:

```bash
kubectl apply -f jac-cloud/scripts/jac-cloud.yml
```

This will:
- Set up RBAC roles and bindings.
- Deploy the `jac-cloud` application in the `littlex` namespace.

---

#### 4. Add the OpenAI API Key (Optional)
Replace `your-openai-key` with your actual API key, encode it in base64, and create the secret:

```bash
echo -n "your-openai-key" | base64
```

Replace the base64 value in the `data.openai-key` field of the secret definition in `jac-cloud.yml`, and then apply it:

```bash
kubectl apply -f jac-cloud/scripts/jac-cloud.yml
```

---

#### 5. Verify Deployment
Ensure that all resources are created successfully:

```bash
kubectl get all -n littlex
```

You should see the `jac-cloud` pod running along with associated resources.

---

### Configuration Details

#### 1. Environment Variables
| Variable          | Description                              | Default Value |
|--------------------|------------------------------------------|---------------|
| `NAMESPACE`        | Target namespace for the deployment.    | `default`     |
| `CONFIGMAP_NAME`   | Name of the ConfigMap to mount.          | `module-config` |
| `FILE_NAME`        | JAC file to execute in the pod.          | `example.jac` |
| `OPENAI_API_KEY`   | OpenAI API key (retrieved from secret).  | None          |

---

#### 2. ConfigMap (`module-config.yml`)
Defines configuration for dynamically loaded modules:

```json
{
  "numpy": {
    "lib_mem_size_req": "100Mi",
    "dependency": [],
    "lib_cpu_req": "500m",
    "load_type": "remote"
  },
  "transformers": {
    "lib_mem_size_req": "2000Mi",
    "dependency": ["torch", "transformers"],
    "lib_cpu_req": "1.0",
    "load_type": "remote"
  },
  "sentence_transformers": {
    "lib_mem_size_req": "2000Mi",
    "dependency": ["sentence-transformers"],
    "lib_cpu_req": "1.0",
    "load_type": "remote"
  }
}
```

---

### Validation and Troubleshooting

#### Verify Namespace
Ensure the `littlex` namespace exists:
```bash
kubectl get namespaces
```

#### Verify ConfigMap
Check if the `module-config` ConfigMap is applied:
```bash
kubectl get configmap -n littlex
```

#### Verify Deployment
Ensure the `jac-cloud` pod is running:
```bash
kubectl get pods -n littlex
```

---

### Advanced Usage

#### Redeploying with Updated Configurations
To update the ConfigMap or deployment:
1. Modify the respective YAML file.
2. Apply the changes:
   ```bash
    kubectl apply -f jac-cloud/scripts/module-config.yml
    kubectl apply -f jac-cloud/scripts/jac-cloud.yml
   ```

#### Access Logs
Monitor the logs of the `jac-cloud` pod:
```bash
kubectl logs -f deployment/jac-cloud -n littlex
```

#### Scale the Deployment
To scale the `jac-cloud` deployment:
```bash
kubectl scale deployment jac-cloud --replicas=3 -n littlex
```

---

### Cleanup
To remove all resources:
```bash
kubectl delete namespace littlex
```
