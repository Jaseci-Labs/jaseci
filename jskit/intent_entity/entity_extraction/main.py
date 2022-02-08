from typing import List
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.models import TARSTagger
from flair.data import Sentence
from flair.trainers import ModelTrainer
import pandas as pd
from utils import create_data
import configparser
import jaseci.actions.remote_actions as jra

config = configparser.ConfigParser()
config.read('config.cfg')


TARS_MODEL_NAME = config['TARS_MODEL']['NER_MODEL']
NER_LABEL_TYPE = config['LABEL_TYPE']['NER']
# 1. Load zero-shot NER tagger
tars = TARSTagger.load(TARS_MODEL_NAME)


def trainEntity():
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

    # tars = TARSClassifier.load('tars-base')
    # 2. make the model aware of the desired set of labels from the new corpus
    tars.add_and_switch_to_new_task(
        "ner tagging", label_dictionary=tag_dictionary, label_type=tag_type)
    # 3. initialize the text classifier trainer with your corpus
    trainer = ModelTrainer(tars, corpus)
    # 4. train model
    trainer.train(base_path='train/ner_tagging',  # path to store the model artifacts
                  learning_rate=0.02,
                  mini_batch_size=1,
                  max_epochs=10,
                  train_with_test=True,
                  train_with_dev=True

                  )
    # 5. Load trained TARS model
    tars = TARSTagger.load('train/ner_tagging/final-model.pt')
    print("model loading completed")


# defining the api for entitydetection
@jra.jaseci_action(act_group=['ent_ext'], aliases=['entitydetection'])
def entityDetection(text: str, ner_labels: List[str]):
    global tars
    if text:
        if ner_labels:
            tars.add_and_switch_to_new_task(
                'Entity Detection Task', ner_labels, label_type=NER_LABEL_TYPE)
            sentence = Sentence(text)
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
            return JSONResponse(content=response_data_format, status_code=200)
        else:
            return JSONResponse(content={"Exception": "NER Labels are missing in request data"}, status_code=400)
    else:
        return JSONResponse(content={"Exception": "Text data is missing in request data"}, status_code=400)


@jra.jaseci_action(act_group=['ent_ext'], aliases=['updateentitydataset'])
def updateDataset(text: str, entity: List[dict]):
    print(entity)
    tag = []
    if text and entity:
        for ent in entity:
            if ent['entity_value'] and ent['entity_name']:
                tag.append((ent['entity_value'], ent['entity_name']))
            else:
                return JSONResponse(content="Entity Data missing in request", status_code=400)
            data = pd.DataFrame([[text, tag
                                  ]], columns=['text', 'annotation'])
            # creating the file.
            if create_data(data):
                trainEntity()
                return JSONResponse(content="Model Training is Completed", status_code=200)
            else:
                return JSONResponse(content="Issue encountered during train data creation", status_code=500)
    else:
        return JSONResponse(content="Need Data for Text and Entity", status_code=400)
