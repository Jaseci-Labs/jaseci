FROM ubuntu:20.04
WORKDIR /
ENV DEBIAN_FRONTEND=noninteractive
COPY requirements.txt requirements.txt
RUN apt update; apt -y upgrade; apt -y install git git-lfs;
RUN mkdir -p /t5/t5-small/;
RUN git clone https://huggingface.co/t5-small /t5/t5-small
RUN apt -y install --no-install-recommends python3.8 python3-pip vim; apt-get clean; rm -rf /var/lib/apt/lists/*;
RUN pip3 install -r requirements.txt;
CMD ["echo", "Ready"]