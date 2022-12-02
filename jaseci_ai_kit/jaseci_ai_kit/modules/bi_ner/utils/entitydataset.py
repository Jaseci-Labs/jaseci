from torch.utils.data import Dataset
import re
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"


def get_id_to_label(batch, scores, tokenizer):
    text_list = []
    entity_list = []
    entity_set = []
    for text_token in batch["text_inputs"]["input_ids"]:
        text = tokenizer.decode(
            text_token, skip_special_tokens=True, clean_up_tokenization_spaces=True
        )
        text_list.append(text)
    for entity_token in batch["entity_inputs"]["input_ids"]:
        entity = tokenizer.decode(
            entity_token, skip_special_tokens=True, clean_up_tokenization_spaces=True
        )
        entity_list.append(entity)
    full_text = " ".join(text_list)
    for text_token, score in zip(batch["text_inputs"]["input_ids"], scores):
        text = tokenizer.decode(
            text_token, skip_special_tokens=True, clean_up_tokenization_spaces=True
        )
        if entity_list[torch.argmax(score).detach().cpu().item()] != "o":
            entity_set.append(
                {
                    "start_index": full_text.index(text),
                    "end_index": full_text.index(text) + len(text),
                    "entity_value": text,
                    "entity_name": entity_list[
                        torch.argmax(score).detach().cpu().item()
                    ],
                }
            )
    return entity_set


def get_train_token(raw_text):
    raw_tokens = re.split(r"\s(?![^\[]*\])", raw_text)

    # a regex for matching the annotation  [entity_value](entity_name)
    entity_value_pattern = r"\[(?P<value>.+?)\]\((?P<entity>.+?)\)"
    entity_value_pattern_compiled = re.compile(entity_value_pattern, flags=re.I | re.M)
    text, entity = [], []
    for raw_token in raw_tokens:
        match = entity_value_pattern_compiled.match(raw_token)
        if match:
            raw_entity_name, raw_entity_value = match.group("entity"), match.group(
                "value"
            )

            for i, raw_entity_token in enumerate(re.split("\s", raw_entity_value)):
                entity_prefix = "B" if i == 0 else "I"
                entity_name = f"{entity_prefix}-{raw_entity_name}"
                text.append(raw_entity_token)
                entity.append(entity_name)
        else:
            text.append(raw_token)
            entity.append("O")

    return text, entity


def get_test_token(raw_text, raw_entities):
    raw_tokens = re.split(r"\s(?![^\[]*\])", raw_text)
    entity = []
    for raw_entity in raw_entities:
        entity_prefix = "B"
        entity_name = f"{entity_prefix}-{raw_entity}"
        entity.append(entity_name)
        entity_prefix = "I"
        entity_name = f"{entity_prefix}-{raw_entity}"
        entity.append(entity_name)
    entity.append("O")
    return raw_tokens, entity


def get_ner_dataset(dataset, tokenizer, split="train"):
    token_text = []
    token_entity = []
    if split == "train":
        for text in dataset["train"]:
            text, entity = get_train_token(text)
            token_text.append(text)
            token_entity.append(entity)
        return EntityDataset(token_text, token_entity, tokenizer)
    else:
        for text in dataset["test"]["text"]:
            text, entity = get_test_token(text, dataset["test"]["entity"])
            token_text.append(text)
            token_entity.append(entity)
        return EntityDataset(token_text, token_entity, tokenizer)


class EntityDataset(Dataset):
    def __init__(self, text, entity, tokenizer):
        self.tokenizer = tokenizer
        self.text = text
        self.entity = entity

    def __len__(self):
        return len(self.text)

    def __getitem__(self, idx):
        text = self.tokenizer(
            self.text[idx],
            max_length=64,
            truncation=True,
            padding="max_length",
            return_token_type_ids=False,
        )
        entity = self.tokenizer(
            self.entity[idx],
            max_length=64,
            truncation=True,
            padding="max_length",
            return_token_type_ids=False,
        )
        long_tensors = [
            text["input_ids"],
            text["attention_mask"],
            entity["input_ids"],
            entity["attention_mask"],
        ]

        (
            text["input_ids"],
            text["attention_mask"],
            entity["input_ids"],
            entity["attention_mask"],
        ) = (torch.tensor(t, dtype=torch.long, device=device) for t in long_tensors)
        return {
            "text_inputs": text,
            "entity_inputs": entity,
        }
