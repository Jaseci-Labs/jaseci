# Common import of AI service
import traceback
from typing import List, Dict, Union, Mapping
import jaseci.actions.remote_actions as jra
from json_to_train import json_to_train, prep_sentence, label_to_intent
from config import model_file_path, train_file_path, clf_json_file_path
from fastapi import HTTPException
import fasttext
import os
import json
from pathlib import Path
# keeps loaded model
model = None


def updatetrainfile(traindata: Dict[str, str] = None):
    with open(clf_json_file_path) as fp:
        data = json.load(fp)
    data.update(traindata)
    json_object = json.dumps(data, indent=4)
    with open(clf_json_file_path, "w") as outfile:
        outfile.write(json_object)


@ jra.jaseci_action(act_group=['fasttext_classifier'])
def train(traindata:  Dict[str, List[str]] = None):
    global model
    print('Training...')
    if traindata is not None:
        updatetrainfile(traindata)

    json_to_train()
    model = fasttext.train_supervised(
        train_file_path, lr=0.25, epoch=30, wordNgrams=3)
    # print('Compressing...')
    # model.quantize(input=train_file_path, retrain=True)
    print('Saving...')
    model.save_model(model_file_path)
    print('')
    print(f'Model saved to {model_file_path}.')

    labels = [label.replace('__label__', '') for label in model.labels]
    print('')
    print(f'LABELS ({len(labels)}):')
    for label in labels:
        print(f'- {label}')
    if traindata is None:
        return model
    else:
        return f"Model training Completed"


@ jra.jaseci_action(act_group=['fasttext_classifier'])
def load_model(model_path: str = None):
    global model, model_file_path
    if model_path is not None:
        if type(model_path) is str:
            model_path = Path(model_path)
        model_file_path = os.path.join(model_path / "model.ftz")
    if os.path.exists(model_file_path):
        print('Model exists. Loading...')
        model = fasttext.load_model(model_file_path)
        print(f'Loaded {model_file_path}')
    else:
        print('Model does not exist. Training...')
        model = train()
    if model_path is None:
        return model
    else:
        return f"Model Loaded From : {model_path}"


@ jra.jaseci_action(act_group=['fasttext_classifier'])
def save_model(model_path: str = None):
    if not model_path.isalnum():
        raise HTTPException(
            status_code=400,
            detail='Invalid model name. Only alphanumeric chars allowed.'
        )
    elif model is None:
        raise HTTPException(
            status_code=404,
            detail='Model has not been created ,yet!'
        )
    print('Saving...')
    if type(model_path) is str:
        model_path = Path(model_path)
    model_path.mkdir(exist_ok=True, parents=True)
    state_save_path = os.path.join(model_path / "model.ftz")
    # model_path = (model_path / "model.ftz")
    model.save_model(state_save_path)
    print('')
    return (f'Model saved to {state_save_path}.')


@ jra.jaseci_action(act_group=['fasttext_classifier'])
def predict(sentences: List[str]):
    global model
    try:
        model = model if model is not None else load_model()
        result = {}
        for sentence in sentences:
            result[sentence] = []
            predictions = model.predict(prep_sentence(sentence))
            for pre in zip(predictions[0], predictions[1]):
                result[sentence].append({
                    'sentence': sentence,
                    'intent': label_to_intent(pre[0]),
                    'probability': pre[1]
                })
        return result
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    print('FasttextClassifier up and running')
    jra.launch_server(port=8000)
