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


# UserName = get_csv_data('userCredentials.csv')
UserName = get_csv_data('addUsers.csv')
qna = get_csv_data('qna.csv')


def read_excel(columName):
    df = pd.read_excel('qna.xlsx', sheet_name='Sheet1')  # can also index sheet by name or fetch all sheets
    mylist = df[columName].tolist()
    return mylist


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
            print("Bot was not created ")
        #     self.create_bot()
        #     time.sleep(3)
        #     res = self.client.post("/jac/walker_run", headers={"authorization": "Token " + self.zsb_token}, json=req)
        #     report_response = res.json()
        #     self.zsb_jid = report_response['report'][0]['jid']
        #     print("Bot Jid for user ", self.userName, " is --- ", report_response['report'][0]['jid'])


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
            # print("Answer: ", answer_var['report'][0]['context']['text'])
            print("----------------------------------------------------")
            time.sleep(1)

class LoadTest(RestUser):
    host = "https://uatosapi.apps.zeroshotbot.com"
    # host = "https://reqres.in"
    tasks = [SeqTask]
    wait_time = constant(2)
