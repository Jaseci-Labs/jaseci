from jaseci.jsorc.live_actions import jaseci_action
import torch
from transformers import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer


@jaseci_action(act_group=["llm"], allow_remote=True)
def setup(model_name="databricks/dolly-v2-3b", tokenizer_name=None, **kwargs):
    global pipeline

    tokenizer_kwargs = kwargs.get("tokenizer_kwargs", {})
    tokenizer = AutoTokenizer.from_pretrained(
        tokenizer_name if tokenizer_name else model_name**tokenizer_kwargs
    )
    model_kwargs = kwargs.get("model_kwargs", {})
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        torch_dtype=torch.float16,
        load_in_8bit=True,
        **model_kwargs
    )

    pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)


@jaseci_action(act_group=["llm"], allow_remote=True)
def generate(text, **kwargs):
    return pipeline(text, **kwargs)
