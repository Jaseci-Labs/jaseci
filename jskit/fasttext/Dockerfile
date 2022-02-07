FROM python:3.7

WORKDIR /usr/src/lib
RUN git clone "https://github.com/facebookresearch/fastText.git" && cd fastText && pip install .

WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /

CMD ["echo", "Ready"]
