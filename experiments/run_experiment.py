import requests
import config
from util import port_fowrward, authenticate

# Port forward
port_fowrward()

# Authenticate
token = authenticate()

# Run experiment
payload = {
    "test": "synthetic_apps",
    "experiment": "restaurant_chatbot",
    "mem": 4,
    "policy": "evaluation",
    "experiment_duration": 3 * 60,
}
headers = {"content-type": "application/json", "Authorization": f"Token {token}"}
res = requests.post(
    url=config.url + "/js_admin/jsorc_loadtest",
    headers=headers,
    json=payload,
    timeout=None,
)
print(res.json())
