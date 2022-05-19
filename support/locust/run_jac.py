from locust import task, HttpUser, SequentialTaskSet, constant, HttpUser
import os
from utils import gen_username, gen_password, load_config
import prepare

TEST_PATH = os.environ.get("LOCUST_TEST_SRC", "")
SNT = ""


def format_output(userName: str, output: str):
    print(f"{userName}: {output}")


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


class SeqTask(SequentialTaskSet):
    def on_start(self):
        self.userName = "Not_exist"  # Initialize
        self.password = "Not_exist"
        self.zsb_token = "None"
        self.zsb_jid = "None"
        global UserID
        self.userName, self.password = gen_username(UserID), gen_password(UserID)
        self.userID = UserID
        token = prepare.login(userID = UserID)
        # global SNT
        self.snt = prepare.registerSentinel(token)
        prepare.load_actions(token)
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
    def walker_run(self):
        for walkerName in load_config(TEST_PATH)["walkers"]:
            req = {"name": walkerName, "snt": self.snt}
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




