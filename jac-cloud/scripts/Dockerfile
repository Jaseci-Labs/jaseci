FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app/littlex
RUN git clone --branch main --depth 1 https://github.com/Jaseci-Labs/littleX.git /app/littlex && \
    pip install --no-cache-dir -r littleX_BE/requirements.txt openai jac-splice-orc

COPY init_jac_cloud.sh /app/
RUN chmod +x /app/init_jac_cloud.sh

EXPOSE 8000
CMD ["/bin/bash", "/app/init_jac_cloud.sh"]