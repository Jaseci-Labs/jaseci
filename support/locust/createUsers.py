import time
import csv
import logging
# import pandas as pd
from locust import task, HttpUser, SequentialTaskSet, constant
from locust_plugins.users import RestUser


def create_new_users():
    with open('addUsers.csv', newline='') as f:
        reader = csv.reader(f)
        # global Users
        users = list(reader)
        return users


Users = create_new_users()


class SeqTask(SequentialTaskSet):

    def on_start(self):
        self.username = "None"
        self.name = "None"
        # users = create_new_users()
        # print("List:", Users)
        global Users
        self.username, self.name = Users.pop()
        # print(self.username, self.name)
        # print("Length: ", len(Users))
        print("START")

    @task
    def new_users(self):
        response = self.client.post("/user/create/", json={
            "email": self.username,
            "password": "Bcstech123",
            "name": self.name,
            "is_activated": "true"
        })
        print(response.status_code)
        if response.status_code == 400:
            logging.info(self.username + " " + response.text)
        elif response.status_code != 201:
            logging.info(self.user, " was not created")
        else:
            # print("List: ", Users)
            print("User added: ", self.username)
        time.sleep(1)

    @task
    def check(self):
        if len(Users) == 0:
            # print("END")
            self.user.environment.runner.quit()


class CreateUsers(RestUser):
    host = "https://uatosapi.apps.zeroshotbot.com"
    tasks = [SeqTask]
    wait_time = constant(2)
