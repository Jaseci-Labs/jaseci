import os
import configparser
import torch
from typing import Dict, List
from fastapi import HTTPException
from transformers import AutoModel, AutoConfig, AutoTokenizer
from utils.evaluate import get_embeddings, get_inference
from utils.models import BiEncoder
import traceback
import numpy as np
from utils.train import train_model
from jaseci.actions.live_actions import jaseci_action
import random

config = configparser.ConfigParser()
model, model_name, shared, seed, tokenizer = None, None, None, None, None
save_restart = False
output_dir = "logoutput"
device = torch.device("cpu")
# uncomment this if you wish to use GPU to train
# this is commented out because this causes issues with
# unittest on machines with GPU
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# funtion to set seed for the module
def set_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


# function for config setup
config.read('utils/config.cfg')


def config_setup():
    """
    Loading configurations from utils/config.cfg and initialize tokenizer and model
    """
    global seed, model, save_restart, tokenizer, device, shared, config
    model_name = config['MODEL_PARAMETERS']['MODEL_NAME']
    shared = config['MODEL_PARAMETERS']['SHARED']
    seed = int(config['TRAIN_PARAMETERS']['SEED'])
    if model is None:
        model_config = AutoConfig.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name,
                                                  do_lower_case=True, clean_text=False)
        if shared == "True":
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
        # torch.save(model.state_dict(), DEFAULT_MODEL_PATH)
        saved_text = save_model(output_dir)
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
    set_seed(seed)


config_setup()

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
def infer(contexts: List, candidates: List):
    """
    Take list of context, candidate and return nearest candidate to the context
    """
    global model
    model.eval()
    predicted_candidate = get_inference(model, tokenizer,
                                        contexts=contexts,
                                        candidates=candidates)
    return predicted_candidate


# API for training
@jaseci_action(act_group=['bi_enc'], allow_remote=True)
def train(contexts: List, candidates: List, labels: List[int]):
    """
    Take list of context, candidate, labels and trains the model
    """
    global model
    model.train()
    try:
        model = train_model(
            model_train=model,
            tokenizer=tokenizer,
            contexts=contexts,
            candidates=candidates,
            labels=labels,
            output_dir="model_output"
        )
        return "Model Training is complete."
    except Exception as e:
        print(e)
        print(traceback.print_exc())
        raise HTTPException(status_code=500, detail=str(e))


# API for geting Context Embedding
@jaseci_action(act_group=['bi_enc'], aliases=['encode_context'])
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


@jaseci_action(act_group=['bi_enc'], aliases=['encode_candidate'])
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
def set_config(training_parameters: Dict = None, model_parameters: Dict = None):
    """
    Update the configuration file with any new incoming parameters
    """
    global config, save_restart
    config.read('utils/config.cfg')
    if training_parameters:
        config['TRAIN_PARAMETERS'].update(training_parameters)
    if model_parameters:
        config['MODEL_PARAMETERS'].update(model_parameters)
        save_restart = True
    with open("utils/config.cfg", 'w') as configfile:
        config.write(configfile)
    try:
        config_setup()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return "Config setup is complete."


@jaseci_action(act_group=['bi_enc'], allow_remote=True)
def save_model(model_path: str):
    """
    saves the model to the provided model_path
    """
    global model, tokenizer, shared, config
    try:
        if not model_path.isalnum():
            raise HTTPException(
                status_code=400,
                detail='Invalid model name. Only alphanumeric chars allowed.'
            )
        if not os.path.exists(model_path):
            os.makedirs(model_path)
        if shared == "True":
            model.config.to_json_file(model_path + "/config.json")
            tokenizer.save_vocabulary(model_path)
            torch.save(model.cand_bert.state_dict(),
                       model_path+"/pytorch_model.bin")
            with open(model_path+"/config.cfg", 'w') as fp:
                config.write(fp)
        else:
            cand_bert_path = os.path.join(model_path)+"/cand_bert/"
            cont_bert_path = os.path.join(model_path)+"/cont_bert/"
            if not os.path.exists(cand_bert_path):
                os.makedirs(cand_bert_path)
            if not os.path.exists(cont_bert_path):
                os.makedirs(cont_bert_path)
            model.cand_bert.config.to_json_file(cand_bert_path + "config.json")
            model.cont_bert.config.to_json_file(cont_bert_path + "config.json")
            tokenizer.save_vocabulary(cand_bert_path)
            tokenizer.save_vocabulary(cont_bert_path)
            torch.save(model.cand_bert.state_dict(),
                       cand_bert_path+"pytorch_model.bin")
            torch.save(model.cont_bert.state_dict(),
                       cont_bert_path+"pytorch_model.bin")
            with open(model_path+"/config.cfg", 'w') as fp:
                config.write(fp)
        return (f'[Saved model at] : {model_path}')
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=['bi_enc'], allow_remote=True)
def load_model(model_path):
    """
    loads the model from the provided model_path
    """
    global device, model, tokenizer, shared, config
    if not os.path.exists(model_path):
        raise HTTPException(
            status_code=404,
            detail='Model path is not available'
        )
    try:
        config.read(model_path+'/config.cfg')
        shared = config['MODEL_PARAMETERS']['SHARED']
        if shared == "True":
            model_config = AutoConfig.from_pretrained(model_name)
            tokenizer = AutoTokenizer.from_pretrained(os.path.join(
                model_path, "vocab.txt"), do_lower_case=True, clean_text=False)
            cont_bert_state_dict = torch.load(
                model_path+"/pytorch_model.bin", map_location="cpu")
            cont_bert = AutoModel.from_pretrained(
                model_path, state_dict=cont_bert_state_dict)
            cand_bert = cont_bert
        else:
            cand_bert_path = os.path.join(model_path, "cand_bert")
            cont_bert_path = os.path.join(model_path, "cont_bert")
            print('Loading parameters from', cand_bert_path)
            cont_bert_state_dict = torch.load(
                cont_bert_path+"/pytorch_model.bin", map_location="cpu")
            cand_bert_state_dict = torch.load(
                cand_bert_path+"/pytorch_model.bin", map_location="cpu")
            cont_bert = AutoModel.from_pretrained(
                cont_bert_path, state_dict=cont_bert_state_dict)
            cand_bert = AutoModel.from_pretrained(
                cand_bert_path, state_dict=cand_bert_state_dict)
            tokenizer = AutoTokenizer.from_pretrained(os.path.join(
                cand_bert_path), do_lower_case=True, clean_text=False)
            model_config = AutoConfig.from_pretrained(
                os.path.join(cand_bert_path, 'config.json'))
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
