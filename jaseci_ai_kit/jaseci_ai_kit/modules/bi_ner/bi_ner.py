from functools import partial
from transformers import Trainer, TrainingArguments
import json
from typing import Dict, List  # , Set, Iterable, Tuple
import os
import numpy as np
import traceback
from .model.base_encoder import BI_Enc_NER
from .model.inference import InferenceBinder
from .datamodel.utils import invert, get_category_id_mapping
from .model.tokenize_data import get_datasets
from jaseci.actions.live_actions import jaseci_action


def config_setup(category_name: List[str] = None):
    global model, example_encoder, category_id_mapping, model_args, device
    dirname = os.path.dirname(__file__)
    m_config_fname = os.path.join(dirname, "model\\m_config.json")
    with open(m_config_fname, "r") as jsonfile:
        model_args = json.load(jsonfile)
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


# API for getting the cosine similarity
@jaseci_action(act_group=["bi_ner"], allow_remote=True)
def cosine_sim(vec_a: List[float], vec_b: List[float]):
    """
    Caculate the cosine similarity score of two given vectors
    Param 1 - First vector
    Param 2 - Second vector
    Return - float between 0 and 1
    """

    result = np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
    return result.astype(float)


@jaseci_action(act_group=["bi_ner"], allow_remote=True)
def dot_prod(vec_a: List[float], vec_b: List[float]):
    """
    Caculate the dot product of two given vectors
    Param 1 - First vector
    Param 2 - Second vector
    Return - dot product
    """
    dot_product = np.matmul(vec_a, vec_b)
    return dot_product.astype(float)


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
    if from_scratch:
        category_name = list(
            set(ele["entity_type"] for val in dataset["annotations"] for ele in val)
        )
        config_setup(category_name=category_name)
    train_dataset = get_datasets(dataset, example_encoder)

    training_args = TrainingArguments(
        output_dir="./result",
        evaluation_strategy="epoch",
        learning_rate=3e-5,
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        num_train_epochs=30,
        weight_decay=0.01,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=model.collate_examples,
        train_dataset=train_dataset,
        eval_dataset=train_dataset,
    )
    train_resp = trainer.train()
    model.eval()
    inference_model = InferenceBinder(
        model,
        category_mapping=invert(category_id_mapping),
        no_entity_category=model_args["unk_category"],
        max_sequence_length=model_args["max_sequence_length"],
        max_entity_length=model_args["max_entity_length"],
        model_args=model_args,
    )
    inference_model.to(device)
    return train_resp


if __name__ == "__main__":
    config_setup()
    from jaseci.actions.remote_actions import launch_server

    launch_server(port=8000)
