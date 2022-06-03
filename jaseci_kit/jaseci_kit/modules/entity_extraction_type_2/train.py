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
def data_set(filename, filename1, filename2, max_len, train_batch_size):
    global id2label, label2id, training_loader, eval_loader, target_labels, test_loader
    ds = load_data(filename)
    train_dataset = ds[0]
    data_labels = ds[1]
    label2id = {k: v for v, k in enumerate(data_labels)}
    id2label = {v: k for v, k in enumerate(data_labels)}

    training_set = dataset(train_dataset, tokenizer, max_len)
    train_params = {"batch_size": train_batch_size, "shuffle": True, "num_workers": 0}
    training_loader = DataLoader(training_set, **train_params)

    # eval dataset
    if os.path.exists(filename1):
        ds1 = load_data(filename1)
        eval_dataset = ds1[0]
        data_labels1 = data_labels + [lab for lab in ds1[1] if lab not in data_labels]
        label2id = {k: v for v, k in enumerate(data_labels1)}
        id2label = {v: k for v, k in enumerate(data_labels1)}
        target_labels = ds1[0]

        eval_set = dataset(eval_dataset, tokenizer, max_len)
        eval_params = {
            "batch_size": train_batch_size,
            "shuffle": True,
            "num_workers": 0,
        }
        eval_loader = DataLoader(eval_set, **eval_params)
    else:
        eval_loader = None
        data_labels1 = data_labels

    # test dataset
    if os.path.exists(filename2):
        ds2 = load_data(filename2)
        test_dataset = ds2[0]
        data_labels2 = data_labels1 + [lab for lab in ds2[1] if lab not in data_labels1]
        # print(data_labels2)
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
            print(
                str(datetime.now()) + "    ",
                f"Training loss per 100 training steps: {loss_step}",
            )

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

    y_true = []
    y_pred = []
    for i in range(len(tr_labels)):
        if tr_labels[i].cpu().item() != 0:
            y_true.append(tr_labels[i].cpu().item())
            y_pred.append(tr_preds[i].cpu().item())
    tr_acc = accuracy_score(y_true, y_pred)

    return epoch_loss, tr_accuracy, tr_acc


# Tracking variables
def eval_score(eval_loader, model):
    ev_loss, ev_accuracy = 0, 0
    nb_ev_steps, nb_ev_examples = 0, 0
    ev_preds, ev_labels = [], []
    model.eval()
    for idx, batch in enumerate(eval_loader):
        ids = batch["ids"].to(device, dtype=torch.long)
        mask = batch["mask"].to(device, dtype=torch.long)
        targets = batch["targets"].to(device, dtype=torch.long)

        outputs = model(input_ids=ids, attention_mask=mask, labels=targets)
        # print(outputs)
        loss, ev_logits = outputs.loss, outputs.logits
        # print(loss)
        ev_loss += loss.item()

        nb_ev_steps += 1
        nb_ev_examples += targets.size(0)

        # compute evaluation accuracy
        flattened_targets = targets.view(-1)
        # shape (batch_size * seq_len,)
        active_logits = ev_logits.view(-1, model.num_labels)
        # shape (batch_size * seq_len, num_labels)
        flattened_predictions = torch.argmax(active_logits, axis=1)
        # shape (batch_size * seq_len,)
        # now, use mask to determine where we should compare predictions
        # with targets (includes [CLS] and [SEP] token predictions)
        active_accuracy = mask.view(-1) == 1
        # active accuracyis also of shape (batch_size * seq_len,)
        targets = torch.masked_select(flattened_targets, active_accuracy)
        predictions = torch.masked_select(flattened_predictions, active_accuracy)

        ev_preds.extend(predictions)
        ev_labels.extend(targets)

        # print(targets)
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
    return ev_epoch_loss, ev_accuracy, ev_acc


# Tracking variables
def test_score(test_loader, model):
    tst_accuracy = 0
    nb_tst_steps, nb_tst_examples = 0, 0
    # global y_pred, y_true
    tst_preds, tst_labels = [], []
    model.eval()
    for idx, batch in enumerate(test_loader):
        ids = batch["ids"].to(device, dtype=torch.long)
        mask = batch["mask"].to(device, dtype=torch.long)
        targets = batch["targets"].to(device, dtype=torch.long)

        outputs = model(input_ids=ids, attention_mask=mask)
        # print(outputs)
        tst_logits = outputs.logits

        nb_tst_steps += 1
        nb_tst_examples += targets.size(0)

        # compute evaluation accuracy
        flattened_targets = targets.view(-1)
        # shape (batch_size * seq_len,)
        active_logits = tst_logits.view(-1, model.num_labels)
        # shape (batch_size * seq_len, num_labels)
        flattened_predictions = torch.argmax(active_logits, axis=1)
        # shape (batch_size * seq_len,)
        # now, use mask to determine where we should compare predictions
        # with targets (includes [CLS] and [SEP] token predictions)
        active_accuracy = mask.view(-1) == 1
        # active accuracyis also of shape (batch_size * seq_len,)
        targets = torch.masked_select(flattened_targets, active_accuracy)
        predictions = torch.masked_select(flattened_predictions, active_accuracy)
        tst_preds.extend(predictions)
        tst_labels.extend(targets)

        # print(targets)
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
    f_micro = f1_score(y_true, y_pred, average="micro")
    return tst_accuracy, cr, f_macro, f_micro, tst_acc


def train(epoch, optimizer, training_loader, max_grad_norm):
    model.train()
    tr_score = train_score(optimizer, training_loader, max_grad_norm)
    if eval_loader is not None:
        ev_score = eval_score(eval_loader, model)
    else:
        ev_score = (None, None, None)
    return tr_score, ev_score


# DEFINING MODEL training
def train_model(
    model_name, epochs, mode, lab_check, learning_rate, max_grad_norm, model_save_path
):
    global model, tokenizer

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

    # log file
    train_logs_name = (
        datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + "_tfm_ner_training_logs.txt"
    )
    with open("train/logs/" + train_logs_name, "a") as out:
        print("==" * 10, "Transformer Ner Training Logs", "==" * 10, "\n", file=out)

        # training start time
        start_time = datetime.now()

        if mode == 3 and lab_check is False:
            resp1 = "data label and model labels is not matching"
            resp2 = " please use default mode for training from scretch"
            return resp1 + resp2

        elif mode == 2:
            print(
                str(datetime.now()) + "    ",
                "Model is loading from scratch in append mode",
                file=out,
            )
            print(
                str(datetime.now()) + "    ",
                "Model is loading from scratch in append mode",
            )
            model = create_model()
            print(str(datetime.now()) + "    ", model, file=out)

        elif mode == 1:

            print(
                str(datetime.now()) + "    ",
                "Model is loading from scratch in default mode",
                file=out,
            )
            print(
                str(datetime.now()) + "    ",
                "Model is loading from scratch in default mode",
            )
            model = create_model()
            print(str(datetime.now()) + "    ", model, file=out)

        else:
            print(
                str(datetime.now()) + "    ",
                "same model is retraining in incremental mode",
                file=out,
            )
            print(
                str(datetime.now()) + "    ",
                "same model is retraining in incremental mode",
            )

        model.to(device)
        optimizer = torch.optim.Adam(params=model.parameters(), lr=learning_rate)

        # Defining the training function on the 80% of the dataset
        # for tuning the bert model
        for epoch in range(epochs):
            t0 = datetime.now()
            print(
                str(datetime.now()) + "    ",
                f"Training epoch: {epoch + 1}/{epochs}",
                file=out,
            )
            print(str(datetime.now()) + "    ", f"Training epoch: {epoch + 1}/{epochs}")
            # calling function epochs train
            status = train(epoch, optimizer, training_loader, max_grad_norm)
            print(
                str(datetime.now()) + "    ",
                f"Training loss epoch: {status[0][0]}",
                file=out,
            )
            print(
                str(datetime.now()) + "    ",
                f"Training accuracy epoch: {status[0][1]}",
                file=out,
            )
            print(
                str(datetime.now()) + "    ",
                f"Training accuracy epoch except('O') : {status[0][2]}",
                file=out,
            )
            print(str(datetime.now()) + "    ", f"Training loss epoch: {status[0][0]}")
            print(
                str(datetime.now()) + "    ", f"Training accuracy epoch: {status[0][1]}"
            )
            print(
                str(datetime.now()) + "    ",
                f"Training accuracy epochexcept('O') : {status[0][2]}",
            )
            print(
                str(datetime.now()) + "    ",
                f"evaluation loss epoch: {status[1][0]}",
                file=out,
            )
            print(
                str(datetime.now()) + "    ",
                f"evaluation accuracy epoch: {status[1][1]}",
                file=out,
            )
            print(
                str(datetime.now()) + "    ",
                f"evaluation accuracy epoch except('O') : {status[1][2]}",
                file=out,
            )
            print(
                str(datetime.now()) + "    ", f"evaluation loss epoch: {status[1][0]}"
            )
            print(
                str(datetime.now()) + "    ",
                f"evaluation accuracy epoch: {status[1][1]}",
            )
            print(
                str(datetime.now()) + "    ",
                f"evaluation accuracy epoch except('O') : {status[1][2]}",
            )

            # saving model to disk
            save_custom_model(f"{model_save_path}/curr_checkpoint/{model_name}")
            print(
                str(datetime.now()) + "    ",
                f"Epoch {epoch + 1} total time taken : {datetime.now() - t0}",
                file=out,
            )
            print(
                str(datetime.now()) + "    ",
                f"Epoch {epoch + 1} total time taken : {datetime.now() - t0}",
            )
            print(str(datetime.now()) + "    ", "--" * 30, file=out)
            print(str(datetime.now()) + "    ", "--" * 30)

        # ########## writing checkpoint

        total_time = datetime.now() - start_time
        print(str(datetime.now()) + "    ", "Model Training is Completed", file=out)
        print(str(datetime.now()) + "    ", "Model Training is Completed")
        print(str(datetime.now()) + "    ", "--" * 30, file=out)
        print(str(datetime.now()) + "    ", "--" * 30)
        print(
            str(datetime.now()) + "    ",
            "Total time taken to completed training : ",
            str(total_time),
            file=out,
        )
        print(
            str(datetime.now()) + "    ",
            "Total time taken to completed training : ",
            str(total_time),
        )
        print(str(datetime.now()) + "    ", "--" * 30, file=out)
        print(str(datetime.now()) + "    ", "--" * 30)

        # ###################### testing started ##########################

        if test_loader is not None:
            st = test_score(test_loader, model)

            time1 = datetime.now()
            print(str(datetime.now()) + "    ", "Model testing is started", file=out)
            print(str(datetime.now()) + "    ", "Model testing is started")
            print(str(datetime.now()) + "    ", "--" * 30, file=out)
            print(str(datetime.now()) + "    ", "--" * 30)

            print(str(datetime.now()) + "    ", f"f1_score(macro) : {st[2]} ", file=out)
            print(str(datetime.now()) + "    ", f"f1_score(micro) : {st[3]} ", file=out)
            print(str(datetime.now()) + "    ", f"Accuracy : {st[0]} ", file=out)
            print(
                str(datetime.now()) + "    ",
                f"Accuracy except('O') : {st[4]} ",
                file=out,
            )
            print(str(datetime.now()) + "    ", "Classification Report", file=out)
            print(str(datetime.now()) + "    ", "--" * 30, file=out)
            print(st[1], file=out)

            print(str(datetime.now()) + "    ", f"f1_score(macro) : {st[2]}")
            print(str(datetime.now()) + "    ", f"f1_score(micro) : {st[3]}")
            print(str(datetime.now()) + "    ", f"Accuracy : {st[0]} ")
            print(str(datetime.now()) + "    ", f"Accuracy except('O') : {st[4]} ")
            print(str(datetime.now()) + "    ", "Classification Report")
            print(str(datetime.now()) + "    ", "--" * 30)
            print(st[1])
            print(str(datetime.now()) + "    ", "--" * 30, file=out)
            print(str(datetime.now()) + "    ", "--" * 30)
            totaltime = datetime.now() - time1
            print(
                str(datetime.now()) + "    ",
                "Total time taken to completed testing : ",
                str(totaltime),
                file=out,
            )
            print(
                str(datetime.now()) + "    ",
                "Total time taken to completed testing : ",
                str(totaltime),
            )
            print(str(datetime.now()) + "    ", "--" * 30, "", file=out)
            print(str(datetime.now()) + "    ", "--" * 30, "")

    # Clearing cuda memory
    # os.remove("train/train.txt")
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
    print(str(datetime.now()) + "    ", f"model saved successful to : {model_path}")


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
