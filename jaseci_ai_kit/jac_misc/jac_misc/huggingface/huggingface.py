from jaseci.jsorc.live_actions import jaseci_action
from jaseci.utils.utils import logger
import requests
from utils import API_ENDPOINTS
import os

@jaseci_action(act_group=["hf"], allow_remote=True)
def setup(api_key:str = os.environ.get('HUGGINGFACE_API_KEY', None)):
    if not api_key:
        logger.error("Huggingface API key not found. Please set the environment variable HUGGINGFACE_API_KEY or pass it as an argument to the setup function using actions call hf.setup")
        return False
    else:
        os.environ['HUGGINGFACE_API_KEY'] = api_key
        return True

@jaseci_action(act_group=["hf"], allow_remote=True)
def query(task:str, model:str = "default", **kwargs):
    if not os.environ.get('HUGGINGFACE_API_KEY', None):
        logger.error("Huggingface API key not found. Please set the environment variable HUGGINGFACE_API_KEY or pass it as an argument to the setup function using actions call hf.setup")
        return
    if task not in API_ENDPOINTS or model not in API_ENDPOINTS[task]:
        logger.error(f"Task {task} or model {model} not found. Please check the documentation for a list of available tasks and models.")
        return
    if kwargs.keys() != set(API_ENDPOINTS[task][model]["PARAMETERS"]):
        logger.error(f"Parameters {kwargs.keys()} do not match the expected parameters {API_ENDPOINTS[task][model]['PARAMETERS']}")
        return
    
    HEADERS = {"Authorization": f"Bearer {os.environ['HUGGINGFACE_API_KEY']}"}
    API_URL = API_ENDPOINTS[task][model]["API_URL"]
    response = requests.post(API_URL, headers=HEADERS, json=kwargs)
    return response.json()