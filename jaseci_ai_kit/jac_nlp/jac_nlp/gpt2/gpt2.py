from transformers import pipeline, GPT2Tokenizer, GPT2Model
import torch
from jaseci.actions.live_actions import jaseci_action
import traceback
from fastapi import HTTPException
from typing import List, Union

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = None
tokenizer = None
generator = None


def setup(model_name: str = "gpt2-medium", get_embeddings: bool = False):
    global model, tokenizer, generator
    if get_embeddings:
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        tokenizer.pad_token = tokenizer.eos_token
        model = GPT2Model.from_pretrained(model_name).to(device)
    else:
        generator = pipeline("text-generation", model=model_name)


setup(model_name="gpt2-medium", get_embeddings=False)


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
        setup(model_name="gpt2-medium", get_embeddings=False)
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
        setup(model_name="gpt2-medium", get_embeddings=True)
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


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    launch_server(port=8000)
