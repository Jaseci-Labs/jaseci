FROM ubuntu:20.04
WORKDIR /
ENV DEBIAN_FRONTEND=noninteractive
ADD ./ /jaseci_ai_kit/
RUN apt update; apt -y upgrade;
RUN apt -y install --no-install-recommends python3.8 python3-pip python3-dev vim git build-essential g++
RUN pip3 install /jaseci_ai_kit
CMD ["echo", "Ready"]
