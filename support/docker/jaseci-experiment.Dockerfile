FROM jaseci/jac-nlp:1.4.0.12
ENV DEBIAN_FRONTEND=noninteractive
ADD . /jaseci
# Install jaseci core
WORKDIR /jaseci/jaseci_core
RUN pip install .
# Install jaseci serv
WORKDIR /jaseci/jaseci_serv
RUN pip install .
# Install jac_nlp, action-configs only
WORKDIR /jaseci/jaseci_ai_kit/jac_nlp
RUN pip install .
WORKDIR /
CMD ["echo", "READY"]
