FROM python:3.10-slim
ARG JASECI_PYPI_VERSION
ARG JASECI_SERV_PYPI_VERSION
ARG JASECI_AI_KIT_PYPI_VERSION
ARG BUILD_WITH_AI
WORKDIR /
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update; apt -y upgrade; apt -y install --no-install-recommends git g++ build-essential pkg-config cmake
# Dependencies for whisper
RUN apt -y install libsndfile1
RUN pip3 install jaseci==$JASECI_PYPI_VERSION
RUN pip3 install jaseci-serv==$JASECI_SERV_PYPI_VERSION
COPY jaseci_ai_kit /jaseci_ai_kit
COPY support/docker/setup-speech.py /jaseci_ai_kit/setup.py
RUN cd /jaseci_ai_kit/; cp setup-speech.py setup.py; pip3 install . --extra-index-url https://download.pytorch.org/whl/cpu;
CMD ["echo", "Ready"]
