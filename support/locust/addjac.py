import logging
from locust import task, HttpUser, SequentialTaskSet, constant, HttpUser
# from locust_plugins.users import RestUser
import os
from credentials import gen_username, gen_password

def format_output(userName:str, output:str):
    print(f'{userName}: {output}')
# Admin LOGIN
# code = 'walker init {report "admin";}'
def get_code(path: str)->str:
    file = open(path, 'r')
    code = file.read()
    file.close()
    return code



UserID = 0
actionLoaded = False

# walkerSequence = ['createPredefines', 'segmenter']
# actionList = ['http://flair-ner:80/', 'http://js-segmenter:80/']
walkerSequence = ['init']
actionList = []

class SeqTask(SequentialTaskSet):
    def on_start(self):
        self.userName = "Not_exist" # Initialize
        self.password = "Not_exist"
        self.zsb_token = "None"
        self.zsb_jid = "None"
        global UserID
        self.userName, self.password = gen_username(UserID), gen_password(UserID)
        self.userID = UserID
        UserID += 1

    # @task
    # def create_user(self):
    #     response = self.client.post("/user/create/", json = {
    #         "email" : self.userName,
    #         "password" : self.password,
    #         "is_activated": True,
    #         "is_superuser": True
    #     })
    #     if response.status_code == 400:
    #         logging.info(self.userName + " " + response.text)
    #     elif response.status_code != 201:
    #         logging.info(self.userName, " was not created")
    #     else:
    #         pass
    #         # print("List: ", Users)
    #         # print("User added: ", self.userName)

    @task
    def generate_userToken(self):
        response = self.client.post("/user/token/", json={"email": self.userName, "password": self.password})
        format_output(self.userName, response.text)
        json_var = response.json()
        self.user_token = json_var['token']

    
    @task 
    def post_jac_prog(self):
        req = {
                'name': 'jac_prog',
                'code': get_code('sample_code/simple/walker.jac'),
            }
        response = self.client.post("/js/sentinel_register",headers = {'authorization' : f'Token {self.user_token}'}, json = req)
        self.sentinel_jid = response.json()[0]['jid']
        # format_output(self.userName, response.text)

    @task
    def load_actions(self):
        global actionList
        global actionLoaded
        if actionLoaded:
            return
        actionLoaded = True
        for action in actionList:
            response = self.client.post("/js_admin/actions_load_remote", headers = {'authorization' : f'Token {self.user_token}'}, json = {
                'url': action
                })
            # print(f"response: {response.text}")

        # response = self.client.post('/js_admin/actions_list', headers = {'authorization' : f'Token {self.user_token}'})
        # print(f"Actions list response: {response.text}")

    @task
    def walker_run(self):
        for walkerName in walkerSequence:
            req = {
                    'name': walkerName,
                    'snt': self.sentinel_jid
                    }
            print(f"Walker {walkerName} running.")
            response = self.client.post("/js/walker_run",headers = {'authorization' : f'Token {self.user_token}'}, json = req)
            print(f"Walker {walkerName} finished. {response.text}")
            print(f"Walker {walkerName} Output: {response.json()}")
    
    

class addJac(HttpUser):
    host = "http://127.0.0.1:8888"
    tasks = [SeqTask]
    wait_time = constant(2)
