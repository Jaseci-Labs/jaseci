from jaseci.jsorc.live_actions import jaseci_action
from jaseci.jsorc.remote_actions import launch_server
from fastapi import HTTPException

from .action_utils import create_series


@jaseci_action(act_group=["forecast"], allow_remote=True)
def preprocess(time: list, variables: dict):
    try:
        global timeseries
        timeseries = create_series(time, variables)
        return "time series data created"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["forecast"], allow_remote=True)
def forecast():
    pass
