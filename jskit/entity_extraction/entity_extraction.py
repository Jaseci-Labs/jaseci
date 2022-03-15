from typing import List
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.models import TARSTagger
from flair.data import Sentence
from flair.trainers import ModelTrainer
import pandas as pd
from utils import create_data
import configparser
from jaseci.actions.live_actions import jaseci_action
import torch
from pathlib import Path

config = configparser.ConfigParser()
config.read('config.cfg')


TARS_MODEL_NAME = config['TARS_MODEL']['NER_MODEL']
NER_LABEL_TYPE = config['LABEL_TYPE']['NER']
# Load zero-shot NER tagger
tars = TARSTagger.load(TARS_MODEL_NAME)
device = torch.device("cpu")
# uncomment this if you wish to use GPU to train
# this is commented out because this causes issues with
# unittest on machines with GPU
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def train_entity():
    """
    funtion for training the model
    """
    global tars
    # define columns
    columns = {0: 'text', 1: 'ner'}
    # directory where the data resides
    data_folder = 'train'
    # initializing the corpus
    corpus: Corpus = ColumnCorpus(data_folder, columns,
                                  train_file='train.txt')
    tag_type = 'ner'
    # make tag dictionary from the corpus
    tag_dictionary = corpus.make_tag_dictionary(tag_type=tag_type)

    # make the model aware of the desired set of labels from the new corpus
    tars.add_and_switch_to_new_task(
        "ner tagging", label_dictionary=tag_dictionary, label_type=tag_type)
    #  initialize the text classifier trainer with your corpus
    trainer = ModelTrainer(tars, corpus)
    # train model
    trainer.train(base_path='train/ner_tagging',  # path to store the model artifacts
                  learning_rate=0.02,
                  mini_batch_size=1,
                  max_epochs=10,
                  train_with_test=True,
                  train_with_dev=True

                  )
    #  Load trained TARS model
    tars = TARSTagger.load('train/ner_tagging/final-model.pt')
    print("model training and loading completed")


# defining the api for entitydetection
@jaseci_action(act_group=['ent_ext'], allow_remote=False)
def entity_detection(text: str, ner_labels: List[str]):
    """
    API for detectiing provided entity in text
    """
    global tars
    if text:
        if ner_labels:
            tars.add_and_switch_to_new_task(
                'Entity Detection Task', ner_labels, label_type=NER_LABEL_TYPE)
            sentence = Sentence(text)
            # predicting entities in the text
            tars.predict(sentence)
            tagged_sentence = sentence.to_dict(NER_LABEL_TYPE)
            json_compatible_data = jsonable_encoder(tagged_sentence)
            response_data_format = {
                "input_text": json_compatible_data["text"], "entities": []}
            for json_data in json_compatible_data["entities"]:
                temp_dict = {}
                temp_dict["entity_text"] = json_data["text"]
                temp_dict["entity_value"] = json_data["labels"][0]["_value"]
                temp_dict["conf_score"] = json_data["labels"][0]["_score"]
                response_data_format['entities'].append(temp_dict)
            return response_data_format
        else:
            raise HTTPException(status_code=404, detail=str(
                "NER Labels are missing in request data"))
    else:
        raise HTTPException(status_code=404, detail=str(
            "Text data is missing in request data"))


@jaseci_action(act_group=['ent_ext'], allow_remote=False)
def train(text: str, entity: List[dict]):
    """
    API for training the model
    """
    tag = []
    if text and entity:
        for ent in entity:
            if ent['entity_value'] and ent['entity_name']:
                tag.append((ent['entity_value'], ent['entity_name']))
            else:
                raise HTTPException(status_code=404, detail=str(
                    "Entity Data missing in request"))
            data = pd.DataFrame([[text, tag
                                  ]], columns=['text', 'annotation'])
            # creating training data
            if create_data(data):
                train_entity()
                return "Model Training is Completed"
            else:
                raise HTTPException(status_code=500, detail=str(
                    "Issue encountered during train data creation"))
    else:
        raise HTTPException(status_code=404, detail=str(
            "Need Data for Text and Entity"))


@jaseci_action(act_group=['ent_ext'], allow_remote=False)
def save_model(model_path: str):
    """
    saves the model to the provided model_path
    """
    global tars
    try:
        if not model_path.isalnum():
            raise HTTPException(
                status_code=400,
                detail='Invalid model name. Only alphanumeric chars allowed.'
            )
        if type(model_path) is str:
            model_path = Path(model_path)
        model_path.mkdir(exist_ok=True, parents=True)
        tars.save(model_path / "final-model.pt")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=['ent_ext'], allow_remote=False)
def load_model(model_path):
    """
    loads the model from the provided model_path
    """
    global tars
    try:
        if type(model_path) is str:
            model_path = Path(model_path)
        if (model_path / "final-model.pt").exists():
            tars.load_state_dict(tars.load(
                model_path / "final-model.pt").state_dict())
        tars.to(device)
        return (f'[loaded model from] : {model_path}')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server
    launch_server(port=8000)
