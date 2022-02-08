from fastapi.responses import JSONResponse
from transformers import BertConfig, BertTokenizer
import torch
import configparser
import os
from Utilities import models, evaluate, train
import jaseci.actions.remote_actions as jra

config = configparser.ConfigParser()

model, model_name, shared, seed, tokenizer = None, None, None, None, None
save_restart = False
output_dir = "log_output"
state_save_path = os.path.join(output_dir, 'pytorch_model.bin')


def config_setup():
    global model, model_name, shared, seed, save_restart, tokenizer, config
    config.read('Utilities/config.cfg')
    model_name = config['MODEL_PARAMETERS']['MODEL_NAME']
    shared = config['MODEL_PARAMETERS']['SHARED']
    seed = config['TRAIN_PARAMETERS']['SEED']
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if model is None:
        bert_config = BertConfig()
        tokenizer = BertTokenizer.from_pretrained(model_name,
                                                  do_lower_case=True)
        model = models.BiEncoderShared(config=bert_config,
                                       model_name=model_name, shared=shared)
    elif save_restart:
        torch.save(model.state_dict(), state_save_path)
        bert_config = BertConfig()
        tokenizer = BertTokenizer.from_pretrained(model_name,
                                                  do_lower_case=True)
        model = models.BiEncoderShared(config=bert_config,
                                       model_name=model_name, shared=shared)
        save_restart = False
    model.to(device)


config_setup()


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


# change to linalg.dot function
@jra.jaseci_action(act_group=['bi_enc'], aliases=['get_bi_cos_sim'])
def cosSimilarityScore(context_embedding, candidate_embedding):
    tensors = (context_embedding, candidate_embedding)
    context_embedding, candidate_embedding = (torch.tensor
                                              (t, dtype=torch.float)
                                              for t in tensors)
    context_embedding = context_embedding.unsqueeze(1)
    dot_product = torch.matmul(context_embedding,
                               candidate_embedding.permute(0, 2, 1))
    dot_product.squeeze_(1)
    cos_similarity = (dot_product + 1) / 2
    return JSONResponse(content={"cos_score": cos_similarity.item()},
                        status_code=200)


@jra.jaseci_action(act_group=['bi_enc'], aliases=['inference'])
def getinference(contexts, candidates):
    global model
    model.eval()
    predicted_label = evaluate.get_inference(model, tokenizer,
                                             context=contexts,
                                             candidate=candidates)
    return JSONResponse(content={"label": predicted_label}, status_code=200)


@jra.jaseci_action(act_group=['bi_enc'], aliases=['train'])
def trainModel(contexts, candidates):
    global model
    model.train()
    try:
        model = train.train_model(model, tokenizer, contexts, candidates)
        return JSONResponse(content="Model Training is comnpleted",
                            status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content="Error Occured", status_code=500)


@jra.jaseci_action(act_group=['bi_enc'], aliases=['getcontextembedding'])
def getContextEmbedding(contexts):
    global model, tokenizer
    model.eval()
    embedding = evaluate.get_context_embedding(model, tokenizer, contexts)
    return JSONResponse(content={"context_embed":
                                 embedding.cpu().numpy().tolist()},
                        status_code=200)


@jra.jaseci_action(act_group=['bi_enc'], aliases=['getcandidateembedding'])
def getCandidateEmbedding(candidates):
    global model, tokenizer
    model.eval()
    embedding = evaluate.get_candidate_embedding(model, tokenizer, candidates)
    return JSONResponse(content={"candidate_embed":
                                 embedding.cpu().numpy().tolist()},
                        status_code=200)


@jra.jaseci_action(act_group=['bi_enc'], aliases=['setconfig'])
def setConfig(training_parameters, model_parameters):
    global config, save_restart
    config.read('Utilities/config.cfg')
    train_param = config['TRAIN_PARAMETERS']
    model_param = config['MODEL_PARAMETERS']
    if training_parameters:
        if "MAX_CONTEXTS_LENGTH" in training_parameters:
            train_param["MAX_CONTEXTS_LENGTH"] = training_parameters[
                'MAX_CONTEXTS_LENGTH']
        if "MAX_RESPONSE_LENGTH" in training_parameters:
            train_param["MAX_RESPONSE_LENGTH"] = training_parameters[
                'MAX_RESPONSE_LENGTH']
        if "TRAIN_BATCH_SIZE" in training_parameters:
            train_param["TRAIN_BATCH_SIZE"] = training_parameters[
                'TRAIN_BATCH_SIZE']
        if "EVAL_BATCH_SIZE" in training_parameters:
            train_param["EVAL_BATCH_SIZE"] = training_parameters[
                'EVAL_BATCH_SIZE']
        if "MAX_HISTORY" in training_parameters:
            train_param["MAX_HISTORY"] = training_parameters['MAX_HISTORY']
        if "LEARNING_RATE" in training_parameters:
            train_param["LEARNING_RATE"] = training_parameters['LEARNING_RATE']
        if "WEIGHT_DECAY" in training_parameters:
            train_param["WEIGHT_DECAY"] = training_parameters['WEIGHT_DECAY']
        if "WARMUP_STEPS" in training_parameters:
            train_param["WARMUP_STEPS"] = training_parameters['WARMUP_STEPS']
        if "ADAM_EPSILON" in training_parameters:
            train_param["ADAM_EPSILON"] = training_parameters['ADAM_EPSILON']
        if "MAX_GRAD_NORM" in training_parameters:
            train_param["MAX_GRAD_NORM"] = training_parameters['MAX_GRAD_NORM']
        if "NUM_TRAIN_EPOCHS" in training_parameters:
            train_param["NUM_TRAIN_EPOCHS"] = training_parameters[
                'NUM_TRAIN_EPOCHS']
        if "SEED" in training_parameters:
            train_param["SEED"] = training_parameters['SEED']
        if "GRADIENT_ACCUMULATION_STEPS" in training_parameters:
            train_param["GRADIENT_ACCUMULATION_STEPS"] = training_parameters[
                'GRADIENT_ACCUMULATION_STEPS']
        if "FP16" in training_parameters:
            train_param["FP16"] = training_parameters['FP16']
        if "FP16_OPT_LEVEL" in training_parameters:
            train_param["FP16_OPT_LEVEL"] = training_parameters[
                'FP16_OPT_LEVEL']
        if "GPU" in training_parameters:
            train_param["GPU"] = training_parameters['GPU']
    if model_parameters:
        if "SHARED" in model_parameters:
            model_param["SHARED"] = model_parameters["SHARED"]
        if "MODEL_NAME" in model_parameters:
            model_param["MODEL_NAME"] = model_parameters["MODEL_NAME"]
        save_restart = True
    with open("Utilities/config.cfg", 'w') as configfile:
        config.write(configfile)
        config_setup()
    return JSONResponse(content="config setup completed", status_code=200)
