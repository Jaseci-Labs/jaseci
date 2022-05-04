from syslog import LOG_INFO
import csv
import logging
from locust import task, HttpUser, SequentialTaskSet, constant
from locust_plugins.users import RestUser

# Admin LOGIN
code = 'walker init {report "admin";}'
def gen_username(id : int)->str:
    return f'jaclang{id}@jaseci.org'

def gen_password(id : int)->str:
    return f'ilovejaclang{id}'


UserID = 0
class SeqTask(SequentialTaskSet):
    def on_start(self):
		# add_users()
        self.userName = "Not_exist"
        self.password = "Not_exist"
        self.zsb_token = "None"
        self.zsb_jid = "None"
        global UserID
        self.userName, self.password = gen_username(UserID), gen_password(UserID)

    @task
    def create_user(self):
        response = self.client.post("/user/create/", json = {
            "email" : self.userName,
            "password" : self.password,
            "is_activated": True,
            "is_superuser": False
        })
        print(f"UserName: {self.userName}")
        if response.status_code == 400:
            logging.info(self.userName + " " + response.text)
        elif response.status_code != 201:
            logging.info(self.userName, " was not created")
        else:
            # print("List: ", Users)
            print("User added: ", self.userName)

    @task
    def generate_userToken(self):
        response = self.client.post("/user/token/", json={"email": self.userName, "password": self.password})
        json_var = response.json()
        # print("Response: ", res.text)
        # print("Status Code: ", response.status_code)
        print("User", self.userName, " --- Token: ", json_var['token'])
        self.user_token = json_var['token']
    
    @task 
    def post_jac_prog(self):
        req = {
                'name': 'jac_prog',
                'code': 'walker init {}'
                }
        response = self.client.post("/js/sentinel_register",headers = {'authorization' : f'Token {self.user_token}'}, json = req)
        print("Status Code: ", response.json())
        self.sentinel_jid = response.json()[0]['jid']

    @task
    def walker_run(self):
        req = {
                'name': 'init',
                'snt': self.sentinel_jid
                }
        response = self.client.post("/js/walker_run",headers = {'authorization' : f'Token {self.user_token}'}, json = req)
        print("Status Code: ", response.json())
	# @task
	# def register_senitel(self):
	# 	print("Token for user: ", self.userName, " is --- ", self.zsb_token)
	# 	req = {

    #         "name": "zsb",
    #         "code": "",   # need to take from .jac file and convert to escape sequence and insert here

    #     }
	# 	response = self.client.post("/jac/senitel_register", headers={"authorization": "Token " + self.zsb_token}, json=req)
	# 	json_var = response.json()
	# @task
	# def set_senitel(self):
	# 	print("Token for user: ", self.userName, " is --- ", self.zsb_token)
	# 	req = {

    #         "name": "zsb",
    #         "code": "",   # need to take from .jac file and convert to escape sequence and insert here

    #     }
	# 	response = self.client.post("/jac/senitel_set", headers={"authorization": "Token " + self.zsb_token}, json=req)
	# 	json_var = response.json()


class addJac(RestUser):
    host = "http://127.0.0.1:8888"
    tasks = [SeqTask]
    wait_time = constant(2)
