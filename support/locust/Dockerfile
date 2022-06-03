FROM python:latest
WORKDIR /locust
EXPOSE 8089
COPY . /locust/src
RUN pip3 install locust
RUN mkdir /locust/csv
CMD locust -f /locust/src/run_jac.py --headless -u $LOCUST_USER_NUMBER -r $LOCUST_SPAWN_RATE -H $LOCUST_HOST --run-time $LOCUST_DURATION --csv=csv/data
