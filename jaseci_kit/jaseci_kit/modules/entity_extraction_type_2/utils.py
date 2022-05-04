import torch

# import numpy as np
# from datasets import load_metric
# transformers library
# from datasets import load_dataset
from transformers import Trainer
from transformers import AutoModelForTokenClassification
from transformers import AutoTokenizer
from transformers import DataCollatorForTokenClassification


def set_device():
    """
    Set the device. CUDA if available, CPU otherwise
    Args:
      None
    Returns:
      Nothing
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device != "cuda":
        print(
            "WARNING: For this notebook to perform best, "
            "if possible, in the menu under `Runtime` -> "
            "`Change runtime type.`  select `GPU` "
        )
    else:
        print("GPU is enabled!")
    return device


device = set_device()


def align_labels_with_tokens(labels, word_ids):
    new_labels = []
    current_word = None
    for word_id in word_ids:
        if word_id != current_word:
            # Start of a new word!
            current_word = word_id
            label = -100 if word_id is None else labels[word_id]
            new_labels.append(label)
        elif word_id is None:
            # Special token
            new_labels.append(-100)
        else:
            # Same word as previous token
            label = labels[word_id]
            # If the label is B-XXX we change it to I-XXX
            if label % 2 == 1:
                label += 1
            new_labels.append(label)
    return new_labels


# tokenize_and_align_labels #######


def tokenize_and_align_labels(examples):
    """
    Tokenises incoming sequences;
    Args:
        examples: Sequence of strings
        Sequences to tokenise
    Returns:
        Returns transformer autotokenizer object with padded,
        truncated input sequences.
    """
    tokenized_inputs = tokenizer(
        examples["tokens"], truncation=True, is_split_into_words=True
    )
    all_labels = examples["ner_tags"]
    new_labels = []
    for i, labels in enumerate(all_labels):
        word_ids = tokenized_inputs.word_ids(i)
        new_labels.append(align_labels_with_tokens(labels, word_ids))
    tokenized_inputs["labels"] = new_labels
    return tokenized_inputs


#     return tokenizer
def labelname(labels_name):
    # global id2label, label2id
    lab = list(model.config.id2label.values())
    labels_name = lab + list(set(labels_name) - set(lab))
    id2label = {str(i): label for i, label in enumerate(labels_name)}
    label2id = {v: k for k, v in id2label.items()}
    return id2label, label2id


def load_trained_model(model_path):
    global tokenizer, model
    print(f"loading model from ** {model_path} ** started..")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    print("Tokenizer loaded successfull!")
    model = AutoModelForTokenClassification.from_pretrained(model_path)
    print(f"loading model from ** {model_path} ** completed!")
    return tokenizer, model

    # print(f'loading model from ** {model_path} ** started..')
    # tokenizer = AutoTokenizer.from_pretrained(model_path)
    # print("Tokenizer loaded successfull!")
    # model = AutoModelForTokenClassification.from_pretrained(
    #     model_path,
    #     id2label=id2label,
    #     label2id=label2id
    # )
    # print(f'loading model from ** {model_path} ** completed!')
    # return tokenizer, model


def save_trained_model(model, tokenizer, model_path):
    model.save_pretrained(model_path)
    tokenizer.save_pretrained(model_path)
    # model.save_model(model_path)


def train_model(tokenized_datasets, args, curr_model_path, id2label, label2id, path):
    """
    initialised model training and start training model
    """
    tokenizer = AutoTokenizer.from_pretrained(curr_model_path)
    model = AutoModelForTokenClassification.from_pretrained(
        curr_model_path,
        id2label=id2label,
        label2id=label2id,
        ignore_mismatched_sizes=True,
    )

    # Setup huggingface trainer
    data_collator = DataCollatorForTokenClassification(tokenizer=tokenizer)
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=tokenized_datasets,
        eval_dataset=tokenized_datasets.shuffle().select(range(1)),
        data_collator=data_collator,
        # compute_metrics=compute_metrics,
        tokenizer=tokenizer,
    )
    print("************ model training is started ****************** ")
    trainer.train()
    trainer.save_model(path)
    torch.cuda.empty_cache()
    print("************ model training is completed! ****************** ")
    return trainer
