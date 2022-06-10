from sklearn.metrics import accuracy_score, f1_score, classification_report
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from .utils.data_tokens import load_data
from torch import cuda
import os
from datetime import datetime


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
        return {
            "ids": torch.tensor(ids, dtype=torch.long),
            "mask": torch.tensor(attn_mask, dtype=torch.long),
            "targets": torch.tensor(label_ids, dtype=torch.long),
        }

    def __len__(self):
        return self.len


# LOADING TRAINING DATASET
def data_set(t_file, v_file, ts_file, max_len, train_batch_size):
    global id2label, label2id, training_loader, val_loader, target_labels, test_loader
    ds = load_data(t_file)
    train_dataset = ds[0]
    data_labels = ds[1]
    label2id = {k: v for v, k in enumerate(data_labels)}
    id2label = {v: k for v, k in enumerate(data_labels)}

    training_set = dataset(train_dataset, tokenizer, max_len)
    train_params = {"batch_size": train_batch_size, "shuffle": True, "num_workers": 0}
    training_loader = DataLoader(training_set, **train_params)

    # val dataset
    if os.path.exists(v_file):
        ds1 = load_data(v_file)
        val_dataset = ds1[0]
        data_labels1 = data_labels + [lab for lab in ds1[1] if lab not in data_labels]
        label2id = {k: v for v, k in enumerate(data_labels1)}
        id2label = {v: k for v, k in enumerate(data_labels1)}
        target_labels = ds1[0]

        val_set = dataset(val_dataset, tokenizer, max_len)
        val_params = {
            "batch_size": train_batch_size,
            "shuffle": True,
            "num_workers": 0,
        }
        val_loader = DataLoader(val_set, **val_params)
    else:
        val_loader = None
        data_labels1 = data_labels

    # test dataset
    if os.path.exists(ts_file):
        ds2 = load_data(ts_file)
        test_dataset = ds2[0]
        data_labels2 = data_labels1 + [lab for lab in ds2[1] if lab not in data_labels1]
        label2id = {k: v for v, k in enumerate(data_labels2)}
        id2label = {v: k for v, k in enumerate(data_labels2)}
        target_labels = ds2[1]

        test_set = dataset(test_dataset, tokenizer, max_len)
        test_params = {
            "batch_size": train_batch_size,
            "shuffle": True,
            "num_workers": 0,
        }
        test_loader = DataLoader(test_set, **test_params)
    else:
        test_loader = None

    return True


def check_labels_ok():
    lst_data_labels = list(id2label.values())
    lst_model_labels = list(model.config.id2label.values())
    for label in lst_data_labels:
        if label not in lst_model_labels:
            return False
    return True


def train_score(optimizer, training_loader, max_grad_norm):
    tr_loss, tr_accuracy = 0, 0
    nb_tr_examples, nb_tr_steps = 0, 0
    tr_preds, tr_labels = [], []
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
            logs(
                str(datetime.now()) + "    ",
                f"Training loss per 100 training steps: {loss_step}",
                logs_file_name,
            )

        # compute training accuracy
        flattened_targets = targets.view(-1)
        active_logits = tr_logits.view(-1, model.num_labels)
        flattened_predictions = torch.argmax(active_logits, axis=1)
        active_accuracy = mask.view(-1) == 1
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

    y_true = []
    y_pred = []
    for i in range(len(tr_labels)):
        if tr_labels[i].cpu().item() != 0:
            y_true.append(tr_labels[i].cpu().item())
            y_pred.append(tr_preds[i].cpu().item())
    tr_acc = accuracy_score(y_true, y_pred)
    logs(
        str(datetime.now()) + "    ",
        f"Training loss epoch: {epoch_loss}",
        logs_file_name,
    )
    logs(
        str(datetime.now()) + "    ",
        f"Training accuracy epoch: {tr_acc}",
        logs_file_name,
    )


# Tracking variables
def val_score(val_loader, model):
    ev_loss, ev_accuracy = 0, 0
    nb_ev_steps, nb_ev_examples = 0, 0
    ev_preds, ev_labels = [], []
    model.eval()
    for idx, batch in enumerate(val_loader):
        ids = batch["ids"].to(device, dtype=torch.long)
        mask = batch["mask"].to(device, dtype=torch.long)
        targets = batch["targets"].to(device, dtype=torch.long)

        outputs = model(input_ids=ids, attention_mask=mask, labels=targets)
        loss, ev_logits = outputs.loss, outputs.logits
        ev_loss += loss.item()

        nb_ev_steps += 1
        nb_ev_examples += targets.size(0)

        # compute valuation accuracy
        flattened_targets = targets.view(-1)
        active_logits = ev_logits.view(-1, model.num_labels)
        flattened_predictions = torch.argmax(active_logits, axis=1)
        active_accuracy = mask.view(-1) == 1
        targets = torch.masked_select(flattened_targets, active_accuracy)
        predictions = torch.masked_select(flattened_predictions, active_accuracy)
        ev_preds.extend(predictions)
        ev_labels.extend(targets)
        tmp_ev_accuracy = accuracy_score(
            targets.cpu().numpy(), predictions.cpu().numpy()
        )
        ev_accuracy += tmp_ev_accuracy
    ev_epoch_loss = ev_loss / nb_ev_steps
    ev_accuracy = ev_accuracy / nb_ev_steps

    y_true = []
    y_pred = []
    for i in range(len(ev_labels)):
        if ev_labels[i].cpu().item() != 0:
            y_true.append(ev_labels[i].cpu().item())
            y_pred.append(ev_preds[i].cpu().item())
    ev_acc = accuracy_score(y_true, y_pred)
    logs(
        str(datetime.now()) + "    ",
        f"Validation loss epoch: {ev_epoch_loss}",
        logs_file_name,
    )
    logs(
        str(datetime.now()) + "    ",
        f"Validation accuracy epoch: {ev_acc}",
        logs_file_name,
    )


# Tracking variables
def test_score(test_loader, model):
    tst_accuracy = 0
    nb_tst_steps, nb_tst_examples = 0, 0
    tst_preds, tst_labels = [], []
    model.eval()
    for idx, batch in enumerate(test_loader):
        ids = batch["ids"].to(device, dtype=torch.long)
        mask = batch["mask"].to(device, dtype=torch.long)
        targets = batch["targets"].to(device, dtype=torch.long)
        outputs = model(input_ids=ids, attention_mask=mask)
        tst_logits = outputs.logits

        nb_tst_steps += 1
        nb_tst_examples += targets.size(0)

        flattened_targets = targets.view(-1)
        active_logits = tst_logits.view(-1, model.num_labels)
        flattened_predictions = torch.argmax(active_logits, axis=1)
        active_accuracy = mask.view(-1) == 1
        targets = torch.masked_select(flattened_targets, active_accuracy)
        predictions = torch.masked_select(flattened_predictions, active_accuracy)
        tst_preds.extend(predictions)
        tst_labels.extend(targets)
        tmp_tst_accuracy = accuracy_score(
            targets.cpu().numpy(), predictions.cpu().numpy()
        )
        tst_accuracy += tmp_tst_accuracy

    tst_accuracy = tst_accuracy / nb_tst_steps
    y_true = []
    y_pred = []
    for i in range(len(tst_labels)):
        if tst_labels[i].cpu().item() != 0:
            y_true.append(tst_labels[i].cpu().item())
            y_pred.append(tst_preds[i].cpu().item())
    tst_acc = accuracy_score(y_true, y_pred)
    cr = classification_report(
        y_true,
        y_pred,
        target_names=sorted(target_labels[1:], reverse=True),
        zero_division=0,
    )

    f_macro = f1_score(y_true, y_pred, average="macro")
    logs(str(datetime.now()) + "    ", f"f1_score(macro) : {f_macro} ", logs_file_name)
    logs(str(datetime.now()) + "    ", f"Accuracy : {tst_acc} ", logs_file_name)
    logs(str(datetime.now()) + "    ", "Classification Report", logs_file_name)
    logs(str(datetime.now()) + "    ", "--" * 30, logs_file_name)
    logs(cr, logs_file_name)
    return "testing done!"


def train(epoch, optimizer, training_loader, max_grad_norm):
    model.train()
    train_score(optimizer, training_loader, max_grad_norm)
    if val_loader is not None:
        val_score(val_loader, model)


# DEFINING MODEL training
def train_model(
    model_name, epochs, mode, lab_check, learning_rate, max_grad_norm, model_save_path
):
    global model, tokenizer, logs_file_name
    # log file
    logs_file_name = (
        datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + "_tfm_ner_training_logs.txt"
    )

    def create_model():
        # ## saving current model
        save_custom_model(f"{model_save_path}/{model_name}")
        model = AutoModelForTokenClassification.from_pretrained(
            model_name,
            ignore_mismatched_sizes=True,
            num_labels=len(label2id),
            id2label=id2label,
            label2id=label2id,
        )
        return model

    # training start time
    start_time = datetime.now()

    if mode == 1:
        logs(
            str(datetime.now()) + "    ",
            "Model is loading from scratch in default mode",
            logs_file_name,
        )
        model = create_model()
        logs(str(datetime.now()) + "    ", model, logs_file_name)

    elif mode == 2:
        logs(
            str(datetime.now()) + "    ",
            "Model is loading from scratch in append mode",
            logs_file_name,
        )
        model = create_model()
        logs(str(datetime.now()) + "    ", model, logs_file_name)

    elif mode == 3 and lab_check is False:
        resp1 = "data label and model labels is not matching"
        resp2 = " please use default mode for training from scretch"
        return resp1 + resp2

    else:
        logs(
            str(datetime.now()) + "    ",
            "same model is retraining in incremental mode",
            logs_file_name,
        )
    model.to(device)
    optimizer = torch.optim.Adam(params=model.parameters(), lr=learning_rate)

    # Defining the training function on the 80% of the dataset
    # for tuning the bert model
    for epoch in range(epochs):
        t0 = datetime.now()
        logs(
            str(datetime.now()) + "    ",
            f"Training epoch: {epoch + 1}/{epochs}",
            logs_file_name,
        )
        # calling function epochs train
        train(epoch, optimizer, training_loader, max_grad_norm)
        # saving model on epochs
        save_custom_model(f"{model_save_path}/curr_checkpoint/{model_name}")
        logs(
            str(datetime.now()) + "    ",
            f"Epoch {epoch + 1} total time taken : {datetime.now() - t0}",
            logs_file_name,
        )
        logs(str(datetime.now()) + "    ", "--" * 30, logs_file_name)

    # writing checkpoint
    total_time = datetime.now() - start_time
    logs(str(datetime.now()) + "    ", "Model Training is Completed", logs_file_name)
    logs(str(datetime.now()) + "    ", "--" * 30, logs_file_name)
    logs(
        str(datetime.now()) + "    ",
        "Total time taken to completed training : ",
        str(total_time),
        logs_file_name,
    )
    logs(str(datetime.now()) + "    ", "--" * 30, logs_file_name)

    # ###################### testing started ##########################
    if test_loader is not None:
        logs(str(datetime.now()) + "    ", "Model testing is started", logs_file_name)
        logs(str(datetime.now()) + "    ", "--" * 30, logs_file_name)
        time1 = datetime.now()
        test_score(test_loader, model)
        logs(str(datetime.now()) + "    ", "--" * 30, logs_file_name)
        totaltime = datetime.now() - time1
        logs(
            str(datetime.now()) + "    ",
            "Total time taken to completed testing : ",
            str(totaltime),
            logs_file_name,
        )
        logs(str(datetime.now()) + "    ", "--" * 30, "", logs_file_name)

    # Clearing cuda memory
    torch.cuda.empty_cache()
    return f"model training is completed. total time taken {total_time}"


def load_custom_model(model_path):
    global model, tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForTokenClassification.from_pretrained(model_path)
    model.to(device)


def save_custom_model(model_path):
    # saving model
    model.save_pretrained(model_path)
    tokenizer.save_pretrained(model_path)
    print(str(datetime.now()) + "   ", f"model saved successful to : {model_path}")


# predicting entities
def predict_text(sentence):
    pipe = pipeline("ner", model=model.to("cpu"), tokenizer=tokenizer)
    entities = pipe(sentence)
    ents = []
    for itm in entities:
        ents.append(
            {
                "entity_value": itm["word"],
                "entity_type": itm["entity"],
                "score": float(itm["score"]),
                "start_index": itm["start"],
                "end_index": itm["end"],
            }
        )
    return ents
