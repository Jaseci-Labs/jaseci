import os, configparser
import torch
from fastapi import HTTPException
from transformers import BertConfig, BertTokenizer
from utils.models import BiEncoderShared
from utils.evaluate import (
    get_context_embedding,
    get_candidate_embedding,
    get_inference
)
from utils.train import train_model
import jaseci.actions.remote_actions as jra

config = configparser.ConfigParser()
model, model_name, shared, seed, tokenizer = None, None, None, None, None
save_restart = False
output_dir = "log_output"
DEFAULT_MODEL_NAME = 'pytorch_model.bin'
DEFAULT_MODEL_PATH = os.path.join(output_dir, 'pytorch_model.bin')


def config_setup():
    """
    Loading configurations from utils/config.cfg and initialize tokenizer and model
    """
    global seed, model, save_restart, tokenizer
    config.read('utils/config.cfg')
    model_name = config['MODEL_PARAMETERS']['MODEL_NAME']
    shared = config['MODEL_PARAMETERS']['SHARED']
    seed = config['TRAIN_PARAMETERS']['SEED']
    device = torch.device("cpu")
    # uncomment this if you wish to use GPU to train
    # this is commented out because this causes issues with
    # unittest on machines with GPU
    #device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if model is None:
        bert_config = BertConfig()
        tokenizer = BertTokenizer.from_pretrained(model_name,
                                                  do_lower_case=True)
        model = BiEncoderShared(config=bert_config,
                                model_name=model_name, shared=shared)
    elif save_restart:
        torch.save(model.state_dict(), DEFAULT_MODEL_PATH)
        bert_config = BertConfig()
        tokenizer = BertTokenizer.from_pretrained(model_name,
                                                  do_lower_case=True)
        model = BiEncoderShared(config=bert_config,
                                model_name=model_name, shared=shared)
        save_restart = False
    model.to(device)

config_setup()

@jra.jaseci_action(act_group=['bi_enc'])
def cos_sim_score(context_embedding, candidate_embedding):
    tensors = (context_embedding, candidate_embedding)
    context_embedding, candidate_embedding = (torch.tensor
                                              (t, dtype=torch.float)
                                              for t in tensors)
    context_embedding = context_embedding.unsqueeze(1)
    dot_product = torch.matmul(context_embedding,
                               candidate_embedding.permute(0, 2, 1))
    dot_product.squeeze_(1)
    cos_similarity = (dot_product + 1) / 2
    return cos_similarity.item()

# TODO: change to linalg.dot function?
# @jra.jaseci_action(act_group=['bi_enc'], aliases=['get_bi_cos_sim'])
# def cosine_sim(vec_a: list, vec_b: list, meta):
#     """
#     Caculate the cosine similarity score of two given vectors
#     Param 1 - First vector
#     Param 2 - Second vector
#     Return - float between 0 and 1
#     """
#     result = np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) *
#                                      np.linalg.norm(vec_b))
#     return result.astype(float)

@jra.jaseci_action(act_group=['bi_enc'])
def infer(contexts, candidates):
    global model
    model.eval()
    predicted_label = get_inference(model, tokenizer,
                                    context=contexts,
                                    candidate=candidates)
    return predicted_label

@jra.jaseci_action(act_group=['bi_enc'])
def train(contexts, candidates):
    global model
    model.train()
    try:
        model = train_model(model, tokenizer, contexts, candidates)
        return "Model Training is complete."
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

@jra.jaseci_action(act_group=['bi_enc'], aliases=['encode_context'])
def get_context_emb(contexts):
    global model, tokenizer
    model.eval()
    embedding = get_context_embedding(model, tokenizer, contexts)
    return embedding.cpu().numpy().tolist()

@jra.jaseci_action(act_group=['bi_enc'], aliases=['encode_candidate'])
def get_candidate_emb(candidates):
    global model, tokenizer
    model.eval()
    embedding = get_candidate_embedding(model, tokenizer, candidates)
    return embedding.cpu().numpy().tolist()

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
