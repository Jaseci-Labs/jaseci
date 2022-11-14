FROM python:3-slim
WORKDIR /
ENV DEBIAN_FRONTEND=noninteractive
COPY requirements.txt requirements.txt
RUN apt update; apt -y upgrade; apt -y install --no-install-recommends git g++;
RUN pip3 install -r requirements.txt
RUN apt -y install --no-install-recommends build-essential pkg-config cmake
RUN pip3 install jaseci_ai_kit
RUN pip3 install -U sumy
CMD ["echo", "Ready"]
