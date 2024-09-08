import requests
import json
import config
from util import authenticate, port_fowrward

# Port forward
port_fowrward()

# Authenticate
token = authenticate()

# Get meta config
payload = {"name": "META_CONFIG"}
headers = {"content-type": "application/json", "Authorization": f"Token {token}"}
res = requests.post(
    url=config.url + "/js_admin/config_get", headers=headers, json=payload
)
meta_config = json.loads(res.json())

# Update meta config to set automation = True
meta_config["automation"] = True

# Set meta config
payload = {"name": "META_CONFIG", "value": json.dumps(meta_config)}
headers = {"content-type": "application/json", "Authorization": f"Token {token}"}
res = requests.post(
    url=config.url + "/js_admin/config_set", headers=headers, json=payload
)


# Refresh the service for the config to take effect
payload = {"name": "meta"}
headers = {"content-type": "application/json", "Authorization": f"Token {token}"}
res = requests.post(
    url=config.url + "/js_admin/service_refresh", headers=headers, json=payload
)
print(res.json())
