#!/bin/sh

if [ "$SERVICE_TYPE" = "pod_manager" ]; then
  echo "Starting Pod Manager with FastAPI..."
  export PYTHONPATH=$PYTHONPATH:/app/grpc_local
  echo "PYTHONPATH is set to $PYTHONPATH"
  uvicorn pod_manager:app --host 0.0.0.0 --port 8000
elif [ "$SERVICE_TYPE" = "module_service" ]; then
  echo "Starting gRPC Module Service..."
  pip install $MODULE_NAME
  export PYTHONPATH=/app
  export PYTHONPATH=$PYTHONPATH:/app/grpc_local
  python server/server.py $MODULE_NAME
else
  echo "Unknown service type: $SERVICE_TYPE"
  exit 1
fi