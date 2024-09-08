from jaseci.jsorc.live_actions import jaseci_action
from jaseci.utils.utils import logger
import requests
from .utils import API_ENDPOINTS
import os


@jaseci_action(act_group=["hf"], allow_remote=True)
def setup(api_key: str = os.environ.get("HUGGINGFACE_API_KEY", None)):
    if not api_key:
        logger.error(
            "Huggingface API key not found. Please set the environment variable HUGGINGFACE_API_KEY or pass it as an argument to the setup function using actions call hf.setup"
        )
        return False
    else:
        os.environ["HUGGINGFACE_API_KEY"] = api_key
        return True


@jaseci_action(act_group=["hf"], allow_remote=True)
def query(
    task: str = None,
    model: str = "default",
    api_url: str = None,
    api_type: str = None,
    **kwargs,
):
    if not os.environ.get("HUGGINGFACE_API_KEY", None):
        logger.error(
            "Huggingface API key not found. Please set the environment variable HUGGINGFACE_API_KEY or pass it as an argument to the setup function using actions call hf.setup"
        )
        return
    if task and (task not in API_ENDPOINTS or model not in API_ENDPOINTS[task]):
        logger.error(
            f"Task {task} or model {model} not found. Please check the documentation for a list of available tasks and models."
        )
        return
    if not task and not api_type and not api_url:
        logger.error(
            "Please pass either a task and model or an api_type and api_url. Please check the documentation for a list of available tasks and models."
        )
        return

    HEADERS = {"Authorization": f"Bearer {os.environ['HUGGINGFACE_API_KEY']}"}

    API_URL = API_ENDPOINTS[task][model]["API_URL"] if not api_url else api_url
    API_TYPE = API_ENDPOINTS[task][model]["API_TYPE"] if not api_type else api_type

    if API_TYPE == "file":
        file = kwargs.pop("file", None)
        if not file:
            logger.error(
                "No files were passed. Please pass a file using the files argument."
            )
            return
        with open(file, "rb") as f:
            data = f.read()
        response = requests.post(API_URL, headers=HEADERS, data=data)
    elif API_TYPE == "input":
        response = requests.post(
            API_URL, headers=HEADERS, json={"inputs": kwargs["inputs"]}
        )
    return response.json()
