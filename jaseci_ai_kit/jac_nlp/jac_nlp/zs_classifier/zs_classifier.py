from typing import List, Union

import numpy as np
from fastapi import HTTPException
from flair.data import Sentence
from flair.models import TARSClassifier
from jaseci.actions.live_actions import jaseci_action


def init_model():
    """load the tars classifier for ZS classification"""
    global classifier
    model_name = "tars-base"
    classifier = TARSClassifier.load(model_name)
    print(f"loaded mode : [{model_name}]")


# initialize the classifier
init_model()


# API for getting the cosine similarity
@jaseci_action(act_group=["bi_enc"], allow_remote=True)
def cosine_sim(vec_a: List[float], vec_b: List[float]):
    """
    Caculate the cosine similarity score of two given vectors
    Param 1 - First vector
    Param 2 - Second vector
    Return - float between 0 and 1
    """

    result = np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
    return result.astype(float)


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


@jaseci_action(act_group=["zs_classifier"], allow_remote=True)
def get_embeddings(texts: Union[str, List[str]]):
    """
    API to get embbeddings for text
    """
    embedder = classifier.tars_embeddings
    if isinstance(texts, str):
        label_sentences = Sentence([texts])
        embedder.embed(label_sentences)
        return label_sentences.get_embedding().cpu().detach().numpy().tolist()
    else:
        embedding_list = []
        for text in texts:
            label_sentences = Sentence(text)
            embedder.embed(label_sentences)
            embedding_list.append(
                label_sentences.get_embedding().cpu().detach().numpy().tolist()
            )
        return embedding_list


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    launch_server(port=8000)
