from transformers import (
    pipeline,
    GPT2Tokenizer,
    GPT2Model,
    AutoTokenizer,
    AutoModelWithLMHead,
)
import torch
from jaseci.jsorc.live_actions import jaseci_action
import traceback
from fastapi import HTTPException
from typing import List, Union
import os
from .train import prepare_data, load_dataset, get_trainer
import shutil

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = None
tokenizer = None
generator = None


@jaseci_action(act_group=["gpt2"], allow_remote=True)
def setup(model_name: str = "gpt2", get_embeddings: bool = False):
    global model, tokenizer, generator
    if get_embeddings:
        generator = None
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        tokenizer.pad_token = tokenizer.eos_token
        model = GPT2Model.from_pretrained(model_name).to(device)
    else:
        model, tokenizer = None, None
        generator = pipeline("text-generation", model=model_name, tokenizer="gpt2")


@jaseci_action(act_group=["gpt2"], allow_remote=True)
def generate(
    text: Union[List[str], str],
    max_length: int = 30,
    min_length: int = 10,
    num_return_sequences: int = 3,
) -> List:
    global generator, model, tokenizer
    if generator is None:
        model, tokenizer = None, None
        model_name = "./gpt2-trained" if os.path.exists("gpt2-trained") else "gpt2"
        setup(model_name=model_name, get_embeddings=False)
    try:
        if isinstance(text, str):
            text = [text]
        return generator(
            text,
            max_length=max_length,
            min_length=min_length,
            num_return_sequences=num_return_sequences,
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["gpt2"], allow_remote=True)
def get_embeddings(text: Union[List[str], str]) -> List:
    global model, tokenizer, generator, device
    if model is None or tokenizer is None:
        generator = None
        setup(model_name="gpt2", get_embeddings=True)
    try:
        if isinstance(text, str):
            text = [text]
        inputs = tokenizer(text, return_tensors="pt", padding=True).to(device)
        with torch.no_grad():
            outputs = model(**inputs)
        return outputs.last_hidden_state.tolist()
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@jaseci_action(act_group=["gpt2"], allow_remote=True)
def train(
    text: Union[List[str], str], epochs: int = 1, use_prev_trained=True, freeze=True
):
    if not use_prev_trained:
        shutil.rmtree("gpt2-trained", ignore_errors=True)
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    train_path, test_path = prepare_data(text)
    train_dataset, test_dataset, data_collator = load_dataset(
        train_path, test_path, tokenizer
    )
    model_name = (
        "./gpt2-trained"
        if os.path.exists("gpt2-trained") and use_prev_trained
        else "gpt2"
    )
    model = AutoModelWithLMHead.from_pretrained(model_name)

    if freeze:
        for param in model.parameters():
            param.requires_grad = False
        model.lm_head.weight.requires_grad = True

    trainer = get_trainer(model, train_dataset, test_dataset, data_collator, epochs)
    trainer.train()
    trainer.save_model()

    global generator
    generator = pipeline("text-generation", model="./gpt2-trained", tokenizer="gpt2")


if __name__ == "__main__":
    from jaseci.jsorc.remote_actions import launch_server

    launch_server(port=8000)
