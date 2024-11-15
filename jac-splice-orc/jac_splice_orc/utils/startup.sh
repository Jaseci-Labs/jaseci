#!/bin/sh

if [ "$SERVICE_TYPE" = "pod_manager" ]; then
  echo "Starting Pod Manager with FastAPI..."
  export PYTHONPATH=$PYTHONPATH:/app/grpc_local
  echo "PYTHONPATH is set to $PYTHONPATH"
  uvicorn pod_manager:app --host 0.0.0.0 --port 8000

elif [ "$SERVICE_TYPE" = "module_service" ]; then
  echo "Starting gRPC Module Service..."

  # Check if a custom requirements.txt exists for the module
  if [ -f "/app/requirements/$MODULE_NAME/requirements.txt" ]; then
    echo "Found requirements.txt for $MODULE_NAME, installing dependencies..."
    pip install -r "/app/requirements/$MODULE_NAME/requirements.txt"
  else
    # If no requirements.txt, attempt to install by module name
    echo "No requirements.txt found, attempting to install module directly: $MODULE_NAME"
    pip install "$MODULE_NAME"
  fi

  export PYTHONPATH=/app
  export PYTHONPATH=$PYTHONPATH:/app/grpc_local

  echo "Starting the module service with module: $MODULE_NAME"
  python server/server.py "$MODULE_NAME"

else
  echo "Unknown service type: $SERVICE_TYPE"
  exit 1
fi
