FROM tensorflow/tensorflow:2.10.0

RUN apt-get update && apt-get install apt-utils build-essential pkg-config git python3-dev -y
RUN rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir jaseci 
RUN pip install --no-cache-dir jaseci_kit
RUN pip install --no-cache-dir jaseci_serv
CMD ["jsctl"]
