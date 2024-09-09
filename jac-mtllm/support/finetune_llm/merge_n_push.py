"""Merge the LoRA with the Base Model and push to the Hugging Face Hub."""

import argparse
import os

from peft import PeftModel

import torch

from transformers import AutoModelForCausalLM, AutoTokenizer

from utils import load_config


def merge_n_push(config: argparse.Namespace, checkpoint: str) -> None:
    """Merge the LoRA with the Base Model and push to the Hugging Face Hub."""
    # Merging the LoRA with the base model
    model = AutoModelForCausalLM.from_pretrained(
        config.model["hf_model"],
        torch_dtype=torch.float16,
        load_in_8bit=False,
        device_map="auto",
        trust_remote_code=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(config.model["hf_model"])
    peft_model = PeftModel.from_pretrained(
        model,
        os.path.join(config.model["output_model"], f"checkpoint-{checkpoint}"),
        from_transformers=True,
        device_map="auto",
    )
    model = peft_model.merge_and_unload()
    model.save_pretrained(os.path.join(config.model["output_model"], "merged"))
    tokenizer.save_pretrained(os.path.join(config.model["output_model"], "merged"))

    # Pushing the model to the Hugging Face Hub
    model.push_to_hub(
        f"{config.push_to_hf['hf_username']}/{config.model['output_model']}"
    )
    tokenizer.push_to_hub(
        f"{config.push_to_hf['hf_username']}/{config.model['output_model']}"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to the configuration file",
    )
    parser.add_argument(
        "--checkpoint",
        type=int,
        default=0,
        help="Checkpoint to merge with the base model",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    merge_n_push(config, args.checkpoint)
