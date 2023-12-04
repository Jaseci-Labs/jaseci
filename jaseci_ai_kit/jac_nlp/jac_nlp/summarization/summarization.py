from typing import List, Union
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from jaseci.jsorc.live_actions import jaseci_action
from fastapi import HTTPException
import requests
from bs4 import BeautifulSoup
from jaseci.utils.model_manager import ModelManager
from jaseci.utils.utils import model_base_path

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_BASE_PATH = model_base_path("jac_nlp/sum")


global tokenizer, model


@jaseci_action(act_group=["summarization"], allow_remote=True)
def setup(model_name: str = "philschmid/bart-large-cnn-samsum"):
    global tokenizer, model
    model_manager = ModelManager(MODEL_BASE_PATH)
    if model_manager.get_latest_version():
        active_model_path = model_manager.get_version_path()
        tokenizer = AutoTokenizer.from_pretrained(
            active_model_path, local_files_only=True
        )
        model = AutoModelForSeq2SeqLM.from_pretrained(
            active_model_path, local_files_only=True
        ).to(device)
    else:
        active_model_path = model_manager.create_version_path()
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
        model.save_pretrained(active_model_path)
        tokenizer.save_vocabulary(active_model_path)
    print(f"Loaded model: {model_name}")


@jaseci_action(act_group=["summarization"], allow_remote=True)
def summarize(
    text: Union[List[str], str] = None,
    url: str = None,
    max_length: Union[int, float] = 1.0,
    min_length: Union[int, float] = 0.1,
    num_beams: int = 4,
) -> List[str]:
    try:
        if text is not None:
            if isinstance(text, str):
                text = [text]
        elif url is not None:
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            text = [" ".join(map(lambda p: p.text, soup.find_all("p")))]
        else:
            raise HTTPException(status_code=400, detail="No text or url provided")

        inputs = tokenizer.batch_encode_plus(text, max_length=1024, return_tensors="pt")

        if not isinstance(max_length, int):
            max_length = int(inputs["input_ids"].shape[1] * max_length)
        if not isinstance(min_length, int):
            min_length = int(inputs["input_ids"].shape[1] * min_length)

        summary_ids = model.generate(
            inputs["input_ids"].to(device),
            num_beams=num_beams,
            max_length=max_length,
            min_length=min_length,
            early_stopping=True,
        )
        return tokenizer.batch_decode(
            summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    from jaseci.jsorc.remote_actions import launch_server

    launch_server(port=8000)
