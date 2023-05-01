import os

# from pathlib import Path

# import fast_enc


def make_path(file):
    return os.path.join(os.path.dirname(__file__), file)


model_dir = make_path("pretrained")
if not os.path.isdir(model_dir):
    model_dir = make_path("pretrained")
    os.mkdir(model_dir)
model_path = make_path(model_dir + "/model.ftz")
model_file_path = make_path(model_path)
train_file_path = make_path(model_dir + "/train.txt")
test_file_path = make_path("test_sentences.txt")
clf_json_file_path = make_path(model_dir + "/training_data.json")
base_json_file_path = make_path(model_dir + "/base_model.json")
