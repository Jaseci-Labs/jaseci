FROM python:3.10-slim
ARG JASECI_PYPI_VERSION
ARG JASECI_SERV_PYPI_VERSION
ARG JASECI_AI_KIT_PYPI_VERSION
ARG BUILD_WITH
WORKDIR /
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update; apt -y upgrade; apt -y install --no-install-recommends git g++ build-essential pkg-config cmake
RUN pip3 install jaseci==$JASECI_PYPI_VERSION
RUN pip3 install jaseci-serv==$JASECI_SERV_PYPI_VERSION
RUN if [ -n "$BUILD_WITH" ]; then pip3 install "$BUILD_WITH"[all]==$JASECI_AI_KIT_PYPI_VERSION --extra-index-url https://download.pytorch.org/whl/cpu; fi
CMD ["echo", "Ready"]
