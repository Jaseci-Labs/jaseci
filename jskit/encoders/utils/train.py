import torch
from torch.utils.data import DataLoader
import os
import time
from tqdm import tqdm
from transformers.optimization import AdamW, get_linear_schedule_with_warmup
from . import tokenizer as token_util
import configparser

config = configparser.ConfigParser()
device, max_contexts_length, max_candidate_length, train_batch_size, \
    eval_batch_size, max_history, learning_rate, weight_decay, warmup_steps, \
    adam_epsilon, max_grad_norm, fp16, fp16_opt_level, gpu, \
    gradient_accumulation_steps, num_train_epochs = None, None, None, None, \
    None, None, None, None, None, None, None, None, None, None, None, None


# training setup
def config_setup():
    global device, basepath, max_contexts_length, max_candidate_length, \
        train_batch_size, eval_batch_size, max_history, learning_rate, \
        weight_decay, warmup_steps, adam_epsilon, max_grad_norm, fp16, \
        fp16_opt_level, gpu, gradient_accumulation_steps, num_train_epochs, shared
    #device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    device = torch.device('cpu')
    config.read('utils/config.cfg')
    max_contexts_length = int(
        config['TRAIN_PARAMETERS']['MAX_CONTEXTS_LENGTH'])
    max_candidate_length = int(
        config['TRAIN_PARAMETERS']['MAX_CANDIDATE_LENGTH'])
    train_batch_size = int(config['TRAIN_PARAMETERS']['TRAIN_BATCH_SIZE'])
    eval_batch_size = int(config['TRAIN_PARAMETERS']['EVAL_BATCH_SIZE'])
    max_history = int(config['TRAIN_PARAMETERS']['MAX_HISTORY'])
    learning_rate = float(config['TRAIN_PARAMETERS']['LEARNING_RATE'])
    weight_decay = float(config['TRAIN_PARAMETERS']['WEIGHT_DECAY'])
    warmup_steps = int(config['TRAIN_PARAMETERS']['WARMUP_STEPS'])
    adam_epsilon = float(config['TRAIN_PARAMETERS']['ADAM_EPSILON'])
    max_grad_norm = float(config['TRAIN_PARAMETERS']['MAX_GRAD_NORM'])
    gradient_accumulation_steps = int(
        config['TRAIN_PARAMETERS']['GRADIENT_ACCUMULATION_STEPS'])
    num_train_epochs = int(config['TRAIN_PARAMETERS']['NUM_TRAIN_EPOCHS'])
    fp16 = bool(config['TRAIN_PARAMETERS']['FP16'])
    fp16_opt_level = str(config['TRAIN_PARAMETERS']['FP16_OPT_LEVEL'])
    gpu = int(config['TRAIN_PARAMETERS']['GPU'])
    shared = config['MODEL_PARAMETERS']['SHARED']


output_dir = "log_output"
train_dir = "."
model = None
global_step, tr_loss, nb_tr_steps, epoch, device, basepath, shared = None, None, \
    None, None, None, None, None


# training function
def train_model(model_train, tokenizer, contexts, candidates, labels, output_dir, val=False):
    config_setup()
    global model, global_step, tr_loss, nb_tr_steps, epoch, device, basepath, shared

    model = model_train
    context_transform = token_util.SelectionJoinTransform(
        tokenizer=tokenizer,
        max_len=int(max_contexts_length)
    )
    candidate_transform = token_util.SelectionSequentialTransform(
        tokenizer=tokenizer,
        max_len=int(max_candidate_length)
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
        batch_size=train_batch_size,
        collate_fn=train_dataset.batchify_join_str,
        shuffle=True
    )
    t_total = len(train_dataloader) // train_batch_size * \
        (max(5, num_train_epochs))
    epoch_start = 1
    global_step = 0
    bert_dir = output_dir+"/bert"
    resp_bert_dir = output_dir+"/resp_bert"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(bert_dir):
        os.makedirs(bert_dir)
    if not os.path.exists(resp_bert_dir):
        os.makedirs(resp_bert_dir)
    log_wf = open(os.path.join(output_dir, 'log.txt'),
                  'a', encoding='utf-8')
    if shared:
        state_save_path = os.path.join(output_dir, 'pytorch_model.bin')
    else:
        state_save_path = os.path.join(bert_dir, 'pytorch_model.bin')
        state_save_path_1 = os.path.join(
            resp_bert_dir, 'pytorch_model.bin')

    state_save_path = os.path.join(output_dir, 'pytorch_model.bin')
    no_decay = ["bias", "LayerNorm.weight"]
    optimizer_grouped_parameters = [
        {
            "params": [
                p for n, p in model.named_parameters() if not any(
                    nd in n for nd in no_decay)],
            "weight_decay": weight_decay,
        },
        {"params": [p for n, p in model.named_parameters() if any(
            nd in n for nd in no_decay)], "weight_decay": 0.0},
    ]
    optimizer = AdamW(optimizer_grouped_parameters,
                      lr=learning_rate, eps=adam_epsilon)
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=warmup_steps, num_training_steps=t_total
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
            model, optimizer, opt_level=fp16_opt_level)
    print_freq = 1
    eval_freq = min(len(train_dataloader), 1000)
    print('Print freq:', print_freq, "Eval freq:", eval_freq)
    train_start_time = time.time()
    print(f"train_start_time : {train_start_time}")
    for epoch in range(epoch_start, int(num_train_epochs) + 1):
        tr_loss = 0
        nb_tr_examples, nb_tr_steps = 0, 0
        with tqdm(total=len(train_dataloader)) as bar:
            for step, batch in enumerate(train_dataloader, start=1):
                model.train()
                optimizer.zero_grad()
                batch = tuple(t.to(device) for t in batch)
                context_token_ids_list_batch,  context_input_masks_list_batch, \
                    candidate_token_ids_list_batch,  candidate_input_masks_list_batch, labels_batch = batch

                loss = model(context_token_ids_list_batch,  context_input_masks_list_batch,
                             candidate_token_ids_list_batch, candidate_input_masks_list_batch,
                             labels_batch)
                print(f"loss is  : {loss}")
                tr_loss += loss.item()
                nb_tr_examples += context_token_ids_list_batch.size(0)
                nb_tr_steps += 1

                if fp16:
                    with amp.scale_loss(loss, optimizer) as scaled_loss:
                        scaled_loss.backward()
                    torch.nn.utils.clip_grad_norm_(
                        amp.master_params(optimizer), max_grad_norm)
                else:
                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(
                        model.parameters(), max_grad_norm)

                optimizer.step()
                if global_step < warmup_steps:
                    scheduler.step()
                model.zero_grad()
                global_step += 1

                if step % print_freq == 0:
                    bar.update(min(print_freq, step))
                    time.sleep(0.02)
                    print(global_step, tr_loss / nb_tr_steps)
                    log_wf.write('%d\t%f\n' %
                                 (global_step, tr_loss / nb_tr_steps))

                log_wf.flush()
                pass
    if shared is True:
        torch.save(model.state_dict(), state_save_path)
    else:
        print('[Saving at]', state_save_path)
        log_wf.write('[Saving at] %s\n' % state_save_path)
        torch.save(model.resp_bert.state_dict(), state_save_path_1)
        torch.save(model.bert.state_dict(), state_save_path)
    return model
