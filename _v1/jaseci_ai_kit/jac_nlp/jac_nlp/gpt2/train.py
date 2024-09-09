import tempfile
from sklearn.model_selection import train_test_split
from transformers import (
    TextDataset,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)
from typing import List, Union


def prepare_data(text: Union[List[str], str], split: float = 0.2):
    if isinstance(text, str):
        text = text.strip().split()
        train, test = train_test_split(text, test_size=split, shuffle=False)
        train, test = " ".join(train), " ".join(test)
    elif isinstance(text, list):
        train, test = train_test_split(text, test_size=split)
        train, test = " ".join(train), " ".join(test)
    else:
        raise Exception("Text must be a string or list of strings")

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(train)
        train_path = f.name
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write(test)
        test_path = f.name
    return train_path, test_path


def load_dataset(train_path, test_path, tokenizer):
    train_dataset = TextDataset(
        tokenizer=tokenizer, file_path=train_path, block_size=128
    )

    test_dataset = TextDataset(tokenizer=tokenizer, file_path=test_path, block_size=128)

    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,
    )
    return train_dataset, test_dataset, data_collator


def get_trainer(model, train_dataset, test_dataset, data_collator, epochs=1):
    training_args = TrainingArguments(
        output_dir="./gpt2-trained",  # The output directory
        overwrite_output_dir=True,  # overwrite the content of the output directory
        num_train_epochs=epochs,  # number of training epochs
        per_device_train_batch_size=32,  # batch size for training
        per_device_eval_batch_size=64,  # batch size for evaluation
        eval_steps=400,  # Number of update steps between two evaluations.
        save_steps=800,  # after # steps model is saved
        warmup_steps=500,  # number of warmup steps for learning rate scheduler
        prediction_loss_only=True,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
    )

    return trainer
