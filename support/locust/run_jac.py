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
        UserID += 1

    @task
    def generate_userToken(self):
        response = self.client.post(
            "/user/token/", json={"email": self.userName, "password": self.password}
        )
        format_output(self.userName, response.text)
        json_var = response.json()
        self.user_token = json_var["token"]

    # @task
    # def get_global_sentinel(self):
    #     req = {
    #             "snt": SNT
    #             }
    #     response = self.client.post(
    #             '/js/sentinel_active_global',
    #             headers = {"authorization": f"Token {self.user_token}"},
    #             )
    #     print(response.text)
    # @task
    @task
    def get_sentinel(self):
        print(SNT)
        headers = {"authorization": f"Token {self.user_token}"}
        response = self.client.post(
            "/js/sentinel_active_global", headers=headers, json={"detailed": False}
        )
        print("GET_SNT:", response.text)

    #     self.snt = prepare.registerSentinel(self.user_token)
    #     prepare.load_actions(self.user_token)

    @task
    def create_graph(self):

        headers = {"authorization": f"Token {self.user_token}"}
        response = self.client.post(
            "/js/graph_create", headers=headers, json={"set_active": True}
        )
        print(response.text)
        self.graph_id = response.json()["jid"]

    @task
    def walker_run(self):
        for walkerName in load_config(TEST_PATH)["walkers"]:
            req = {"name": walkerName, "snt": SNT}
            # print(f"Walker {walkerName} running.")
            response = self.client.post(
                "/js/walker_run",
                headers={"authorization": f"Token {self.user_token}"},
                json=req,
            )
            print(
                f"User {self.userName}: Walker {walkerName} finished. {response.text}"
            )

    @task
    def delete_graph(self):

        headers = {"authorization": f"Token {self.user_token}"}
        response = self.client.post(
            "/js/graph_delete", headers=headers, json={"gph": self.graph_id}
        )


class addJac(HttpUser):
    host = "http://127.0.0.1:8888"
    tasks = [SeqTask]
    wait_time = constant(0)


token = prepare.login(userID=0)
# # global SNT
SNT = prepare.registerSentinel(token)
prepare.setSentinelGlobal(token=token, snt=SNT)
prepare.load_actions(token)
