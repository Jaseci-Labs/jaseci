FROM ubuntu:20.04
WORKDIR /
ENV DEBIAN_FRONTEND=noninteractive
COPY requirements.txt requirements.txt
RUN apt update; apt -y upgrade; apt -y install git git-lfs;
ADD https://tfhub.dev/google/universal-sentence-encoder/4?tf-hub-format=compressed /universal-sentence-encoder_4.tar.gz
RUN mkdir -p /models/use/
RUN tar -xvzf universal-sentence-encoder_4.tar.gz -C /models/use/
RUN apt -y install --no-install-recommends python3.8 python3-pip vim; apt-get clean; rm -rf /var/lib/apt/lists/*;
RUN pip3 install -r requirements.txt;
CMD ["echo", "Ready"]
