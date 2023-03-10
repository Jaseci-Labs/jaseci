import torch
import warnings
import configparser

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from jaseci.actions.live_actions import jaseci_action
from jaseci.actions.remote_actions import launch_server
from fastapi import HTTPException

config = configparser.ConfigParser()

model = AutoModelForSeq2SeqLM.from_pretrained(config["MODEL"]["T5_LARGE_HIQAULITY"])
tokenizer = AutoTokenizer.from_pretrained(config["TOKENIZER"]["T5_LARGE_HIQAULITY"])

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)


@jaseci_action(act_group=["paraphraser"], allow_remote=True)
def paraphrase(text: str):
    try:
        encoding = tokenizer.encode_plus(
            text, max_length=128, padding=True, return_tensors="pt"
        )
        input_ids, attention_mask = encoding["input_ids"].to(device), encoding[
            "attention_mask"
        ].to(device)

        diverse_beam_outputs = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_length=128,
            early_stopping=True,
            num_beams=5,
            num_beam_groups=5,
            num_return_sequences=5,
            diversity_penalty=0.70,
        )
        paraphrase_list = []

        for beam_output in diverse_beam_outputs:
            sent = tokenizer.decode(
                beam_output, skip_special_tokens=True, clean_up_tokenization_spaces=True
            )
            paraphrase_list.append(sent)

        return paraphrase_list

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
