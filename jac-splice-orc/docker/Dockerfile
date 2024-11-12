# Use a single base image
FROM python:3.12-slim

# Install common dependencies
RUN pip install --no-cache-dir grpcio grpcio-tools fastapi uvicorn kubernetes python-multipart numpy

# Create a working directory
WORKDIR /app

# Copy the gRPC service proto file for module services
COPY grpc_local/module_service.proto /app/grpc_local/

# Run gRPC file generation
RUN python -m grpc_tools.protoc \
    -I/app/grpc_local \
    --python_out=/app/grpc_local \
    --grpc_python_out=/app/grpc_local \
    /app/grpc_local/module_service.proto

# Copy pod manager code, server, and utils
COPY managers/pod_manager.py /app/pod_manager.py
COPY server /app/server
COPY utils /app/utils

# Expose the relevant ports (50051 for gRPC, 8000 for FastAPI)
EXPOSE 50051 8000

# Use an environment variable to decide what service to run
# Default to "module_service"
ENV SERVICE_TYPE="module_service"

# Define entrypoint script that decides which service to start
COPY utils/startup.sh /app/utils/startup.sh
RUN chmod +x /app/utils/startup.sh

# Start the appropriate service based on the environment variable
CMD ["/app/utils/startup.sh"]
