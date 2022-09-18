import os
import torch
from typing import Dict, List, Union
from fastapi import HTTPException
from transformers import AutoModel, AutoConfig, AutoTokenizer
import traceback
import numpy as np
from jaseci.actions.live_actions import jaseci_action
import random
import json
import shutil

from .utils.evaluate import get_embeddings  # noqa
from .utils.models import BiEncoder  # noqa
from .utils.train import train_model  # noqa


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
    trf_config = AutoConfig.from_pretrained(model_config["model_name"])
    tokenizer = AutoTokenizer.from_pretrained(
        model_config["model_name"], do_lower_case=True, clean_text=False
    )
    if model_config["shared"] is True:
        cont_bert = AutoModel.from_config(trf_config)
        cand_bert = cont_bert
        print("shared model created")
    else:
        cont_bert = AutoModel.from_config(trf_config)
        cand_bert = AutoModel.from_config(trf_config)
        print("non shared model created")
    model = BiEncoder(
        config=trf_config,
        cont_bert=cont_bert,
        cand_bert=cand_bert,
        shared=model_config["shared"],
        loss_type=model_config["loss_type"],
        loss_function=model_config["loss_function"],
    )

    model.to(train_config["device"])
    set_seed(train_config["seed"])


config_setup()


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


@jaseci_action(act_group=["bi_enc"], allow_remote=True)
def dot_prod(vec_a: List[float], vec_b: List[float]):
    """
    Caculate the dot product of two given vectors
    Param 1 - First vector
    Param 2 - Second vector
    Return - dot product
    """
    dot_product = np.matmul(vec_a, vec_b)
    return dot_product.astype(float)


@jaseci_action(act_group=["bi_enc"], allow_remote=True)
def infer(
    contexts: Union[List[str], List[List]],
    candidates: Union[List[str], List[List]],
    context_type: str,
    candidate_type: str,
):
    """
    Take list of context, candidate and return nearest candidate to the context
    """
    model.eval()
    predicted_candidates = []
    try:
        if (context_type == "text") and (candidate_type == "text"):
            con_embed = []
            con_embed = get_context_emb(contexts)
            cand_embed = get_candidate_emb(candidates)
        elif (context_type == "text") and (candidate_type == "embedding"):
            con_embed = get_context_emb(contexts)
            cand_embed = candidates
        elif (context_type == "embedding") and (candidate_type == "text"):
            con_embed = contexts
            cand_embed = get_candidate_emb(candidates)

        elif (context_type == "embedding") and (candidate_type == "embedding"):
            con_embed = contexts
            cand_embed = candidates
        else:
            raise HTTPException(status_code=404, detail=str("input type not supported"))
        for data, cont in zip(con_embed, contexts):
            score_dat = []
            out_data = {"context": str, "candidate": [], "score": [], "predicted": {}}
            if candidate_type == "embedding":
                for lbl in cand_embed:
                    if model_config["loss_type"] == "cos":
                        score_dat.append(cosine_sim(vec_a=data, vec_b=lbl))
                out_data["predicted"] = {
                    "label": candidates[
                        out_data["score"].index(max(out_data["score"]))
                    ],
                    "score": max(out_data["score"]),
                }
                predicted_candidates.append(int(np.argmax(score_dat)))
            else:
                for lbl, cand in zip(cand_embed, candidates):
                    if model_config["loss_type"] == "cos":
                        out_data["context"] = cont
                        out_data["candidate"].append(cand)
                        out_data["score"].append(cosine_sim(vec_a=data, vec_b=lbl))
                    else:
                        out_data["context"] = cont
                        out_data["candidate"].append(cand)
                        out_data["score"].append(float(dot_prod(vec_a=data, vec_b=lbl)))
                out_data["predicted"] = {
                    "label": candidates[
                        out_data["score"].index(max(out_data["score"]))
                    ],
                    "score": max(out_data["score"]),
                }
                predicted_candidates.append(out_data)
        return predicted_candidates
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=str(
                f"""input type can be
         'embedding' or 'text', context and
        candidate type should match the content of contexts and candidates.
        Exception : {e}"""
            ),
        )


# API for training
@jaseci_action(act_group=["bi_enc"], allow_remote=True)
def train(dataset: Dict = None, from_scratch=False, training_parameters: Dict = None):
    """
    Take list of context, candidate, labels and trains the model
    """
    global model
    train_data = {"contexts": [], "candidates": [], "labels": []}
    if from_scratch is True:
        save_model(model_config["model_save_path"])
        config_setup()
    model.train()
    try:
        if training_parameters is not None:
            with open(t_config_fname, "w+") as jsonfile:
                train_config.update(training_parameters)
                json.dump(train_config, jsonfile, indent=4)
        for data in dataset.keys():
            for dat in dataset[data]:
                train_data["contexts"].append(dat)
                train_data["candidates"].append(data)
                train_data["labels"].append(1)
        model = train_model(
            model=model,
            tokenizer=tokenizer,
            contexts=train_data["contexts"],
            candidates=train_data["candidates"],
            labels=train_data["labels"],
            train_config=train_config,
        )
        return "Model Training is complete."
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# API for geting Context Embedding
@jaseci_action(act_group=["bi_enc"], aliases=["encode_context"], allow_remote=True)
def get_context_emb(contexts: List):
    """
    Take list of context and returns the embeddings
    """
    model.eval()
    embedding = []
    for cont in contexts:
        embedding.append(
            get_embeddings(
                model=model,
                tokenizer=tokenizer,
                text_data=cont,
                embed_type="context",
                train_config=train_config,
            )
        )
    return embedding


# API for geting Candidates Embedding


@jaseci_action(act_group=["bi_enc"], aliases=["encode_candidate"], allow_remote=True)
def get_candidate_emb(candidates: List):
    """
    Take list of candidates and returns the embeddings
    """
    model.eval()
    embedding = get_embeddings(
        model,
        tokenizer,
        text_data=candidates,
        embed_type="candidate",
        train_config=train_config,
    )
    return embedding


# API for setting the training and model parameters
@jaseci_action(act_group=["bi_enc"], allow_remote=True)
def get_train_config():
    try:
        with open(t_config_fname, "r") as jsonfile:
            data = json.load(jsonfile)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["bi_enc"], allow_remote=True)
def set_train_config(training_parameters: Dict = None):
    global train_config
    try:
        with open(t_config_fname, "w+") as jsonfile:
            train_config.update(training_parameters)
            json.dump(train_config, jsonfile, indent=4)
        return "Config setup is complete."
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["bi_enc"], allow_remote=True)
def get_model_config():
    try:
        with open(m_config_fname, "r") as jsonfile:
            data = json.load(jsonfile)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["bi_enc"], allow_remote=True)
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


@jaseci_action(act_group=["bi_enc"], allow_remote=True)
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
        if model_config["shared"] is True:
            model.cont_bert.save_pretrained(model_path)
            tokenizer.save_vocabulary(model_path)
            print(f"Saving shared model to : {model_path}")
        else:
            cand_bert_path = os.path.join(model_path + "/cand_bert")
            cont_bert_path = os.path.join(model_path + "/cont_bert")
            if not os.path.exists(cand_bert_path):
                os.makedirs(cand_bert_path)
            if not os.path.exists(cont_bert_path):
                os.makedirs(cont_bert_path)
            tokenizer.save_vocabulary(cand_bert_path)
            tokenizer.save_vocabulary(cont_bert_path)
            model.cont_bert.save_pretrained(cont_bert_path)
            model.cand_bert.save_pretrained(cand_bert_path)
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


@jaseci_action(act_group=["bi_enc"], allow_remote=True)
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
            cont_bert = AutoModel.from_pretrained(model_path, local_files_only=True)
            cand_bert = cont_bert
            print(f"Loading shared model from : {model_path}")
        else:
            cand_bert_path = os.path.join(model_path, "cand_bert")
            cont_bert_path = os.path.join(model_path, "cont_bert")
            print(f"Loading non-shared model from : {model_path}")
            cont_bert = AutoModel.from_pretrained(cont_bert_path, local_files_only=True)
            cand_bert = AutoModel.from_pretrained(cand_bert_path, local_files_only=True)
            trf_config = AutoConfig.from_pretrained(
                cont_bert_path, local_files_only=True
            )
            tokenizer = AutoTokenizer.from_pretrained(
                cand_bert_path, do_lower_case=True, clean_text=False
            )
        model = BiEncoder(
            config=trf_config,
            cont_bert=cont_bert,
            cand_bert=cand_bert,
            shared=model_config_data["shared"],
            loss_type=model_config["loss_type"],
            loss_function=model_config["loss_function"],
        )
        model.to(train_config["device"])
        return f"[loaded model from] : {model_path}"
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    launch_server(port=8000)
