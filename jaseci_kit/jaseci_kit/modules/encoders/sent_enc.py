from typing import List
from sentence_transformers import InputExample, losses
from sentence_transformers import SentenceTransformer, models
from sentence_transformers.util import cos_sim
from torch import nn
from torch.utils.data import DataLoader
import nlpaug.augmenter.word as naw
import torch
import math
from datetime import datetime
import numpy as np
from fastapi.responses import JSONResponse
from jaseci.actions.live_actions import jaseci_action

model_name = "bert-base-uncased"
device = "cuda" if torch.cuda.is_available() else "cpu"
num_epochs = 2
model_save_path = (
    "output/sent_"
    + model_name.replace("/", "-")
    + "-"
    + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
)


def create_model(model_name="bert-base-uncased", max_seq_length=256):
    word_embedding_model = models.Transformer(model_name, max_seq_length=max_seq_length)
    pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension())
    dense_model = models.Dense(
        in_features=pooling_model.get_sentence_embedding_dimension(),
        out_features=256,
        activation_function=nn.Tanh(),
    )

    model = SentenceTransformer(
        modules=[word_embedding_model, pooling_model, dense_model]
    )
    return model


model = create_model(model_name=model_name, max_seq_length=256)


def get_aug_sample(text1, text2):
    # Synonym replacement using BERT ####
    aug = naw.ContextualWordEmbsAug(
        model_path=model_name, action="insert", device=device
    )
    aug_samples = []
    for sample1, sample2 in zip(text1, text2):
        augmented_texts = aug.augment([sample1, sample2])
        print(augmented_texts)
        inp_example = InputExample(texts=augmented_texts, label=0)
        aug_samples.append(inp_example)
    print("Textual augmentation completed....")
    print("Number of silver pairs generated: {}".format(len(aug_samples)))
    return aug_samples


@jaseci_action(act_group=["sent_enc"], aliases=["train_model"], allow_remote=True)
def train(text1: List[str], text2: List[str]):
    global model, model_name, device

    try:
        gold_samples = []
        for sample1, sample2 in zip(text1, text2):
            inp_example = InputExample(texts=[sample1, sample2], label=1)
            gold_samples.append(inp_example)
        # generate Samples for 0 labels
        aug_samples = get_aug_sample(text1, text2)
        # Define your train dataset, the dataloader and the train loss
        train_dataloader = DataLoader(
            gold_samples + aug_samples, shuffle=True, batch_size=16
        )
        train_loss = losses.ContrastiveLoss(model)
        # Configure the training.
        # 10% of train data for warm-up
        warmup_steps = math.ceil(len(train_dataloader) * num_epochs * 0.1)
        print("Warmup-steps: {}".format(warmup_steps))
        # Tune the model
        model.fit(
            train_objectives=[(train_dataloader, train_loss)],
            epochs=num_epochs,
            warmup_steps=warmup_steps,
            output_path=model_save_path,
        )
        return JSONResponse(content="Model Training is comnpleted", status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content=f"Error Occured {str(e)}", status_code=500)


@jaseci_action(act_group=["sent_enc"], aliases=["inference"])
def predict(text1: str, text2: List[str]):
    try:
        sim = np.zeros(len(text2))
        text_embeddings = model.encode(text1)
        label_embeddings = model.encode(text2)
        for i in range(len(text2)):
            sim[i] = cos_sim(text_embeddings, label_embeddings[i])
        print(sim)
        return JSONResponse(
            {"label": text2[np.argmax(sim)], "conf_score": sim[np.argmax(sim)]}
        )
    except Exception as e:
        print(e)
        return JSONResponse(content=f"Error Occured : {str(e)}", status_code=500)


@jaseci_action(act_group=["sent_enc"], aliases=["getembeddings"])
def getEmbedding(text):
    global model
    model.eval()
    try:
        embeddings = model.encode(text)
        return JSONResponse(
            content={"embed": np.squeeze(np.asarray(embeddings)).tolist()},
            status_code=200,
        )
    except Exception as e:
        print(e)
        return JSONResponse(content=f"Error Occured : {str(e)}", status_code=500)


@jaseci_action(act_group=["sent_enc"], aliases=["get_cos_sim"])
def cosine_sim(vec_a: list, vec_b: list, meta):
    """
    Caculate the cosine similarity score of two given vectors
    Param 1 - First vector
    Param 2 - Second vector
    Return - float between 0 and 1
    """
    result = np.dot(vec_a, vec_b) / (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
    return result.astype(float)
