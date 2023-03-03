import requests
import json
import config
from util import authenticate, port_fowrward

# Authenticate
token = authenticate()

# Get redis config
payload = {"name": "REDIS_CONFIG"}
headers = {"content-type": "application/json", "Authorization": f"Token {token}"}
res = requests.post(
    url=config.url + "/js_admin/config_get", headers=headers, json=payload
)
redis_config = json.loads(res.json())

# Update redis config to point out at the right one
redis_config["automated"] = False
redis_config["host"] = "lljasecidev-redis.default.svc.cluster.local"

# Set meta config
payload = {"name": "REDIS_CONFIG", "value": json.dumps(redis_config)}
headers = {"content-type": "application/json", "Authorization": f"Token {token}"}
res = requests.post(
    url=config.url + "/js_admin/config_set", headers=headers, json=payload
)

# Refresh the service for the config to take effect
payload = {"name": "redis"}
headers = {"content-type": "application/json", "Authorization": f"Token {token}"}
res = requests.post(
    url=config.url + "/js_admin/service_refresh", headers=headers, json=payload
)


# Get task config
payload = {"name": "TASK_CONFIG"}
headers = {"content-type": "application/json", "Authorization": f"Token {token}"}
res = requests.post(
    url=config.url + "/js_admin/config_get", headers=headers, json=payload
)
task_config = json.loads(res.json())

# Update task config to use the correct redis
task_config["broker_url"] = "redis://lljasecidev-redis.default.svc.cluster.local:6379/1"

# Set meta config
payload = {"name": "TASK_CONFIG", "value": json.dumps(redis_config)}
headers = {"content-type": "application/json", "Authorization": f"Token {token}"}
res = requests.post(
    url=config.url + "/js_admin/config_set", headers=headers, json=payload
)

# Refresh the service for the config to take effect
payload = {"name": "task"}
headers = {"content-type": "application/json", "Authorization": f"Token {token}"}
res = requests.post(
    url=config.url + "/js_admin/service_refresh", headers=headers, json=payload
)
