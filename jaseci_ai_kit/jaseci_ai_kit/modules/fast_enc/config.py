import os
from pathlib import Path


def make_path(file):
    return os.path.join(os.path.dirname(__file__), file)


model_dir = Path("pretrained_model")
model_dir.mkdir(exist_ok=True, parents=True)
model_path = model_dir / "model.ftz"
model_file_path = make_path(model_path)
train_path = model_dir / "train.txt"
train_file_path = make_path(train_path)
test_file_path = make_path("test_sentences.txt")
json_file_path = model_dir / "training_data.json"
clf_json_file_path = make_path(json_file_path)
base_file_path = model_dir / "base_model.json"
base_json_file_path = make_path(base_file_path)
