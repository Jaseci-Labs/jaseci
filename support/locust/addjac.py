from syslog import LOG_INFO
import time
import csv
import logging
# import pandas as pd
from locust import task, HttpUser, SequentialTaskSet, constant
from locust_plugins.users import RestUser


#Admin LOGIN
class SeqTask(SequentialTaskSet):


 def on_start(self):
        # add_users()
        self.userName = "Not_exist"
        self.password = "Not_exist"
        self.zsb_token = "None"
        self.zsb_jid = "None"
        global UserName
       

 def generate_userToken(self):
        response = self.client.post("/user/token/", json={"email": self.userName, "password": "Bcstech123!"})
        print("User: ", self.userName)
        json_var = response.json()
        # print("Response: ", res.text)
        # print("Status Code: ", response.status_code)
        print("User", self.userName, " --- Token: ", json_var['token'])
        self.zsb_token = json_var['token']

 def register_senitel(self):
        print("Token for user: ", self.userName, " is --- ", self.zsb_token)
        req = {

            "name": "zsb",
            "code": "",   # need to take from .jac file and convert to escape sequence and insert here
           
        }
        response = self.client.post("/jac/senitel_register", headers={"authorization": "Token " + self.zsb_token}, json=req)
        json_var = response.json()

 def set_senitel(self):
        print("Token for user: ", self.userName, " is --- ", self.zsb_token)
        req = {

            "name": "zsb",
            "code": "",   # need to take from .jac file and convert to escape sequence and insert here
           
        }
        response = self.client.post("/jac/senitel_set", headers={"authorization": "Token " + self.zsb_token}, json=req)
        json_var = response.json()


class addJac():
    host = "https://uatosapi.apps.zeroshotbot.com"
    tasks = [SeqTask]
    wait_time = constant(2)
