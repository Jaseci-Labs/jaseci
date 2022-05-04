import time
import csv
import logging
# import pandas as pd
from locust import task, HttpUser, SequentialTaskSet, constant
from locust_plugins.users import RestUser


def get_csv_data(filename):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        # global UserName
        users = list(reader)
        print(users)
        return users


Users = get_csv_data('addUsers.csv')
qna = get_csv_data('qna.csv')


class SeqTask(SequentialTaskSet):

    def on_start(self):
        self.username = "None"
        self.name = "None"
        self.zsb_token = "None"
        self.zsb_jid = "None"
        # users = create_new_users()
        global Users
        # print("List:", Users)
        self.username, self.name = Users.pop()
        # print(self.username, self.name)
        # print("Length: ", len(Users))
        print("START")

    # @task
    # def test(self):
    #     print("Testing")

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
    def generate_userToken(self):
        response = self.client.post("/user/token/", json={"email": self.username, "password": "Bcstech123"})
        print("User: ", self.username)
        json_var = response.json()
        # print("Response: ", res.text)
        # print("Status Code: ", response.status_code)
        print("User", self.username, " --- Token: ", json_var['token'])
        self.zsb_token = json_var['token']

    # Set default senital
    @task
    def default_sentinel(self):
        response = self.client.post("/jac/sentinel_active_global", headers={"authorization": "Token " + self.zsb_token})
        print("Default senital set for user:", self.username, "-----", response.text)
        # print("Token for user :", self.username, " is ", self.zsb_token)

    @task
    def create_graph(self):
        # Get Active Graph
        # print("Token for user :", self.username, " is ", self.zsb_token)
        graph_response = self.client.post("/jac/graph_active_get", headers={"authorization": "Token " + self.zsb_token})
        res_var = graph_response.json()

        # Check if jid object exists in json
        if "jid" in res_var:
            print("Graph already exists")
        else:
            response = self.client.post("/jac/graph_create", headers={"authorization": "Token " + self.zsb_token})
            print("Graph: ", response.text)

    @task
    def zsb_init(self):
        # print("Token for user :", self.username, " is ", self.zsb_token)
        response = self.client.post("/jac/walker_run", headers={"authorization": "Token " + self.zsb_token},
                                    json={

                                        "name": "init",
                                        "ctx": {
                                        },
                                        "nd": "active:graph",
                                        "snt": "active:sentinel"

                                    })
        time.sleep(1)
        print("INIT: ", response.text)

    def create_bot(self):
        print("Token for user :", self.username, " is ", self.zsb_token)
        # get_bot_response
        response = self.client.post("/jac/walker_run", headers={"authorization": "Token " + self.zsb_token}, json={
            "name": "add_bot",
            "nd": "active:graph",
            "ctx": {
                "name": "locustBot",
                "description": "this is a test bot for Locust testing"
            },
            "snt": "active:sentinel"
        })
        time.sleep(3)
        print("ADDED BOT for user: ", self.username, "Response Code: ", response.status_code)

    @task
    def create_and_get_bot(self):
        print("Token for user: ", self.username, " is --- ", self.zsb_token)
        req = {

            "name": "get_bots",
            "nd": "active:graph",
            "ctx": {},
            "snt": "active:sentinel"

        }
        # print("request: ", req)
        # ---- Get response for get bots api ------
        response = self.client.post("/jac/walker_run", headers={"authorization": "Token " + self.zsb_token}, json=req)
        json_var = response.json()

        if len(json_var['report']) >= 1:
            print("Bot already exists : ")
            self.zsb_jid = json_var['report'][0]['jid']
            print("Existing JID for user : ", self.username, " is ----- ", self.zsb_jid)
        else:
            self.create_bot()
            time.sleep(3)
            res = self.client.post("/jac/walker_run", headers={"authorization": "Token " + self.zsb_token}, json=req)
            report_response = res.json()
            self.zsb_jid = report_response['report'][0]['jid']
            print("Bot Jid for user ", self.username, " is --- ", report_response['report'][0]['jid'])

    @task
    def create_answers(self):
        # answers = read_excel("Answers")

        # global zsb_jid
        print("JID or user : ", self.username, " is ----", self.zsb_jid)
        for ans in qna:
            # print(zsb_token)
            # print('"{0}"'.format(zsb_jid))
            response = self.client.post("/jac/walker_run", headers={"authorization": "Token " + self.zsb_token}, json={
                "name": "create_answer",
                "nd": self.zsb_jid,
                "ctx": {"text": ans[1]},
                "snt": "active:sentinel"

            })
            print("Status Code: ", response.status_code)
            print("Answer: ", ans[1])
            time.sleep(1)

    @task
    def check(self):
        if len(Users) == 0:
            # print("END")
            self.user.environment.runner.quit()


class CreateUsers(RestUser):
    host = "http://127.0.0.1:8000"
    tasks = [SeqTask]
    wait_time = constant(2)
