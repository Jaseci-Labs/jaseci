from torch.utils.data import DataLoader
from tqdm.autonotebook import trange
import os
from transformers.optimization import AdamW, get_linear_schedule_with_warmup
import torch
import math


def train_model(model, train_dataset, train_config):
    train_dataloader = DataLoader(
        train_dataset,
        batch_size=train_config["train_batch_size"],
        shuffle=True,
    )
    t_total = (
        len(train_dataloader)
        // train_config["gradient_accumulation_steps"]
        * (max(5, train_config["num_train_epochs"]))
    )

    global_step = 0
    if not os.path.exists(train_config["basepath"]):
        os.makedirs(train_config["basepath"])
    log_wf = open(
        os.path.join(train_config["basepath"], "log.txt"), "w", encoding="utf-8"
    )  # will be used in for logging
    no_decay = ["bias", "LayerNorm.weight"]
    optimizer_grouped_parameters = [
        {
            "params": [
                p
                for n, p in model.named_parameters()
                if not any(nd in n for nd in no_decay)
            ],
            "weight_decay": train_config["weight_decay"],
        },
        {
            "params": [
                p
                for n, p in model.named_parameters()
                if any(nd in n for nd in no_decay)
            ],
            "weight_decay": 0.0,
        },
    ]
    optimizer = AdamW(
        optimizer_grouped_parameters,
        lr=train_config["learning_rate"],
        eps=train_config["adam_epsilon"],
    )
    warmup_steps = math.ceil(
        len(train_dataset)
        * train_config["num_train_epochs"]
        / train_config["train_batch_size"]
        * 0.1
    )
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=warmup_steps, num_training_steps=t_total
    )
    for epoch in trange(
        train_config["num_train_epochs"], desc="Epoch", disable=False, unit="batch"
    ):
        tr_loss = 0
        nb_tr_steps = 0
        with trange(len(train_dataloader), unit="it") as bar:
            for step, batch in enumerate(train_dataloader, start=1):
                model.train()
                optimizer.zero_grad()
                loss = model.training_step(batch)
                tr_loss += loss.item()
                nb_tr_steps += 1
                if (step + 1) % train_config["gradient_accumulation_steps"] == 0:

                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(
                        model.parameters(), train_config["max_grad_norm"]
                    )

                    optimizer.step()
                    scheduler.step()
                    model.zero_grad()
                    global_step += 1
                    bar.update()

        print(
            f"""\n
            Epoch : {epoch+1}
            loss : {tr_loss/nb_tr_steps}
            LR : {optimizer.param_groups[0]['lr']}\n"""
        )
        log_wf.write(f"{epoch+1}\t{tr_loss/nb_tr_steps}\n")
    log_wf.close()
    return model
