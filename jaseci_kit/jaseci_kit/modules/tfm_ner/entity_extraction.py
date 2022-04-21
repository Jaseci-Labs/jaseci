import shutil
import os
import torch
import traceback
from fastapi import HTTPException
from jaseci.actions.live_actions import jaseci_action
from typing import List, Dict
from transformers import pipeline
from utils import tokenize_and_align_labels, train_model
from utils import save_trained_model, load_trained_model
from transformers import TrainingArguments
#from create_data import create_dataset
from utils import labelname
import json

dataset = None
model = None
tokenizer = None

# Extracting Entities
# loading deafult distilber model
# dm = loadmodel("distilbert-base-uncased", "conll2003")


def config_setup():
    """
    Loading configurations from config and
    initialize tokenizer and model
    """
    global tokenizer, model, train_config, model_config, curr_model_path
    m_config_fname = "config/model_config.json"
    t_config_fname = "config/train_config.json"
    with open(m_config_fname, "r") as jsonfile:
        model_config = json.load(jsonfile)
    with open(t_config_fname, "r") as jsonfile:
        train_config = json.load(jsonfile)
    curr_model_path = model_config["model_name"]
    mod = load_trained_model(curr_model_path)
    tokenizer = mod[0]
    model = mod[1]


config_setup()


@jaseci_action(act_group=['extract_entity'], allow_remote=True)
def extract_entity(text: str = None):

    if model is not None and tokenizer is not None:
        try:
            classifier = pipeline(
                'ner', model=model, tokenizer=tokenizer,
                aggregation_strategy="first")
            entities = classifier(text)
            ents = []
            for i in range(len(entities)):
                data = {
                    "text": entities[i]['word'],
                    "entity": entities[i]['entity_group'],
                    "score": float(entities[i]['score']),
                    # "word index" : entities[i]['index'],
                    "start": entities[i]['start'],
                    "end": entities[i]['end']
                }
                ents.append(data)
            torch.cuda.empty_cache()
            return ents
        except Exception as e:
            print(traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=404, detail=str(
            "Please train model or load previous trained model"))

# load model to memory


@jaseci_action(act_group=['extract_entity'], allow_remote=True)
def load_model(model_path: str = 'default'):
    global model, tokenizer, curr_model_path
    curr_model_path = model_path
    if not os.path.exists(model_path):
        raise HTTPException(
            status_code=404,
            detail='Model path is not available'
        )
    try:
        print("loading latest trained model to memory...")
        mod = load_trained_model(model_path)
        tokenizer = mod[0]
        model = mod[1]
        print("latest trained model successful load to memory!")
        return {"status": f"model {model_path} Loaded in memory Successfull!"}
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))

# save model to disk


@jaseci_action(act_group=['extract_entity'], allow_remote=True)
def save_model(model_path: str = 'mymodel'):
    try:
        save_trained_model(model, tokenizer, model_path)
        print(f'current model {model_path} saved to disk.')
        return {"status": f"model {model_path} saved Successfull!"}
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))


# load dataset
@jaseci_action(act_group=['extract_entity'], allow_remote=True)
def load_dataset(text: str, entity: List[Dict]):
    global dataset, label_name
    try:
        data = [{"text": text, "entity": entity}]
        # TODO: revert this
        #datasets = create_dataset(data)
        dataset = datasets[0]
        label_name = datasets[1]
        # create_dataset(text, ents)

        return {"status": "Dataset Loaded Successfull!"}
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=400, detail=str(e))


# API for setting the training and model parameters
@ jaseci_action(act_group=['extract_entity'], allow_remote=True)
def get_train_config():
    try:
        with open("config/train_config.json", "r") as jsonfile:
            data = json.load(jsonfile)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ jaseci_action(act_group=['extract_entity'], allow_remote=True)
def set_train_config(training_parameters: Dict = None):
    global train_config
    try:
        with open("config/train_config.json", "w+") as jsonfile:
            train_config.update(training_parameters)
            json.dump(train_config, jsonfile, indent=4)
        return "Config setup is complete."
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ jaseci_action(act_group=['extract_entity'], allow_remote=True)
def get_model_config():
    try:
        with open("config/model_config.json", "r") as jsonfile:
            data = json.load(jsonfile)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ jaseci_action(act_group=['extract_entity'], allow_remote=True)
def set_model_config(model_parameters: Dict = None):
    global model_config
    try:
        save_model(model_config["model_save_path"])
        with open("config/model_config.json", "w+") as jsonfile:
            model_config.update(model_parameters)
            json.dump(model_config, jsonfile, indent=4)

        config_setup()
        return "Config setup is complete."

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=['extract_entity'], allow_remote=True)
def train():
    """
    creating model traing steps
    """
    # removing old checkpoint data
    try:
        shutil.rmtree('checkpoint')
    except Exception as e:
        traceback.format_exc()
        print(str(e))

    if dataset is not None:
        try:
            global tokenizer
            global trainer
            args = TrainingArguments(
                output_dir="checkpoint",
                overwrite_output_dir=train_config['overwrite_output_dir'],
                evaluation_strategy=train_config['evaluation_strategy'],
                per_device_train_batch_size=train_config['train_batch_size'],
                per_device_eval_batch_size=train_config['eval_batch_size'],
                learning_rate=train_config['learning_rate'],
                weight_decay=train_config['weight_decay'],
                num_train_epochs=train_config['num_train_epochs']
            )

            # creating labels set
            label = labelname(label_name)
            print("#$_"*10, label, label_name)
            # Creating Tokeninzed Dataset
            print("creating tokeninzed dataset starting ..")
            tokenized_datasets = dataset.map(
                tokenize_and_align_labels,
                batched=True,
                remove_columns=dataset.column_names,
            )
            print("creating tokeninzed dataset completed!")

            trainer = train_model(tokenized_datasets, args,
                                  curr_model_path,
                                  label[0], label[1], 'default')
            # save_model('default')
            # print('model saved.')

            print("loading latest trained model ...")
            load_model('default')
            print("latest trained model successfully loaded!")
        except Exception as e:
            print(traceback.format_exc())
            raise HTTPException(status_code=500, detail=str(e))
    else:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(
            "Please load dataset for model training!"))


if __name__ == '__main__':
    from jaseci.actions.remote_actions import launch_server
    print('DistilBert model Running ...')
    launch_server(host='127.0.0.1', port=8000)
