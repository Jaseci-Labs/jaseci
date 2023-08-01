from random import random
from typing import List, Optional, Dict
from fastapi import HTTPException
from flair.data import Corpus
from flair.datasets import ColumnCorpus
from flair.models import TARSTagger, SequenceTagger

from flair.embeddings import WordEmbeddings, StackedEmbeddings, FlairEmbeddings
from flair.file_utils import cached_path
from flair.file_utils import cached_path
from flair.data import Sentence
from flair.trainers import ModelTrainer
import pandas as pd
from .entity_utils import create_data, create_data_new
import configparser
from jaseci.jsorc.live_actions import jaseci_action
import torch
import os
from pathlib import Path
from datetime import datetime
import warnings
from jaseci.utils.utils import model_base_path
from jaseci.utils.model_manager import ModelManager
import shutil
import traceback

from jaseci.utils.utils import model_base_path

warnings.filterwarnings("ignore")


config = configparser.ConfigParser()
MODEL_BASE_PATH = model_base_path("jac_nlp/ent_ext")
TARS_NER_PATH = (
    "https://nlp.informatik.hu-berlin.de/resources/models/tars-ner/tars-ner.pt"
)
# 1. initialize each embedding for LSTM
embedding_types = [
    # GloVe embeddings
    WordEmbeddings("glove"),
    # contextual string embeddings, forward
    FlairEmbeddings("news-forward"),
    # contextual string embeddings, backward
    FlairEmbeddings("news-backward"),
]

# embedding stack consists of Flair and GloVe embeddings
embeddings = StackedEmbeddings(embeddings=embedding_types)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


@jaseci_action(act_group=["ent_ext"], allow_remote=True)
def setup(reload=False):
    """create a tagger as per the model provided through config"""

    global tagger, NER_MODEL_NAME, NER_LABEL_TYPE, MODEL_TYPE, config
    global model_manager, active_model_path
    model_manager = ModelManager(MODEL_BASE_PATH)
    if model_manager.get_latest_version():
        active_model_path = model_manager.get_version_path()

        if (active_model_path / "final-model.pt").exists():
            tagger = TARSTagger.load(f"{active_model_path}/final-model.pt")
        else:
            tagger = TARSTagger.load(f"{active_model_path}/tars-ner.pt")
        config.read(active_model_path / "config.cfg")
        NER_MODEL_NAME = config["TAGGER_MODEL"]["NER_MODEL"]
        NER_LABEL_TYPE = config["LABEL_TYPE"]["NER"]
        MODEL_TYPE = config["TAGGER_MODEL"]["MODEL_TYPE"]
    else:
        active_model_path = model_manager.create_version_path()
        if reload is False:
            config.read(os.path.join(os.path.dirname(__file__), "config.cfg"))
        NER_MODEL_NAME = config["TAGGER_MODEL"]["NER_MODEL"]
        NER_LABEL_TYPE = config["LABEL_TYPE"]["NER"]
        MODEL_TYPE = config["TAGGER_MODEL"]["MODEL_TYPE"]
        if MODEL_TYPE.lower() == "trfmodel" and NER_MODEL_NAME.lower() != "none":
            tagger = TARSTagger(embeddings=NER_MODEL_NAME)
        elif NER_MODEL_NAME.lower() != "none" and MODEL_TYPE.lower() in ["lstm", "gru"]:
            tagger = SequenceTagger.load(cached_path(NER_MODEL_NAME, active_model_path))
        elif MODEL_TYPE.lower() in "tars" and NER_MODEL_NAME.lower() != "none":
            tagger = TARSTagger.load(cached_path(TARS_NER_PATH, active_model_path))
        shutil.copyfile(
            os.path.join(os.path.dirname(__file__), "config.cfg"),
            os.path.join(active_model_path, "config.cfg"),
        )
        print(f"loaded mode : [{NER_MODEL_NAME}]")


def train_entity(train_params: dict):
    """
    funtion for training the model
    """
    global tagger, NER_MODEL_NAME, MODEL_TYPE, active_model_path
    # define columns
    columns = {0: "text", 1: "ner"}
    # directory where the data resides
    data_folder = "train"
    # initializing the corpus
    corpus: Corpus = ColumnCorpus(data_folder, columns, train_file="train.txt")
    # make tag dictionary from the corpus
    tag_dictionary = corpus.make_tag_dictionary(tag_type=NER_LABEL_TYPE)

    # make the model aware of the desired set of labels from the new corpus
    try:
        if MODEL_TYPE.lower() in ["trfmodel", "tars"]:
            # initialize Tars tagger with a new task
            val = random()
            tagger.add_and_switch_to_new_task(
                "ner_train" + str(val),
                label_dictionary=tag_dictionary,
                label_type=NER_LABEL_TYPE,
            )
        elif tagger is None and MODEL_TYPE.lower() in ["lstm", "gru"]:
            # initialize sequence tagger
            tagger = SequenceTagger(
                hidden_size=256,
                embeddings=embeddings,
                tag_dictionary=tag_dictionary,
                tag_type=NER_LABEL_TYPE,
                rnn_type=MODEL_TYPE,
            )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(f"Model load error : {e}"))
    #  initialize the Sequence trainer with your corpus
    trainer = ModelTrainer(tagger, corpus)
    active_model_path = str(model_manager.create_version_path())
    # train model
    trainer.train(
        base_path=active_model_path,  # path to store model
        learning_rate=train_params["LR"],
        mini_batch_size=train_params["batch_size"],
        max_epochs=train_params["num_epoch"],
        train_with_test=True,
        train_with_dev=True,
    )
    #  Load trained Sequence Tagger model
    tagger = tagger.load(f"{active_model_path}/final-model.pt")
    torch.cuda.empty_cache()
    print(f"model training and loading completed from {active_model_path.name}")


# creating train val and test dataset
def create_train_data(dataset, fname):
    data = pd.DataFrame(columns=["text", "annotation"])
    for t_data in dataset:
        tag = []
        for ent in t_data["entities"]:
            if ent["entity_value"] and ent["entity_type"]:
                tag.append(
                    (
                        ent["entity_value"],
                        ent["entity_type"],
                        ent["start_index"],
                        ent["end_index"],
                    )
                )
            else:
                raise HTTPException(
                    status_code=404, detail=str("Entity Data missing in request")
                )
        data = data.append(
            {"text": t_data["context"], "annotation": tag}, ignore_index=True
        )
    # creating training data
    try:
        completed = create_data(data, fname)
    except Exception as e:
        completed = create_data_new(data, fname)
        print(f"Exception  : {e}")
    return completed


def train_and_val_entity(train_params: dict):
    """
    function for training the model
    """
    global tagger, NER_MODEL_NAME, MODEL_TYPE, active_model_path

    # Define constants
    data_folder = "train"
    checkpoint_file_path = Path(f"{active_model_path}/checkpoint.pt")
    # Define columns
    columns = {0: "text", 1: "ner"}

    # Check if the necessary training files exist
    if not os.path.isfile(f"{data_folder}/train.txt"):
        raise FileNotFoundError(f"Cannot find the training file in {data_folder}")

    # Initialize the corpus
    if os.path.isfile(f"{data_folder}/val.txt") and os.path.isfile(
        f"{data_folder}/test.txt"
    ):
        corpus: Corpus = ColumnCorpus(
            data_folder,
            columns,
            train_file="train.txt",
            dev_file="val.txt",
            test_file="test.txt",
        )
    elif os.path.isfile(f"{data_folder}/test.txt"):
        corpus: Corpus = ColumnCorpus(
            data_folder,
            columns,
            train_file="train.txt",
            test_file="test.txt",
        )
    elif os.path.isfile(f"{data_folder}/val.txt"):
        corpus: Corpus = ColumnCorpus(
            data_folder,
            columns,
            train_file="train.txt",
            dev_file="val.txt",
        )
    else:
        corpus: Corpus = ColumnCorpus(data_folder, columns, train_file="train.txt")

    # Load the model from checkpoint if it exists
    if checkpoint_file_path.exists():
        tagger = TARSTagger.load(checkpoint_file_path)
        tag_dictionary = corpus.make_label_dictionary(label_type=NER_LABEL_TYPE)
        try:
            tagger.add_and_switch_to_new_task(
                "ner_train_nerd",
                label_dictionary=tag_dictionary,
                label_type=NER_LABEL_TYPE,
            )
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Model load error: {e}")
        trainer = ModelTrainer(tagger, corpus)
        trainer.resume(
            model=tagger,
            learning_rate=train_params["LR"],
            mini_batch_size=train_params["batch_size"],
            max_epochs=train_params["num_epoch"],
            train_with_test=True,
            train_with_dev=True,
            embeddings_storage_mode="cuda",
            checkpoint=True,
        )
    else:
        tag_dictionary = corpus.make_label_dictionary(label_type=NER_LABEL_TYPE)
        try:
            tagger.add_and_switch_to_new_task(
                "ner_train_nerd",
                label_dictionary=tag_dictionary,
                label_type=NER_LABEL_TYPE,
            )
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Model load error: {e}")
        trainer = ModelTrainer(tagger, corpus)
        active_model_path = str(model_manager.create_version_path())
        trainer.train(
            base_path=active_model_path,
            learning_rate=train_params["LR"],
            mini_batch_size=train_params["batch_size"],
            max_epochs=train_params["num_epoch"],
            train_with_test=True,
            train_with_dev=True,
            checkpoint=True,
        )

    # Load trained Sequence Tagger model
    tagger = tagger.load(f"{active_model_path}/final-model.pt")
    torch.cuda.empty_cache()
    with open(f"{active_model_path}/config.cfg", "w") as configfile:
        config.write(configfile)
    print("Model training and loading completed.")
    return active_model_path.split("/")[-1]


# defining the api for entity detection
@jaseci_action(act_group=["ent_ext"], allow_remote=True)
def entity_detection(text: str, ner_labels: Optional[List] = ["PREDEFINED"]):
    """
    API for detectiing provided entity in text
    """
    global tagger, MODEL_TYPE
    if tagger is not None:
        if text:
            if ner_labels:
                if MODEL_TYPE.lower() in ["trfmodel", "tars"]:
                    val = random()
                    tagger.add_and_switch_to_new_task(
                        "Entity Detection Task" + str(val),
                        ner_labels,
                        label_type=NER_LABEL_TYPE,
                    )
                sentence = Sentence(text)
                # predicting entities in the text
                tagger.predict(sentence)
                tagged_sentence = sentence.to_dict(NER_LABEL_TYPE)
                response_data_format = {"entities": []}
                response_data_format["text"] = tagged_sentence["text"]
                for entity, entity_details in zip(
                    sentence.get_spans(NER_LABEL_TYPE),
                    tagged_sentence[NER_LABEL_TYPE],
                ):
                    temp_dict = {}
                    temp_dict["entity_text"] = entity.text
                    temp_dict["entity_value"] = entity_details["value"]
                    temp_dict["conf_score"] = entity_details["confidence"]
                    temp_dict["start_pos"] = entity.start_position
                    temp_dict["end_pos"] = entity.end_position
                    response_data_format["entities"].append(temp_dict)
                return response_data_format
            else:
                raise HTTPException(
                    status_code=404,
                    detail=str("NER Labels are missing in request data"),
                )
        else:
            raise HTTPException(
                status_code=404, detail=str("Text data is missing in request data")
            )
    else:
        raise HTTPException(
            status_code=404, detail=str("Please train the Model before Using")
        )


@jaseci_action(act_group=["ent_ext"], allow_remote=True)
def train(
    train_data: List[dict] = [],
    val_data: Optional[List[dict]] = [],
    test_data: Optional[List[dict]] = [],
    train_params: Dict = {"num_epoch": 10, "batch_size": 8, "LR": 0.02},
):
    """
    API for training the model
    """
    try:
        time1 = datetime.now()
        if len(val_data) != 0:
            create_train_data(val_data, "val")

        if len(test_data) != 0:
            create_train_data(test_data, "test")

        if len(train_data) != 0:
            completed = create_train_data(train_data, "train")
            if completed is True:
                version_id = train_and_val_entity(train_params)
                total_time = datetime.now() - time1
                print(f"total time taken to complete Training : {total_time}")
                return f"Model Training is Completed, VersionId: {version_id}"
            else:
                raise HTTPException(
                    status_code=500,
                    detail=str("Issue encountered during train data creation"),
                )
        else:
            raise HTTPException(
                status_code=404, detail=str("Need Data for Text and Entity")
            )
    except Exception as e:
        traceback.print_exc()
        return str(e)


@jaseci_action(act_group=["ent_ext"], allow_remote=True)
def save_model(version_id: Optional[str] = None):
    """
    saves the model to the provided model_path
    """
    global tagger, active_model_path
    if tagger is not None:
        try:
            active_model_path = model_manager.create_version_path(version_id)
            tagger.save(active_model_path / "final-model.pt", checkpoint=False)
            with open(f"{active_model_path}/config.cfg", "w") as configfile:
                config.write(configfile)
            return f"Saved model to : {active_model_path.name}"
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(
            status_code=404, detail=str("Please Initailize the model before saving")
        )


@jaseci_action(act_group=["ent_ext"], allow_remote=True)
def load_model(version_id=None, default=False):
    """
    loads the model from the provided model_path
    """
    global tagger, active_model_path
    try:
        if default is True:
            model_manager.set_latest_version()
            setup()
            return f"[default model loaded model from] : {config['TAGGER_MODEL']['NER_MODEL']}"  # noqa
        active_model_path = model_manager.get_version_path(version_id)
        if (active_model_path / "final-model.pt").exists():
            tagger.load_state_dict(
                tagger.load(active_model_path / "final-model.pt").state_dict()
            )
            tagger.to(device)
            return f"[loaded model from] : {active_model_path.name}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["ent_ext"], allow_remote=True)
def set_config(ner_model: str = None, model_type: str = None):
    """
    Update the configuration file with new model parameters
    ner_model types:
    1. Pre-trained LSTM / GRU : ["ner", "ner-fast","ner-large"]
    2. Huggingface model : all available models
    model_type :
    1. "TRFMODEL" : for huggingface models
    2. "LSTM" or "GRU" : RNN models
    """
    global config, active_model_path
    if ner_model or model_type:
        config["TAGGER_MODEL"]["NER_MODEL"] = ner_model
        config["TAGGER_MODEL"]["MODEL_TYPE"] = model_type
    with open(f"{active_model_path}/config.cfg", "w") as configfile:
        config.write(configfile)
    try:
        setup(reload=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return "Config setup is complete."


if __name__ == "__main__":
    from jaseci.jsorc.remote_actions import launch_server

    launch_server(port=8000)
