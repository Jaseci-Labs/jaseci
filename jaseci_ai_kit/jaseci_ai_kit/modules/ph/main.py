from http.client import ImproperConnectionState
from typing import Any
from jaseci.actions.live_actions import jaseci_action
import warnings
import os
import traceback
from fastapi import HTTPException

from .utils.util import read_yaml, write_yaml
from .inference import InferenceList
from .train import train


HEAD_NOT_FOUND = "No Active head found. Please create a head first using create_head."
HEAD_LIST_NOT_FOUND = (
    "No Active head list found. Please create a head list first using create_head_list."
)


warnings.filterwarnings("ignore")


def setup():
    global config, il
    dirname = os.path.dirname(__file__)
    config = read_yaml(os.path.join(dirname, "config.yaml"))
    il = InferenceList()


setup()

### Start of PersonalizedHead Actions ###


@jaseci_action(act_group=["ph"], allow_remote=True)
def create_head_list(config_file: str, overwrite: bool = False) -> None:
    """
    Create a holder for heads
    """
    print("Creating head list")
    try:
        global il, config
        new_config = read_yaml(config_file)
        config = {**config, **new_config}
        il = InferenceList(config=config)
        if overwrite:
            write_yaml(config, config_file)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["ph"], allow_remote=True)
def create_head(
    config_file: str = None, uuid: str = None, overwrite: bool = False
) -> None:
    """
    Create a personalized head. This will create a new inference engine.
    @param new_config: new config to be used for the head
    """
    try:
        global il, config
        if config_file:
            new_config = read_yaml(config_file)
            config = {**config, **new_config}
            if overwrite:
                write_yaml(config, config_file)
            _uuid = il.add(config=config, uuid=uuid)
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
        else:
            raise Exception(HEAD_LIST_NOT_FOUND)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["ph"], allow_remote=True)
def train_head(config_file: str = None, uuid: str = None) -> None:
    """
    Train the current active model.
    @param new_config: new config yaml to be used for training
    """
    try:
        global config
        new_config = read_yaml(config_file)
        config = {**config, **new_config}
        write_yaml(config, config_file)
        train({"config": config_file, "device": None, "resume": None, "uuid": uuid})
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["ph"], allow_remote=True)
def load_weights(uuid: str, path: str) -> None:
    try:
        global il
        if il:
            try:
                il.load_weights(uuid, path)
            except ImproperConnectionState:
                raise Exception(HEAD_NOT_FOUND)
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
