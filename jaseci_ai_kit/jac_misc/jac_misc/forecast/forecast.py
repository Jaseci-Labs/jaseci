from jaseci.jsorc.live_actions import jaseci_action
from jaseci.jsorc.remote_actions import launch_server
from fastapi import HTTPException


@jaseci_action(act_group=["forecast"], allow_remote=True)
def preprocess():
    pass


@jaseci_action(act_group=["forecast"], allow_remote=True)
def forecast():
    pass
