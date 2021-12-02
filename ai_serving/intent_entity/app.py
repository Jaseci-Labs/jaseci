from pydantic import BaseModel
from typing import List,Optional
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForTokenClassification

#initializing the FastApi object
app = FastAPI()

#declaring the request body content
class ParseText(BaseModel):
    text: str 
    labels: List
    is_multi_label: Optional[bool] = False

#zero-Shot_model
zs_model_name="joeddav/bart-large-mnli-yahoo-answers"
zs_pipeline = pipeline("zero-shot-classification", model=zs_model_name)
print("Label Classification Model Loaded\n")

#NER-Model
ner_model_name = "dbmdz/bert-large-cased-finetuned-conll03-english"
tokenizer = AutoTokenizer.from_pretrained(ner_model_name)
model = AutoModelForTokenClassification.from_pretrained(ner_model_name)
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer)
print("NER Model Loaded\n")

#defining the api for intentclassification
@app.post("/intentclassification")
def intentClassification(request_data : ParseText):
    print(request_data.text)
    zs_results = zs_pipeline(request_data.text, request_data.labels, multi_label=request_data.is_multi_label)
    print("Label Classification Score :\n")
    print(f'Text : {zs_results["sequence"]} \n\t\tIntents\t\t\t\t\t\tScores\n{zs_results["labels"]} : {zs_results["scores"]}')
    json_compatible_data = jsonable_encoder(zs_results)
    return JSONResponse(content=json_compatible_data,status_code=200)

#defining the api for entitydetection
@app.post("/entitydetection")
def entityDetection(text : str):
    ner_results = ner_pipeline(text)
    entities=[]
    for results in ner_results:
        entities.append({"entity" : results["entity"],"conf_score":float(results["score"]),"word":results["word"]})
    json_compatible_data = jsonable_encoder(entities)
    return JSONResponse(content=json_compatible_data,status_code=200)
