import torch
from torch.utils.data import DataLoader
from . import tokenizer as token_util


def get_inference(model, tokenizer, contexts, candidates, train_config):
    context_transform = token_util.SelectionJoinTransform(
        tokenizer=tokenizer, max_len=train_config["max_contexts_length"]
    )
    candidate_transform = token_util.SelectionSequentialTransform(
        tokenizer=tokenizer, max_len=train_config["max_candidate_length"]
    )
    labels = [0] * len(candidates)
    test_data = token_util.SelectionDataset(
        contexts=contexts,
        candidates=candidates,
        context_transform=context_transform,
        candidate_transform=candidate_transform,
        mode="eval",
        labels=labels,
    )
    val_dataloader = DataLoader(
        test_data,
        batch_size=train_config["eval_batch_size"],
        collate_fn=test_data.batchify_join_str,
        shuffle=False,
    )
    results = []
    for step, batch in enumerate(val_dataloader, start=1):
        batch = tuple(t.to(train_config["device"]) for t in batch)
        (
            context_token_ids_list_batch,
            context_input_masks_list_batch,
            candidate_token_ids_list_batch,
            candidate_input_masks_list_batch,
            _,
        ) = batch
        with torch.no_grad():
            logits = model(
                context_token_ids_list_batch,
                context_input_masks_list_batch,
                candidate_token_ids_list_batch,
                candidate_input_masks_list_batch,
                mode="eval",
            )
        _, prediction = torch.max(logits, dim=-1)
        prediction = prediction.tolist()
        if isinstance(prediction, list):
            for pred in prediction:
                results.append(candidates[pred])
        else:
            results.append(candidates[prediction])
    return results


# function provides embedding for context and candidate
def get_embeddings(model, tokenizer, text_data, train_config, embed_type="context"):
    if embed_type == "context":
        context_transform = token_util.SelectionJoinTransform(
            tokenizer=tokenizer, max_len=train_config["max_contexts_length"]
        )
        context_data = token_util.EvalDataset(
            text_data,
            context_transform=context_transform,
            candidate_transform=None,
            mode=embed_type,
        )
    else:
        candidate_transform = token_util.SelectionSequentialTransform(
            tokenizer=tokenizer, max_len=train_config["max_candidate_length"]
        )
        context_data = token_util.EvalDataset(
            text_data,
            context_transform=None,
            candidate_transform=candidate_transform,
            mode=embed_type,
        )
    dataloader = DataLoader(
        context_data,
        batch_size=train_config["eval_batch_size"],
        collate_fn=context_data.eval_str,
        shuffle=False,
        num_workers=0,
    )

    for step, batch in enumerate(dataloader, start=1):
        batch = tuple(t.to(train_config["device"]) for t in batch)
        token_ids_batch, input_masks_batch = batch

        with torch.no_grad():
            if embed_type == "context":
                embeddings = model(
                    context_input_ids=token_ids_batch,
                    context_input_masks=input_masks_batch,
                    get_embedding=embed_type,
                    mode="get_embed",
                )
            else:
                embeddings = model(
                    candidate_input_ids=token_ids_batch,
                    candidate_input_masks=input_masks_batch,
                    get_embedding=embed_type,
                    mode="get_embed",
                )

    return embeddings.squeeze(0).detach().tolist()
