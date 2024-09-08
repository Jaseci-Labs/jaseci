import re
import json

from .config import train_file_path, clf_json_file_path


def intent_to_label(intent):
    intent = intent.replace("_", "-")
    intent = intent.replace(" ", "-")
    return f"__label__{intent}"


def label_to_intent(label):
    label = label.replace("__label__", "")
    return label.replace("-", " ")


def prep_label(intent):
    return intent_to_label(intent)


def prep_sentence(sentence):
    processed = sentence.lower()
    processed = re.sub(r"-", " ", processed)
    processed = re.sub(r"[^a-zA-Z0-9 ]", "", processed)
    # processed = re.sub(r'[0-9]', '[D]', processed)
    return processed


def json_to_train():
    result = []
    with open(clf_json_file_path, "r", encoding="utf-8") as clf_file:
        clf_data = json.load(clf_file)
    for intent, data in clf_data.items():
        label = prep_label(intent)
        for sentence in data:
            sentence = prep_sentence(sentence)
            result.append(f"{label} {sentence}")
    with open(train_file_path, "w", encoding="utf-8") as of:
        of.write("\n".join(result))

    print(f"Wrote {len(result)} sentences to {train_file_path}")


if __name__ == "__main__":
    json_to_train()
