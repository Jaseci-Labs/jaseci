import os
import torch
from typing import Dict, List
from fastapi import HTTPException
from transformers import AutoModel, AutoConfig, AutoTokenizer
import traceback
import numpy as np
from jaseci.actions.live_actions import jaseci_action
import random
import json
import shutil

from utils.bi_enc_model import BiEncoder
from utils.entitydataset import get_ner_dataset
from utils.train import train_model
from utils.evaluate import eval_model

# device = torch.device("cpu")
# uncomment this if you wish to use GPU to train
# this is commented out because this causes issues with
# unittest on machines with GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# funtion to set seed for the module
def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def config_setup():
    """
    Loading configurations from utils/config.cfg and
    initialize tokenizer and model
    """
    global model, tokenizer, model_config, train_config, t_config_fname, m_config_fname
    dirname = os.path.dirname(__file__)
    m_config_fname = os.path.join(dirname, "utils/model_config.json")
    t_config_fname = os.path.join(dirname, "utils/train_config.json")
    with open(m_config_fname, "r") as jsonfile:
        model_config = json.load(jsonfile)
    with open(t_config_fname, "r") as jsonfile:
        train_config = json.load(jsonfile)

    train_config.update({"device": device.type})
    t_config = AutoConfig.from_pretrained(model_config["t_model_name"])
    e_config = AutoConfig.from_pretrained(model_config["e_model_name"])

    tokenizer = AutoTokenizer.from_pretrained(
        model_config["t_model_name"], do_lower_case=True, clean_text=False
    )
    t_model = AutoModel.from_config(t_config)
    e_model = AutoModel.from_config(e_config)
    print("non shared model created")
    model = BiEncoder(
        t_config=t_config,
        e_config=e_config,
        t_model=t_model,
        e_model=e_model,
    )

    model.to(train_config["device"])
    set_seed(train_config["seed"])


config_setup()


@jaseci_action(act_group=["bi_ner"], allow_remote=True)
def predict(texts: List[str], entities: List[str]):
    """
    Take list of texts, entities and rets the entities
    """
    model.eval()
    predicted_candidates = []
    t_dataset = {"test": {"text": texts, "entity": entities}}
    try:
        test_ds = get_ner_dataset(dataset=t_dataset, tokenizer=tokenizer, split="test")
        predicted_candidates = eval_model(
            model=model,
            tokenizer=tokenizer,
            test_dataset=test_ds,
            train_config=train_config,
        )
        return predicted_candidates
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=404,
            detail=str(f"Exception : {e}"),
        )


"""
train_data={"train":[
    "my name is [Shawn](name)",
    "[Jemmott](name) is my name",
    "I'm [Juan](name)",
    "Everyone call me by the name [Katryn](name)",
    "You can call me [Spence](name)",
    "My mother give me the name [marks](name)",
    "I live at [482 Mandela Avenue](address)"
],
"test":{"text":["i am john smith","my place is in michigan"],
"entity":["name","address"]
}
}

"""


# API for training
@jaseci_action(act_group=["bi_ner"], allow_remote=True)
def train(
    dataset: Dict = {"train": []},
    training_parameters: Dict = None,
):
    """
    Take list of context, candidate, labels and trains the model
    """
    global model
    model.train()
    try:
        if training_parameters is not None:
            with open(t_config_fname, "w+") as jsonfile:
                train_config.update(training_parameters)
                json.dump(train_config, jsonfile, indent=4)
        if len(dataset["train"]) > 0:
            train_ds = get_ner_dataset(dataset=dataset, tokenizer=tokenizer)
        else:
            raise HTTPException(
                status_code=500, detail=str("Train Data can not be null")
            )
        model = train_model(
            model=model,
            train_dataset=train_ds,
            train_config=train_config,
        )
        return "Model Training is complete."
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# API for setting the training and model parameters
@jaseci_action(act_group=["bi_ner"], allow_remote=True)
def get_train_config():
    try:
        with open(t_config_fname, "r") as jsonfile:
            data = json.load(jsonfile)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["bi_ner"], allow_remote=True)
def set_train_config(training_parameters: Dict = None):
    global train_config
    try:
        with open(t_config_fname, "w+") as jsonfile:
            train_config.update(training_parameters)
            json.dump(train_config, jsonfile, indent=4)
        return "Config setup is complete."
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["bi_ner"], allow_remote=True)
def get_model_config():
    try:
        with open(m_config_fname, "r") as jsonfile:
            data = json.load(jsonfile)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["bi_ner"], allow_remote=True)
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
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["bi_ner"], allow_remote=True)
def save_model(model_path: str):
    """
    saves the model to the provided model_path
    """
    try:
        if not model_path.replace("_", "").isalnum():
            raise HTTPException(
                status_code=400,
                detail="""
                Invalid model name. Model Name can only have Alphanumeric
                 and '_' characters.""",
            )
        if not os.path.exists(model_path):
            os.makedirs(model_path)

        t_model_path = os.path.join(model_path + "/t_model")
        e_model_path = os.path.join(model_path + "/e_model")
        if not os.path.exists(t_model_path):
            os.makedirs(t_model_path)
        if not os.path.exists(e_model_path):
            os.makedirs(e_model_path)
        tokenizer.save_vocabulary(t_model_path)
        tokenizer.save_vocabulary(e_model_path)
        model.entity_embedder.save_pretrained(e_model_path)
        model.text_embedder.save_pretrained(t_model_path)
        print(f"Saving non-shared model to : {model_path}")
        shutil.copyfile(
            os.path.join(os.path.dirname(__file__), "utils/train_config.json"),
            os.path.join(model_path, "train_config.json"),
        )
        shutil.copyfile(
            os.path.join(os.path.dirname(__file__), "utils/model_config.json"),
            os.path.join(model_path, "model_config.json"),
        )
        return f"[Saved model at] : {model_path}"
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["bi_ner"], allow_remote=True)
def load_model(model_path):
    """
    loads the model from the provided model_path
    """
    global model, tokenizer
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Model path is not available")
    try:
        with open(m_config_fname, "r") as jsonfile:
            model_config_data = json.load(jsonfile)
        if model_config_data["shared"] is True:
            trf_config = AutoConfig.from_pretrained(model_path, local_files_only=True)
            tokenizer = AutoTokenizer.from_pretrained(
                model_path, do_lower_case=True, clean_text=False
            )
            e_model = AutoModel.from_pretrained(model_path, local_files_only=True)
            t_model = e_model
            print(f"Loading shared model from : {model_path}")
        else:
            t_model_path = os.path.join(model_path, "t_model")
            e_model_path = os.path.join(model_path, "e_model")
            print(f"Loading non-shared model from : {model_path}")
            e_model = AutoModel.from_pretrained(e_model_path, local_files_only=True)
            t_model = AutoModel.from_pretrained(t_model_path, local_files_only=True)
            trf_config = AutoConfig.from_pretrained(e_model_path, local_files_only=True)
            tokenizer = AutoTokenizer.from_pretrained(
                t_model_path, do_lower_case=True, clean_text=False
            )
        model = BiEncoder(
            config=trf_config,
            e_model=e_model,
            t_model=t_model,
        )
        model.to(train_config["device"])
        return f"[loaded model from] : {model_path}"
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    launch_server(port=8000)
