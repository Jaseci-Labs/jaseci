from transformers import BartTokenizer, BartForConditionalGeneration
import torch
from typing import List, Union
from jaseci.actions.live_actions import jaseci_action
import traceback
from fastapi import HTTPException
import requests
from bs4 import BeautifulSoup


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


@jaseci_action(act_group=["bart_sum"], allow_remote=True)
def setup(
    tokenizer: str = "facebook/bart-large-cnn", model: str = "facebook/bart-large-cnn"
):
    global bart_tokenizer, bart_model
    bart_tokenizer = BartTokenizer.from_pretrained(tokenizer)
    bart_model = BartForConditionalGeneration.from_pretrained(model).to(device)


setup(tokenizer="facebook/bart-large-cnn", model="facebook/bart-large-cnn")


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
