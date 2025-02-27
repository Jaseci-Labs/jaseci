#!/bin/sh

# Function to log messages
log() {
  echo "[INFO] $1"
}

if [ "$SERVICE_TYPE" = "pod_manager" ]; then
  log "Starting Pod Manager with FastAPI..."

  # Set PYTHONPATH to include /app and /app/grpc_local
  export PYTHONPATH=/app:/app/grpc_local
  log "PYTHONPATH is set to $PYTHONPATH"

  # Run FastAPI app
  uvicorn managers.pod_manager:app --host 0.0.0.0 --port 8000

elif [ "$SERVICE_TYPE" = "module_service" ]; then
  log "Starting gRPC Module Service..."

  if [ -z "$MODULE_NAME" ]; then
    log "MODULE_NAME is not set. Exiting..."
    exit 1
  fi

  MODULE_REQUIREMENTS="/app/requirements/$MODULE_NAME/requirements.txt"
  if [ -f "$MODULE_REQUIREMENTS" ]; then
    log "Found requirements.txt for $MODULE_NAME, installing dependencies..."
    pip install -r "$MODULE_REQUIREMENTS"
  else
    log "No requirements.txt found, attempting to install module directly: $MODULE_NAME"
    pip install "$MODULE_NAME"
  fi

  export PYTHONPATH=/app:/app/grpc_local
  log "PYTHONPATH is set to $PYTHONPATH"

  log "Starting the module service with module: $MODULE_NAME"
  python server/server.py "$MODULE_NAME"

else
  log "Unknown service type: $SERVICE_TYPE"
  exit 1
fi
