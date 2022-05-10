import logging
from locust import task, HttpUser, SequentialTaskSet, constant
from locust_plugins.users import RestUser

def format_output(userName:str, output:str):
    print(f'{userName}: {output}')
# Admin LOGIN
# code = 'walker init {report "admin";}'
def get_code(path: str)->str:
    file = open(path, 'r')
    code = file.read()
    file.close()
    return code

def gen_username(id : int)->str:
    return f'jaclang{id}@jaseci.org'

def gen_password(id : int)->str:
    return f'ilovejaclang{id}'


UserID = 0
actionLoaded = False

walkerSequence = ['createPredefines', 'segmenter']
actionList = ['http://fair-ner:80/']

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

    @task
    def create_user(self):
        response = self.client.post("/user/create/", json = {
            "email" : self.userName,
            "password" : self.password,
            "is_activated": True,
            "is_superuser": False
        })
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
        self.user_token = json_var['token']

    
    @task 
    def post_jac_prog(self):
        req = {
                'name': 'jac_prog',
                'code': get_code('../../examples/JPrime/jprime.jac'),
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
            print(f"{action} loaded")

    @task
    def walker_run(self):
        for walkerName in walkerSequence:
            req = {
                    'name': walkerName,
                    'snt': self.sentinel_jid
                    }
            response = self.client.post("/js/walker_run",headers = {'authorization' : f'Token {self.user_token}'}, json = req)
            print(f"Walker {walkerName} Output: {response.json()}")
    
    

class addJac(RestUser):
    host = "http://127.0.0.1:8888"
    tasks = [SeqTask]
    wait_time = constant(2)
