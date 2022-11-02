FROM python:3-slim
WORKDIR /
ENV DEBIAN_FRONTEND=noninteractive
COPY requirements.txt requirements.txt
RUN apt update; apt -y upgrade; apt -y install --no-install-recommends git g++;
RUN pip3 install -r requirements.txt
CMD ["echo", "Ready"]