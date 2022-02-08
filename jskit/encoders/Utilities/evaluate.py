import torch
from torch.utils.data import DataLoader
from Utilities import tokenizer as token_util
import configparser
config = configparser.ConfigParser()

max_history, max_contexts_length, max_candidate_length, device = None, \
    None, None, None


def config_setup():
    global max_history, max_contexts_length, max_candidate_length, device
    config.read('Utilities/config.cfg')
    max_history = int(config['TRAIN_PARAMETERS']['MAX_HISTORY'])
    max_contexts_length = int(
        config['TRAIN_PARAMETERS']['MAX_CONTEXTS_LENGTH'])
    max_candidate_length = int(
        config['TRAIN_PARAMETERS']['MAX_RESPONSE_LENGTH'])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


config_setup()


def get_inference(model, tokenizer, context, candidate):
    global max_history, max_contexts_length, max_candidate_length, device
    context_transform = token_util.SelectionJoinTransform(
        tokenizer=tokenizer,
        max_len=max_contexts_length,
        max_history=max_history)
    candidate_transform = token_util.SelectionSequentialTransform(
        tokenizer=tokenizer,
        max_len=max_candidate_length,
        max_history=None, pair_last=False)

    test_data = token_util.SelectionDataset(context,
                                            candidate,
                                            context_transform,
                                            candidate_transform)
    val_dataloader = DataLoader(test_data,
                                batch_size=1,
                                collate_fn=test_data.batchify_join_str,
                                shuffle=False)
    for step, batch in enumerate(val_dataloader, start=1):
        batch = tuple(t.to(device) for t in batch)
        context_token_ids_list_batch, context_segment_ids_list_batch, \
            context_input_masks_list_batch, candidate_token_ids_list_batch, \
            candidate_segment_ids_list_batch, \
            candidate_input_masks_list_batch, labels_batch = batch
        with torch.no_grad():
            context_data = {
                "context_input_ids": context_token_ids_list_batch,
                "context_segment_ids": context_segment_ids_list_batch,
                "context_input_masks": context_input_masks_list_batch}
            candidate_data = {
                "candidate_input_ids": candidate_token_ids_list_batch,
                "candidates_segment_ids": candidate_segment_ids_list_batch,
                "candidate_input_masks": candidate_input_masks_list_batch}
        logits = model(context_data, candidate_data, eval=True)
        _, prediction = torch.max(logits, dim=1)
        print(candidate[prediction])
        return candidate[prediction]


def get_context_embedding(model, tokenizer, context):
    global max_history, max_contexts_length, max_candidate_length
    context_transform = token_util.SelectionJoinTransform(
        tokenizer=tokenizer,
        max_len=max_contexts_length,
        max_history=max_history)

    context_data = token_util.ContextData(context, context_transform)
    context_token_ids_list_batch, context_segment_ids_list_batch, \
        context_input_masks_list_batch = context_data.get_data()
    with torch.no_grad():
        embedding_data = {
            "context_input_ids": context_token_ids_list_batch,
            "context_segment_ids": context_segment_ids_list_batch,
            "context_input_masks": context_input_masks_list_batch}
        embeddings = model(context_data=embedding_data,
                           eval=True, get_embedding=True)
    # print(embeddings)
    return embeddings


def get_candidate_embedding(model, tokenizer, candidate):
    global max_history, max_contexts_length, max_candidate_length
    candidate_transform = token_util.SelectionSequentialTransform(
        tokenizer=tokenizer,
        max_len=max_candidate_length,
        max_history=None, pair_last=False)

    candidate_data = token_util.CandidateData(candidate, candidate_transform)
    candidate_token_ids_list, candidate_segment_ids_list, \
        candidate_input_masks_list = candidate_data.get_data()
    with torch.no_grad():
        embedding_data = {
            "candidate_input_ids": candidate_token_ids_list,
            "candidates_segment_ids": candidate_segment_ids_list,
            "candidate_input_masks": candidate_input_masks_list}
        embeddings = model(candidate_data=embedding_data,
                           eval=True,
                           get_embedding=True)
    return embeddings
