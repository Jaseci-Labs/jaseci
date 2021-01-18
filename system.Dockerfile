FROM ubuntu:20.04
WORKDIR /
COPY requirements.txt requirements.txt
ENV DEBIAN_FRONTEND=noninteractive
RUN apt update; apt -y upgrade; apt -y install --no-install-recommends python3.8 python3-pip git openjdk-8-jre vim; apt-get clean; rm -rf /var/lib/apt/lists/*;  pip3 install -r requirements.txt;
CMD ["echo", "Ready"]
#postgresql libc-dev libpq-dev make