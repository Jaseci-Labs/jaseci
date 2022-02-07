from msilib.schema import ListBox
from operator import mod
from pydantic import BaseModel
from typing import List,Optional
from fastapi import FastAPI, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from transformers import BertModel, BertConfig, BertTokenizer
import torch
from torch.nn import CosineSimilarity
import os
import configparser
from models import BiEncoderShared,PolyEncoderModelShared
from train import train_model
from evaluate import get_inference,get_candidate_embedding,get_context_embedding
config = configparser.ConfigParser()
model,model_name,shared,seed,poly_m,architecture,tokenizer=None,None,None,None,None,None,None
def config_setup():
    global model,model_name,shared,seed,poly_m,architecture,tokenizer,config
    config.read('config.cfg')
    model_name = config['MODEL_PARAMETERS']['MODEL_NAME']
    architecture = config['MODEL_PARAMETERS']['ARCHITECTURE']
    shared = config['MODEL_PARAMETERS']['SHARED']
    seed = config['TRAIN_PARAMETERS']['SEED']
    poly_m = config['MODEL_PARAMETERS']['POLY_M']

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    bert_config = BertConfig()
    tokenizer = BertTokenizer.from_pretrained(model_name, do_lower_case=True)
    if architecture == 'poly':
        if shared:
            model = PolyEncoderModelShared(config=bert_config, model_name=model_name, poly_m=poly_m)
    elif architecture == 'bi':
        if shared:
            model = BiEncoderShared(bert_config,model_name)
    else:
        raise Exception('Unknown architecture.')
    model.to(device)

#initializing the FastApi object
app = FastAPI()
#declaring the request body content for intent classification
class ParseText(BaseModel):
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
@app.get("/cossimilarityscore")
def cosSimilarityScore(request_data : ScoreEmbeddings):
    # cos_sim = CosineSimilarity(dim=1, eps=1e-6)
    tensors=(request_data.context_embedding,request_data.candidate_embedding)
    context_embedding,candidate_embedding= (torch.tensor(t, dtype=torch.float) for t in tensors)
    context_embedding = context_embedding.unsqueeze(1)
    dot_product = torch.matmul(context_embedding, candidate_embedding.permute(0, 2, 1))  # take this as logits
    dot_product.squeeze_(1)
    cos_similarity = (dot_product + 1) / 2
    # sim_score=cos_sim(context_embedding,candidate_embedding.squeeze(0))
    # print(cos_similarity)
    return JSONResponse(content={"cos_score":cos_similarity.item()})

@app.post("/predict")
def getinference(request_data : ParseText):
    global model
    model.eval()
    predicted_label=get_inference(model,tokenizer,context=request_data.contexts,candidate=request_data.candidates)
    return JSONResponse(content={"label":predicted_label})

@app.post("/trainmodel")
def trainModel(request_data:TrainData):
    global model
    model.train()
    try:
        model = train_model(model,tokenizer,request_data.contexts,request_data.candidates)
        return JSONResponse(content="Model Training is comnpleted",status_code=200)
    except:
        return JSONResponse(content="Error Occured",status_code=500)

@app.get("/getcontextembedding")
def getContextEmbedding(request_data : ParseText):
    global model,tokenizer
    embedding=get_context_embedding(model,tokenizer,request_data.contexts)
    return JSONResponse(content={"context_embed":embedding.cpu().numpy().tolist()})

@app.get("/getcandidateembedding")
def getCandidateEmbedding(request_data : ParseText):
    global model,tokenizer
    embedding=get_candidate_embedding(model,tokenizer,request_data.candidates)
    return JSONResponse(content={"candidate_embed":embedding.cpu().numpy().tolist()})

@app.put("/setconfig")
def setConfig(request_data : ConfigData):
    global config
    if request_data.training_parameters:
        config['TRAIN_PARAMETERS']={
        "MAX_CONTEXTS_LENGTH":request_data.training_parameters['MAX_CONTEXTS_LENGTH'],
        "MAX_RESPONSE_LENGTH":request_data.training_parameters['MAX_RESPONSE_LENGTH'],
        "TRAIN_BATCH_SIZE":request_data.training_parameters['TRAIN_BATCH_SIZE'],
        "EVAL_BATCH_SIZE":request_data.training_parameters['EVAL_BATCH_SIZE'],
        "MAX_HISTORY":request_data.training_parameters['MAX_HISTORY'],
        "LEARNING_RATE":request_data.training_parameters['LEARNING_RATE'],
        "WEIGHT_DECAY":request_data.training_parameters['WEIGHT_DECAY'],
        "WARMUP_STEPS":request_data.training_parameters['WARMUP_STEPS'],
        "ADAM_EPSILON":request_data.training_parameters['ADAM_EPSILON'],
        "MAX_GRAD_NORM":request_data.training_parameters['MAX_GRAD_NORM'],
        "NUM_TRAIN_EPOCHS":request_data.training_parameters['NUM_TRAIN_EPOCHS'],
        "SEED":request_data.training_parameters['SEED'],
        "GRADIENT_ACCUMULATION_STEPS":request_data.training_parameters['GRADIENT_ACCUMULATION_STEPS'],
        "FP16":request_data.training_parameters['FP16'],
        "FP16_OPT_LEVEL":request_data.training_parameters['FP16_OPT_LEVEL'],
        "GPU":request_data.training_parameters['GPU']
        }
    if request_data.model_parameters:
        config["MODEL_PARAMETERS"]={	
        "ARCHITECTURE":request_data.model_parameters["ARCHITECTURE"],
        "SHARED":request_data.model_parameters["SHARED"],
        "MODEL_NAME":request_data.model_parameters["MODEL_NAME"],
        "POLY_M":request_data.model_parameters["POLY_M"]
        }
        with open("config.cfg", 'w') as configfile:
            config.write(configfile)
        config_setup()
    return JSONResponse(content="config setup completed")