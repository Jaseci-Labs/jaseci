import traceback
from fastapi import HTTPException
from jaseci.actions.live_actions import jaseci_action
from typing import Dict, List, Optional
import os
import pandas as pd
import json
import warnings
from .train import (
    predict_text,
    training,
    load_custom_model,
    save_custom_model,
    data_set,
    check_labels_ok,
    model_versions,
)
from .entity_utils import create_data, create_data_new

warnings.filterwarnings("ignore")


def config_setup():
    """
    Loading configurations from config and
    initialize tokenizer and model
    """
    global train_config, model_config, curr_model_path
    global t_config_fname, m_config_fname
    dirname = os.path.dirname(__file__)
    m_config_fname = os.path.join(dirname, "utils/model_config.json")
    t_config_fname = os.path.join(dirname, "utils/train_config.json")

    with open(t_config_fname, "r") as jsonfile:
        train_config = json.load(jsonfile)
    with open(m_config_fname, "r") as jsonfile:
        model_config = json.load(jsonfile)

    curr_model_path = model_config["model_name"]
    # staging_model_path = model_config["staging_model_path"]
    # if staging_model_path is not None:
    #     load_custom_model(staging_model_path)
    #     curr_model_path = staging_model_path
    # else:
    load_custom_model(curr_model_path)


# calling the default configuration from "model config and train config file"
config_setup()
# creating variable for training mode
enum = {"default": 1, "append": 2, "incremental": 3}


# creating train eval and test dataset
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


# creating api for infer new data in staging
@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def extract_entity(text: str = None):
    try:
        data = predict_text(text)
        return data
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))


@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def train(
    use_mlflow: bool = False,
    tracking_uri: str = "sqlite:///mlrunsdb.db",
    exp_name: str = "tfm_ner",
    exp_run_name: str = "transformer_ner",
    description: str = "Running the latest model on fincorp dataset",
    mode: str = train_config["MODE"],
    epochs: int = train_config["EPOCHS"],
    train_data: List[dict] = [],
    val_data: Optional[List[dict]] = [],
    test_data: Optional[List[dict]] = [],
):
    """
    API for training the model
    """
    if not os.path.exists("train/logs"):
        os.makedirs("train/logs")
    if epochs:
        train_config["EPOCHS"] = epochs

    if mode == "default" or mode == "incremental":
        if os.path.exists("train/train_backup_file.txt"):
            os.remove("train/train_backup_file.txt")
        if os.path.exists("train/val_backup_file.txt"):
            os.remove("train/val_backup_file.txt")
        if os.path.exists("train/test_backup_file.txt"):
            os.remove("train/test_backup_file.txt")

        if os.path.exists("train/train.txt"):
            os.remove("train/train.txt")
        if os.path.exists("train/val.txt"):
            os.remove("train/val.txt")
        if os.path.exists("train/test.txt"):
            os.remove("train/test.txt")

        train_file = "train/train.txt"
        val_file = "train/val.txt"
        test_file = "train/test.txt"

    elif mode == "append":
        train_file = "train/train_backup_file.txt"
        val_file = "train/val_backup_file.txt"
        test_file = "train/test_backup_file.txt"

    else:
        st = {
            "Status": "training failed",
            "Error": "Please define training mode",
            "Available mode": ["default", "append", "incremental"],
        }
        raise HTTPException(status_code=400, detail=st)

    if len(val_data) != 0:
        create_train_data(val_data, "val")

    if len(test_data) != 0:
        create_train_data(test_data, "test")

    if len(train_data) != 0:
        completed = create_train_data(train_data, "train")
        if completed is True:

            # loading training dataset
            data_set(
                train_file,
                val_file,
                test_file,
                train_config["MAX_LEN"],
                train_config["TRAIN_BATCH_SIZE"],
            )

            # checking data and model labels
            data_lab = check_labels_ok()
            print("model training started")
            status = training(
                model_name=curr_model_path,
                epochs=train_config["EPOCHS"],
                mode=enum[mode],
                lab_check=data_lab,
                learning_rate=train_config["LEARNING_RATE"],
                max_grad_norm=train_config["MAX_GRAD_NORM"],
                model_save_path=model_config["model_save_path"],
                use_mlflow=use_mlflow,
                tracking_uri=tracking_uri,
                exp_name=exp_name,
                exp_run_name=exp_run_name,
                description=description,
            )
            print("model training Completed")
            model_config.update({"staging_model_path": status[0]})
            with open(m_config_fname, "w+") as jsonfile:
                json.dump(model_config, jsonfile, indent=4)
            return status[1]
        else:
            raise HTTPException(
                status_code=500,
                detail=str("Issue encountered during train data creation"),
            )
    else:
        raise HTTPException(
            status_code=404, detail=str("Need Data for Text and Entity")
        )


@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def load_model(model_path: str = "default", local_file: bool = False):
    global curr_model_path
    curr_model_path = model_path
    if local_file is True and not os.path.exists(model_path):
        return "Model path is not available"
    try:
        print("loading latest trained model to memory...")
        load_custom_model(model_path)
        print("model successfully load to memory!")
        return {"status": "model Loaded Successfull!"}
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))


@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def get_model_verion(registered_model_name: str = "tfm_ner"):
    mv = model_versions(registered_model_name)
    return mv


@jaseci_action(act_group=["tfm_ner"], allow_remote=True)
def save_model(model_path: str = "mymodel"):
    try:
        save_custom_model(model_path)
        print(f"current model {model_path} saved to disk.")
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

        config_setup()
        return "Config setup is complete."
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    launch_server(port=8000)
