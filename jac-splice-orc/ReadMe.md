Certainly! I'll update the README to make it more accurate based on the recent changes we've made, such as moving configurations to a `config.json` file and updating the code structure. Here's the revised README:

---

# JAC Cloud Orchestrator (`jac-splice-orc`)

![Docker Pulls](https://img.shields.io/docker/pulls/ashishmahendra/jac-splice-orc)

JAC Cloud Orchestrator (`jac-splice-orc`) is a system designed to dynamically import any Python module, deploy it as a Kubernetes Pod, and expose it as an independent gRPC service. This enables any Python module to be used as a microservice, providing flexibility and scalability in a cloud environment.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
  - [System Components](#system-components)
  - [Data Flow](#data-flow)
- [Project Structure](#project-structure)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [1. Install Dependencies](#1-install-dependencies)
  - [2. Configure the System](#2-configure-the-system)
  - [3. Initialize the System](#3-initialize-the-system)
- [Usage](#usage)
  - [Client Application](#client-application)
  - [Example Usage](#example-usage)
- [Configuration](#configuration)
  - [Environment Variables](#environment-variables)
  - [Module Configuration](#module-configuration)
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

### System Components

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

### Data Flow

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
│   ├── __init__.py
│   ├── config/
│   │   └── config.json                  # Main configuration file
│   ├── config_loader.py                 # Configuration loader utility
│   ├── grpc_local/
│   │   ├── __init__.py
│   │   └── module_service.proto         # Protocol Buffers definition
│   ├── managers/
│   │   ├── __init__.py
│   │   ├── pod_manager.py               # Pod Manager to handle pod operations
│   │   ├── proxy_manager.py             # Proxy Manager for handling client-side proxying
│   ├── plugin/
│   │   ├── __init__.py
│   │   └── splice_plugin.py             # Plugin for integration with jaclang
│   ├── server/
│   │   ├── __init__.py
│   │   └── server.py                    # gRPC server to serve the imported module as a service
│   └── utils/
│       ├── __init__.py
│       └── startup.sh                   # Startup script for initializing the server
├── k8s/
│   ├── pod_manager_deployment.yml       # Kubernetes deployment manifest
├── docker/
│   ├── Dockerfile                       # Dockerfile
├── requirements.txt                     # Python dependencies
├── setup.py                             # Installation script
└── README.md                            # Project documentation
```

---

## Setup

### Prerequisites

- **Kubernetes** (version 1.21 or later): [Install Kubernetes](https://kubernetes.io/docs/setup/)
- **Python** (version 3.9 or later): [Install Python](https://www.python.org/downloads/)
- **kubectl** command-line tool: [Install kubectl](https://kubernetes.io/docs/tasks/tools/)

Ensure all prerequisites are correctly installed and configured before proceeding.

### 1. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 2. Configure the System

#### **Configuration File**

The application uses a `config.json` file located in the `config/` directory for all configurations.

**Example `config/config.json`:**

```json
{
  "kubernetes": {
    "namespace": "jac-splice-orc",
    "service_account_name": "smartimportsa",
    "pod_manager": {
      "image_name": "ashishmahendra/jac-splice-orc:0.1.8",
      "deployment_yaml": "k8s/pod_manager_deployment.yml",
      "service_name": "pod-manager-service"
    }
  },
  "module_config": {
    "numpy": {
      "lib_mem_size_req": "100Mi",
      "dependency": [],
      "lib_cpu_req": "500m",
      "load_type": "remote"
    },
    "pandas": {
      "lib_mem_size_req": "200Mi",
      "dependency": ["numpy", "pytz", "dateutil"],
      "lib_cpu_req": "700m",
      "load_type": "remote"
    },
    "transformers": {
      "lib_mem_size_req": "2000Mi",
      "dependency": ["torch", "transformers"],
      "lib_cpu_req": "1.0",
      "load_type": "remote"
    },
    "ollama": {
      "lib_mem_size_req": "300Mi",
      "dependency": ["ollama"],
      "lib_cpu_req": "500m",
      "load_type": "remote"
    }
  },
  "environment": {
    "POD_MANAGER_URL": "http://localhost:8000"
  }
}
```

#### **Adjust Configurations**

- Update the `namespace` if you want to deploy to a different Kubernetes namespace.
- Modify `module_config` to specify which modules should be handled remotely and their resource requirements.
- Ensure the `POD_MANAGER_URL` is set correctly; it will be updated automatically during initialization.

### 3. Initialize the System

Use the provided CLI command to initialize the Pod Manager and Kubernetes resources:

```bash
jac orc_initialize your-namespace
```

- Replace `your-namespace` with the desired namespace or omit to use the default from the configuration.
- This command will:
  - Create the Kubernetes namespace (if it doesn't exist).
  - Create the service account and necessary RBAC permissions.
  - Deploy the Pod Manager using the specified deployment file.
  - Update the `POD_MANAGER_URL` in the `config.json` file with the actual service URL.

---

## Usage

### Client Application

The client application provides a seamless way to interact with remote modules as if they were local. It handles the complexities of remote communication, serialization, and deserialization.

#### **Client Components**

- **`ModuleProxy`**: Provides proxy objects for modules, handling remote method calls.
- **`RemoteObjectProxy`**: Acts as a dynamic proxy for method calls on remote modules or objects.

### Example Usage

Below is an example of how to use the system to perform remote method calls on a module, specifically using `numpy`:

```jac
with entry {
    import: py numpy;
    arr = numpy.array([1, 2, 3, 4]);
    print(arr);
    result = numpy.sum(arr);  # Remote method call
    print(result);
}
```

**Explanation:**

- **Importing the Module**: The `import: py numpy;` statement triggers the remote loading of the `numpy` module.
- **Using the Module**: You can use the `numpy` module as if it were local. The underlying system handles the remote execution transparently.
- **Method Calls**: Method calls like `numpy.array()` and `numpy.sum()` are executed on the remote module.

---

## Configuration

### Environment Variables

While most configurations are now stored in `config.json`, you can still use environment variables if needed.

- **`POD_MANAGER_URL`**: URL of the Pod Manager service (updated automatically during initialization).
- **`NAMESPACE`**: Kubernetes namespace to deploy pods (default is `jac-splice-orc`).

### Module Configuration

In the `config.json` file, under `module_config`, you can specify configurations for each module:

- **`dependency`**: List of additional Python packages required by the module.
- **`lib_cpu_req`**: CPU resource request for the pod (e.g., `"500m"`).
- **`lib_mem_size_req`**: Memory resource request for the pod (e.g., `"512Mi"`).
- **`load_type`**: Set to `"remote"` to handle the module remotely.

**Example:**

```json
"numpy": {
  "lib_mem_size_req": "100Mi",
  "dependency": [],
  "lib_cpu_req": "500m",
  "load_type": "remote"
}
```

---

## Flow Diagram

![Flow Diagram](jac_splice_orc/assets/Splice-Orc.png)

---

## Notes

- **Configuration Management**: The system now uses a `config.json` file for configuration, enhancing flexibility and maintainability.
- **Namespace Handling**: You can specify the Kubernetes namespace during initialization or let it default to the one specified in the configuration.
- **Pod Manager URL**: The `POD_MANAGER_URL` is automatically updated in the configuration file after initialization, ensuring that the client knows how to communicate with the Pod Manager.
- **Error Handling**: If the `POD_MANAGER_URL` is not set, the system will prompt you to run the initialization command.
