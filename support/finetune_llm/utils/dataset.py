"""Utility functions for dataset processing."""

from datasets import Dataset, load_dataset


def formatted_train(input: str, response: str) -> str:
    """Format the input and response into the chat prompt format."""
    return f"<|user|>\n{input}</s>\n<|assistant|>\n{response}</s>"


def prepare_train_data(dataset: str) -> Dataset:
    """Prepare the training data for the MTLLM model."""
    dataset = load_dataset(dataset)
    dataset_df = dataset.to_pandas()
    dataset_df["text"] = dataset_df[["meaning_in", "meaning_out"]].apply(
        lambda x: formatted_train(x["meaning_in"], x["meaning_out"]), axis=1
    )
    dataset = Dataset.from_pandas(dataset_df)
    return dataset
