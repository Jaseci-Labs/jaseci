import torch
from jaseci.actions.live_actions import jaseci_action
from transformers import T5Tokenizer, T5ForConditionalGeneration  # , T5Config

# from fastapi import HTTPException

model = T5ForConditionalGeneration.from_pretrained("t5-small")
tokenizer = T5Tokenizer.from_pretrained("t5-small")
device = torch.device("cpu")


# generates summary based on text
def t5_generate_sum(text, min_length, max_length):
    preprocess_text = text.strip().replace("\n", "")
    t5_prepared_Text = "summarize: " + preprocess_text

    tokenized_text = tokenizer.encode(t5_prepared_Text, return_tensors="pt").to(device)

    summary_ids = model.generate(
        tokenized_text,
        num_beams=4,
        no_repeat_ngram_size=2,
        min_length=min_length,
        max_length=max_length,
        early_stopping=True,
    )

    output = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return output


# summarize a large body of text using t5 model (small model)
# which returns data at a fast rate.
@jaseci_action(act_group=["t5_sum"], allow_remote=True)
def classify_text(text: str, min_length: int = 30, max_length: int = 100):
    output = t5_generate_sum(text, min_length, max_length)
    return output


if __name__ == "__main__":
    from jaseci.actions.remote_actions import launch_server

    launch_server(port=8000)
