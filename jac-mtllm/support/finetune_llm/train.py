"""Training script for the MTLLM Model finetuning task."""

import argparse
import os

from merge_n_push import merge_n_push

from peft import LoraConfig

from transformers import TrainingArguments

from trl import SFTTrainer

from utils import load_config
from utils.dataset import prepare_train_data
from utils.model import get_model_tokenizer

import wandb

seed = 42


def train(config: argparse.Namespace) -> None:
    """Train the model on the given dataset."""
    wandb.init(project=config.model["output_model"])  # type: ignore
    os.environ["WANDB_PROJECT"] = config.model["output_model"]
    os.environ["WANDB_LOG_MODEL"] = "checkpoint"

    train_data = prepare_train_data(config.model["hf_dataset"])
    train_eval_data = train_data.train_test_split(test_size=0.2, seed=seed)
    train_data = train_eval_data["train"]
    eval_data = train_eval_data["test"]

    model, tokenizer = get_model_tokenizer(config.model["hf_model"])

    peft_config = LoraConfig(**config.lora_config)
    training_args = TrainingArguments(
        output_dir=config.model["output_model"],
        report_to="wandb",
        **config.training_args
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=train_data,
        eval_dataset=eval_data,
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
        action="store_true",
        help="Push the trained model to the Hugging Face Hub",
    )
    args = parser.parse_args()
    config = load_config(args.config)
    train(config)

    if args.push_to_hf:
        checkpoint = input("Enter the checkpoint to push to the Hugging Face Hub: ")
        merge_n_push(config, checkpoint)
