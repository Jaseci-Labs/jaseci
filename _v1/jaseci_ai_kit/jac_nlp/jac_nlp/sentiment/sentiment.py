import warnings

from jaseci.jsorc.live_actions import jaseci_action
from jaseci.jsorc.remote_actions import launch_server
from fastapi import HTTPException

from transformers import pipeline

model = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis")


@jaseci_action(act_group=["sentiment"], allow_remote=True)
def predict(texts: list):
    try:
        prediction_list = model(texts)
        return prediction_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
