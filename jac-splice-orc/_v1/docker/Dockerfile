# Use a single base image
FROM python:3.12-slim

# Install common dependencies
RUN pip install --no-cache-dir \
    grpcio \
    grpcio-tools \
    grpcio-health-checking\
    fastapi \
    uvicorn \
    kubernetes \
    python-multipart \
    numpy

# Set the working directory for subsequent commands
WORKDIR /app

# Copy the entire application directory into the container
COPY ../../jac_splice_orc /app

# Generate the gRPC service files
RUN python -m grpc_tools.protoc \
    -I./grpc_local \
    --python_out=./grpc_local \
    --grpc_python_out=./grpc_local \
    ./grpc_local/module_service.proto

# Expose the relevant ports (50051 for gRPC, 8000 for FastAPI)
EXPOSE 50051 8000

# Use an environment variable to decide what service to run
ENV SERVICE_TYPE="module_service"

# Make the entrypoint script executable
RUN chmod +x ./utils/startup.sh

# Start the appropriate service based on the environment variable
CMD ["./utils/startup.sh"]
