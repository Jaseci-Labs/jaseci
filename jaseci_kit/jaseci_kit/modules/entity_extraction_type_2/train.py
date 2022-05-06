from sklearn.metrics import accuracy_score
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from utils.data_tokens import load_data
from torch import cuda
import os


device = "cuda" if cuda.is_available() else "cpu"
print("Using device for training -> ", device)


# # preparing dataset for training
# ### TOKENIZE DATASET


def tokenize_and_preserve_labels(sentence, text_labels, tokenizer):
    """
    Word piece tokenization makes it difficult to match word labels
    back up with individual word pieces. This function tokenizes each
    word one at a time so that it is easier to preserve the correct
    label for each subword. It is, of course, a bit slower in processing
    time, but it will help our model achieve higher accuracy.
    """

    tokenized_sentence = []
    labels = []
    sentence = sentence.strip()
    for word, label in zip(sentence.split(), text_labels.split(",")):

        # Tokenize the word and count # of subwords the word is broken into
        tokenized_word = tokenizer.tokenize(word)
        n_subwords = len(tokenized_word)

        # Add the tokenized word to the final tokenized word list
        tokenized_sentence.extend(tokenized_word)

        # Add the same label to the new list of labels `n_subwords` times
        labels.extend([label] * n_subwords)

    return tokenized_sentence, labels


# ## CREATE DATASET
class dataset(Dataset):
    def __init__(self, dataframe, tokenizer, max_len):
        self.len = len(dataframe)
        self.data = dataframe
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __getitem__(self, index):
        # step 1: tokenize (and adapt corresponding labels)
        sentence = self.data.sentence[index]
        word_labels = self.data.word_labels[index]
        tokenized_sentence, labels = tokenize_and_preserve_labels(
            sentence, word_labels, self.tokenizer
        )

        # step 2: add special tokens (and corresponding labels)
        tokenized_sentence = ["[CLS]"] + tokenized_sentence + ["[SEP]"]
        # add special tokens
        labels.insert(0, "O")
        # add outside label for [CLS] token
        labels.insert(-1, "O")
        # add outside label for [SEP] token

        # step 3: truncating/padding
        maxlen = self.max_len

        if len(tokenized_sentence) > maxlen:
            # truncate
            tokenized_sentence = tokenized_sentence[:maxlen]
            labels = labels[:maxlen]
        else:
            # pad
            tokenized_sentence = tokenized_sentence + [
                "[PAD]" for _ in range(maxlen - len(tokenized_sentence))
            ]
            labels = labels + ["O" for _ in range(maxlen - len(labels))]

        # step 4: obtain the attention mask
        attn_mask = [1 if tok != "[PAD]" else 0 for tok in tokenized_sentence]

        # step 5: convert tokens to input ids
        ids = self.tokenizer.convert_tokens_to_ids(tokenized_sentence)

        label_ids = [label2id[label] for label in labels]
        # the following line is deprecated
        # label_ids = [label if label != 0 else -100 for label in label_ids]

        return {
            "ids": torch.tensor(ids, dtype=torch.long),
            "mask": torch.tensor(attn_mask, dtype=torch.long),
            "targets": torch.tensor(label_ids, dtype=torch.long),
        }

    def __len__(self):
        return self.len


# LOADING TRAINING DATASET
def data_set(filename, max_len, train_batch_size):
    global id2label, label2id, training_loader
    ds = load_data(filename)
    data = ds[0]
    id2label = ds[1]
    label2id = ds[2]
    lab = list(id2label.values())

    train_dataset = data

    training_set = dataset(train_dataset, tokenizer, max_len)

    train_params = {"batch_size": train_batch_size, "shuffle": True, "num_workers": 0}
    training_loader = DataLoader(training_set, **train_params)
    return lab


def check_labels_ok():
    lst_data_labels = list(id2label.values())
    lst_model_labels = list(model.config.id2label.values())
    for label in lst_data_labels:
        if label not in lst_model_labels:
            return False
    return True


# DEFINING MODEL training
def train_model(
    model_name, epochs, mode, lab_check, learning_rate, max_grad_norm, model_save_path
):
    global model, tokenizer

    def create_model():
        # ## saving current model
        save_custom_model(model_save_path)
        model = AutoModelForTokenClassification.from_pretrained(
            model_name,
            ignore_mismatched_sizes=True,
            num_labels=len(label2id),
            id2label=id2label,
            label2id=label2id,
        )
        return model

    if mode == 3 and lab_check is False:
        resp1 = "data label and model labels is not matching"
        resp2 = " please use default mode for training from scretch"
        return resp1 + resp2

    elif mode == 2:
        print("***" * 10, "Model is loading from scratch in append mode")
        model = create_model()

    elif mode == 1:
        print("***" * 10, "Model is loading from scratch in default mode")
        model = create_model()

    else:
        print("***" * 10, "same model is retraining in incremental mode")

    model.to(device)
    optimizer = torch.optim.Adam(params=model.parameters(), lr=learning_rate)

    # Defining the training function on the 80% of the dataset
    # for tuning the bert model
    def train(epoch):
        tr_loss, tr_accuracy = 0, 0
        nb_tr_examples, nb_tr_steps = 0, 0
        tr_preds, tr_labels = [], []
        # put model in training mode
        model.train()

        for idx, batch in enumerate(training_loader):
            ids = batch["ids"].to(device, dtype=torch.long)
            mask = batch["mask"].to(device, dtype=torch.long)
            targets = batch["targets"].to(device, dtype=torch.long)

            outputs = model(input_ids=ids, attention_mask=mask, labels=targets)
            loss, tr_logits = outputs.loss, outputs.logits
            tr_loss += loss.item()

            nb_tr_steps += 1
            nb_tr_examples += targets.size(0)

            if idx % 100 == 0:
                loss_step = tr_loss / nb_tr_steps
                print(f"Training loss per 100 training steps: {loss_step}")

            # compute training accuracy
            flattened_targets = targets.view(-1)
            # shape (batch_size * seq_len,)
            active_logits = tr_logits.view(-1, model.num_labels)
            # shape (batch_size * seq_len, num_labels)
            flattened_predictions = torch.argmax(active_logits, axis=1)
            # shape (batch_size * seq_len,)
            # now, use mask to determine where we should compare predictions
            # with targets (includes [CLS] and [SEP] token predictions)
            active_accuracy = mask.view(-1) == 1
            # active accuracyis also of shape (batch_size * seq_len,)
            targets = torch.masked_select(flattened_targets, active_accuracy)
            predictions = torch.masked_select(flattened_predictions, active_accuracy)

            tr_preds.extend(predictions)
            tr_labels.extend(targets)

            tmp_tr_accuracy = accuracy_score(
                targets.cpu().numpy(), predictions.cpu().numpy()
            )
            tr_accuracy += tmp_tr_accuracy

            # gradient clipping
            torch.nn.utils.clip_grad_norm_(
                parameters=model.parameters(), max_norm=max_grad_norm
            )

            # backward pass
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        epoch_loss = tr_loss / nb_tr_steps
        tr_accuracy = tr_accuracy / nb_tr_steps
        print(f"Training loss epoch: {epoch_loss}")
        print(f"Training accuracy epoch: {tr_accuracy}")

    for epoch in range(epochs):
        print(f"Training epoch: {epoch + 1}")
        train(epoch)
    # Clearing cuda memory
    os.remove("train/train.txt")
    torch.cuda.empty_cache()
    return "model training is completed."


def load_custom_model(model_path):
    global model, tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForTokenClassification.from_pretrained(model_path)
    model.to(device)


def save_custom_model(model_path):
    # saving model
    model.save_pretrained(model_path)
    tokenizer.save_pretrained(model_path)
    print(f"model saved successful to : {model_path}")


# predicting entities
def predict_text(sentence):
    pipe = pipeline(
        "ner", model=model.to("cpu"), tokenizer=tokenizer, aggregation_strategy="first"
    )
    entities = pipe(sentence)
    ents = []
    for i in range(len(entities)):
        e_data = {
            "text": entities[i]["word"],
            "entity": entities[i]["entity_group"],
            "score": float(entities[i]["score"]),
            "start": entities[i]["start"],
            "end": entities[i]["end"],
        }
        ents.append(e_data)
    torch.cuda.empty_cache()
    return ents
