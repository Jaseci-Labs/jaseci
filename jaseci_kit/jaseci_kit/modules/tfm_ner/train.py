from transformers import (
    AutoTokenizer,
    DataCollatorForTokenClassification,
    AutoModelForTokenClassification,
    TrainingArguments,
    Trainer,
)
from transformers import pipeline
from torch import cuda
from datetime import datetime
import numpy as np
import evaluate
import re

device = "cuda" if cuda.is_available() else "cpu"
print("Using device for training -> ", device)


# Logging
def logs(*args):
    with open("train/logs/" + args[-1], "a") as f:
        data = ""
        for arg in args[:-1]:
            data += str(arg)
        print(data)
        f.write(data)
        f.write("\n")


metric = evaluate.load("seqeval")
model = None


def compute_metrics(eval_preds):
    logits, labels = eval_preds
    predictions = np.argmax(logits, axis=-1)

    # Remove ignored index (special tokens) and convert to labels
    true_labels = [
        [val_dm.unique_entities[lbl] for lbl in label if lbl != -100]
        for label in labels
    ]
    true_predictions = [
        [
            val_dm.unique_entities[p]
            for (p, lbl) in zip(prediction, label)
            if lbl != -100
        ]
        for prediction, label in zip(predictions, labels)
    ]
    all_metrics = metric.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": all_metrics["overall_precision"],
        "recall": all_metrics["overall_recall"],
        "f1": all_metrics["overall_f1"],
        "accuracy": all_metrics["overall_accuracy"],
    }


def get_tokens_with_entities(raw_text: str):
    # split the text by spaces only if the space does not occur between square brackets
    # we do not want to split "multi-word" entity value yet
    raw_tokens = re.split(r"\s(?![^\[]*\])", raw_text)

    # a regex for matching the annotation  [entity_value](entity_name)
    entity_value_pattern = r"\[(?P<value>.+?)\]\((?P<entity>.+?)\)"
    entity_value_pattern_compiled = re.compile(entity_value_pattern, flags=re.I | re.M)

    tokens_with_entities = []

    for raw_token in raw_tokens:
        match = entity_value_pattern_compiled.match(raw_token)
        if match:
            raw_entity_name, raw_entity_value = match.group("entity"), match.group(
                "value"
            )

            for i, raw_entity_token in enumerate(re.split("\s", raw_entity_value)):
                entity_prefix = "B" if i == 0 else "I"
                entity_name = f"{entity_prefix}-{raw_entity_name}"
                tokens_with_entities.append((raw_entity_token, entity_name))
        else:
            tokens_with_entities.append((raw_token, "O"))

    return tokens_with_entities


class NERDataMaker:
    def __init__(self, texts):
        self.unique_entities = []
        self.processed_texts = []

        temp_processed_texts = []
        for text in texts:
            tokens_with_entities = get_tokens_with_entities(text)
            for _, ent in tokens_with_entities:
                if ent not in self.unique_entities:
                    self.unique_entities.append(ent)
            temp_processed_texts.append(tokens_with_entities)

        self.unique_entities.sort(key=lambda ent: ent if ent != "O" else "")

        for tokens_with_entities in temp_processed_texts:
            self.processed_texts.append(
                [
                    (t, self.unique_entities.index(ent))
                    for t, ent in tokens_with_entities
                ]
            )

    @property
    def id2label(self):
        return dict(enumerate(self.unique_entities))

    @property
    def label2id(self):
        return {v: k for k, v in self.id2label.items()}

    def __len__(self):
        return len(self.processed_texts)

    def __getitem__(self, idx):
        def _process_tokens_for_one_text(id, tokens_with_encoded_entities):
            ner_tags = []
            tokens = []
            for t, ent in tokens_with_encoded_entities:
                ner_tags.append(ent)
                tokens.append(t)

            return {"id": id, "ner_tags": ner_tags, "tokens": tokens}

        tokens_with_encoded_entities = self.processed_texts[idx]
        if isinstance(idx, int):
            return _process_tokens_for_one_text(idx, tokens_with_encoded_entities)
        else:
            return [
                _process_tokens_for_one_text(i + idx.start, tee)
                for i, tee in enumerate(tokens_with_encoded_entities)
            ]

    def as_hf_dataset(self, tokenizer):
        from datasets import Dataset, Features, Value, ClassLabel, Sequence

        def tokenize_and_align_labels(examples):
            tokenized_inputs = tokenizer(
                examples["tokens"], truncation=True, is_split_into_words=True
            )

            labels = []
            for i, label in enumerate(examples["ner_tags"]):
                word_ids = tokenized_inputs.word_ids(
                    batch_index=i
                )  # Map tokens to their respective word.
                previous_word_idx = None
                label_ids = []
                for word_idx in word_ids:  # Set the special tokens to -100.
                    if word_idx is None:
                        label_ids.append(-100)
                    elif (
                        word_idx != previous_word_idx
                    ):  # Only label the first token of a given word.
                        label_ids.append(label[word_idx])
                    else:
                        label_ids.append(-100)
                    previous_word_idx = word_idx
                labels.append(label_ids)

            tokenized_inputs["labels"] = labels
            return tokenized_inputs

        ids, ner_tags, tokens = [], [], []
        for i, pt in enumerate(self.processed_texts):
            ids.append(i)
            pt_tokens, pt_tags = list(zip(*pt))
            ner_tags.append(pt_tags)
            tokens.append(pt_tokens)
        data = {"id": ids, "ner_tags": ner_tags, "tokens": tokens}
        features = Features(
            {
                "tokens": Sequence(Value("string")),
                "ner_tags": Sequence(ClassLabel(names=self.unique_entities)),
                "id": Value("int32"),
            }
        )
        ds = Dataset.from_dict(data, features)
        tokenized_ds = ds.map(tokenize_and_align_labels, batched=True)
        return tokenized_ds


def load_custom_model(model_path, train_dm=None):
    global model, tokenizer, data_collator
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForTokenClassification.from_pretrained(
        model_path,
        num_labels=len(train_dm.unique_entities),
        id2label=train_dm.id2label,
        label2id=train_dm.label2id,
    )
    model.to(device)
    data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)


def train_model(train_data, val_data, train_config):
    global val_dm
    if len(train_data) != 0:
        train_dm = NERDataMaker(train_data)
        train_ds = train_dm.as_hf_dataset(tokenizer=tokenizer)
        print(f"total Train examples = {len(train_data)}")
    if len(val_data) != 0:
        val_dm = NERDataMaker(val_data)
        val_ds = val_dm.as_hf_dataset(tokenizer=tokenizer)
        print(f"total validation examples = {len(val_dm)}")
    else:
        val_dm = train_dm
        val_ds = train_ds
    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        learning_rate=train_config["LEARNING_RATE"],
        per_device_train_batch_size=train_config["TRAIN_BATCH_SIZE"],
        per_device_eval_batch_size=train_config["VALID_BATCH_SIZE"],
        num_train_epochs=train_config["EPOCHS"],
        weight_decay=0.01,
    )
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
        callbacks=None,
    )

    trainer.train()


def save_custom_model(model_path):
    # saving model
    model.save_pretrained(model_path)
    tokenizer.save_pretrained(model_path)
    print(str(datetime.now()) + "   ", f"model saved successful to : {model_path}")


# predicting entities
def predict_text(sentence):
    if model is not None:
        pipe = pipeline(
            "ner",
            model=model.to("cpu"),
            tokenizer=tokenizer,
            aggregation_strategy="first",
        )
        entities = pipe(sentence)
        ents = []
        for itm in entities:
            ents.append(
                {
                    "entity_text": itm["word"],
                    "entity_value": itm["entity_group"],
                    "conf_score": float(itm["score"]),
                    "start_pos": itm["start"],
                    "end_pos": itm["end"],
                }
            )
        return ents
    return "Model not trained"
