import json
import os
import shutil
import warnings
from pathlib import Path
from typing import Dict, List, Optional

from fastapi import HTTPException
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from jaseci.jsorc.live_actions import jaseci_action
from jaseci.utils.utils import model_base_path
from jaseci.utils.model_manager import ModelManager
from jaseci.utils.utils import logger

from .train import (
    NERDataMaker,
    predict_text,
    train_model,
    load_custom_model,
    save_custom_model,
    reset_model,
)


warnings.filterwarnings("ignore")
MODEL_BASE_PATH = str(model_base_path("jac_nlp/tfm_ner"))
AVAILABLE_MODES = ["default", "append", "incremental"]
TRAIN_LOG_DIR = "train/logs"
TRAIN_FILE_PATH = "train/train.json"


@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def setup():
    """
    Loading configurations from config and
    initialize tokenizer and model
    """
    global train_config, model_config, active_model_path
    global t_config_fname, m_config_fname, model_manager

    model_manager = ModelManager(MODEL_BASE_PATH)
    if model_manager.get_latest_version():
        active_model_path = model_manager.get_version_path()
    else:
        active_model_path = str(model_manager.create_version_path())
        for config_file in ("train_config.json", "model_config.json"):
            src_path = os.path.join(os.path.dirname(__file__), f"utils/{config_file}")
            dst_path = os.path.join(active_model_path, config_file)
            shutil.copyfile(src_path, dst_path)

        with open(os.path.join(active_model_path, "model_config.json"), "r") as f:
            model_config = json.load(f)

        model = AutoModelForSequenceClassification.from_pretrained(
            model_config["model_name"]
        )
        tokenizer = AutoTokenizer.from_pretrained(model_config["model_name"])
        tokenizer.save_vocabulary(active_model_path)
        model.save_pretrained(active_model_path)
        del model, tokenizer
    load_custom_model(MODEL_BASE_PATH)

    m_config_fname = os.path.join(active_model_path, "model_config.json")
    t_config_fname = os.path.join(active_model_path, "train_config.json")

    with open(t_config_fname, "r") as f:
        train_config = json.load(f)
    with open(m_config_fname, "r") as f:
        model_config = json.load(f)


@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def extract_entity(text: str = None):
    try:
        data = predict_text(text)
        if isinstance(data, list):
            return data
        else:
            return "No active model found. Please train or load model first before inference."
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def train(
    mode: str = "default",
    epochs: int = 20,
    train_data: List = [],
    val_data: Optional[List] = [],
) -> dict:
    """
    API for training the model
    """
    global TRAIN_FILE_PATH
    # Ensure that logs directory exists
    os.makedirs(TRAIN_LOG_DIR, exist_ok=True)
    if mode not in AVAILABLE_MODES:
        st = {
            "Status": "training failed",
            "Error": f"Invalid training mode: {mode}. Available modes: {available_modes}",
        }
        raise HTTPException(status_code=400, detail=st)
    if mode == "default":
        train_config["EPOCHS"] = epochs
    elif mode == "incremental":
        train_config["EPOCHS"] += epochs
        with open(TRAIN_FILE_PATH, "w") as fp:
            json.dump(train_data, fp)
    elif mode == "append":
        train_config["EPOCHS"] = epochs
        if os.path.exists(TRAIN_FILE_PATH):
            with open(TRAIN_FILE_PATH, "r") as fp:
                old_train_data = json.load(fp)
            train_data += old_train_data
    with open(TRAIN_FILE_PATH, "w") as fp:
        json.dump(train_data, fp)
    try:
        train_dm = NERDataMaker(train_data)
        load_custom_model(active_model_path, train_dm)
        train_model(train_data=train_data, val_data=val_data, train_config=train_config)
        logger.info("Model training completed.")
        return save_model()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Error encountered during training."
        )


@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def load_model(version_id: str = None, local_file: bool = True):
    global active_model_path
    try:
        global TRAIN_FILE_PATH
        logger.info(f"Loading model '{version_id}'...")
        active_model_path = str(model_manager.get_version_path(version_id))
        TRAIN_FILE_PATH = os.path.join(active_model_path, "train.json")
        if os.path.exists(TRAIN_FILE_PATH):
            with open(TRAIN_FILE_PATH, "r") as fp:
                train_data = json.load(fp)
            train_dm = NERDataMaker(train_data)
            load_custom_model(active_model_path, train_dm)
            logger.info("Model loaded successfully!")
            return f"Model loaded successfully! with VersionId: {version_id}"
        else:
            raise FileNotFoundError("Cannot load model: train.json not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def save_model(version_id: str = None):
    global active_model_path
    try:
        active_model_path = str(model_manager.create_version_path(version_id))
        save_custom_model(active_model_path)
        print(f"current model {active_model_path} saved to disk.")
        shutil.copy(TRAIN_FILE_PATH, active_model_path)
        for config_file in ("train_config.json", "model_config.json"):
            src_path = os.path.join(os.path.dirname(__file__), f"utils/{config_file}")
            dst_path = os.path.join(active_model_path, config_file)
            shutil.copyfile(src_path, dst_path)
        return {"status": f"model {active_model_path} saved Successfull!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# API for setting the training and model parameters
@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def get_train_config():
    try:
        with open(t_config_fname, "r") as jsonfile:
            data = json.load(jsonfile)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def set_train_config(training_parameters: Dict = None):
    global train_config, t_config_fname
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
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def set_model_config(model_parameters: Dict = None):
    global model_config, m_config_fname
    try:
        save_model(model_config["model_save_path"])
        model_config.update(model_parameters)
        with open(m_config_fname, "w+") as jsonfile:
            json.dump(model_config, jsonfile, indent=4)
        model_manager.set_latest_version()
        reset_model()
        setup()
        return "Config setup is complete."
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    from jaseci.jsorc.remote_actions import launch_server

    launch_server(port=8000)
