from fastapi.responses import JSONResponse
from transformers import BertConfig, BertTokenizer
import torch.nn.functional as F
import torch
import configparser
import os
from Utilities import models, evaluate, train
from jaseci.actions.live_actions import jaseci_action
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
    poly_m = config['MODEL_PARAMETERS']['POLY_M']
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if model is None:
        bert_config = BertConfig()
        tokenizer = BertTokenizer.from_pretrained(
            model_name,
            do_lower_case=True)
        model = models.PolyEncoderModelShared(
            config=bert_config,
            model_name=model_name,
            poly_m=poly_m,
            shared=shared)
    elif save_restart:
        torch.save(model.state_dict(), state_save_path)
        bert_config = BertConfig()
        tokenizer = BertTokenizer.from_pretrained(
            model_name,
            do_lower_case=True)
        model = models.PolyEncoderModelShared(
            config=bert_config,
            model_name=model_name,
            poly_m=poly_m,
            shared=shared)
        save_restart = False
    model.to(device)


config_setup()


@jaseci_action(act_group=['poly_enc'], aliases=['get_poly_cos_sim'],
               allow_remote=True)
def cosSimilarityScore(context_embedding, candidate_embedding):
    tensors = (context_embedding, candidate_embedding)
    context_vecs, candidates_vec = (torch.tensor(
        t, dtype=torch.float) for t in tensors)
    candidates_vec = candidates_vec.view(1, 1, -1).expand(1, 1, 64)
    final_context_vec = models.dot_attention(
        candidates_vec,
        context_vecs,
        context_vecs,
        None, None)
    final_context_vec = F.normalize(final_context_vec, 2, -1)
    dot_product = torch.sum(final_context_vec * candidates_vec, -1)
    cos_similarity = (dot_product + 1) / 2
    return JSONResponse(content={"cos_score": cos_similarity.item()})


@jaseci_action(act_group=['poly_enc'], aliases=['inference'],
               allow_remote=True)
def getinference(contexts, candidates):
    global model
    model.eval()
    predicted_label = evaluate.get_inference(
        model,
        tokenizer,
        context=contexts,
        candidate=candidates)
    return JSONResponse(content={"label": predicted_label})


@jaseci_action(act_group=['poly_enc'], aliases=['train'], allow_remote=True)
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


@jaseci_action(act_group=['poly_enc'], aliases=['getcontextembedding'],
               allow_remote=True)
def getContextEmbedding(contexts):
    global model, tokenizer
    model.eval()
    embedding = evaluate.get_context_embedding(
        model,
        tokenizer,
        contexts)
    return JSONResponse(content={
        "context_embed": embedding.cpu().numpy().tolist()})


@jaseci_action(act_group=['poly_enc'], aliases=['getcandidateembedding'],
               allow_remote=True)
def getCandidateEmbedding(candidates):
    global model, tokenizer
    model.eval()
    embedding = evaluate.get_candidate_embedding(model, tokenizer, candidates)
    return JSONResponse(content={
        "candidate_embed": embedding.cpu().numpy().tolist()})


@jaseci_action(act_group=['poly_enc'], aliases=['setconfig'],
               allow_remote=True)
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
        if "POLY_M" in model_parameters:
            model_param["POLY_M"] = model_parameters["POLY_M"]
        save_restart = True
    with open("Utilities/config.cfg", 'w') as configfile:
        config.write(configfile)
        config_setup()
    return JSONResponse(content="config setup completed")
