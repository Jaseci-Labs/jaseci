FROM python:3.8-slim-buster

COPY requirements.txt ./

RUN pip install -r requirements.txt
RUN pip install numpy

RUN python -m nltk.downloader punkt

ADD scraper.py /

CMD ["uvicorn", "scraper:app", "--proxy-headers","--reload", "--host", "0.0.0.0"]