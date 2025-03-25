### **PREREQUISITE**
generate module_service files if there are changes in [module_service.proto](./grpc_local/module_service.proto) or changes in grpc libraries versions
> python -m grpc_tools.protoc -I./jac_splice_orc/proxy/grpc_local --python_out=./jac_splice_orc/proxy/grpc_local --grpc_python_out=./jac_splice_orc/proxy/grpc_local ./jac_splice_orc/proxy/grpc_local/module_service.proto

### **DEV**
> poetry install --with proxy\
> pip install numpy\
> export PYTHONPATH=/home/your_user/jaseci/jac-splice-orc/jac_splice_orc/proxy/grpc_local && poetry run proxy "numpy"

### **PROD**
> poetry install --with proxy --without dev\
> pip install numpy\
> export PYTHONPATH=/home/your_user/jaseci/jac-splice-orc/jac_splice_orc/proxy/grpc_local && poetry run proxy "numpy"