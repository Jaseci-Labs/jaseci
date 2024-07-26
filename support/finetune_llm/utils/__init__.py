"""Utility functions for finetuning LLMs."""

from argparse import Namespace

import yaml


def load_config(yaml_file: str) -> Namespace:
    """Load the configuration file."""
    with open(yaml_file, "r") as file:
        config = yaml.safe_load(file)
    return Namespace(**config)
