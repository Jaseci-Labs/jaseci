import os
import configparser
import torch
from typing import Dict, List, Union
from fastapi import HTTPException
from transformers import AutoModel, AutoConfig, AutoTokenizer
from utils.evaluate import get_embeddings, get_inference
from utils.models import BiEncoder
import traceback
import numpy as np
from utils.train import train_model
from jaseci.actions.live_actions import jaseci_action
import random
import json
import shutil

# config = configparser.ConfigParser()
model, model_name, tokenizer = None, None, None
save_restart = False
basepath = None
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
    Loading configurations from utils/config.cfg and initialize tokenizer and model
    """
    global model, save_restart, tokenizer, shared, model_config, model_save_path
    dirname = os.path.dirname(__file__)
    config_fname = os.path.join(dirname, "utils/model_config.json")
    with open(config_fname, "r") as jsonfile:
        model_config = json.load(jsonfile)
    model_name = model_config["model_name"]
    shared = model_config["shared"]
    model_save_path = model_config["model_save_path"]
    if model is None:
        model_config = AutoConfig.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name,
                                                  do_lower_case=True, clean_text=False)
        if shared is True:
            cont_bert = AutoModel.from_config(model_config)
            cand_bert = cont_bert
            print("shared model created")
        else:
            cont_bert = AutoModel.from_config(model_config)
            cand_bert = AutoModel.from_config(model_config)
            print("non shared model created")
        model = BiEncoder(config=model_config,
                          cont_bert=cont_bert, cand_bert=cand_bert, shared=shared)

    elif save_restart:
        saved_text = save_model(model_save_path)
        if "Saved" in saved_text:
            print(saved_text)
        else:
            print("Unable to save live model")
        model_config = AutoConfig.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name,
                                                  do_lower_case=True, clean_text=False)
        cont_bert = AutoModel.from_config(model_config)
        cand_bert = AutoModel.from_config(model_config)
        model = BiEncoder(config=model_config,
                          cont_bert=cont_bert, cand_bert=cand_bert, shared=shared)
        save_restart = False

    model.to(device)
    set_seed(12345)


config_setup()


# to validate data and datatype provided
def is_list_of(data, dtype):
    return bool(data) and isinstance(data, list) and all(isinstance(elem, dtype) for elem in data)


# API for getting the cosine similarity
@jaseci_action(act_group=['bi_enc'], allow_remote=True)
def cosine_sim(vec_a: List[float], vec_b: List[float], meta):
    """
    Caculate the cosine similarity score of two given vectors
    Param 1 - First vector
    Param 2 - Second vector
    Return - float between 0 and 1
    """
    result = np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) *
                                     np.linalg.norm(vec_b))
    return result.astype(float)


@jaseci_action(act_group=['bi_enc'], allow_remote=True)
def infer(contexts: Union[List[str], List[List]], candidates: Union[List[str], List[List]], context_type: str, candidate_type: str):
    """
    Take list of context, candidate and return nearest candidate to the context
    """
    global model
    model.eval()
    predicted_candidates = []
    if (context_type == "text") and (candidate_type == "text"):
        predicted_candidates = get_inference(model, tokenizer,
                                             contexts=contexts,
                                             candidates=candidates)
    elif (context_type == "text") and (candidate_type == "embedding"):
        con_embed = []
        con_embed = get_context_emb(contexts)
        for data in con_embed:
            score_dat = []
            for lbl in candidates:
                score_dat.append(cosine_sim(
                    vec_a=data, vec_b=lbl, meta="string"))
            predicted_candidates.append(float(np.argmax(score_dat)))

    elif (context_type == "embedding") and (candidate_type == "text"):
        cand_embed = []
        predicted_candidates = []
        cand_embed = get_candidate_emb(candidates)
        for data in contexts:
            score_dat = []
            for lbl in cand_embed:
                score_dat.append(cosine_sim(
                    vec_a=data, vec_b=lbl, meta="string"))
            predicted_candidates.append(candidates[np.argmax(score_dat)])
    elif (context_type == "embedding") and (candidate_type == "embedding"):
        for data in contexts:
            score_dat = []
            for lbl in candidates:
                score_dat.append(cosine_sim(
                    vec_a=data, vec_b=lbl, meta="string"))
            predicted_candidates.append(float(np.argmax(score_dat)))
    else:
        raise HTTPException(status_code=404, detail=str(
            "input type not supported"))
    return predicted_candidates


# API for training
@jaseci_action(act_group=['bi_enc'], allow_remote=True)
def train(contexts: List, candidates: List, labels: List[int]):
    """
    Take list of context, candidate, labels and trains the model
    """
    global model, model_save_path
    model.train()
    try:
        model = train_model(
            model_train=model,
            tokenizer=tokenizer,
            contexts=contexts,
            candidates=candidates,
            labels=labels
        )
        save_model(model_path=model_save_path)
        return "Model Training is complete."
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# API for geting Context Embedding
@jaseci_action(act_group=['bi_enc'], aliases=['encode_context'], allow_remote=True)
def get_context_emb(contexts: List):
    """
    Take list of context and returns the embeddings
    """
    global model, tokenizer
    model.eval()
    embedding = get_embeddings(
        model=model, tokenizer=tokenizer, text_data=contexts, embed_type="context")
    return embedding

# API for geting Candidates Embedding


@jaseci_action(act_group=['bi_enc'], aliases=['encode_candidate'], allow_remote=True)
def get_candidate_emb(candidates: List):
    """
    Take list of candidates and returns the embeddings
    """
    global model, tokenizer
    model.eval()
    embedding = get_embeddings(
        model, tokenizer, text_data=candidates, embed_type="candidate")
    return embedding


# API for setting the training and model parameters
@jaseci_action(act_group=['bi_enc'], allow_remote=True)
def get_train_config():
    try:
        with open("utils/train_config.json", "r") as jsonfile:
            data = json.load(jsonfile)
            print("Read successful")
        print(data)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=['bi_enc'], allow_remote=True)
def set_train_config(training_parameters: Dict = None):
    try:
        with open("utils/train_config.json", "r") as jsonfile:
            data = json.load(jsonfile)
        with open("utils/train_config.json", "w+") as jsonfile:
            data.update(training_parameters)
            json.dump(data, jsonfile, indent=4)
        return "Config setup is complete."
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=['bi_enc'], allow_remote=True)
def get_model_config():
    try:
        with open("utils/model_config.json", "r") as jsonfile:
            data = json.load(jsonfile)
            print("Read successful")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=['bi_enc'], allow_remote=True)
def set_model_config(model_parameters: Dict = None):
    global save_restart
    try:
        with open("utils/model_config.json", "r") as jsonfile:
            data = json.load(jsonfile)
        with open("utils/model_config.json", "w+") as jsonfile:
            data.update(model_parameters)
            json.dump(data, jsonfile, indent=4)
        save_restart = True
        config_setup()
        return "Config setup is complete."

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=['bi_enc'], allow_remote=True)
def save_model(model_path: str):
    """
    saves the model to the provided model_path
    """
    global model, tokenizer, shared
    try:
        if not model_path.isalnum():
            raise HTTPException(
                status_code=400,
                detail='Invalid model name. Only alphanumeric chars allowed.'
            )
        if not os.path.exists(model_path):
            os.makedirs(model_path)
        if shared is True:
            model.cont_bert.save_pretrained(model_path)
            tokenizer.save_vocabulary(model_path)
        else:
            cand_bert_path = os.path.join(model_path)+"/cand_bert/"
            cont_bert_path = os.path.join(model_path)+"/cont_bert/"
            if not os.path.exists(cand_bert_path):
                os.makedirs(cand_bert_path)
            if not os.path.exists(cont_bert_path):
                os.makedirs(cont_bert_path)
            tokenizer.save_vocabulary(cand_bert_path)
            tokenizer.save_vocabulary(cont_bert_path)
            model.cont_bert.save_pretrained(cont_bert_path)
            model.cand_bert.save_pretrained(cand_bert_path)

        shutil.copyfile(os.path.join(os.path.dirname(__file__), 'utils/train_config.json'),
                        os.path.join(model_path, "train_config.json"))
        shutil.copyfile(os.path.join(os.path.dirname(__file__), 'utils/model_config.json'),
                        os.path.join(model_path, "model_config.json"))
        return (f'[Saved model at] : {model_path}')
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=['bi_enc'], allow_remote=True)
def load_model(model_path):
    """
    loads the model from the provided model_path
    """
    global device, model, tokenizer, shared
    if not os.path.exists(model_path):
        raise HTTPException(
            status_code=404,
            detail='Model path is not available'
        )
    try:
        with open("utils/model_config.json", "r") as jsonfile:
            model_config_data = json.load(jsonfile)
        if model_config_data['shared'] is True:
            model_config = AutoConfig.from_pretrained(
                model_path, local_files_only=True)
            tokenizer = AutoTokenizer.from_pretrained(
                model_path, do_lower_case=True, clean_text=False)
            cont_bert = AutoModel.from_pretrained(
                model_path, local_files_only=True)
            cand_bert = cont_bert
        else:
            cand_bert_path = os.path.join(model_path, "cand_bert")
            cont_bert_path = os.path.join(model_path, "cont_bert")
            print('Loading parameters from', cand_bert_path)
            cont_bert = AutoModel.from_pretrained(
                cont_bert_path, local_files_only=True)
            cand_bert = AutoModel.from_pretrained(
                cont_bert_path, local_files_only=True)
            model_config = AutoConfig.from_pretrained(
                cont_bert_path, local_files_only=True)
            tokenizer = AutoTokenizer.from_pretrained(
                cand_bert_path, do_lower_case=True, clean_text=False)
        model = BiEncoder(config=model_config,
                          cont_bert=cont_bert, cand_bert=cand_bert, shared=shared)
        model.to(device)
        return (f'[loaded model from] : {model_path}')
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server
    launch_server(port=8000)
