# Design Considerations: Migrating jac-splice-orc to Ray

**Objective:**
This document evaluates specific challenges when considering migrating the **jac-splice-orc** Kubernetes-based orchestration system to the **Ray** distributed computing framework.

---

## 🔸 Current State Overview

The **jac-splice-orc** system currently leverages:

* Kubernetes pods for dynamic, isolated deployment of Python modules.
* gRPC communication for transparent client-to-module interactions.
* Containerized dependency management using Docker.
* Explicit CPU and memory allocation defined through Kubernetes manifests.
* FastAPI-based API for managing deployments, allowing easy and clear orchestration of pods through declarative manifests.
* Lifecycle management and dynamic deployment configuration from environment variables (e.g., `MODULES`).

Migrating to Ray introduces simplified distributed execution but presents significant trade-offs requiring thorough evaluation.

---

## 🚩 Key Challenges & Pain Points

### 1. **Loss of Container-Level Isolation**

**Current Approach:**

* Kubernetes provides strong container-based isolation (Docker), preventing interference and ensuring dependency encapsulation.

**With Ray:**

* Ray executes modules as tasks or actors sharing the same Python runtime environment, offering only process-level isolation.

**Impact:**

* Higher risk of dependency conflicts between modules.
* Increased possibility of memory leaks or resource contention.
* Reduced compliance with stringent security policies requiring strict isolation.

**Severity:** High 🔴

---

### 2. **Complex Dependency Management**

**Current Approach:**

* Docker-based management offers predictable, clearly defined dependencies.
* Each service independently maintains exact environment requirements.

**With Ray:**

* Dependencies are managed via Python virtual environments (Conda, virtualenv) or Ray runtime environments.
* Increased complexity in managing diverse dependencies across modules.

**Impact:**

* Greater risk of version conflicts and runtime instability.
* Increased operational overhead in handling and validating dependencies across distributed environments.

**Severity:** High 🔴

---

### 3. **Reduced Explicit Resource Control**

**Current Approach:**

* Kubernetes manifests explicitly define CPU, memory, and resource quotas, ensuring predictable, stable operation.

**With Ray:**

* Resource allocation is dynamic and abstracted.
* Limited direct visibility and explicit control over granular resource allocation compared to Kubernetes.

**Impact:**

* Challenges in enforcing precise resource usage guarantees.
* Potential performance variability due to dynamic resource management.

**Severity:** Medium 🟠

---

### 4. **Complex Fault Isolation and Recovery**

**Current Approach:**

* Kubernetes pod-based isolation simplifies identification, isolation, and recovery from faults.
* Automatic restart and self-healing mechanisms provided natively by Kubernetes.

**With Ray:**

* Fault isolation becomes complex due to shared process-level execution.
* More intricate error handling mechanisms required for isolating failed tasks or actors.

**Impact:**

* Increased risk of cascading failures affecting multiple modules simultaneously.
* Higher operational burden for monitoring and recovering failed services.

**Severity:** High 🔴

---

## 📌 Summary of Specific Challenges

| Pain Point                           | Severity  | Direct Impact Area                  |
| ------------------------------------ | --------- | ----------------------------------- |
| Loss of Container-Level Isolation    | High 🔴   | Security, Stability                 |
| Complex Dependency Management        | High 🔴   | Development, Operational Efficiency |
| Reduced Explicit Resource Control    | Medium 🟠 | Performance, Predictability         |
| Complex Fault Isolation and Recovery | High 🔴   | Reliability, Maintenance            |

---
