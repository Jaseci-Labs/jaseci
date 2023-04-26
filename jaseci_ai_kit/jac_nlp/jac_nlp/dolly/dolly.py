from jaseci.jsorc.live_actions import jaseci_action
import torch
from .instruct_pipeline import InstructionTextGenerationPipeline
from transformers import AutoModelForCausalLM, AutoTokenizer


def setup(model: str = "dolly-v2-3b"):
    global pipeline
    tokenizer = AutoTokenizer.from_pretrained(
        "databricks/dolly-v2-3b", padding_side="left"
    )
    model = AutoModelForCausalLM.from_pretrained(
        "databricks/dolly-v2-3b", device_map="auto", torch_dtype=torch.bfloat16
    )
    pipeline = InstructionTextGenerationPipeline(model=model, tokenizer=tokenizer)


@jaseci_action(act_group=["dolly"], allow_remote=True)
def generate(prompt: str):
    global pipeline
    return pipeline(prompt)[0]["generated_text"]
