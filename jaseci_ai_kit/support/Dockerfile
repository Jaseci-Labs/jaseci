FROM ubuntu:20.04
WORKDIR /
ENV DEBIAN_FRONTEND=noninteractive
#ADD ./ /jaseci_ai_kit/
RUN apt update; apt -y upgrade;
RUN apt -y install --no-install-recommends python3.8 python3-pip python3-dev vim git build-essential g++
RUN pip3 install jaseci_ai_kit==1.3.5.22
RUN pip3 install flair==0.10
RUN pip3 install protobuf==3.20.3
RUN pip3 install sumy==0.11.0
COPY ../../support/docker/trained_models trained_models/
CMD ["echo", "Ready"]
