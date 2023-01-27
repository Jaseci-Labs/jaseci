from functools import partial
from transformers import Trainer, TrainingArguments
import json
from typing import Dict, List
import os
import traceback
from fastapi import HTTPException

from .model.base_encoder import BI_Enc_NER
from .model.inference import Bi_NER_Infer
from .datamodel.utils import invert, get_category_id_mapping
from .model.tokenize_data import get_datasets
from jaseci.actions.live_actions import jaseci_action


def config_setup(category_name: List[str] = None):
    global model, example_encoder, category_id_mapping, device
    global model_args, m_config_fname, train_args, t_config_fname

    dirname = os.path.dirname(__file__)
    m_config_fname = os.path.join(dirname, "config/m_config.json")
    with open(m_config_fname, "r") as jsonfile:
        model_args = json.load(jsonfile)
    t_config_fname = os.path.join(dirname, "config/t_config.json")
    with open(t_config_fname, "r") as jsonfile:
        train_args = json.load(jsonfile)
    if category_name is None:
        category_name = ["PER", "ORG", "LOC", "MISC"]
    category_id_mapping = get_category_id_mapping(model_args, category_name)
    model_args["descriptions"] = category_name
    model = BI_Enc_NER(model_args)
    example_encoder = partial(
        model.prepare_inputs,
        category_mapping=invert(category_id_mapping),
        no_entity_category=model_args["unk_category"],
    )
    device = model.device


# initialize the model
config_setup()


@jaseci_action(act_group=["bi_ner"], allow_remote=True)
def infer(contexts: List[str]):
    """
    Take list of context, candidate and return nearest candidate to the context
    """
    predicted_candidates = []
    try:
        model_predictions = inference_model(contexts)
        for pred in range(len(contexts)):
            entity_data = {contexts[pred]: []}
            if len(model_predictions[pred]) > 0:
                for entities in model_predictions[pred]:
                    srt = list(list(entities.as_tuple()))[0]
                    end = list(list(entities.as_tuple()))[1]
                    entity_data[contexts[pred]].append(
                        {
                            "start": srt,
                            "end": end,
                            "type": list(list(entities.as_tuple()))[2],
                            "value": contexts[pred][srt:end],
                        }
                    )
            predicted_candidates.append(entity_data)
        return predicted_candidates
    except Exception as e:
        print("Exeptions : ", e)
        traceback.print_exc()


# API for training
@jaseci_action(act_group=["bi_ner"], allow_remote=True)
def train(dataset: Dict = None, from_scratch=True, training_parameters: Dict = None):
    """
    Take list of context, candidate, labels and trains the model
    """
    global model, inference_model
    if training_parameters is not None:
        with open(t_config_fname, "w+") as jsonfile:
            train_args.update(training_parameters)
            json.dump(train_args, jsonfile, indent=4)
    category_name = list(
        set(ele["entity_type"] for val in dataset["annotations"] for ele in val)
    )
    def_category = list(category_id_mapping.values())
    def_category.pop(-1)
    if from_scratch or not (sorted(def_category) == sorted(category_name)):
        config_setup(category_name=category_name)
    train_dataset = get_datasets(dataset, example_encoder)

    training_args = TrainingArguments(
        output_dir=train_args["logpath"],
        evaluation_strategy=train_args["evaluation_strategy"],
        learning_rate=train_args["learning_rate"],
        per_device_train_batch_size=train_args["train_batch_size"],
        per_device_eval_batch_size=train_args["eval_batch_size"],
        num_train_epochs=train_args["num_train_epochs"],
        weight_decay=train_args["weight_decay"],
    )
    model.train()
    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=model.collate_examples,
        train_dataset=train_dataset,
        eval_dataset=train_dataset,
    )
    train_resp = trainer.train()
    inference_model = Bi_NER_Infer(
        model,
        category_mapping=invert(category_id_mapping),
        no_entity_category=model_args["unk_category"],
        max_sequence_length=model_args["max_sequence_length"],
        max_entity_length=model_args["max_entity_length"],
        model_args=model_args,
    )
    inference_model.to(device)
    return train_resp


# API for setting the training and model parameters
@jaseci_action(act_group=["bi_ner"], allow_remote=True)
def get_train_config():
    try:
        with open(t_config_fname, "r") as jsonfile:
            data = json.load(jsonfile)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["bi_ner"], allow_remote=True)
def set_train_config(training_parameters: Dict = None):
    global train_args
    try:
        with open(t_config_fname, "w+") as jsonfile:
            train_args.update(training_parameters)
            json.dump(train_args, jsonfile, indent=4)
        return "Config setup is complete."
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["bi_ner"], allow_remote=True)
def get_model_config():
    try:
        with open(m_config_fname, "r") as jsonfile:
            model_args = json.load(jsonfile)
        return model_args
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["bi_ner"], allow_remote=True)
def set_model_config(model_parameters: Dict = None):
    global model_args
    try:
        model.save(train_args["logpath"])
        with open(m_config_fname, "w+") as jsonfile:
            model_args.update(model_parameters)
            json.dump(model_args, jsonfile, indent=4)

        config_setup()
        return "Config setup is complete."
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["bi_ner"], allow_remote=True)
def save_model(model_path: str):
    """
    saves the model to the provided model_path
    """
    try:
        return model.save(model_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["bi_ner"], allow_remote=True)
def load_model(model_path):
    """
    loads the model from the provided model_path
    """
    global model, inference_model
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Model path is not available")
    try:
        model.load(model_path)
        model.to(device)
        inference_model = Bi_NER_Infer(
            model,
            category_mapping=invert(category_id_mapping),
            no_entity_category=model_args["unk_category"],
            max_sequence_length=model_args["max_sequence_length"],
            max_entity_length=model_args["max_entity_length"],
            model_args=model_args,
        )
        inference_model.to(device)
        return f"[loaded model from] : {model_path}"
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    launch_server(port=8000)
