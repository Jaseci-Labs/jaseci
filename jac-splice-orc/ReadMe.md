# JAC Cloud Orchestrator

![Docker Pulls](https://img.shields.io/docker/pulls/ashishmahendra/jac-splice-orc)

JAC Cloud Orchestrator (`jac-splice-orc`) is a system designed to dynamically import any Python module, deploy it as a Kubernetes Pod, and expose it as an independent gRPC service. This enables any Python module to be used as a microservice, providing flexibility and scalability in a cloud environment.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [1. Deploy the Pod Manager](#1-deploy-the-pod-manager)
  - [2. Access the Pod Manager](#2-access-the-pod-manager)
  - [3. Dynamic Pod Creation](#3-dynamic-pod-creation)
- [Usage](#usage)
  - [Client Application](#client-application)
  - [Example Usage](#example-usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Imagine having the ability to use any Python module as a remote service, seamlessly integrating it into your application without worrying about the underlying infrastructure. JAC Cloud Orchestrator allows you to dynamically deploy Python modules as microservices in a Kubernetes environment, exposing them via gRPC for remote execution.

This system abstracts away the complexities of remote execution, pod management, and inter-service communication, enabling developers to focus on building applications rather than managing infrastructure.

---

## Features

- **Dynamic Module Deployment**: Import and deploy any Python module as a Kubernetes Pod on-demand.
- **gRPC Service Exposure**: Expose modules as gRPC services for efficient remote procedure calls.
- **Transparent Remote Execution**: Use remote modules as if they were local, with automatic handling of data serialization and deserialization.
- **Pod Management**: Automatically create, manage, and terminate pods based on usage.
- **Scalability**: Scale services horizontally by deploying multiple instances.
- **Resource Optimization**: Allocate resources dynamically, ensuring optimal utilization.

---

## Architecture

![Architecture Diagram](jac_splice_orc/assets/Splice-Orc-2.png)


### **System Components**

1. **Client Application**
   - The interface through which users interact with remote modules.
   - Handles serialization and deserialization of data.
   - Provides proxy objects to interact with remote modules seamlessly.

2. **Pod Manager**
   - Manages Kubernetes pods and services for modules.
   - Receives requests from the client and ensures the appropriate pods are running.
   - Forwards method execution requests to the corresponding pods.

3. **Module Server (Pod)**
   - Runs the requested Python module within a Kubernetes pod.
   - Exposes the module's functionalities via a gRPC server.
   - Executes methods and returns results to the Pod Manager.

### **Data Flow**

1. **Client Requests**: The client makes a request to use a module's method.
2. **Pod Manager Processing**: The Pod Manager checks if the module's pod is running; if not, it creates it.
3. **Method Execution**: The Pod Manager forwards the request to the module's pod.
4. **Result Retrieval**: The module pod executes the method and returns the result.
5. **Client Receives Result**: The client receives and deserializes the result, making it available for use.

---

## Project Structure

```
jac-splice-orc/
│
├── jac_splice_orc/
│   ├── Dockerfile                         # Dockerfile for building the containerized service
│   ├── __init__.py                        # Package initializer
│   ├── grpc_local/
│   │   ├── __init__.py
│   │   └── module_service.proto           # Protocol Buffers definition
│   ├── managers/
│   │   ├── __init__.py
│   │   ├── deploy.py                      # Deployment script for the Pod Manager
│   │   ├── pod_manager.py                 # Pod manager to handle pod operations
│   │   ├── pod_manager_deployment.yml     # Kubernetes deployment file for the pod manager
│   │   └── proxy_manager.py               # Proxy manager for handling client-side proxying
│   ├── plugin/
│   │   ├── __init__.py
│   │   └── splice_plugin.py               # Plugin for integration with jaclang
│   ├── server/
│   │   ├── __init__.py
│   │   └── server.py                      # gRPC server to serve the imported module as a service
│   ├── test/
│   │   ├── __init__.py
│   │   └── test_pod_manager.py            # Tests
│   └── utils/
│       ├── __init__.py
│       └── startup.sh                     # Startup script for initializing the server
├── requirements.txt                       # Python dependencies
└── README.md                              # Project documentation
```

---

## Setup

### Prerequisites

- **Docker** (version 20.10 or later): [Install Docker](https://docs.docker.com/get-docker/)
- **Kubernetes** (version 1.21 or later): [Install Kubernetes](https://kubernetes.io/docs/setup/)
- **Helm** (version 3.0 or later): [Install Helm](https://helm.sh/docs/intro/install/)
- **Nginx Ingress Controller**: [Set up Nginx Ingress](https://kubernetes.github.io/ingress-nginx/deploy/)
- **Python** (version 3.9 or later): [Install Python](https://www.python.org/downloads/)
- **kubectl** command-line tool: [Install kubectl](https://kubernetes.io/docs/tasks/tools/)

Ensure all prerequisites are correctly installed and configured before proceeding.

### 1. Deploy the Pod Manager

The Pod Manager is responsible for handling pod operations such as creation, scaling, and deletion.

You can deploy the Pod Manager using the `deploy.py` script provided in the `managers` directory.

**Usage:**

```bash
python managers/deploy.py
```

This script will handle the deployment of the Pod Manager to your Kubernetes cluster.

Ensure the Pod Manager service is up and running:

```bash
kubectl get pods
```

### 2. Access the Pod Manager

Once the Pod Manager is deployed, you can access it via the exposed Nginx Ingress. Ensure your Ingress Controller is running correctly.

Update your DNS or `/etc/hosts` file to point to the ingress IP if necessary.

### 3. Dynamic Pod Creation

You can dynamically create and manage pods by sending requests to the Pod Manager. The Pod Manager will deploy the specified module as an independent service.

---

## Usage

### Client Application

The client application provides a seamless way to interact with remote modules as if they were local. It handles the complexities of remote communication, serialization, and deserialization.

#### **Client Components**

- **PodManagerProxy**: Communicates with the Pod Manager to create pods and run modules.
- **ModuleProxy**: Provides proxy objects for modules.
- **RemoteObjectProxy**: Acts as a dynamic proxy for method calls on remote modules or objects.

### Example Usage

Below is an example of how to use the system to perform remote method calls on a module, specifically using `numpy`:

```jac
with entry{
    import:py numpy;
    arr = numpy.array([1, 2, 3, 4]);
    print(arr);
    result = numpy.sum(arr);  # Remote method call
    print(result);
}
```

**Explanation:**

- **Initialization**: The `ModuleProxy` initializes communication with the Pod Manager.
- **Module Configuration**: Specify any dependencies or resource requirements.
- **Getting Module Proxy**: `get_module_proxy` creates the pod for the module and returns a proxy object.
- **Using Remote Module**: Use the proxy object (`numpy` in this case) to call methods as if they were local.

---

## Configuration

### Environment Variables

- `POD_MANAGER_URL`: URL of the Pod Manager service.
- `MODULE_NAME`: Name of the Python module to deploy.
- `PORT`: Port on which the gRPC server will run (default is `50051`).
- `NAMESPACE`: Kubernetes namespace to deploy pods (default is `default`).

### Module Configuration

When creating a module proxy, you can specify configuration options:

- `dependency`: List of additional Python packages required by the module.
- `lib_cpu_req`: CPU resource request for the pod (e.g., `"500m"`).
- `lib_mem_size_req`: Memory resource request for the pod (e.g., `"512Mi"`).

```python
module_config = {
    "dependency": ["scipy==1.7.1"],  # Example dependency
    "lib_cpu_req": "500m",
    "lib_mem_size_req": "512Mi",
}
```
---

## **Flow Diagram**

![Flow Diagram](jac_splice_orc/assets/Splice-Orc.png)

---


