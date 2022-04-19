import time
import csv
import pandas as pd
from locust import task, HttpUser, SequentialTaskSet, constant
from locust_plugins.users import RestUser


def get_csv_data(filename):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        # global UserName
        users = list(reader)
        print(users)
        return users


UserName = get_csv_data('userCredentials.csv')
qna = get_csv_data('qna.csv')


class SeqTask(SequentialTaskSet):

    def on_start(self):
        # add_users()
        self.userName = "Not_exist"
        self.password = "Not_exist"
        self.zsb_token = "None"
        self.zsb_jid = "None"
        global UserName
        if len(UserName) > 0:
            self.userName, self.password = UserName.pop()
            # print("Length of list is :", len(UserName))
        else:
            get_csv_data('userCredentials.csv')

    @task
    def generate_userToken(self):
        response = self.client.post("/user/token/", json={"email": self.userName, "password": self.password})
        print("User: ", self.userName)
        json_var = response.json()
        # print("Response: ", res.text)
        # print("Status Code: ", response.status_code)
        print("User", self.userName, " --- Token: ", json_var['token'])
        self.zsb_token = json_var['token']

    @task
    def default_sentinel(self):
        response = self.client.post("/jac/sentinel_active_global", headers={"authorization": "Token " + self.zsb_token})
        print("Default senital set for user:", self.userName, "-----", response.text)
        # print("Token for user :", self.userName, " is ", self.zsb_token)

    @task
    def create_graph(self):
        # Get Active Graph
        # print("Token for user :", self.userName, " is ", self.zsb_token)
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
        # print("Token for user :", self.userName, " is ", self.zsb_token)
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
        print("Token for user :", self.userName, " is ", self.zsb_token)
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
        print("ADDED BOT for user: ", self.userName, "Response Code: ", response.status_code)

    @task
    def create_and_get_bot(self):
        print("Token for user: ", self.userName, " is --- ", self.zsb_token)
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
            print("Existing JID for user : ", self.userName, " is ----- ", self.zsb_jid)
        else:
            self.create_bot()
            time.sleep(3)
            res = self.client.post("/jac/walker_run", headers={"authorization": "Token " + self.zsb_token}, json=req)
            report_response = res.json()
            self.zsb_jid = report_response['report'][0]['jid']
            print("Bot Jid for user ", self.userName, " is --- ", report_response['report'][0]['jid'])

    @task
    def create_answers(self):
        #answers = read_excel("Answers")

        # global zsb_jid
        print("JID or user : ", self.userName, " is ----", self.zsb_jid)
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
            # print("Answer: ", ans)
            time.sleep(1)

    @task
    def ask_questions(self):
        # questions = read_excel("Questions")
        for questions in qna:
            response = self.client.post("/jac/walker_run", headers={"authorization": "Token " + self.zsb_token}, json={
                "name": "ask_question",
                "nd": self.zsb_jid,
                "ctx": {
                    "text": questions[0],
                    "metadata": {
                        "channel": "ZSB Platform"}
                },
                "snt": "active:sentinel"

            })
            answer_var = response.json()
            print(response.status_code)
            print("User:", self.userName)
            print("Question: ", questions[0])
            print("Answer: ", answer_var['report'][0]['context']['text'])
            print("----------------------------------------------------")
            time.sleep(2)

    # def on_stop(self):
    #     response = self.client.post("/jac/walker_run", headers={"authorization": "Token " + self.zsb_token}, json={

    #         "name": "delete_bot",
    #         "nd": self.zsb_jid,
    #         "ctx": {},
    #         "snt": "active:sentinel"
    #     })
    #     print("Deleted bot with Jid: ", self.zsb_jid)


class LoadTest(RestUser):
    host = "https://uatosapi.apps.zeroshotbot.com"
    # host = "https://reqres.in"
    tasks = [SeqTask]
    wait_time = constant(2)
