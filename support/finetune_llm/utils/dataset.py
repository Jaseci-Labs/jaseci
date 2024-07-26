"""Utility functions for dataset processing."""

from datasets import Dataset, load_dataset


def formatted_train(input: str, response: str) -> str:
    """Format the input and response into the chat prompt format."""
    return f"{input}{response}"


def prepare_train_data(dataset: str) -> Dataset:
    """Prepare the training data for the MTLLM model."""
    _dataset = load_dataset(dataset)
    dataset_df = _dataset.to_pandas()
    dataset_df["text"] = dataset_df[["input_prompt", "output_prompt"]].apply(
        lambda x: formatted_train(x["input_prompt"], x["output_prompt"]), axis=1
    )
    _dataset_ = Dataset.from_pandas(dataset_df)
    return _dataset_
