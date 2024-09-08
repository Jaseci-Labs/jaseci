from typing import Tuple, Callable, List, Set, Iterable, Dict
import json
from transformers import BatchEncoding
from ..datamodel.example import TypedSpan, Example
from ..datamodel.dataset import NERDataset


def prepare_descriptions() -> Dict[str, str]:
    with open("/home/ubuntu/binder/data/genia/descriptions.json") as f:
        return json.load(f)


def read_annotation(annotations) -> Set[TypedSpan]:
    collected_annotations: Set[TypedSpan] = set()
    for line in annotations:
        collected_annotations.add(
            TypedSpan(
                int(line["start_index"]), int(line["end_index"]), line["entity_type"]
            )
        )
    return collected_annotations


def read_data(dataset: Dict) -> Tuple[List[str], List[Set[TypedSpan]]]:
    list1, list2 = [], []
    for text, entity in zip(dataset["text"], dataset["annotations"]):
        list1.append(text)
        list2.append(read_annotation(entity))
    return list1, list2


def get_datasets(
    dataset: Dict,
    example_encoder: Callable[[List[str], List[Set[TypedSpan]]], Iterable[Example]],
) -> Tuple[NERDataset]:
    return NERDataset(example_encoder(*read_data(dataset)))


def tokenize_descriptions(
    descriptions: List[str], tokenizer, max_length
) -> BatchEncoding:
    return tokenizer(
        descriptions,
        return_tensors="pt",
        truncation=True,
        max_length=max_length,
        add_special_tokens=True,
        padding=True,
    )
