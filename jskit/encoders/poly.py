from pydantic import BaseModel
from typing import List,Optional
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from transformers import BertModel, BertConfig, BertTokenizer
import torch
import configparser
from Utilities import models,evaluate,train
import torch.nn.functional as F

config = configparser.ConfigParser()
model,model_name,shared,seed,poly_m,tokenizer=None,None,None,None,None,None
def config_setup():
    global model,model_name,shared,seed,poly_m,tokenizer,config
    config.read('Utilities/config.cfg')
    model_name = config['MODEL_PARAMETERS']['MODEL_NAME']
    shared = config['MODEL_PARAMETERS']['SHARED']
    seed = config['TRAIN_PARAMETERS']['SEED']
    poly_m = config['MODEL_PARAMETERS']['POLY_M']

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    bert_config = BertConfig()
    tokenizer = BertTokenizer.from_pretrained(model_name, do_lower_case=True)
    if shared and (model is None):
        model = models.PolyEncoderModelShared(config=bert_config, model_name=model_name, poly_m=poly_m,shared=shared)
    model.to(device)
config_setup()
#initializing the FastApi object
app = FastAPI()
#declaring the request body content for intent classification
class ParseText(BaseModel):
    contexts: Optional[str] = None  
    candidates: Optional[List]=None

class Embeddings(BaseModel):
    contexts: Optional[str] = None  
    candidates: Optional[List]=None
class TrainData(BaseModel):
    contexts: Optional[List] = None  
    candidates: Optional[List]=None

class ScoreEmbeddings(BaseModel):
    context_embedding: List   
    candidate_embedding: List

class ConfigData(BaseModel):
    training_parameters: Optional[dict]=None   
    model_parameters: Optional[dict]=None   

import itertools
@jra.jaseci_action(act_group=['poly_enc'], aliases=['get_poly_cos_sim'])
def cosSimilarityScore(request_data : ScoreEmbeddings):
    tensors=(request_data.context_embedding,request_data.candidate_embedding)
    context_vecs,candidates_vec= (torch.tensor(t, dtype=torch.float) for t in tensors)
    candidates_vec = candidates_vec.view(1, 1, -1).expand(1, 1, 64)
    final_context_vec = models.dot_attention(candidates_vec, context_vecs, context_vecs, None, None)
    final_context_vec = F.normalize(final_context_vec, 2, -1)  # [bs, res_cnt, dim], res_cnt==bs when training
    dot_product = torch.sum(final_context_vec * candidates_vec, -1)
    cos_similarity = (dot_product + 1) / 2
    return JSONResponse(content={"cos_score":cos_similarity.item()})

@jra.jaseci_action(act_group=['poly_enc'], aliases=['inference'])
def getinference(request_data : ParseText):
    global model
    model.eval()
    predicted_label=evaluate.get_inference(model,tokenizer,context=request_data.contexts,candidate=request_data.candidates)
    return JSONResponse(content={"label":predicted_label})

@jra.jaseci_action(act_group=['poly_enc'], aliases=['train'])
def trainModel(request_data:TrainData):
    global model
    model.train()
    try:
        model = train.train_model(model,tokenizer,request_data.contexts,request_data.candidates)
        return JSONResponse(content="Model Training is comnpleted",status_code=200)
    except:
        return JSONResponse(content="Error Occured",status_code=500)

@jra.jaseci_action(act_group=['poly_enc'], aliases=['getcontextembedding'])
def getContextEmbedding(request_data : Embeddings):
    global model,tokenizer
    embedding=evaluate.get_context_embedding(model,tokenizer,request_data.contexts)
    return JSONResponse(content={"context_embed":embedding.cpu().numpy().tolist()})

@jra.jaseci_action(act_group=['poly_enc'], aliases=['getcandidateembedding'])
def getCandidateEmbedding(request_data : Embeddings):
    global model,tokenizer
    embedding=evaluate.get_candidate_embedding(model,tokenizer,request_data.candidates)
    return JSONResponse(content={"candidate_embed":embedding.cpu().numpy().tolist()})

@jra.jaseci_action(act_group=['poly_enc'], aliases=['setconfig'])
def setConfig(request_data : ConfigData):
    global config
    config.read('Utilities/config.cfg')
    train_param=config['TRAIN_PARAMETERS']
    model_param=config['MODEL_PARAMETERS']
    if request_data.training_parameters:
        if "MAX_CONTEXTS_LENGTH" in request_data.training_parameters:
            train_param["MAX_CONTEXTS_LENGTH"]=request_data.training_parameters['MAX_CONTEXTS_LENGTH']
        if "MAX_RESPONSE_LENGTH" in request_data.training_parameters:
            train_param["MAX_RESPONSE_LENGTH"]=request_data.training_parameters['MAX_RESPONSE_LENGTH']
        if "TRAIN_BATCH_SIZE" in request_data.training_parameters:            
            train_param["TRAIN_BATCH_SIZE"]=request_data.training_parameters['TRAIN_BATCH_SIZE']
        if "EVAL_BATCH_SIZE" in request_data.training_parameters: 
            train_param["EVAL_BATCH_SIZE"]=request_data.training_parameters['EVAL_BATCH_SIZE']
        if "MAX_HISTORY" in request_data.training_parameters: 
            train_param["MAX_HISTORY"]=request_data.training_parameters['MAX_HISTORY']
        if "LEARNING_RATE" in request_data.training_parameters: 
            train_param["LEARNING_RATE"]=request_data.training_parameters['LEARNING_RATE']
        if "WEIGHT_DECAY" in request_data.training_parameters: 
            train_param["WEIGHT_DECAY"]=request_data.training_parameters['WEIGHT_DECAY']
        if "WARMUP_STEPS" in request_data.training_parameters: 
            train_param["WARMUP_STEPS"]=request_data.training_parameters['WARMUP_STEPS']
        if "ADAM_EPSILON" in request_data.training_parameters: 
            train_param["ADAM_EPSILON"]=request_data.training_parameters['ADAM_EPSILON']
        if "MAX_GRAD_NORM" in request_data.training_parameters: 
            train_param["MAX_GRAD_NORM"]=request_data.training_parameters['MAX_GRAD_NORM']
        if "NUM_TRAIN_EPOCHS" in request_data.training_parameters: 
            train_param["NUM_TRAIN_EPOCHS"]=request_data.training_parameters['NUM_TRAIN_EPOCHS']
        if "SEED" in request_data.training_parameters: 
            train_param["SEED"]=request_data.training_parameters['SEED']
        if "GRADIENT_ACCUMULATION_STEPS" in request_data.training_parameters: 
            train_param["GRADIENT_ACCUMULATION_STEPS"]=request_data.training_parameters['GRADIENT_ACCUMULATION_STEPS']
        if "FP16" in request_data.training_parameters: 
            train_param["FP16"]=request_data.training_parameters['FP16']
        if "FP16_OPT_LEVEL" in request_data.training_parameters: 
            train_param["FP16_OPT_LEVEL"]=request_data.training_parameters['FP16_OPT_LEVEL']
        if "GPU" in request_data.training_parameters: 
            train_param["GPU"]=request_data.training_parameters['GPU']
    if request_data.model_parameters:
        if "SHARED" in request_data.model_parameters: 
            model_param["SHARED"]=request_data.model_parameters["SHARED"]
        if "MODEL_NAME" in request_data.model_parameters: 
            model_param["MODEL_NAME"]=request_data.model_parameters["MODEL_NAME"]
        if "POLY_M" in request_data.model_parameters: 
            model_param["POLY_M"]=request_data.model_parameters["POLY_M"]            
    with open("Utilities/config.cfg", 'w') as configfile:
        config.write(configfile)
        config_setup()
    return JSONResponse(content="config setup completed")