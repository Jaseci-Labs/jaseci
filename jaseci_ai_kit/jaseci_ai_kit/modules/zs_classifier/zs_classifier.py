from typing import List, Union
from fastapi import HTTPException
from jaseci.actions.live_actions import jaseci_action

# import torch
from flair.models import TARSClassifier
from flair.data import Sentence

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def init_model():
    """load the tars classifier for ZS classification"""

    global classifier
    model_name = "tars-base"
    classifier = TARSClassifier.load(model_name)
    print(f"loaded mode : [{model_name}]")


# initialize the classifier
init_model()


# defining the api for ZS classification
@jaseci_action(act_group=["zs_classifier"], allow_remote=True)
def classify(text: Union[str, List[str]], classes: List[str]):
    """
    API for classifying text among classes provided
    """
    response_data_format = []
    try:
        if isinstance(text, list):
            for sent_text in text:
                resp_data = {}
                sent = Sentence(sent_text)
                # predicting class for the text
                classifier.predict_zero_shot(sent, classes)
                pred_output = sent.to_dict()
                resp_data[pred_output["text"]] = pred_output["all labels"]
                response_data_format.append(resp_data)
        else:
            sent = Sentence(text)
            classifier.predict_zero_shot(sent, classes)
            pred_output = sent.to_dict()
            resp_data = {}
            resp_data[pred_output["text"]] = pred_output["all labels"]
            response_data_format.append(resp_data)
        return response_data_format
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(f"Exception :{e}"))


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    launch_server(port=8000)
