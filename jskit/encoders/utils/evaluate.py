import os
import torch
from torch.utils.data import DataLoader
from . import tokenizer as token_util
import configparser
config = configparser.ConfigParser()

max_history, max_contexts_length, max_candidate_length, device = None, \
    None, None, None


# inference parameters setup
def config_setup():
    global max_history, max_contexts_length, max_candidate_length, device
    dirname = os.path.dirname(__file__)
    config_fname = os.path.join(dirname, 'config.cfg')
    config.read(config_fname)
    max_history = int(config['TRAIN_PARAMETERS']['MAX_HISTORY'])
    max_contexts_length = int(
        config['TRAIN_PARAMETERS']['MAX_CONTEXTS_LENGTH'])
    max_candidate_length = int(
        config['TRAIN_PARAMETERS']['MAX_CANDIDATE_LENGTH'])
    # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    device = torch.device('cpu')


config_setup()


def get_inference(model, tokenizer, contexts, candidates):
    global max_history, max_contexts_length, max_candidate_length, device
    context_transform = token_util.SelectionJoinTransform(
        tokenizer=tokenizer,
        max_len=max_contexts_length
    )
    candidate_transform = token_util.SelectionSequentialTransform(
        tokenizer=tokenizer,
        max_len=max_candidate_length
    )
    labels = [0] * len(candidates)
    test_data = token_util.SelectionDataset(
        contexts=contexts,
        candidates=candidates,
        context_transform=context_transform,
        candidate_transform=candidate_transform, mode="eval",
        labels=labels
    )
    val_dataloader = DataLoader(
        test_data,
        batch_size=1,
        collate_fn=test_data.batchify_join_str,
        shuffle=False
    )
    for step, batch in enumerate(val_dataloader, start=1):
        batch = tuple(t.to(device) for t in batch)
        context_token_ids_list_batch, context_input_masks_list_batch,\
            candidate_token_ids_list_batch, candidate_input_masks_list_batch,\
            labels_batch = batch
        with torch.no_grad():
            logits = model(context_token_ids_list_batch,  context_input_masks_list_batch,
                           candidate_token_ids_list_batch, candidate_input_masks_list_batch, mode="eval")
        _, prediction = torch.max(logits, dim=-1)
        return candidates[prediction]


# function provides embedding for context and candidate
def get_embeddings(model, tokenizer, text_data, embed_type="context"):
    global max_history, max_contexts_length, max_candidate_length, device
    if embed_type == "context":
        context_transform = token_util.SelectionJoinTransform(
            tokenizer=tokenizer,
            max_len=max_contexts_length)
        context_data = token_util.EvalDataset(
            text_data, context_transform=context_transform, candidate_transform=None, mode=embed_type)
    else:
        candidate_transform = token_util.SelectionSequentialTransform(
            tokenizer=tokenizer,
            max_len=max_candidate_length)
        context_data = token_util.EvalDataset(
            text_data, context_transform=None, candidate_transform=candidate_transform, mode=embed_type)
    dataloader = DataLoader(context_data, batch_size=1,
                            collate_fn=context_data.eval_str, shuffle=False, num_workers=0)
    for step, batch in enumerate(dataloader, start=1):
        batch = tuple(t.to(device) for t in batch)
        token_ids_list_batch,  input_masks_list_batch = batch

        with torch.no_grad():
            if embed_type == "context":
                embeddings = model(context_input_ids=token_ids_list_batch,
                                   context_input_masks=input_masks_list_batch, get_embedding=embed_type, mode="get_embed")
            else:
                embeddings = model(candidate_input_ids=token_ids_list_batch,
                                   candidate_input_masks=input_masks_list_batch, get_embedding=embed_type, mode="get_embed")
                embeddings = embeddings.squeeze(0)

    return embeddings.squeeze(0).detach().tolist()
