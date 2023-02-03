import requests
import subprocess
import config

# Authenticate
def authenticate():
    payload = {"email": config.user_email, "password": config.user_pw}
    res = requests.post(url=config.url + "/user/token/", json=payload)
    token = res.json()["token"]
    return token


# Port forward, useful for local experiment
def port_fowrward():
    cmd = "kubectl port-forward svc/jaseci 8000:80"
    proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    subprocess.run(["sleep", "1"])
