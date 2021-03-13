FROM ubuntu:20.04
WORKDIR /
ENV DEBIAN_FRONTEND=noninteractive
ENV GIT_LFS_SKIP_SMUDGE=1
COPY requirements.use.txt requirements.txt
RUN apt update; apt -y upgrade; apt -y install git git-lfs;
RUN git clone https://prod:Pr0dN1nj4@models.jaseci.org/marsninja/jsmodels.git
RUN cd jsmodels && git lfs pull --include "universal-sentence-encoder-multilingual-qa_3.tar.gz" && mv models /
RUN cd /models; cd use && tar -xvvzf universal-sentence-encoder-multilingual-qa_3.tar.gz; cd /;
RUN apt -y install --no-install-recommends python3.8 python3-pip vim; apt-get clean; rm -rf /var/lib/apt/lists/*;
RUN pip3 install -r requirements.txt;
CMD ["echo", "Ready"]
