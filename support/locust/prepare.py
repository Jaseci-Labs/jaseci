import requests
import utils
import os


TEST_PATH = os.environ.get("LOCUST_TEST_SRC", "")
HOST = os.environ.get("LOCUST_HOST", "http://localhost:8888")

# Log in as user 0, return the token
def login():
    userName = utils.gen_username(0)
    password = utils.gen_password(0)
    response = requests.post(
        HOST + "/user/token/", json={"email": userName, "password": password}
    )
    return response.json()["token"]


# register sentinel, return the jid
def registerSentinel(token: str):
    req = {
        "name": "jac_prog",
        "code": utils.get_code(utils.load_config(TEST_PATH)["src"]),
    }
    response = requests.post(
        HOST + "/js/sentinel_register",
        headers={"authorization": f"Token {token}"},
        json=req,
    )
    return response.json()[0]["jid"]


def setSentinelGlobal(token: str, snt: str):
    response = requests.post(
        HOST + "/js_admin/global_sentinel_set",
        headers={"authorization": f"Token {token}"},
        json={"snt": snt},
    )


def load_actions(token: str):
    for action in utils.load_config(TEST_PATH)["remote_actions"]:
        response = requests.post(
            HOST + "/js_admin/actions_load_remote",
            headers={"authorization": f"Token {token}"},
            json={"url": action},
        )
    for action in utils.load_config(TEST_PATH)["local_actions"]:
        response = requests.post(
            HOST + "/js_admin/actions_load_local",
            headers={"authorization": f"Token {token}"},
            json={"file": action},
        )

    response = requests.post(
        HOST + "/js_admin/actions_list",
        headers={"authorization": f"Token {token}"},
    )

    # print(response.text)
