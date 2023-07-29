from jaseci.jsorc.live_actions import jaseci_action
from jaseci.jsorc.remote_actions import launch_server
from fastapi import HTTPException

from .action_utils import create_series, train_test_split


@jaseci_action(act_group=["forecast"], allow_remote=True)
def preprocess(time: list, variables: dict):
    try:
        global timeseries
        timeseries = create_series(time, variables)
        return "Time series object created successfully!"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["forecast"], allow_remote=True)
def split(cuttoff: str, scale: bool):
    try:
        global train
        global validation
        train, validation = train_test_split(timeseries, cuttoff, scale)
        return "Data splitted in to train and validation successfully!"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["forecast"], allow_remote=True)
def create_model():
    pass


@jaseci_action(act_group=["forecast"], allow_remote=True)
def forecast():
    pass
