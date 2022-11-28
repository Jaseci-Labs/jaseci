FROM python:3.10-slim
ARG JASECI_AI_KIT_PYPI_VERSION
WORKDIR /
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update; apt -y upgrade; apt -y install --no-install-recommends git g++ build-essential pkg-config cmake
RUN pip3 install jaseci-ai-kit==$JASECI_AI_KIT_PYPI_VERSION
CMD ["echo", "Ready"]
