FROM ubuntu:20.04
WORKDIR /
ENV DEBIAN_FRONTEND=noninteractive
COPY requirements.txt requirements.txt
RUN apt update; apt -y upgrade;
RUN apt -y install --no-install-recommends python3.8 python3-pip vim git;
RUN pip3 install -r requirements.txt;
CMD ["echo", "Ready"]
