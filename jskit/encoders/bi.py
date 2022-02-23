import os
import configparser
import torch
from typing import List
from fastapi import HTTPException
from transformers import BertModel, BertConfig, BertTokenizer
from utils.evaluate import get_embeddings
from utils.models import BiEncoder
import traceback
import numpy as np
from utils.train import train_model
import jaseci.actions.remote_actions as jra

config = configparser.ConfigParser()
model, model_name, shared, seed, tokenizer = None, None, None, None, None
save_restart = False
output_dir = "log_output"
DEFAULT_MODEL_NAME = 'pytorch_model.bin'
DEFAULT_MODEL_PATH = os.path.join(output_dir, 'pytorch_model.bin')


# function for config setup
def config_setup():
    """
    Loading configurations from utils/config.cfg and initialize tokenizer and model
    """
    global seed, model, save_restart, tokenizer
    config.read('utils/config.cfg')
    model_name = config['MODEL_PARAMETERS']['MODEL_NAME']
    shared = config['MODEL_PARAMETERS']['SHARED']
    seed = int(config['TRAIN_PARAMETERS']['SEED'])
    device = torch.device("cpu")
    # uncomment this if you wish to use GPU to train
    # this is commented out because this causes issues with
    # unittest on machines with GPU
    #device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if model is None:
        bert_config = BertConfig()
        tokenizer = BertTokenizer.from_pretrained(model_name,
                                                  do_lower_case=True, clean_text=False)
        if shared is True:
            cont_bert = BertModel(bert_config)
            cand_bert = cont_bert
            print("shared model created")
        else:
            cont_bert = BertModel(bert_config)
            cand_bert = BertModel(bert_config)
            print("non shared model created")
        model = BiEncoder(config=bert_config,
                          cont_bert=cont_bert, cand_bert=cand_bert, shared=shared)

    elif save_restart:
        torch.save(model.state_dict(), DEFAULT_MODEL_PATH)
        bert_config = BertConfig()
        tokenizer = BertTokenizer.from_pretrained(model_name,
                                                  do_lower_case=True, clean_text=False)
        cont_bert = BertModel(bert_config)
        cand_bert = BertModel(bert_config)
        model = BiEncoder(config=bert_config,
                          cont_bert=cont_bert, cand_bert=cand_bert, shared=shared)
        save_restart = False
    model.to(device)


config_setup()

# API for getting the cosine similarity


@jra.jaseci_action(act_group=['bi_enc'])
def cosine_sim(vec_a: list, vec_b: list, meta):
    """
    Caculate the cosine similarity score of two given vectors
    Param 1 - First vector
    Param 2 - Second vector
    Return - float between 0 and 1
    """
    result = np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) *
                                     np.linalg.norm(vec_b))
    return result.astype(float)


# @jra.jaseci_action(act_group=['bi_enc'])
# def infer(contexts, candidates):
#     global model
#     model.eval()
#     predicted_label = get_inference(model, tokenizer,
#                                     context=contexts,
#                                     candidate=candidates)
#     return predicted_label

# API for training
@jra.jaseci_action(act_group=['bi_enc'])
def train(contexts: List, candidates: List):
    global model
    model.train()
    try:
        model = train_model(model, tokenizer, contexts,
                            candidates, output_dir="model_output")
        return "Model Training is complete."
    except Exception as e:
        print(e)
        print(traceback.print_exc())
        raise HTTPException(status_code=500, detail=str(e))

# API for geting Context Embedding


@jra.jaseci_action(act_group=['bi_enc'], aliases=['encode_context'])
def get_context_emb(contexts: List):
    global model, tokenizer
    model.eval()
    embedding = get_embeddings(
        model=model, tokenizer=tokenizer, text_data=contexts, embed_type="context")
    return embedding

# API for geting Candidates Embedding


@jra.jaseci_action(act_group=['bi_enc'], aliases=['encode_candidate'])
def get_candidate_emb(candidates: List):
    global model, tokenizer
    model.eval()
    embedding = get_embeddings(
        model, tokenizer, text_data=candidates, embed_type="candidate")
    return embedding

# API for setting the training and model parameters


@jra.jaseci_action(act_group=['bi_enc'])
def set_config(training_parameters, model_parameters):
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

    config_setup()
    return "Config setup is complete."


@jra.jaseci_action(act_group=['bi_enc'])
def save_model(model_name):
    global model
    if not model.isalnum():
        raise HTTPException(
            status_code=400,
            detail='Invalid model name. Only alphanumeric chars allowed.'
        )
    model_path = os.path.join(output_dir, f'{model_name}.bin')
    torch.save(model.state_dict(), model_path)


@jra.jaseci_action(act_group=['bi_enc'])
def load_model(model_name):
    pass


if __name__ == "__main__":
    jra.launch_server(port=8000)
