import torch
from torch.utils.data import DataLoader
import os
from tqdm.autonotebook import trange
from transformers.optimization import AdamW, get_linear_schedule_with_warmup
from . import tokenizer as token_util


def train_model(model, tokenizer, contexts, candidates, labels, train_config):

    context_transform = token_util.SelectionJoinTransform(
        tokenizer=tokenizer,
        max_len=train_config['max_contexts_length']
    )
    candidate_transform = token_util.SelectionSequentialTransform(
        tokenizer=tokenizer,
        max_len=int(train_config['max_candidate_length'])
    )
    train_dataset = token_util.SelectionDataset(
        contexts=contexts,
        candidates=candidates,
        labels=labels,
        context_transform=context_transform,
        candidate_transform=candidate_transform
    )
    train_dataloader = DataLoader(
        train_dataset,
        batch_size=train_config['train_batch_size'],
        collate_fn=train_dataset.batchify_join_str,
        shuffle=True
    )
    t_total = len(train_dataloader) // train_config['train_batch_size'] * \
        (max(5, train_config['num_train_epochs']))
    global_step = 0
    if not os.path.exists(train_config['basepath']):
        os.makedirs(train_config['basepath'])
    # log_wf = open(os.path.join(train_config['basepath'], 'log.txt'),
    #               'a', encoding='utf-8') # will be used in for logging
    no_decay = ["bias", "LayerNorm.weight"]
    optimizer_grouped_parameters = [
        {
            "params": [
                p for n, p in model.named_parameters() if not any(
                    nd in n for nd in no_decay)],
            "weight_decay": train_config['weight_decay'],
        },
        {"params": [p for n, p in model.named_parameters() if any(
            nd in n for nd in no_decay)], "weight_decay": 0.0},
    ]
    optimizer = AdamW(optimizer_grouped_parameters,
                      lr=train_config['learning_rate'],
                      eps=train_config['adam_epsilon'])
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=train_config['warmup_steps'],
        num_training_steps=t_total
    )
    fp16 = False
    if fp16:
        try:
            from apex import amp
        except ImportError:
            raise ImportError(
                '''Please install apex from https://www.github.com/nvidia/apex
                to use fp16 training''')
        model, optimizer = amp.initialize(
            model, optimizer, opt_level=train_config['fp16_opt_level'])
    for epoch in trange(train_config['num_train_epochs'], desc="Epoch",
                        disable=False, unit='batch'):
        tr_loss = 0
        nb_tr_examples, nb_tr_steps = 0, 0
        with trange(len(train_dataloader), unit="it") as bar:
            for step, batch in enumerate(train_dataloader, start=1):
                model.train()
                optimizer.zero_grad()
                batch = tuple(t.to(train_config['device']) for t in batch)
                context_token_ids_list_batch, \
                    context_input_masks_list_batch, \
                    candidate_token_ids_list_batch, \
                    candidate_input_masks_list_batch, \
                    labels_batch = batch

                loss = model(context_token_ids_list_batch,
                             context_input_masks_list_batch,
                             candidate_token_ids_list_batch,
                             candidate_input_masks_list_batch,
                             labels_batch)
                tr_loss += loss.item()
                nb_tr_examples += context_token_ids_list_batch.size(0)
                nb_tr_steps += 1

                if fp16:
                    with amp.scale_loss(loss, optimizer) as scaled_loss:
                        scaled_loss.backward()
                    torch.nn.utils.clip_grad_norm_(
                        amp.master_params(optimizer),
                        train_config['max_grad_norm'])
                else:
                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(
                        model.parameters(), train_config['max_grad_norm'])

                optimizer.step()
                if global_step < train_config['warmup_steps']:
                    scheduler.step()
                model.zero_grad()
                global_step += 1
                bar.update()
        print(f"\nEpoch : {epoch+1} \t loss : {tr_loss/nb_tr_steps}\n")

    return model
