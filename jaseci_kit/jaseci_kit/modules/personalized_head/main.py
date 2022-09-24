from typing import Any, Dict
from jaseci.actions.live_actions import jaseci_action
import warnings
import os
import traceback
from fastapi import HTTPException

from .utils import read_yaml, write_yaml
from .inference import InferenceEngine
from .train import train


MODEL_NOT_FOUND = "No Active model found. Please create a model first using create_head."


warnings.filterwarnings("ignore")


def setup():
    global config, ie
    dirname = os.path.dirname(__file__)
    config = read_yaml(os.path.join(dirname, "config.yaml"))
    ie = None


setup()

### Start of PersonalizedHead Actions ###


@jaseci_action(act_group=["personalized_head"], allow_remote=True)
def create_head(new_config: Dict = None):
    '''
    Create a personalized head. This will create a new inference engine.
    @param new_config: new config to be used for the head
    '''
    try:
        global ie, config
        if new_config:
            config = {**config, **new_config}
        ie = InferenceEngine(config, "ph")
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["personalized_head"], allow_remote=True)
def predict(data: Any) -> Any:
    '''
    Predict using the current active model.
    @param data: data to be used for prediction
    '''
    try:
        global ie
        if ie:
            return int(ie.predict(data).argmax())
        else:
            raise Exception(MODEL_NOT_FOUND)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["personalized_head"], allow_remote=True)
def train_model(config_file: str = None):
    '''
    Train the current active model.
    @param new_config: new config yaml to be used for training
    '''
    try:
        global ie, config
        new_config = read_yaml(config_file)
        config = {**config, **new_config}
        # overwrite the config file with config
        write_yaml(config, config_file)
        train({
            "config": config_file,
            "device": None,
            "resume": None,
        })
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["personalized_head"], allow_remote=True)
def load_weights(path: str):
    try:
        global ie
        if ie:
            ie.load_weights(path)
        else:
            raise Exception(MODEL_NOT_FOUND)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

### End of PersonalizedHead Actions ###


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server
    launch_server(port=8000)
