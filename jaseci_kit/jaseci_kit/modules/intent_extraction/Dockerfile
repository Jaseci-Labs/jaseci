FROM ubuntu:20.04
WORKDIR /
ENV DEBIAN_FRONTEND=noninteractive

# OS dependencies
RUN apt update; apt -y upgrade
RUN apt -y install --no-install-recommends python3.8 python3-pip vim; apt-get clean; rm -rf /var/lib/apt/lists/*

# Python dependenicies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /app

# TODO: Pull pre-trained model from public model hub. You can use ADD.
# These are usually downloaded as a tar ball
# For example, for USE encoder, we are downloading from TF Hub
# ADD https://tfhub.dev/google/universal-sentence-encoder/4?tf-hub-format=compressed /universal-sentence-encoder_4.tar.gz

# TODO: Process the model files as needed
# For example, for USE encoder, we need to untar
# RUN mkdir -p /universal-sentence-encoder_4/
# RUN tar -xvzf universal-sentence-encoder_4.tar.gz -C /universal-sentence-encoder_4/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
