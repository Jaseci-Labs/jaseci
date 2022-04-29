import traceback
from fastapi import HTTPException
from jaseci.actions.live_actions import jaseci_action
from typing import Dict, List
from train import predict_text, train_model
from train import load_custom_model, save_custom_model
import json
from train import data_set, check_labels_ok
import os
import pandas as pd
from entity_utils import create_data, create_data1


def config_setup():
    """
    Loading configurations from config and
    initialize tokenizer and model
    """
    global train_config, model_config, curr_model_path
    global t_config_fname, m_config_fname
    m_config_fname = "utils/model_config.json"
    t_config_fname = "utils/train_config.json"

    # conf = config(t_config_fname, m_config_fname)
    with open(t_config_fname, "r") as jsonfile:
        train_config = json.load(jsonfile)
    with open(m_config_fname, "r") as jsonfile:
        model_config = json.load(jsonfile)

    curr_model_path = model_config["model_name"]
    load_custom_model(curr_model_path)


def load_parameter():
    global MAX_LEN, TRAIN_BATCH_SIZE, VALID_BATCH_SIZE
    global EPOCHS, LEARNING_RATE, MAX_GRAD_NORM, lab, model_save_path
    # global model_name

    MAX_LEN = train_config["MAX_LEN"]
    TRAIN_BATCH_SIZE = train_config["TRAIN_BATCH_SIZE"]
    VALID_BATCH_SIZE = train_config["VALID_BATCH_SIZE"]
    EPOCHS = train_config["EPOCHS"]
    LEARNING_RATE = train_config["LEARNING_RATE"]
    MAX_GRAD_NORM = train_config["MAX_GRAD_NORM"]
    EPOCHS = train_config["EPOCHS"]
    lab = ['O']
    model_save_path = model_config['model_save_path']

    # model_name = model_config['model_name']


config_setup()
load_parameter()

# def check_train_cond():

enum = {
    "default": 1,
    "append": 2,
    "incremental": 3
}


@jaseci_action(act_group=['extract_entity'], allow_remote=True)
def train(mode: str = "default",
          epochs: int = 40,
          train_data: List[dict] = None
          ):
    """
    API for training the model
    """
    if epochs:
        EPOCHS = epochs

    if mode == "default":
        if os.path.exists("train/train_backup_file.txt"):
            os.remove("train/train_backup_file.txt")
        train_file = 'train/train.txt'
    elif mode == 'incremental':
        train_file = 'train/train.txt'
    elif mode == 'append':
        train_file = 'train/train_backup_file.txt'
    else:
        return "Please define mode of training"

    data = pd.DataFrame(columns=["text", "annotation"])
    if train_data:
        for t_data in train_data:
            tag = []
            for ent in t_data["entities"]:
                if ent['entity_value'] and ent['entity_type']:
                    tag.append((ent['entity_value'], ent['entity_type'],
                                ent["start_index"], ent["end_index"]))
                else:
                    raise HTTPException(status_code=404, detail=str(
                        "Entity Data missing in request"))
            data = data.append({"text": t_data["context"],
                                "annotation": tag}, ignore_index=True)
        # creating training data
        try:
            completed = create_data(data)
        except Exception as e:
            completed = create_data1(data)
            print(f"Exception  : {e}")
        if completed is True:

            # loading training dataset
            data_set(train_file, lab, MAX_LEN, TRAIN_BATCH_SIZE)

            # checking data and model labels
            data_lab = check_labels_ok()
            print("model training started")
            status = train_model(curr_model_path, EPOCHS, enum[mode], data_lab,
                                 LEARNING_RATE, MAX_GRAD_NORM, model_save_path)
            print("model training Completed")
            return status
        else:
            raise HTTPException(status_code=500, detail=str(
                "Issue encountered during train data creation"))
    else:
        raise HTTPException(status_code=404, detail=str(
            "Need Data for Text and Entity"))


@jaseci_action(act_group=['extract_entity'], allow_remote=True)
def extract_entity(text: str = None):
    try:
        data = predict_text(text)
        return data
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))


@jaseci_action(act_group=['extract_entity'], allow_remote=True)
def load_model(model_path: str = 'default'):
    global curr_model_path
    curr_model_path = model_path
    if not os.path.exists(model_path):
        raise HTTPException(
            status_code=404,
            detail='Model path is not available'
        )
    try:
        print("loading latest trained model to memory...")
        load_custom_model(model_path)
        print("model successfully load to memory!")
        return {"status": f"model {model_path} Loaded in memory Successfull!"}
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))


@jaseci_action(act_group=['extract_entity'], allow_remote=True)
def save_model(model_path: str = 'mymodel'):
    try:
        save_custom_model(model_path)
        print(f'current model {model_path} saved to disk.')
        return {"status": f"model {model_path} saved Successfull!"}
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))


# API for setting the training and model parameters
@ jaseci_action(act_group=['extract_entity'], allow_remote=True)
def get_train_config():
    try:
        with open(t_config_fname, "r") as jsonfile:
            data = json.load(jsonfile)
        return data
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@ jaseci_action(act_group=['extract_entity'], allow_remote=True)
def set_train_config(training_parameters: Dict = None):
    global train_config
    try:
        with open(t_config_fname, "w+") as jsonfile:
            train_config.update(training_parameters)
            json.dump(train_config, jsonfile, indent=4)

        load_parameter()
        return "Config setup is complete."
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@ jaseci_action(act_group=['extract_entity'], allow_remote=True)
def get_model_config():
    try:
        with open(m_config_fname, "r") as jsonfile:
            data = json.load(jsonfile)
        return data
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@ jaseci_action(act_group=['extract_entity'], allow_remote=True)
def set_model_config(model_parameters: Dict = None):
    global model_config
    try:
        save_model(model_config["model_save_path"])
        with open(m_config_fname, "w+") as jsonfile:
            model_config.update(model_parameters)
            json.dump(model_config, jsonfile, indent=4)

        config_setup()
        return "Config setup is complete."
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


# @jaseci_action(act_group=['extract_entity'], allow_remote=True)
# def train():
#     try:
#         data_set('train/train.txt')
#         print("model training started")
#         train_model()
#         print("model training Completed")
#     except Exception as e:
#         print(traceback.format_exc())
#         raise HTTPException(status_code=400, detail=str(e))


# ###################################
if __name__ == '__main__':
    from jaseci.actions.remote_actions import launch_server
    print('Model Running ...')
    launch_server(port=8000)
