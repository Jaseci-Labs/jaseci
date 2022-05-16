FROM python:latest
WORKDIR /locust
EXPOSE 8089
COPY . /locust/src
COPY sample_code /locust/sample_code
RUN pip3 install locust
CMD locust -f /locust/src/addjac.py --headless -u 5 -r 1 -H $LOCUST_HOST
