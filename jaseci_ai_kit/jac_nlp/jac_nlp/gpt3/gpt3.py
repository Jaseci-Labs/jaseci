import os
import openai
from jaseci.actions.live_actions import jaseci_action
import traceback
from fastapi import HTTPException

DEFAULT_ARGS = {
    "model": "text-davinci-003",
    "temperature": 0,
    "max_tokens": 100,
    "top_p": 1,
    "frequency_penalty": 0.0,
    "presence_penalty": 0.0,
}


def setup(api_key: str):
    if api_key:
        openai.api_key = api_key
    else:
        print(
            "Please provide an API key through the OPENAI_API_KEY environment variable or the set_api_key action."
        )


setup(api_key=os.environ.get("OPENAI_API_KEY", None))


@jaseci_action(act_group=["gpt3"], allow_remote=True)
def set_api_key(api_key: str):
    try:
        setup(api_key)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["gpt3"], allow_remote=True)
def generate(text: str, args: dict = DEFAULT_ARGS):
    try:
        response = openai.Completion.create(prompt=text, **args)
        return response["choices"]
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    launch_server(port=8000)
