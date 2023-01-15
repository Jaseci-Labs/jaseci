from typing import Dict, List
from sentence_transformers import InputExample, losses
from sentence_transformers import SentenceTransformer, models
from sentence_transformers.util import cos_sim, dot_score, semantic_search
from torch import nn
from torch.utils.data import DataLoader
import torch
import math
from datetime import datetime
import numpy as np
from fastapi import HTTPException
from jaseci.actions.live_actions import jaseci_action

"""
Declaring the training config
"""
training_config: Dict = {
    "device": "cuda" if torch.cuda.is_available() else "cpu",
    "num_epochs": 2,
    "model_save_path": (
        "output/sent_model" + "-" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ),
    "model_name": "bert-base-uncased",
}


def create_model(model_name="bert-base-uncased", max_seq_length=256):
    """
    This fumctions can be used to create a custom sbert model from transformers
    model name :- valid transformer model from the hugging face hub
    max_seq_len :- the max_seq_len that it would support for tokenization
    Returns :- returns the custom tranformer model in sbert setup
    """
    word_embedding_model = models.Transformer(model_name, max_seq_length=max_seq_length)
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
    dense_model = models.Dense(
        in_features=pooling_model.get_sentence_embedding_dimension(),
        out_features=max_seq_length,
        activation_function=nn.Tanh(),
    )

    model = SentenceTransformer(
        modules=[word_embedding_model, pooling_model, dense_model]
    )
    return model


@jaseci_action(act_group=["sbert_sim"], allow_remote=True)
def train(dataset: List, training_parameters: Dict = None):
    """
    this train function can be used to train the Sbert model to improve
    the sentence similarity.
    train data :- takes list of sentence1 and sentence2 followed by the similarity score
    training_parameter :- take the dictionary of parameters that can be used to
    manipulate the training
    Returns :- confirmations when training is completed
    """
    global model, training_config
    try:
        training_config.update(training_parameters)
        gold_samples = []
        for t_data in dataset:
            inp_example = InputExample(texts=[t_data[0], t_data[1]], label=t_data[2])
            gold_samples.append(inp_example)
        # Define your train dataset, the dataloader and the train loss
        train_dataloader = DataLoader(gold_samples, shuffle=True, batch_size=16)
        train_loss = losses.CosineSimilarityLoss(model)
        # Configure the training.
        # 10% of train data for warm-up
        warmup_steps = math.ceil(
            len(train_dataloader) * training_config["num_epochs"] * 0.1
        )
        print("Warmup-steps: {}".format(warmup_steps))
        # Tune the model
        model.fit(
            train_objectives=[(train_dataloader, train_loss)],
            epochs=training_config["num_epochs"],
            warmup_steps=warmup_steps,
            output_path=training_config["model_save_path"],
        )
        return "Model Training is completed"
    except Exception as e:
        print(e)
        return f"Error Occured {str(e)}"


@jaseci_action(act_group=["sbert_sim"], allow_remote=True)
def get_text_sim(query: List[str], corpus: List[str], top_k=1):
    """
    Calculates the similarity score between query and corpus
    query :- contains a list of queries that is scored against the list of corpus
    corpus :- contain a list of entries that is evaluated with each query
    top_k :- returns k number of top similar entries in corpus
    Returns :- a dictionary with query as key and list of top_k sentences
    from corpus as value
    """
    try:
        resp_sim_matrix = {}
        text_embeddings = model.encode(query)
        label_embeddings = model.encode(corpus)
        all_sim_data = semantic_search(text_embeddings, label_embeddings)
        count = 0
        for sim_data in all_sim_data:
            resp_sim_matrix[query[count]] = []
            for sim_obj in sim_data[:top_k]:
                resp_sim_matrix[query[count]].append(
                    {
                        "text": corpus[sim_obj["corpus_id"]],
                        "sim_score": sim_obj["score"],
                    }
                )
            count += 1
        return resp_sim_matrix
    except Exception as e:
        print(e)
        return f"Error Occured : {str(e)}"


@jaseci_action(act_group=["sbert_sim"], allow_remote=True)
def getembeddings(text: List[str]):
    """
    encodes the list of sentences provided and returns the respected embeddings
    text : contains a list of sentences to generate encodings
    Returns:  List of encoding for each text
    """
    global model
    model.eval()
    try:
        embeddings = model.encode(text)
        return {np.squeeze(np.asarray(embeddings)).tolist()}
    except Exception as e:
        print(e)
        return f"Error Occured : {str(e)}"


@jaseci_action(act_group=["sbert_sim"], allow_remote=True)
def get_cos_score(vec_a: list, vec_b: list):
    """
    Caculate the cosine similarity score of two given vectors
    Param 1 - First vector
    Param 2 - Second vector
    Return - float between 0 and 1
    """
    return np.asarray(cos_sim(vec_a, vec_b)).tolist()


@jaseci_action(act_group=["sbert_sim"], allow_remote=True)
def get_dot_score(vec_a: list, vec_b: list):
    """
    Caculate the dot product of two given vectors
    Param 1 - First vector
    Param 2 - Second vector
    Return - float between 0 and 1
    """
    return np.asarray(dot_score(vec_a, vec_b)).tolist()


@jaseci_action(act_group=["sbert_sim"], allow_remote=True)
def load_model(model_name="all-MiniLM-L12-v2", model_type="default"):
    """
    Load models load in the memory for similarty scoring
    model_type : can be default or tfm_model
            default : loads model from the sbert model zoo
            tfm_model : load tranformer model from the huggingface hub
    model_name : this is name of the model to be loaded
    Returns: confirmation if the model is loaded
    """
    global model
    if model_type == "tfm_model":
        model = create_model(model_name=model_name, max_seq_length=512)
        return f"{model_name} - loaded from huggingface hub"
    elif model_type == "default":
        model = SentenceTransformer(model_name)
        return f"{model_name} - loaded from SBERT library"
    else:
        raise HTTPException(
            status_code=500,
            detail=str(
                """Supported model_type :-  1) 'tfm_model' for transformer based models,
                                            2) 'default' for Sbert models"""
            ),
        )


@jaseci_action(act_group=["sbert_sim"], allow_remote=True)
def get_train_config():
    """
    returns the active values of the training config
    Returns: a dictionary with key as param name and value as current status
    """
    try:
        return training_config
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    load_model()
    launch_server(port=8000)
