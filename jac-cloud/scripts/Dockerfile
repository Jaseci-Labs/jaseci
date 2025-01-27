# Use Python 3.12 slim as the base
FROM python:3.12-slim

# Install git (to clone the repo)
RUN apt-get update && apt-get install -y --no-install-recommends git


# Set up a working directory
WORKDIR /app

# Clone the LittleX repo (main branch) into /app/littlex
RUN git clone --branch main https://github.com/Jaseci-Labs/littleX.git /app/littlex

# Install Python dependencies from the cloned repo
WORKDIR /app/littlex/littleX_BE
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install openai
RUN pip install jac-splice-orc
WORKDIR /app/littlex
# Copy our startup script into the image (you'll create it locally)
COPY init_jac_cloud.sh /app/init_jac_cloud.sh
RUN chmod +x /app/init_jac_cloud.sh

# Expose the FastAPI port
EXPOSE 8000

# Set default environment variables, can be overridden in K8s
ENV NAMESPACE=default
ENV CONFIGMAP_NAME=module-config
ENV FILE_NAME=littleX_BE/littleX_mini.jac

# By default, run the init_jac_cloud.sh script
CMD ["/bin/bash", "/app/init_jac_cloud.sh"]
