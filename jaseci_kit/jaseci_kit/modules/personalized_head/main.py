from typing import Any, Dict
from jaseci.actions.live_actions import jaseci_action
import warnings
import os
import traceback
from fastapi import HTTPException

from utils import read_yaml
from inference import InferenceEngine


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
def train(new_config: Dict = None):
    '''
    Train the current active model.
    @param new_config: new config to be used for training
    '''
    try:
        global ie, config
        if new_config:
            config = {**config, **new_config}
        # TODO: train the model
        # TODO: return Metrics
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["personalized_head"], allow_remote=True)
def load_weights(path: str):
    try:
        global ie
        if ie:
            ie.load_weights(path)
            # TODO: Update the Configuration File with new weights
        else:
            raise Exception(MODEL_NOT_FOUND)
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

### End of PersonalizedHead Actions ###


# Module Compositor Start
'''
TODO: Compositor creator (create_composite)

Args:
---- List of Modules: list
---- parameters: list<dict>
'''

'''
TODO: predict (predict)

Args:
---- input
Return:
---- output
'''

'''
TODO: train (train)

Args:
---- dataset
'''
# Module Compositor End

# action load compositor
# can compositor.create_composite

# create_compistor([use_enc, personalized_header],["", {
#     yaml:
#     ajdnas:
# }])
# compositor.predict('user_1', input) --> output;
# compositor.train(dataset, user_1);

# similar image ---> text ----> image
# image, imge2

if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server
    launch_server(port=8000)
