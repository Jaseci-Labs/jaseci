
import torch
import torch.nn as nn
from transformers import PreTrainedModel, AutoModel
import torch.nn.functional as F


def dot_attention(q, k, v, v_mask=None, dropout=None):
    attention_weights = torch.matmul(q, k.transpose(-1, -2))
    if v_mask is not None:
        extended_v_mask = (1.0 - v_mask.unsqueeze(1)) * -100000.0
        attention_weights += extended_v_mask
    attention_weights = F.softmax(attention_weights, -1)
    if dropout is not None:
        attention_weights = dropout(attention_weights)
    output = torch.matmul(attention_weights, v)
    return output


class PolyEncoderModelShared(nn.Module):
    def __init__(self, config, model_name, shared: bool, *inputs, **kwargs):
        super(PolyEncoderModelShared, self).__init__()
        if shared is True:
            self.cont_model = AutoModel.from_pretrained(model_name)
            self.cand_model = self.cont_model
        else:
            self.cont_model = AutoModel.from_pretrained(model_name)
            self.cand_model = AutoModel.from_pretrained(model_name)
        self.vec_dim = 64

        self.poly_m = int(kwargs['poly_m'])
        self.poly_code_embeddings = nn.Embedding(
            self.poly_m + 1, config.hidden_size)
        try:
            self.dropout = nn.Dropout(config.hidden_dropout_prob)
            self.context_fc = nn.Linear(config.hidden_size, self.vec_dim)
            self.candidate_fc = nn.Linear(config.hidden_size, self.vec_dim)
        except Exception:
            self.dropout = nn.Dropout(config.dropout)
            self.context_fc = nn.Linear(config.dim, self.vec_dim)
            self.candidate_fc = nn.Linear(config.dim, self.vec_dim)

    def forward(self, context_data=None, candidate_data=None, labels=None,
                eval=False, get_embedding=False):
        if get_embedding and context_data is not None:
            context_input_ids, context_segment_ids, \
                context_input_masks = context_data[
                    "context_input_ids"], \
                context_data['context_segment_ids'], \
                context_data["context_input_masks"]
            res_cnt, seq_length = context_input_ids.unsqueeze(0).shape
            state_vecs = self.cont_model(context_input_ids.unsqueeze(0),
                                         context_input_masks.unsqueeze(0),
                                         context_segment_ids.unsqueeze(0))[0]
            poly_code_ids = torch.arange(
                self.poly_m, dtype=torch.long, device=context_input_ids.device)
            poly_code_ids += 1
            poly_code_ids = poly_code_ids.unsqueeze(0).expand(1, self.poly_m)
            poly_codes = self.poly_code_embeddings(poly_code_ids)
            context_vec = dot_attention(
                poly_codes, state_vecs, state_vecs,
                context_input_masks.unsqueeze(0), self.dropout)
            context_vec = self.context_fc(self.dropout(context_vec))
            context_vec = F.normalize(context_vec, 2, -1)
            return context_vec
        elif get_embedding and candidate_data is not None:
            candidates_input_ids, candidates_segment_ids, \
                candidates_input_masks = candidate_data[
                    "candidate_input_ids"], \
                candidate_data['candidates_segment_ids'], \
                candidate_data["candidate_input_masks"]
            res_cnt, seq_length = candidates_input_ids.shape
            batch_size = 1
            candidates_input_ids = candidates_input_ids.view(-1, seq_length)
            candidates_input_masks = candidates_input_masks.view(
                -1, seq_length)
            candidates_segment_ids = candidates_segment_ids.view(
                -1, seq_length)
            state_vecs = self.cand_model(
                candidates_input_ids, candidates_input_masks,
                candidates_segment_ids)[0]
            poly_code_ids = torch.zeros(
                batch_size * res_cnt, 1, dtype=torch.long,
                device=candidates_input_ids.device)
            poly_codes = self.poly_code_embeddings(poly_code_ids)
            candidates_vec = dot_attention(
                poly_codes, state_vecs, state_vecs, candidates_input_ids,
                self.dropout)
            candidates_vec = candidates_vec.view(batch_size, res_cnt, -1)
            candidates_vec = self.context_fc(self.dropout(candidates_vec))
            candidates_vec = F.normalize(candidates_vec, 2, -1)
            return candidates_vec
        context_input_ids, context_segment_ids, \
            context_input_masks = context_data["context_input_ids"], \
            context_data['context_segment_ids'], \
            context_data["context_input_masks"]
        candidates_input_ids, candidates_segment_ids, \
            candidates_input_masks = candidate_data["candidate_input_ids"], \
            candidate_data['candidates_segment_ids'], \
            candidate_data["candidate_input_masks"]
        # only select the first candidate (whose lbl==1)
        if labels is not None:
            candidates_input_ids = candidates_input_ids[:, 0, :].unsqueeze(1)
            candidates_segment_ids = candidates_segment_ids[:, 0, :].unsqueeze(
                1)
            candidates_input_masks = candidates_input_masks[:, 0, :].unsqueeze(
                1)

        state_vecs = self.cont_model(
            context_input_ids, context_input_masks, context_segment_ids)[0]
        batch_size, res_cnt, seq_length = candidates_input_ids.shape
        poly_code_ids = torch.arange(
            self.poly_m, dtype=torch.long, device=context_input_ids.device)
        poly_code_ids += 1
        poly_code_ids = poly_code_ids.unsqueeze(
            0).expand(batch_size, self.poly_m)
        poly_codes = self.poly_code_embeddings(poly_code_ids)
        context_vecs = dot_attention(
            poly_codes, state_vecs, state_vecs,
            context_input_masks, self.dropout)

        # candidate encoder
        candidates_input_ids = candidates_input_ids.view(-1, seq_length)
        candidates_input_masks = candidates_input_masks.view(-1, seq_length)
        candidates_segment_ids = candidates_segment_ids.view(-1, seq_length)

        state_vecs = self.cand_model(
            candidates_input_ids, candidates_input_masks,
            candidates_segment_ids)[0]  # [bs, length, dim]
        poly_code_ids = torch.zeros(
            batch_size * res_cnt, 1, dtype=torch.long,
            device=context_input_ids.device)
        poly_codes = self.poly_code_embeddings(poly_code_ids)
        candidates_vec = dot_attention(
            poly_codes, state_vecs, state_vecs,
            candidates_input_masks, self.dropout)
        candidates_vec = candidates_vec.view(batch_size, res_cnt, -1)

        # Norm here first, which is equivalent to getting context_vec
        #  and candidate_vec in some way
        context_vecs = self.context_fc(self.dropout(context_vecs))
        context_vecs = F.normalize(context_vecs, 2, -1)  # [bs, m, dim]
        candidates_vec = self.candidate_fc(self.dropout(candidates_vec))
        candidates_vec = F.normalize(candidates_vec, 2, -1)

        # poly final context vector aggregation
        if labels is not None:
            candidates_vec = candidates_vec.view(
                1, batch_size, -1).expand(batch_size, batch_size, self.vec_dim)
        final_context_vec = dot_attention(
            candidates_vec, context_vecs, context_vecs, None, self.dropout)
        # [bs, res_cnt, dim], res_cnt==bs when training
        final_context_vec = F.normalize(final_context_vec, 2, -1)

        # [bs, res_cnt], res_cnt==bs when training
        dot_product = torch.sum(final_context_vec * candidates_vec, -1)
        if labels is not None:
            mask = torch.eye(context_input_ids.size(0)).to(
                context_input_ids.device)
            loss = F.log_softmax(dot_product * 5, dim=-1) * mask
            loss = (-loss.sum(dim=1)).mean()

            return loss
        else:
            cos_similarity = (dot_product + 1) / 2
            return cos_similarity


class BiEncoder(PreTrainedModel):
    def __init__(self, config, *inputs, **kwargs):
        super().__init__(config, *inputs, **kwargs)
        # if shared is true it creates only one model (Siamese type)
        if kwargs['shared'] is True:
            self.cont_bert = kwargs['cont_bert']
            self.cand_bert = self.cont_bert
        else:
            self.cont_bert = kwargs['cont_bert']
            self.cand_bert = kwargs['cand_bert']
        self.input_size = None
        self.l_type = kwargs['loss_type']
        self.l_func = kwargs['loss_function']

    def loss_func(self, candidate_vec, context_vec, labels, l_type='cos',
                  l_func='MSE'):
        candidate_vec = candidate_vec.squeeze(1)
        labels = labels.squeeze(1)
        if l_type == 'dot':
            dot_product = torch.matmul(
                context_vec, candidate_vec.t())
            mask = torch.eye(self.input_size).to(
                candidate_vec.device)
            dot_product = 1 - F.log_softmax(dot_product, dim=-1) * mask
            if l_func == 'contrastive':
                dot_product = dot_product.mean(dim=-1)
                loss = 0.5 * (labels.float() * dot_product.pow(2) +
                              (1 - labels).float() *
                              F.relu(0.5 - dot_product).pow(2))
                loss = loss.mean()
            else:
                loss_fnct = nn.MSELoss()
                loss = loss_fnct(dot_product.mean(dim=-1), target=labels)
        else:
            cos = nn.CosineSimilarity()
            if l_func == 'contrastive':
                loss_angle = 1 - cos(context_vec, candidate_vec)
                loss = 0.5 * (labels.float() * loss_angle.pow(2) +
                              (1 - labels).float() *
                              F.relu(0.5 - loss_angle).pow(2))
                loss = loss.mean(dim=-1)
            else:
                loss_angle = cos(context_vec, candidate_vec)
                loss_fnct = nn.MSELoss()
                loss = loss_fnct(loss_angle, target=labels)
        return loss

    def forward(self, context_input_ids=None, context_input_masks=None,
                candidate_input_ids=None, candidate_input_masks=None,
                labels=None, get_embedding=None, mode="train", pooling="mean"):
        # only select the first candidate (whose lbl==1)
        # if labels is not None:
        #   candidate_input_ids = candidate_input_ids[:, 0, :].unsqueeze(1)
        #   candidate_input_masks = candidate_input_masks[:, 0, :].unsqueeze(1)
        # gets the context embedding
        if get_embedding == "context" or mode == "train" or mode == "eval":
            self.input_size = context_input_ids.size(0)
            context_vec = self.cont_bert(context_input_ids,
                                         context_input_masks)[0]
            if pooling == "mean":
                # Mean pooling
                output_vectors = []
                input_mask_expanded = context_input_masks.unsqueeze(
                    -1).expand(context_vec.size()).float()
                sum_embeddings = torch.sum(
                    context_vec * input_mask_expanded, 1)
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
            candidate_vec = self.cand_bert(candidate_input_ids,
                                           candidate_input_masks)[0]
            if pooling == "mean":
                # Mean pooling
                output_vectors = []
                input_mask_expanded = candidate_input_masks.unsqueeze(
                    -1).expand(candidate_vec.size()).float()
                sum_embeddings = torch.sum(
                    candidate_vec * input_mask_expanded, 1)
                sum_mask = input_mask_expanded.sum(1)
                sum_mask = torch.clamp(sum_mask, min=1e-9)
                output_vectors.append(sum_embeddings / sum_mask)
                candidate_vec = torch.cat(output_vectors, 1)
                candidate_vec = candidate_vec.view(batch_size, res_cnt, -1)
                if get_embedding == "candidate":
                    return candidate_vec
        if labels is not None and mode == "train":
            return self.loss_func(candidate_vec=candidate_vec,
                                  context_vec=context_vec, labels=labels,
                                  l_type=self.l_type, l_func=self.l_func)
