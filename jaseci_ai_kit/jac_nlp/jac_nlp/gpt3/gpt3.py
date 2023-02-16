import os
import openai
from jaseci.actions.live_actions import jaseci_action
import traceback
from fastapi import HTTPException

TASKS = {
    "q&a": {
        "model": "text-davinci-003",
        "temperature": 0,
        "max_tokens": 100,
        "top_p": 1,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "stop": ["\n"],
    },
}


def setup(api_key: str):
    if api_key:
        openai.api_key = api_key
    else:
        raise HTTPException(status_code=400, detail="OPENAI_API_KEY not set")


setup(api_key=os.environ.get("OPENAI_API_KEY", None))


@jaseci_action(act_group=["gpt2"], allow_remote=True)
def generate(text: str, task: str = None, args: dict = {}):
    if task and task in TASKS:
        default_args = TASKS[task]
        default_args.update(args)
    elif task:
        raise HTTPException(status_code=400, detail=f"task {task} not found")
    elif args:
        default_args = args
    else:
        raise HTTPException(status_code=400, detail=f"task or args must be provided")

    try:
        response = openai.Completion.create(prompt=text, **default_args)
        return response
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
