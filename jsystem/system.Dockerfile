FROM ubuntu:20.04
WORKDIR /
ENV DEBIAN_FRONTEND=noninteractive
COPY requirements.txt requirements.txt
COPY models models
RUN cd models; mkdir use && tar -xvvzf tarballs/universal-sentence-encoder-multilingual-qa_3.tar.gz -C use; cd /;
RUN apt update; apt -y upgrade; apt -y install --no-install-recommends python3.8 python3-pip git openjdk-8-jre vim; apt-get clean; rm -rf /var/lib/apt/lists/*;
RUN pip3 install -r requirements.txt;
CMD ["echo", "Ready"]