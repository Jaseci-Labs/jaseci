#!/bin/bash

# Fail on error
set -e

echo "Starting jac-cloud pod initialization..."

# Default values for variables
NAMESPACE=${NAMESPACE:-default}
CONFIGMAP_NAME=${CONFIGMAP_NAME:-module-config}
FILE_NAME=${FILE_NAME:-module-config} 

echo "Using Namespace: $NAMESPACE"
echo "Using ConfigMap: $CONFIGMAP_NAME"
echo "Running Jac File: $FILE_NAME"

# Step 1: Initialize Pod Manager and Kubernetes setup
echo "Running orc_initialize..."
jac orc_initialize  $NAMESPACE
if [ $? -ne 0 ]; then
  echo "orc_initialize failed. Exiting..."
  exit 1
fi

# Step 2: Start Jac Serve
echo "Starting Jac Serve with file: $FILE_NAME..."
jac serve $FILE_NAME
if [ $? -ne 0 ]; then
  echo "Jac Serve failed. Exiting..."
  exit 1
fi
