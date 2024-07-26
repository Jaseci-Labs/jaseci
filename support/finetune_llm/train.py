"""Training script for the MTLLM Model finetuning task."""

import argparse

from peft import LoraConfig

from transformers import TrainingArguments

from trl import SFTTrainer

from utils import load_config
from utils.dataset import prepare_train_data
from utils.merge_n_push import merge_n_push
from utils.model import get_model_tokenizer


def train(config: argparse.Namespace) -> None:
    """Train the model on the given dataset."""
    train_data = prepare_train_data(config.model["hf_dataset"])
    model, tokenizer = get_model_tokenizer(config.model["hf_model"])
    peft_config = LoraConfig(**config.lora_config)
    training_args = TrainingArguments(**config.training_args)
    trainer = SFTTrainer(
        model=model,
        train_dataset=train_data,
        peft_config=peft_config,
        args=training_args,
        tokenizer=tokenizer,
        packing=False,
        **config.trainer
    )
    trainer.train()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to the configuration file",
    )
    parser.add_argument(
        "--push_to_hf",
        type=bool,
        default=False,
        help="Push the model to the Hugging Face model hub",
    )
    args = parser.parse_args()
    config = load_config(args.config)
    train(config)

    if args.push_to_hf:
        checkpoint = input("Enter the checkpoint to push to the Hugging Face Hub: ")
        merge_n_push(config, checkpoint)
