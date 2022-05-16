FROM python:latest
WORKDIR /locust
EXPOSE 8089
COPY . /locust/src
COPY sample_code /locust/sample_code
RUN pip3 install locust
CMD locust -f /locust/src/addjac.py --headless -u $LOCUST_USER_NUMBER -r $LOCUST_SPAWN_RATE -H $LOCUST_HOST --run-time $LOCUST_DURATION
