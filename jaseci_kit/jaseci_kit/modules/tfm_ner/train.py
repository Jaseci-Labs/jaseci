import shutil
from sklearn.metrics import accuracy_score, f1_score, classification_report
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline
from .utils.data_tokens import load_data
from torch import cuda
import os
from datetime import datetime
import mlflow
from mlflow.tracking import MlflowClient

device = "cuda" if cuda.is_available() else "cpu"
print("Using device for training -> ", device)


def start_mlflow_exp(tracking_uri, tfm_exp_name):
    # adding tracking url for storing parameter and merics data
    mlflow.set_tracking_uri(tracking_uri)
    # getting experiment Id if None then creat new one
    experiment_id = mlflow.get_experiment_by_name(tfm_exp_name)
    if experiment_id is None:
        experiment_id = mlflow.create_experiment(tfm_exp_name)
    else:
        experiment_id = experiment_id.experiment_id
    print("experiment_id : ", experiment_id)
    return experiment_id


# changing stages of register model default values("Staging", "Production")
def transition(model_name, version, stage):
    client = MlflowClient()
    client.transition_model_version_stage(
        name=model_name, version=version, stage=stage, archive_existing_versions=True
    )


# Logging
def logs(*args):
    with open("train/logs/" + args[-1], "a") as f:
        data = ""
        for arg in args[:-1]:
            data += str(arg)
        print(data)
        f.write(data)
        f.write("\n")


# preparing dataset for training
# TOKENIZE DATASET
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


# ch3cking the labels is matching with current model config
def check_labels_ok():
    lst_data_labels = list(id2label.values())
    lst_model_labels = list(model.config.id2label.values())
    for label in lst_data_labels:
        if label not in lst_model_labels:
            return False
    return True


# checking training score
def train_score(optimizer, training_loader, max_grad_norm, use_mlflow):
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

    # logging training result in database or in local directry
    if use_mlflow is True:
        mlflow.log_metric("Train Epoch Loss", epoch_loss, step=nb_tr_steps)
        mlflow.log_metric("Train Epoch Accuracy", tr_acc, step=nb_tr_steps)

    # creating training logs
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
    return tr_acc


# checking val score and  Tracking variables
def val_score(val_loader, model, use_mlflow):
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
    # logging validation result in database or in local directry
    if use_mlflow is True:
        mlflow.log_metric("Val epoch loss", ev_epoch_loss, step=nb_ev_steps)
        mlflow.log_metric("Val epoch accuracy", ev_acc, step=nb_ev_steps)

    # creating logs
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
    return ev_acc


# checking testing score and Tracking variables
def test_score(test_loader, model, use_mlflow):
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
    labs = model.config.id2label
    y_true = [labs[int(e)] for e in y_true]
    y_pred = [labs[int(e)] for e in y_pred]
    tst_acc = accuracy_score(y_true, y_pred)
    cr = classification_report(
        y_true,
        y_pred,
        zero_division=0,
    )

    f_macro = f1_score(y_true, y_pred, average="macro")
    # logging testing result in database or in local directry
    if use_mlflow is True:
        mlflow.log_metric("Test f1_macro", f_macro)
        mlflow.log_metric("Test accuracy", tst_acc)

    # creating logs
    logs(str(datetime.now()) + "    ", f"f1_score(macro) : {f_macro} ", logs_file_name)
    logs(str(datetime.now()) + "    ", f"Accuracy : {tst_acc} ", logs_file_name)
    logs(str(datetime.now()) + "    ", "Classification Report", logs_file_name)
    logs(str(datetime.now()) + "    ", "--" * 30, logs_file_name)
    logs(cr, logs_file_name)
    return "testing done!"


# function for start model training sepratly
def start_model_training(
    epochs,
    optimizer,
    max_grad_norm,
    model_save_path,
    model_name,
    start_time,
    use_mlflow,
):
    best_acc = 0
    for epoch in range(epochs):
        t0 = datetime.now()
        logs(
            str(datetime.now()) + "    ",
            f"Training epoch: {epoch + 1}/{epochs}",
            logs_file_name,
        )
        # calling function epochs train
        model.train()
        acc = train_score(optimizer, training_loader, max_grad_norm, use_mlflow)
        if val_loader is not None:
            acc = val_score(val_loader, model, use_mlflow)
        # acc = train(epoch, optimizer, training_loader, max_grad_norm)
        if acc > best_acc:
            best_acc = acc
            save_custom_model(f"{model_save_path}/model/{model_name}")

        logs(
            str(datetime.now()) + "    ",
            f"Epoch {epoch + 1} total time taken : {datetime.now() - t0}",
            logs_file_name,
        )
    logs(str(datetime.now()) + "    ", "--" * 30, logs_file_name)
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
        test_score(test_loader, model, use_mlflow)
        logs(str(datetime.now()) + "    ", "--" * 30, logs_file_name)
        totaltime = datetime.now() - time1
        logs(
            str(datetime.now()) + "    ",
            "Total time taken to completed testing : ",
            str(totaltime),
            logs_file_name,
        )
        logs(str(datetime.now()) + "    ", "--" * 30, "", logs_file_name)


# changing model layer if labels is changing
def create_model(model_name, id2label, label2id):
    # loading current model
    model = AutoModelForTokenClassification.from_pretrained(
        model_name,
        ignore_mismatched_sizes=True,
        num_labels=len(label2id),
        id2label=id2label,
        label2id=label2id,
    )
    return model


# DEFINING MODEL training for api
def training(
    model_name,
    epochs,
    mode,
    lab_check,
    learning_rate,
    max_grad_norm,
    model_save_path,
    use_mlflow,
    tracking_uri,
    exp_name,
    exp_run_name,
    description,
):
    global model, tokenizer, logs_file_name
    # log file
    logs_file_name = (
        datetime.now().strftime("%Y%m%d_%H%M%S") + "_tfm_ner_training_logs.txt"
    )
    # training start time
    start_time = datetime.now()
    if mode == 1:
        logs(
            str(datetime.now()) + "    ",
            "Model is loading from scratch in default mode",
            logs_file_name,
        )
        model = create_model(model_name, id2label, label2id)
        logs(str(datetime.now()) + "    ", model, logs_file_name)

    elif mode == 2:
        logs(
            str(datetime.now()) + "    ",
            "Model is loading from scratch in append mode",
            logs_file_name,
        )
        model = create_model(model_name, id2label, label2id)
        logs(str(datetime.now()) + "    ", model, logs_file_name)

    elif mode == 3 and lab_check is False:
        resp1 = "data label and model labels is not matching"
        resp2 = " please use default mode for training from scretch"
        return resp1 + resp2

    else:
        logs(
            str(datetime.now()) + "    ",
            "same model is re-training in incremental mode",
            logs_file_name,
        )
    model.to(device)
    optimizer = torch.optim.Adam(params=model.parameters(), lr=learning_rate)

    if use_mlflow is True:
        experiment_id = start_mlflow_exp(tracking_uri, exp_name)
        # start training with MLFlow
        with mlflow.start_run(
            run_name=exp_run_name,
            experiment_id=experiment_id,
            nested=True,
            description=description,
        ):
            # writing parameters
            mlflow.log_params(
                {
                    "Epochs": epochs,
                    "Optimizer": optimizer,
                    "Learning Rate": learning_rate,
                }
            )
            # starting model training
            start_model_training(
                epochs,
                optimizer,
                max_grad_norm,
                model_save_path,
                model_name,
                start_time,
                use_mlflow,
            )

            # storing model data on cloud or local storage with log_artifact
            mlflow.log_artifacts(
                f"{model_save_path}/model/{model_name}",
                artifact_path="pytorch_model/model",
            )

            # logging model data for model versioning
            mlflow.pytorch.log_model(
                model, artifact_path="pytorch_model", registered_model_name=exp_run_name
            )

            # delete temp model data
            if os.path.exists(f"{model_save_path}/model"):
                shutil.rmtree(f"{model_save_path}/model")

            # getting latest model version and register model as Staging
            client = MlflowClient()
            ver_lst = [
                dict(mv)
                for mv in client.search_model_versions(f"name='{exp_run_name}'")
            ]
            # client.search_registered_models()
            version = ver_lst[-1]["version"]
            source_path = ver_lst[-1]["source"] + "/model"
            transition(model_name=exp_run_name, version=version, stage="Staging")
    else:
        start_model_training(
            epochs,
            optimizer,
            max_grad_norm,
            model_save_path,
            model_name,
            start_time,
            use_mlflow,
        )
        source_path = f"{model_save_path}/model/{model_name}"

    # Clearing cuda memory
    torch.cuda.empty_cache()
    return source_path, "model training is completed."


def load_custom_model(model_path):
    global model, tokenizer
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForTokenClassification.from_pretrained(model_path)
        model.to(device)
    except Exception:
        tokenizer = AutoTokenizer.from_pretrained(model_path + "/model")
        model = AutoModelForTokenClassification.from_pretrained(model_path + "/model")
        model.to(device)


def save_custom_model(model_path):
    # saving model
    model.save_pretrained(model_path)
    tokenizer.save_pretrained(model_path)
    print(str(datetime.now()) + "   ", f"model saved successful to : {model_path}")


# predicting entities
def predict_text(sentence):
    pipe = pipeline(
        "ner", model=model.to("cpu"), tokenizer=tokenizer, aggregation_strategy="first"
    )
    entities = pipe(sentence)
    # print(entities)
    ents = []
    for itm in entities:
        ents.append(
            {
                "text": itm["word"],
                "entity": itm["entity_group"],
                "score": float(itm["score"]),
                "start": itm["start"],
                "end": itm["end"],
            }
        )
    return ents


# checking all available model versions
def model_versions(name):
    # getting all available model version with specific experiment name.
    client = MlflowClient()
    mv_lst = []
    for mv in client.search_model_versions(f"name='{name}'"):
        mv_lst.append(dict(mv))
    return mv_lst
