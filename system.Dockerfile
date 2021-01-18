FROM ubuntu:20.04
WORKDIR /
COPY requirements.txt requirements.txt
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update; apt -y upgrade; apt -y install --no-install-recommends python3.8 python3-pip git postgresql make openjdk-8-jre vim libc-dev libpq-dev; apt-get clean; rm -rf /var/lib/apt/lists/*;  pip3 install -r requirements.txt;
CMD ["echo", "Ready"]
