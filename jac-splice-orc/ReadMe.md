# JAC Cloud Orchestrator

[![Docker Pulls](https://img.shields.io/docker/pulls/ashishmahendra/jac-cloud-orc)](https://hub.docker.com/r/your-docker-username/jac-cloud-orc)

JAC Cloud Orchestrator (`jac-cloud-orc`) is a system designed to dynamically import any Python module, deploy it as a Kubernetes Pod, and expose it as an independent gRPC service. This enables any Python module to be used as a microservice, providing flexibility and scalability in a cloud environment.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [1. Deploy the Pod Manager](#2-deploy-the-pod-manager)
  - [2. Access the Pod Manager](#3-access-the-pod-manager)
  - [3. Dynamic Pod Creation](#5-dynamic-pod-creation)
- [Usage](#usage)
  - [Example API Call to Create a Pod](#example-api-call-to-create-a-pod)
  - [Example API Call to Run a Module's Method](#example-api-call-to-run-a-modules-method)

## Features

- **Dynamic Module Deployment**: Import any Python module and deploy it as a Kubernetes Pod.
- **gRPC Service Exposure**: Expose modules as gRPC services for remote execution.
- **Pod Management**: Create, manage, and terminate pods dynamically.
- **Ingress Routing**: Utilize Nginx Ingress Controller for routing and service exposure.
- **Scalability**: Scale services horizontally by deploying multiple instances.

## Project Structure

```
jac-cloud-orc/
│
├── grpc_local/                         # gRPC protobuf files for communication
│   ├── module_service.proto            # Protocol Buffers definition
│   ├── module_service_pb2.py           # Generated Python classes
│   └── module_service_pb2_grpc.py      # Generated gRPC service stubs
│
├── managers/                           # Managers for handling pods and proxying
│   ├── pod_manager.py                  # Pod manager to handle pod operations
│   ├── proxy_manager.py                # Proxy manager for handling proxy-related tasks
│   └── pod_manager_deployment.yml      # Kubernetes deployment file for the pod manager
│
├── server/                             # The main server code to serve module gRPC services
│   └── server.py                       # gRPC server to serve the imported module as a service
│
├── utils/                              # Utility code for additional helper functionality
│   ├── __init__.py                     # Makes utils a Python package
│   └── startup.sh                      # Startup script for initializing the server
│
├── Dockerfile                          # Dockerfile for building the containerized service
├── requirements.txt                    # Python dependencies
├── LICENSE                             # Project license
└── README.md                           # Project documentation
```

## Setup

### Prerequisites

- **Docker** (version 20.10 or later): [Install Docker](https://docs.docker.com/get-docker/)
- **Kubernetes** (version 1.21 or later): [Install Kubernetes](https://kubernetes.io/docs/setup/)
- **Helm** (version 3.0 or later): [Install Helm](https://helm.sh/docs/intro/install/)
- **Nginx Ingress Controller**: [Set up Nginx Ingress](https://kubernetes.github.io/ingress-nginx/deploy/)
- **Python** (version 3.12 or later): [Install Python](https://www.python.org/downloads/)

Ensure all prerequisites are correctly installed and configured before proceeding.


### 1. Deploy the Pod Manager

The Pod Manager is responsible for handling pod operations such as creation, scaling, and deletion.

Deploy the Pod Manager to Kubernetes using the provided YAML file:

```bash
kubectl apply -f managers/pod_manager_deployment.yml
```

Ensure the Pod Manager service is up and running:

```bash
kubectl get pods
```

### 2. Access the Pod Manager

Once the Pod Manager is deployed, you can access it via the exposed Nginx Ingress. Ensure your Ingress Controller is running correctly.

Update your DNS or `/etc/hosts` file to point to the ingress IP if necessary.

### 3. Dynamic Pod Creation

You can dynamically create and manage pods by sending requests to the Pod Manager. The Pod Manager will deploy the specified module as an independent service.

## Usage

### Example API Call to Create a Pod

```bash
POST http://pod-manager.your-domain.com/create_pod/<module_name>
```

- Replace `pod-manager.your-domain.com` with your actual Pod Manager URL.
- Replace `<module_name>` with the name of the module you want to deploy.

### Example API Call to Run a Module's Method

```bash
POST http://pod-manager.your-domain.com/run_module
```

**Query Parameters**:

- `module_name`: Name of the module (e.g., `numpy`)
- `method_name`: Name of the method to invoke (e.g., `array`)

**Request Body**:

```json
{
    "args": [16, 20, 24],
    "kwargs": {}
}
```

**Example using `curl`**:

```bash
curl -X POST \
  'http://pod-manager.your-domain.com/run_module?module_name=numpy&method_name=array' \
  -H 'Content-Type: application/json' \
  -d '{"args": [16, 20, 24], "kwargs": {}}'
```

**Sample Response**:

```json
{
    "result": [16, 20, 24],
}
```

## Configuration

The following environment variables can be set:

- `MODULE_NAME`: Name of the Python module to deploy.
- `PORT`: Port on which the gRPC server will run (default is `50051`).
- `POD_MANAGER_URL`: URL of the Pod Manager service.

