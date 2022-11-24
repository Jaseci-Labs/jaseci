from transformers import BartTokenizer, BartForConditionalGeneration
import torch
from typing import List, Union
from jaseci.actions.live_actions import jaseci_action


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

bart_tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")
bart_model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn").to(
    device
)

@jaseci_action(act_group=["bart_sum"], allow_remote=True)
def summarize(
    text: Union[List[str], str],
    max_length: int = 100,
    min_length: int = 10,
    num_beams: int = 4,
) -> Union[List[str], str]:

    if isinstance(text, str):
        text = [text]

    inputs = bart_tokenizer.batch_encode_plus(
        text, max_length=1024, return_tensors="pt"
    )
    summary_ids = bart_model.generate(
        inputs["input_ids"].to(device),
        num_beams=num_beams,
        max_length=max_length,
        min_length=min_length,
        early_stopping=True,
    )
    if isinstance(text, str):
        summary_ids = summary_ids[0]

    return bart_tokenizer.batch_decode(
        summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=True
    )
