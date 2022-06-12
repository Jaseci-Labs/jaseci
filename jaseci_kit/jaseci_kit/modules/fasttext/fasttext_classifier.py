import os
import json
from pathlib import Path
import shutil
from typing import List, Dict
import fasttext
import traceback
from fastapi import HTTPException
from jaseci.actions.live_actions import jaseci_action
from .json_to_train import json_to_train, prep_sentence, label_to_intent
from .config import (
    model_file_path,
    train_file_path,
    clf_json_file_path,
    model_dir,
    base_json_file_path,
)

model = None
"""
Below code is to create a base_model.json file,
which help initialize a default model with a default data,
if not already exist.
"""
model_dir.mkdir(exist_ok=True, parents=True)
if not os.path.exists(base_json_file_path):
    default_data = {
        "sample_train_intent": ["this is a sample train text to create base model"]
    }
    json_object = json.dumps(default_data, indent=4)
    with open((model_dir / "base_model.json"), "w") as outfile:
        outfile.write(json_object)


def updatetrainfile(traindata: Dict[str, str] = None, train_with_existing=True):
    data = {}
    """
    if we alreading have a existing training_data.json and we have to
    train_with_existing we append the data to the  training_data.json file
    otherwise we create training_data.json from the data provided
    """

    if os.path.exists(clf_json_file_path):
        with open(clf_json_file_path) as fp:
            data = json.load(fp)
    if train_with_existing is True:
        data.update(traindata)
    else:
        data = traindata
    json_object = json.dumps(data, indent=4)
    with open(clf_json_file_path, "w") as outfile:
        outfile.write(json_object)


@jaseci_action(act_group=["fast_enc"], allow_remote=True)
def train(traindata: Dict[str, List[str]] = None, train_with_existing: bool = True):
    global model
    print("Training...")
    # we pass the ##train_with_existing param to updatetrainfile function
    updatetrainfile(traindata, train_with_existing)

    json_to_train()
    model = fasttext.train_supervised(train_file_path, lr=0.25, epoch=30, wordNgrams=3)
    # print('Compressing...')
    # model.quantize(input=train_file_path, retrain=True)
    print("Saving...")
    model.save_model(model_file_path)
    print("")
    print(f"Model saved to {model_file_path}.")

    labels = [label.replace("__label__", "") for label in model.labels]
    print("")
    print(f"LABELS ({len(labels)}):")
    for label in labels:
        print(f"- {label}")
    if traindata is None:
        return model
    else:
        return "Model training Completed"


@jaseci_action(act_group=["fast_enc"], allow_remote=True)
def load_model(model_path: str = None):
    global model, model_file_path
    if model_path is not None:
        if type(model_path) is str:
            model_path = Path(model_path)
        model_file_path = os.path.join(model_path / "model.ftz")
    if os.path.exists(model_file_path):
        print("Model exists. Loading...")
        model = fasttext.load_model(model_file_path)
        print(f"Loaded {model_file_path}")
    else:
        print("Model does not exist. Training...")
        model = train()
    if model_path is None:
        return model
    else:
        return f"Model Loaded From : {model_path}"


@jaseci_action(act_group=["fast_enc"], allow_remote=True)
def save_model(model_path: str = None):
    if not model_path.isalnum():
        raise HTTPException(
            status_code=400,
            detail="Invalid model name. Only alphanumeric chars allowed.",
        )
    elif model is None:
        raise HTTPException(status_code=404, detail="Model has not been created ,yet!")
    print("Saving...")
    if type(model_path) is str:
        model_path = Path(model_path)
    model_path.mkdir(exist_ok=True, parents=True)
    state_save_path = os.path.join(model_path / "model.ftz")
    # model_path = (model_path / "model.ftz")
    model.save_model(state_save_path)
    # we also ship the training_data.json file
    # with the model to maintain the state of the model
    shutil.copyfile(base_json_file_path, model_path / "training_data.json")
    return f"Model saved to {model_path}."


@jaseci_action(act_group=["fast_enc"], allow_remote=True)
def predict(sentences: List[str]):
    global model
    try:
        model = model if model is not None else load_model()
        result = {}
        for sentence in sentences:
            result[sentence] = []
            predictions = model.predict(prep_sentence(sentence))
            for pre in zip(predictions[0], predictions[1]):
                result[sentence].append(
                    {
                        "sentence": sentence,
                        "intent": label_to_intent(pre[0]),
                        "probability": pre[1],
                    }
                )
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    print("FasttextClassifier up and running")
    launch_server(port=8000)
