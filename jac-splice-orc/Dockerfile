FROM python:3.12-slim

RUN pip install grpcio grpcio-tools

COPY grpc_local /app/grpc_local
COPY server /app/server
COPY utils /app/utils

WORKDIR /app

EXPOSE 50051

CMD ["sh", "/app/utils/startup.sh"]
