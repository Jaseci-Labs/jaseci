import torch
from torch.utils.data import Dataset


# this class transforms data in required training format
# and inference for text and tokens
class SelectionDataset(Dataset):
    def __init__(
        self,
        contexts,
        candidates,
        context_transform,
        candidate_transform,
        labels=None,
        mode="train",
    ):
        self.context_transform = context_transform
        self.candidate_transform = candidate_transform
        self.data_source = []
        self.mode = mode
        if mode == "eval":
            for text in contexts:
                group = {"context": None, "candidates": [], "labels": []}
                for cand in candidates:
                    group["candidates"].append(cand)
                    # below label is 0 for all,used for help in inference
                    group["labels"].append(0)
                    group["context"] = [text]
                self.data_source.append(group)
        else:
            group = {"context": None, "candidates": [], "labels": []}
            for text, cand, lbl in zip(contexts, candidates, labels):
                group = {"context": None, "candidates": [], "labels": []}
                # below code is to combine positive and negetive sample
                # if lbl == 1 and len(group['candidates']) > 0:
                #     self.data_source.append(group)
                #     group = {
                #         'context': None,
                #         'candidates': [],
                #         'labels': []
                #     }
                group["candidates"].append(cand)
                group["labels"].append(lbl)
                group["context"] = [text]
                # if len(group['candidates']) > 0:
                self.data_source.append(group)
        group = {"context": None, "candidates": [], "labels": []}
        if len(self.data_source) < 2 and mode != "eval":
            group["context"] = ["This is sample text"]
            group["candidates"].append("sampletext")
            group["labels"].append(1)
            if len(candidates) > 1:
                group["context"] = ["This is a sample text"]
                group["candidates"].append("notsampletext")
                group["labels"].append(0)
            self.data_source.append(group)

    def __len__(self):
        return len(self.data_source)

    def __getitem__(self, index):
        group = self.data_source[index]
        context, candidates, labels = (
            group["context"],
            group["candidates"],
            group["labels"],
        )

        transformed_context = self.context_transform(
            context
        )  # [token_ids],[seg_ids],[masks]
        transformed_candidates = self.candidate_transform(
            candidates
        )  # [token_ids],[seg_ids],[masks]
        ret = transformed_context, transformed_candidates, labels

        return ret

    def batchify_join_str(self, batch):

        (
            contexts_token_ids_list_batch,
            contexts_input_masks_list_batch,
            candidates_token_ids_list_batch,
            candidates_input_masks_list_batch,
        ) = ([], [], [], [])
        labels_batch = []
        for sample in batch:
            (contexts_token_ids_list, contexts_input_masks_list), (
                candidates_token_ids_list,
                candidates_input_masks_list,
            ) = sample[:2]

            contexts_token_ids_list_batch.append(contexts_token_ids_list)
            contexts_input_masks_list_batch.append(contexts_input_masks_list)

            candidates_token_ids_list_batch.append(candidates_token_ids_list)
            candidates_input_masks_list_batch.append(candidates_input_masks_list)

            labels_batch.append(sample[-1])

        long_tensors = [
            contexts_token_ids_list_batch,
            contexts_input_masks_list_batch,
            candidates_token_ids_list_batch,
            candidates_input_masks_list_batch,
        ]

        (
            contexts_token_ids_list_batch,
            contexts_input_masks_list_batch,
            candidates_token_ids_list_batch,
            candidates_input_masks_list_batch,
        ) = (torch.tensor(t, dtype=torch.long) for t in long_tensors)

        labels_batch = torch.tensor(labels_batch, dtype=torch.float)
        return (
            contexts_token_ids_list_batch,
            contexts_input_masks_list_batch,
            candidates_token_ids_list_batch,
            candidates_input_masks_list_batch,
            labels_batch,
        )


# this class transforms data to generate embeddings
class EvalDataset(Dataset):
    def __init__(
        self, texts, context_transform=None, candidate_transform=None, mode="context"
    ):
        self.context_transform = context_transform
        self.candidate_transform = candidate_transform
        self.data_source = []
        self.mode = mode
        group = {"text": []}
        if mode == "context":
            group["text"].append(texts)
        else:
            for text in texts:
                group["text"].append(text)
        self.data_source.append(group)

    def __len__(self):
        return len(self.data_source)

    def __getitem__(self, index):
        group = self.data_source[index]
        text = group["text"]
        if self.mode == "context":
            transformed_text = self.context_transform(text)  # [token_ids],[masks]
        else:
            transformed_text = self.candidate_transform(text)  # [token_ids],[masks]

        return transformed_text

    def eval_str(self, batch):
        token_ids_list_batch, input_masks_list_batch = [], []
        for sample in batch:
            token_ids_list, input_masks_list = sample
            token_ids_list_batch.append(token_ids_list)
            input_masks_list_batch.append(input_masks_list)

        long_tensors = [token_ids_list_batch, input_masks_list_batch]
        token_ids_list_batch, input_masks_list_batch = (
            torch.tensor(t, dtype=torch.long) for t in long_tensors
        )
        return token_ids_list_batch, input_masks_list_batch


# this class is for creating token data for candidate
class SelectionSequentialTransform(object):
    def __init__(self, tokenizer, max_len):
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __call__(self, texts):
        input_ids_list, input_masks_list = [], []
        for text in texts:
            tokenized_dict = self.tokenizer.encode_plus(
                text, padding="max_length", max_length=self.max_len, truncation=True
            )
            input_ids, input_masks = (
                tokenized_dict["input_ids"],
                tokenized_dict["attention_mask"],
            )
            assert len(input_ids) == self.max_len
            assert len(input_masks) == self.max_len
            input_ids_list.append(input_ids)
            input_masks_list.append(input_masks)
        return input_ids_list, input_masks_list


# this class is for creating token data for context
class SelectionJoinTransform(object):
    def __init__(self, tokenizer, max_len):
        self.tokenizer = tokenizer
        self.max_len = max_len

        self.cls_id = self.tokenizer.convert_tokens_to_ids("[CLS]")
        self.sep_id = self.tokenizer.convert_tokens_to_ids("[SEP]")
        self.pad_id = 0

    def __call__(self, texts):
        # another option is to use [SEP], but here we follow the discussion at:
        # https://github.com/facebookresearch/ParlAI/issues/2306#issuecomment-599180186
        context = "\n".join(texts)
        tokenized_dict = self.tokenizer.encode_plus(context)
        input_ids, input_masks = (
            tokenized_dict["input_ids"],
            tokenized_dict["attention_mask"],
        )
        input_ids = input_ids[-self.max_len :]
        input_ids[0] = self.cls_id
        input_masks = input_masks[-self.max_len :]
        input_ids += [self.pad_id] * (self.max_len - len(input_ids))
        input_masks += [0] * (self.max_len - len(input_masks))
        assert len(input_ids) == self.max_len
        assert len(input_masks) == self.max_len

        return input_ids, input_masks
