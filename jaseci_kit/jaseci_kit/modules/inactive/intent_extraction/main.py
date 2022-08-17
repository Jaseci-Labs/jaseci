from pydantic import BaseModel
from typing import List, Optional
from fastapi import FastAPI, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from flair.data import Corpus
from flair.datasets import SentenceDataset
from flair.trainers import ModelTrainer
from flair.models import TARSClassifier
from flair.data import Sentence

import os
import configparser

config = configparser.ConfigParser()
config.read("config.cfg")

# initializing the FastApi object
app = FastAPI()

# declaring the request body content for intent classification
class ParseText(BaseModel):
    text: Optional[str] = None
    labels: Optional[List] = None
    is_multi_label: Optional[bool] = True


# declaring the request body for updateDataSet
class UpdateData(BaseModel):
    text: Optional[str] = None
    label: Optional[str] = None
    topic: Optional[str] = "topic"


tars_model_name = config["TARS_MODEL"]["INTENT_MODEL"]
tars = TARSClassifier.load(tars_model_name)

# defining the api for intentclassification
@app.post("/intentclassification")
def intentClassification(request_data: ParseText):
    global tars
    if request_data.text:
        if request_data.labels:
            sentence = Sentence(request_data.text)
            tars.predict_zero_shot(
                sentence, request_data.labels, multi_label=request_data.is_multi_label
            )
            tagged_sentence = sentence.to_dict()
            json_compatible_data = jsonable_encoder(tagged_sentence)
            response_data_format = {
                "input_text": json_compatible_data["text"],
                "intents": [],
            }
            for json_data in json_compatible_data["labels"]:
                temp_dict = {}
                temp_dict["intent"] = json_data["value"]
                temp_dict["conf_score"] = json_data["confidence"]
                response_data_format["intents"].append(temp_dict)
            return JSONResponse(content=response_data_format, status_code=200)
        else:
            return JSONResponse(
                content={"Exception": "Intents are missing in request data"},
                status_code=400,
            )
    else:
        return JSONResponse(
            content={"Exception": "Text data is missing in request data"},
            status_code=400,
        )


def trainIntent(text: str, topic: str, label: str):
    global tars
    train = SentenceDataset(
        [
            Sentence(text).add_label(topic, label),
        ]
    )
    corpus = Corpus(train=train, test=train)
    # 2. make the model aware of the desired set of labels from the new corpus
    tars.add_and_switch_to_new_task(
        "Train Data",
        label_dictionary=corpus.make_label_dictionary(label_type=topic),
        label_type=topic,
    )
    # 3. initialize the text classifier trainer with your corpus
    trainer = ModelTrainer(tars, corpus)
    # 4. train model
    directory = f"taggers/{topic}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    trainer.train(
        base_path=directory,  # path to store the model artifacts
        learning_rate=0.02,
        mini_batch_size=1,
        max_epochs=10,
        train_with_dev=True,
    )
    # 5. Load few-shot TARS model
    tars = TARSClassifier.load(f"{directory}/final-model.pt")


@app.post("/updateintentdataset")
def updateDataset(request_data: UpdateData, background_tasks: BackgroundTasks):
    print(request_data)
    if request_data and request_data.label and request_data.text:
        background_tasks.add_task(
            trainIntent, request_data.text, request_data.topic, request_data.label
        )
        return JSONResponse(content="Model Training is started", status_code=200)
    else:
        return JSONResponse(content="Need Data for Text and Label", status_code=400)


@app.get("/")
def healthCheck():
    return JSONResponse(content={"Health": "Ok"}, status_code=200)
