import torch
import torch.nn as nn
from transformers import PreTrainedModel
import torch.nn.functional as F


class PolyEncoder(PreTrainedModel):
    def __init__(self, config, *inputs, **kwargs):
        super().__init__(config, *inputs, **kwargs)
        if kwargs["shared"] is True:
            self.cont_bert = kwargs["cont_bert"]
            self.cand_bert = self.cont_bert
        else:
            self.cont_bert = kwargs["cont_bert"]
            self.cand_bert = kwargs["cand_bert"]
        self.input_size = None
        self.l_type = kwargs["loss_type"]
        self.l_func = kwargs["loss_function"]
        self.poly_m = kwargs["poly_m"]
        self.poly_code_embeddings = nn.Embedding(self.poly_m, config.hidden_size)
        # https://github.com/facebookresearch/ParlAI/blob/master/parlai/agents/transformer/polyencoder.py#L355 # noqa
        torch.nn.init.normal_(
            self.poly_code_embeddings.weight, config.hidden_size**-0.5
        )

    def dot_attention(self, q, k, v):
        # q: [bs, poly_m, dim] or [bs, res_cnt, dim]
        # k=v: [bs, length, dim] or [bs, poly_m, dim]
        attn_weights = torch.matmul(q, k.transpose(2, 1))  # [bs, poly_m, length]
        attn_weights = F.softmax(attn_weights, -1)
        output = torch.matmul(attn_weights, v)  # [bs, poly_m, dim]
        return output

    def forward(
        self,
        context_input_ids=None,
        context_input_masks=None,
        candidate_input_ids=None,
        candidate_input_masks=None,
        labels=None,
        get_embedding=None,
        mode="train",
        pooling="mean",
    ):
        if get_embedding == "context" or mode == "train" or mode == "eval":
            # batch_size, res_cnt, seq_length = context_input_ids.shape
            # context encoder
            context_vec = self.cont_bert(context_input_ids, context_input_masks)[0]
            if pooling == "mean":
                poly_code_ids = torch.arange(self.poly_m, dtype=torch.long).to(
                    context_input_ids.device
                )
                poly_code_ids = poly_code_ids.unsqueeze(0).expand(
                    context_input_ids.shape[0], self.poly_m
                )
                poly_codes = self.poly_code_embeddings(
                    poly_code_ids
                )  # [bs, poly_m, dim]
                context_vec = self.dot_attention(
                    poly_codes, context_vec, context_vec
                )  # [bs, poly_m, dim]
                if get_embedding == "context":
                    return context_vec
        if get_embedding == "candidate" or mode == "train" or mode == "eval":
            batch_size, res_cnt, seq_length = candidate_input_masks.shape
            candidate_input_ids = candidate_input_ids.view(-1, seq_length)
            candidate_input_masks = candidate_input_masks.view(-1, seq_length)
            candidate_vec = self.cand_bert(candidate_input_ids, candidate_input_masks)[
                0
            ]
            if pooling == "mean":
                # Mean pooling
                output_vectors = []
                input_mask_expanded = (
                    candidate_input_masks.unsqueeze(-1)
                    .expand(candidate_vec.size())
                    .float()
                )
                sum_embeddings = torch.sum(candidate_vec * input_mask_expanded, 1)
                sum_mask = input_mask_expanded.sum(1)
                sum_mask = torch.clamp(sum_mask, min=1e-9)
                output_vectors.append(sum_embeddings / sum_mask)
                candidate_vec = torch.cat(output_vectors, 1)
                candidate_vec = candidate_vec.view(batch_size, res_cnt, -1)
                if get_embedding == "candidate":
                    return candidate_vec
        # merge
        if labels is not None:
            # we are recycling candidates for faster training
            # we repeat candidates for batch_size times to simulate test phase
            # so that every context is paired with batch_size candidates
            candidate_vec = candidate_vec.permute(1, 0, 2)  # [1, bs, dim]
            candidate_vec = candidate_vec.expand(
                batch_size, batch_size, candidate_vec.shape[2]
            )
            context_vec = self.dot_attention(
                candidate_vec, context_vec, context_vec
            ).squeeze()
            dot_product = (context_vec * candidate_vec).sum(-1)  # [bs, bs]
            mask = torch.eye(batch_size).to(context_input_ids.device)  # [bs, bs]
            dot_product = 1 - F.log_softmax(dot_product, dim=-1) * mask
            # loss = (-loss.sum(dim=1)).mean()
            loss_fnct = nn.MSELoss()
            loss = loss_fnct(dot_product.mean(dim=-1), target=labels.squeeze(1))
            return loss
        else:
            context_vec = self.dot_attention(
                candidate_vec, context_vec, context_vec
            )  # [bs, res_cnt, dim]
            dot_product = (context_vec * candidate_vec).sum(-1)
            return dot_product


class BiEncoder(PreTrainedModel):
    def __init__(self, config, *inputs, **kwargs):
        super().__init__(config, *inputs, **kwargs)
        # if shared is true it creates only one model (Siamese type)
        if kwargs["shared"] is True:
            self.cont_bert = kwargs["cont_bert"]
            self.cand_bert = self.cont_bert
        else:
            self.cont_bert = kwargs["cont_bert"]
            self.cand_bert = kwargs["cand_bert"]
        self.input_size = None
        self.l_type = kwargs["loss_type"]
        self.l_func = kwargs["loss_function"]

    def loss_func(self, candidate_vec, context_vec, labels, l_type="cos", l_func="MSE"):
        candidate_vec = candidate_vec.squeeze(1)
        labels = labels.squeeze(1)
        if l_type == "dot":
            dot_product = torch.matmul(context_vec, candidate_vec.t())
            mask = torch.eye(self.input_size).to(candidate_vec.device)
            dot_product = 1 - F.log_softmax(dot_product, dim=-1) * mask
            if l_func == "contrastive":
                dot_product = dot_product.mean(dim=-1)
                loss = 0.5 * (
                    labels.float() * dot_product.pow(2)
                    + (1 - labels).float() * F.relu(0.5 - dot_product).pow(2)
                )
                loss = loss.mean()
            else:
                loss_fnct = nn.MSELoss()
                loss = loss_fnct(dot_product.mean(dim=-1), target=labels)
        else:
            cos = nn.CosineSimilarity()
            if l_func == "contrastive":
                loss_angle = 1 - cos(context_vec, candidate_vec)
                loss = 0.5 * (
                    labels.float() * loss_angle.pow(2)
                    + (1 - labels).float() * F.relu(0.5 - loss_angle).pow(2)
                )
                loss = loss.mean(dim=-1)
            else:
                loss_angle = cos(context_vec, candidate_vec)
                loss_fnct = nn.MSELoss()
                loss = loss_fnct(loss_angle, target=labels)
        return loss

    def forward(
        self,
        context_input_ids=None,
        context_input_masks=None,
        candidate_input_ids=None,
        candidate_input_masks=None,
        labels=None,
        get_embedding=None,
        mode="train",
        pooling="mean",
    ):
        # only select the first candidate (whose lbl==1)
        # if labels is not None:
        #   candidate_input_ids = candidate_input_ids[:, 0, :].unsqueeze(1)
        #   candidate_input_masks = candidate_input_masks[:, 0, :].unsqueeze(1)
        # gets the context embedding
        if get_embedding == "context" or mode == "train" or mode == "eval":
            self.input_size = context_input_ids.size(0)
            context_vec = self.cont_bert(context_input_ids, context_input_masks)[0]
            if pooling == "mean":
                # Mean pooling
                output_vectors = []
                input_mask_expanded = (
                    context_input_masks.unsqueeze(-1).expand(context_vec.size()).float()
                )
                sum_embeddings = torch.sum(context_vec * input_mask_expanded, 1)
                sum_mask = input_mask_expanded.sum(1)
                sum_mask = torch.clamp(sum_mask, min=1e-9)
                output_vectors.append(sum_embeddings / sum_mask)
                context_vec = torch.cat(output_vectors, 1)
                if get_embedding == "context":
                    return context_vec
        # gets the candidate embedding
        if get_embedding == "candidate" or mode == "train" or mode == "eval":
            batch_size, res_cnt, seq_length = candidate_input_ids.shape
            candidate_input_ids = candidate_input_ids.view(-1, seq_length)
            candidate_input_masks = candidate_input_masks.view(-1, seq_length)
            candidate_vec = self.cand_bert(candidate_input_ids, candidate_input_masks)[
                0
            ]
            if pooling == "mean":
                # Mean pooling
                output_vectors = []
                input_mask_expanded = (
                    candidate_input_masks.unsqueeze(-1)
                    .expand(candidate_vec.size())
                    .float()
                )
                sum_embeddings = torch.sum(candidate_vec * input_mask_expanded, 1)
                sum_mask = input_mask_expanded.sum(1)
                sum_mask = torch.clamp(sum_mask, min=1e-9)
                output_vectors.append(sum_embeddings / sum_mask)
                candidate_vec = torch.cat(output_vectors, 1)
                candidate_vec = candidate_vec.view(batch_size, res_cnt, -1)
                if get_embedding == "candidate":
                    return candidate_vec
        if labels is not None and mode == "train":
            return self.loss_func(
                candidate_vec=candidate_vec,
                context_vec=context_vec,
                labels=labels,
                l_type=self.l_type,
                l_func=self.l_func,
            )
