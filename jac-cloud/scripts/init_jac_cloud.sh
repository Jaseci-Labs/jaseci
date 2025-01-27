#!/bin/bash

# Exit on any error
set -e

echo "=== Starting jac-cloud Pod Initialization ==="

# Default values for variables
NAMESPACE=${NAMESPACE:-default}
CONFIGMAP_NAME=${CONFIGMAP_NAME:-module-config}
FILE_NAME=${FILE_NAME:-example.jac}

# Display configuration
echo "Using Namespace: $NAMESPACE"
echo "Running Jac File: $FILE_NAME"

# Helper function for logging
log_info() {
  echo "[INFO] $1"
}

log_error() {
  echo "[ERROR] $1"
  exit 1
}

# Step 1: Initialize Pod Manager and Kubernetes setup
log_info "Running orc_initialize for namespace: $NAMESPACE..."
if ! jac orc_initialize "$NAMESPACE"; then
  log_error "orc_initialize failed. Exiting..."
fi
log_info "orc_initialize completed successfully."

# Step 2: Start Jac Serve
log_info "Starting Jac Serve with file: $FILE_NAME..."
if ! jac serve "$FILE_NAME"; then
  log_error "Jac Serve failed. Exiting..."
fi

