FROM python:3.10-slim
ARG JASECI_PYPI_VERSION
ARG JASECI_SERV_PYPI_VERSION
ARG JASECI_AI_KIT_PYPI_VERSION
ARG BUILD_WITH_AI
WORKDIR /
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update; apt -y upgrade; apt -y install --no-install-recommends git g++ build-essential pkg-config cmake
RUN pip3 install jaseci==$JASECI_PYPI_VERSION
RUN pip3 install jaseci-serv==$JASECI_SERV_PYPI_VERSION
COPY jaseci_ai_kit /jaseci_ai_kit
RUN cd /jaseci_ai_kit/; cp setup-text-cpu.py setup.py; pip3 install . --extra-index-url https://download.pytorch.org/whl/cpu;
CMD ["echo", "Ready"]
