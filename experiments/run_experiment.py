import requests
import json
import config
from util import port_fowrward, authenticate

# Port forward
port_fowrward()

# Authenticate
token = authenticate()

# Run experiment
payload = {
    "test": "synthetic_apps",
    "experiment": "discussion_analysis",
    "mem": 4,
    "policy": "all_remote",
}
headers = {"content-type": "application/json", "Authorization": f"Token {token}"}
res = requests.post(
    url=config.url + "/js_admin/jsorc_loadtest", headers=headers, json=payload
)
print(res.json())
