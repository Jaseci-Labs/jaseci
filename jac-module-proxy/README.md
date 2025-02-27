# **Setup**
### **LOCAL PREREQUISITE**
> pre-commit install

### **PREREQUISITE**
generate module_service files if there are changes in [module_service.proto](./server/grpc_local/module_service.proto) or changes in grpc libraries versions
> python -m grpc_tools.protoc -I./server/grpc_local --python_out=./server/grpc_local --grpc_python_out=./server/grpc_local ./server/grpc_local/module_service.proto

### **DEV**
> poetry install\
> pip install numpy\
> PYTHONPATH=/home/boyong/jaseci/jac-module-proxy/server/grpc_local && poetry run deploy "numpy"

### **PROD**
> poetry install --without dev\
> pip install numpy\
> PYTHONPATH=/home/boyong/jaseci/jac-module-proxy/server/grpc_local && poetry run deploy "numpy"