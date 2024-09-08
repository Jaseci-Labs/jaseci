import traceback
from fastapi import HTTPException
from jaseci.jsorc.live_actions import jaseci_action
from typing import Dict, List, Optional
import os
import json
import warnings
from .train import (
    predict_text,
    load_custom_model,
    save_custom_model,
    NERDataMaker,
    train_model,
)
import shutil
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from jaseci.utils.utils import model_base_path


warnings.filterwarnings("ignore")


@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def setup():
    """
    Loading configurations from config and
    initialize tokenizer and model
    """
    global train_config, model_config, MODEL_BASE_PATH
    global t_config_fname, m_config_fname
    dirname = os.path.dirname(__file__)
    m_config_fname = os.path.join(dirname, "utils/model_config.json")
    t_config_fname = os.path.join(dirname, "utils/train_config.json")

    with open(t_config_fname, "r") as jsonfile:
        train_config = json.load(jsonfile)
    with open(m_config_fname, "r") as jsonfile:
        model_config = json.load(jsonfile)
    MODEL_BASE_PATH = str(model_base_path("jac_nlp/tfm_ner"))
    os.makedirs(MODEL_BASE_PATH, exist_ok=True)
    if not os.listdir(MODEL_BASE_PATH):
        model = AutoModelForSequenceClassification.from_pretrained(
            model_config["model_name"]
        )
        tokenizer = AutoTokenizer.from_pretrained(model_config["model_name"])
        tokenizer.save_vocabulary(MODEL_BASE_PATH)
        model.save_pretrained(MODEL_BASE_PATH)
        del model, tokenizer
    load_custom_model(MODEL_BASE_PATH)


enum = {"default": 1, "append": 2, "incremental": 3}


@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def extract_entity(text: str = None):
    try:
        data = predict_text(text)
        if isinstance(data, list):
            return data
        else:
            return "No active model found. Please train or load model first before inference."
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def train(
    mode: str = "default",
    epochs: int = 20,
    train_data: List = [],
    val_data: Optional[List] = [],
):
    """
    API for training the model
    """
    if not os.path.exists("train/logs"):
        os.makedirs("train/logs")
    if mode == "default":
        train_config["EPOCHS"] = epochs
        with open("train/train.json", "w") as fp:
            json.dump(train_data, fp)
    elif mode == "incremental":
        train_config["EPOCHS"] = train_config["EPOCHS"] + epochs
        with open("train/train.json", "w") as fp:
            json.dump(train_data, fp)
    elif mode == "append":
        train_config["EPOCHS"] = epochs
        if os.path.exists("train/train.json"):
            with open("train/train.json", "r") as fp:
                old_train_data = json.load(fp)
            for data in old_train_data:
                train_data.append(data)
            with open("train/train.json", "w") as fp:
                json.dump(train_data, fp)

    else:
        st = {
            "Status": "training failed",
            "Error": "Please define training mode",
            "Available mode": ["default", "append", "incremental"],
        }
        raise HTTPException(status_code=400, detail=st)

    try:
        train_dm = NERDataMaker(train_data)
        load_custom_model(MODEL_BASE_PATH, train_dm)
        train_model(train_data=train_data, val_data=val_data, train_config=train_config)
        print("model training Completed")
        return {"status": "model Training Successful!"}
    except Exception as e:
        print(e)
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=str("Issue encountered during train "),
        )


@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def load_model(model_path: str = "default", local_file: bool = True):
    global MODEL_BASE_PATH
    if not os.path.isabs(model_path):
        model_path = str(MODEL_BASE_PATH / Path(model_path))
    MODEL_BASE_PATH = model_path
    train_file_path = os.path.join(model_path, "train.json")
    if local_file is True and not os.path.exists(model_path):
        return "Model path is not available"
    try:
        print("loading latest trained model to memory...")
        if os.path.exists(train_file_path):
            with open(train_file_path, "r") as fp:
                train_data = json.load(fp)
            train_dm = NERDataMaker(train_data)
            load_custom_model(MODEL_BASE_PATH, train_dm)
            print("model successfully load to memory!")
            return {"status": "model Loaded Successfull!"}
        else:
            raise HTTPException(status_code=400, detail=str("cannot load model"))
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))


@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def save_model(model_path: str = "mymodel"):
    try:
        if not os.path.isabs(model_path):
            model_path = str(MODEL_BASE_PATH / Path(model_path))
        save_custom_model(model_path)
        print(f"current model {model_path} saved to disk.")
        shutil.copy("train/train.json", model_path)
        return {"status": f"model {model_path} saved Successfull!"}
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))


# API for setting the training and model parameters
@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def get_train_config():
    try:
        with open(t_config_fname, "r") as jsonfile:
            data = json.load(jsonfile)
        return data
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def set_train_config(training_parameters: Dict = None):
    global train_config
    try:
        train_config.update(training_parameters)
        with open(t_config_fname, "w+") as jsonfile:
            json.dump(train_config, jsonfile, indent=4)

        return "Config setup is complete."
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def get_model_config():
    try:
        with open(m_config_fname, "r") as jsonfile:
            data = json.load(jsonfile)
        return data
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def set_model_config(model_parameters: Dict = None):
    global model_config
    try:
        save_model(model_config["model_save_path"])
        model_config.update(model_parameters)
        with open(m_config_fname, "w+") as jsonfile:
            json.dump(model_config, jsonfile, indent=4)

        setup()
        return "Config setup is complete."
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    from jaseci.jsorc.remote_actions import launch_server

    launch_server(port=8000)
