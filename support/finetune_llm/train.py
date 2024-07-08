"""Training script for the MTLLM Model finetuning task."""

import argparse

from huggingface_hub import login

from peft import LoraConfig

from transformers import TrainingArguments

from trl import SFTTrainer

import utils.constants as cons
from utils.dataset import prepare_train_data
from utils.model import get_model_tokenizer


def train(args: argparse.Namespace) -> None:
    """Train the model on the given dataset."""
    train_data = prepare_train_data(args.dataset)
    model, tokenizer = get_model_tokenizer(args.model_id)
    peft_config = LoraConfig(
        r=8, lora_alpha=16, lora_dropout=0.05, bias="none", task_type="CAUSAL_LM"
    )
    training_args = TrainingArguments(
        output_dir=args.output_model_name,
        per_device_train_batch_size=16,
        gradient_accumulation_steps=4,
        optim="paged_adamw_32bit",
        learning_rate=args.lr,
        lr_scheduler_type="cosine",
        save_strategy="epoch",
        logging_steps=10,
        num_train_epochs=args.max_num_epochs,
        max_steps=250,
        fp16=True,
    )
    trainer = SFTTrainer(
        model=model,
        train_dataset=train_data,
        peft_config=peft_config,
        dataset_text_field="text",
        args=training_args,
        tokenizer=tokenizer,
        packing=False,
        max_seq_length=1024,
    )
    trainer.train()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset", type=str, default=cons.HF_DATASET, help="Dataset ID to train on"
    )
    parser.add_argument(
        "--model_id", type=str, default=cons.HF_MODEL, help="Model ID to train"
    )
    parser.add_argument(
        "--output_model_name",
        type=str,
        default=cons.OUTPUT_MODEL,
        help="Output model name",
    )
    parser.add_argument(
        "--hf_token", type=str, required=True, help="Hugging Face API token"
    )

    parser.add_argument(
        "--max_num_epochs",
        type=int,
        default=cons.MAX_NUM_EPOCHS,
        help="Maximum number of epochs to train for",
    )
    parser.add_argument(
        "--lr", type=float, default=cons.LR, help="Learning rate for the model"
    )

    args = parser.parse_args()

    login(args.hf_token)

    train(args)
