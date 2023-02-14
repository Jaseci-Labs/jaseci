from http.client import ImproperConnectionState
from typing import Any, Dict
import warnings
import os
import traceback
from fastapi import HTTPException
import logging

from jaseci.actions.live_actions import jaseci_action

from .utils.util import read_yaml, deep_update, save_custom_python
from .inference import InferenceList

warnings.filterwarnings("ignore")


HEAD_NOT_FOUND = "No Active head found. Please create a head first using create_head."
HEAD_LIST_NOT_FOUND = "No Active head list found. Use create_head_list first."


def setup():
    global il, list_config
    dirname = os.path.dirname(__file__)
    list_config = read_yaml(os.path.join(dirname, "config.yaml"))
    if os.path.exists("heads/config.yaml") and os.path.exists("heads/custom.py"):
        logging.warning("Found a heads list in the current directory. Loading it ...")
        il = InferenceList(config=read_yaml("heads/config.yaml"))
    else:
        logging.info("No heads list found. Run create_head_list to create one.")
        il = None


setup()

### Start of PersonalizedHead Actions ###


@jaseci_action(act_group=["ph"], allow_remote=True)
def create_head_list(config: Dict = None, python: str = None) -> None:
    """
    Create a holder for all the heads
    """
    try:
        global il, list_config
        if config:
            deep_update(list_config, config)
        if python:
            os.makedirs("heads", exist_ok=True)
            save_custom_python(python)
        il = InferenceList(config=list_config)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["ph"], allow_remote=True)
def create_head(uuid: str = None, config: Dict = None) -> None:
    """
    Create a personalized head. This will create a new inference engine.
    @param config: new config to be used for the head
    """
    try:
        global il, list_config
        if config:
            head_config = list_config.copy()
            deep_update(head_config, config)
            _uuid = il.add(config=head_config, uuid=uuid)
        else:
            _uuid = il.add(uuid=uuid)
        return _uuid
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["ph"], allow_remote=True)
def predict(uuid: str, data: Any) -> Any:
    """
    Predict using the current active model.
    @param data: data to be used for prediction
    """
    try:
        global il
        if il:
            try:
                return il.predict(uuid, data)
            except ImproperConnectionState:
                raise Exception(HEAD_NOT_FOUND)
            except Exception as e:
                raise e
        else:
            raise Exception(HEAD_LIST_NOT_FOUND)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["ph"], allow_remote=True)
def train_head(uuid: str, config: Dict = None, auto_update: bool = True) -> None:
    """
    Train the current active model.
    @param config: new config to be used for training
    """
    try:
        global il
        if il:
            try:
                il.train(uuid, config, auto_update)
            except ImproperConnectionState:
                raise Exception(HEAD_NOT_FOUND)
            except Exception as e:
                raise e
        else:
            raise Exception(HEAD_LIST_NOT_FOUND)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["ph"], allow_remote=True)
def get_config(uuid: str) -> Dict:
    """
    Get the config of the personalized head.
    """
    try:
        global il
        if il:
            try:
                return il.get_config(uuid)
            except ImproperConnectionState:
                raise Exception(HEAD_NOT_FOUND)
            except Exception as e:
                raise e
        else:
            raise Exception(HEAD_LIST_NOT_FOUND)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["ph"], allow_remote=True)
def check_head(uuid: str) -> bool:
    try:
        global il
        if il:
            return il.check(uuid)
        else:
            raise Exception(HEAD_LIST_NOT_FOUND)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


### End of PersonalizedHead Actions ###


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    launch_server(port=8000)
