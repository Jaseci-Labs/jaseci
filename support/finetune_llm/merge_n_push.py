"""Merge the LoRA with the Base Model and push to the Hugging Face Hub."""

import argparse
import os

from huggingface_hub import login

from peft import PeftModel

import torch

from transformers import AutoModelForCausalLM, AutoTokenizer

import utils.constants as cons


def merge_n_push(args: argparse.Namespace) -> None:
    """Merge the LoRA with the Base Model and push to the Hugging Face Hub."""
    # Merging the LoRA with the base model
    model = AutoModelForCausalLM.from_pretrained(
        args.base_model_id,
        torch_dtype=torch.float16,
        load_in_8bit=False,
        device_map="auto",
        trust_remote_code=True,
    )
    tokenizer = AutoTokenizer.from_pretrained(args.base_model_id)
    peft_model = PeftModel.from_pretrained(
        model, args.checkpoint_dir, from_transformers=True, device_map="auto"
    )
    model = peft_model.merge_and_unload()
    model.save_pretrained(os.path.join(args.output_model_name, "merged"))
    tokenizer.save_pretrained(os.path.join(args.output_model_name, "merged"))

    # Pushing the model to the Hugging Face Hub
    model.push_to_hub(
        f"{args.hf_username}/{args.output_model_name}", token=args.hf_token
    )
    tokenizer.push_to_hub(
        f"{args.hf_username}/{args.output_model_name}", token=args.hf_token
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--base_model_id", type=str, default=cons.HF_MODEL, help="Base model ID"
    )
    parser.add_argument(
        "--output_model_name",
        type=str,
        default=cons.OUTPUT_MODEL,
        help="Output model name",
    )
    parser.add_argument(
        "--checkpoint_dir", type=str, required=True, help="Model Checkpoint directory"
    )
    parser.add_argument(
        "--hf_username", type=str, required=True, help="Hugging Face username"
    )
    parser.add_argument(
        "--hf_token", type=str, required=True, help="Hugging Face API token"
    )

    args = parser.parse_args()

    login(args.hf_token)
    merge_n_push(args)
