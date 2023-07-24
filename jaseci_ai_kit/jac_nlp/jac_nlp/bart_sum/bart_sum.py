from transformers import BartTokenizer, BartForConditionalGeneration
import torch
from typing import List, Union
from jaseci.jsorc.live_actions import jaseci_action
import traceback
from fastapi import HTTPException
import requests
from bs4 import BeautifulSoup
from jaseci.utils.utils import model_base_path
import os

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BART_SUM_ROOT = model_base_path("jac_nlp/bart_sum")


@jaseci_action(act_group=["bart_sum"], allow_remote=True)
def setup(
    tokenizer: str = "facebook/bart-large-cnn",
    model: str = "philschmid/bart-large-cnn-samsum",
):
    global bart_tokenizer, bart_model
    os.makedirs(BART_SUM_ROOT, exist_ok=True)
    if all(
        os.path.isfile(os.path.join(BART_SUM_ROOT, f_name))
        for f_name in ["vocab.json", "pytorch_model.bin", "config.json"]
    ):
        bart_tokenizer = BartTokenizer.from_pretrained(tokenizer, local_files_only=True)
        bart_model = BartForConditionalGeneration.from_pretrained(
            model, local_files_only=True
        ).to(device)
    else:
        bart_tokenizer = BartTokenizer.from_pretrained(tokenizer)
        bart_model = BartForConditionalGeneration.from_pretrained(model).to(device)
        bart_model.save_pretrained(BART_SUM_ROOT)
        bart_tokenizer.save_vocabulary(BART_SUM_ROOT)


@jaseci_action(act_group=["bart_sum"], allow_remote=True)
def summarize(
    text: Union[List[str], str] = None,  # type: ignore
    url: str = None,  # type: ignore
    max_length: Union[int, float] = 1.0,
    min_length: Union[int, float] = 0.1,
    num_beams: int = 4,
) -> List[str]:
    global bart_tokenizer, bart_model
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

        inputs = bart_tokenizer.batch_encode_plus(
            text, max_length=1024, return_tensors="pt"
        )

        if not isinstance(max_length, int):
            max_length = int(inputs["input_ids"].shape[1] * max_length)
        if not isinstance(min_length, int):
            min_length = int(inputs["input_ids"].shape[1] * min_length)

        summary_ids = bart_model.generate(
            inputs["input_ids"].to(device),
            num_beams=num_beams,
            max_length=max_length,
            min_length=min_length,
            early_stopping=True,
        )
        return bart_tokenizer.batch_decode(
            summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    from jaseci.jsorc.remote_actions import launch_server

    launch_server(port=8000)
