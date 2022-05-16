import os
import json
def gen_username(id: int) -> str:
    return f"jaclang{id}@jaseci.org"


def gen_password(id: int) -> str:
    return f"ilovejaclang{id}"

def load_config(path: str):
    config_path = os.path.join(path, "config.json")
    config = json.load(open(config_path, "r"))
    src = config.get("src", "")
    src = os.path.join(path, src)
    config["src"] = src
    return config

def get_code(path: str) -> str:
    file = open(path, "r")
    code = file.read()
    file.close()
    return code
