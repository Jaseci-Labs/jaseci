import json
from locust import task, HttpUser, SequentialTaskSet, constant, HttpUser
import os
from credentials import gen_username, gen_password

TEST_PATH = "sample_code/bi_enc_test"


def format_output(userName: str, output: str):
    print(f"{userName}: {output}")


def get_code(path: str) -> str:
    file = open(path, "r")
    code = file.read()
    file.close()
    return code


UserID = 0
actionLoaded = False


def print_response(response):
    failure = False
    if response.status_code != 200 and response.status_code != 201:
        failure = True
    success = response.json().get("success", False)
    if not success:
        failure = True
    if failure:
        print(response.text)


def load_config(path: str):
    config_path = os.path.join(path, "config.json")
    config = json.load(open(config_path, "r"))
    src = config.get("src", "")
    src = os.path.join(path, src)
    config["src"] = src
    return config


class SeqTask(SequentialTaskSet):
    def on_start(self):
        self.userName = "Not_exist"  # Initialize
        self.password = "Not_exist"
        self.zsb_token = "None"
        self.zsb_jid = "None"
        global UserID
        self.userName, self.password = gen_username(UserID), gen_password(UserID)
        self.userID = UserID
        UserID += 1

    @task
    def generate_userToken(self):
        response = self.client.post(
            "/user/token/", json={"email": self.userName, "password": self.password}
        )
        format_output(self.userName, response.text)
        json_var = response.json()
        self.user_token = json_var["token"]

    @task
    def post_jac_prog(self):
        req = {
            "name": "jac_prog",
            "code": get_code(load_config(TEST_PATH)["src"]),
        }
        response = self.client.post(
            "/js/sentinel_register",
            headers={"authorization": f"Token {self.user_token}"},
            json=req,
        )
        self.sentinel_jid = response.json()[0]["jid"]

    @task
    def load_actions(self):
        global actionList
        global actionLoaded
        if actionLoaded:
            return
        actionLoaded = True
        for action in load_config(TEST_PATH)["remote_actions"]:
            response = self.client.post(
                "/js_admin/actions_load_remote",
                headers={"authorization": f"Token {self.user_token}"},
                json={"url": action},
            )
            # print(f"response: {response.text}")
            print_response(response)
        for action in load_config(TEST_PATH)["local_actions"]:
            response = self.client.post(
                "/js_admin/actions_load_local",
                headers={"authorization": f"Token {self.user_token}"},
                json={"file": action},
            )
            # print(f"response: {response.text}")
            print_response(response)

        response = self.client.post(
            "/js_admin/actions_list",
            headers={"authorization": f"Token {self.user_token}"},
        )
        print(f"Actions list response: {response.text}")

    @task
    def walker_run(self):
        for walkerName in load_config(TEST_PATH)["walkers"]:
            req = {"name": walkerName, "snt": self.sentinel_jid}
            # print(f"Walker {walkerName} running.")
            response = self.client.post(
                "/js/walker_run",
                headers={"authorization": f"Token {self.user_token}"},
                json=req,
            )
            print(f"Walker {walkerName} finished. {response.text}")
            # print(f"Walker {walkerName} Output: {response.json()}")


class addJac(HttpUser):
    host = "http://127.0.0.1:8888"
    tasks = [SeqTask]
    wait_time = constant(2)
