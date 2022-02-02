
import torch
import torch.nn as nn
from transformers import BertModel
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



class BiEncoderShared(nn.Module):
  def __init__(self, config,model_name, *inputs, **kwargs):
    super(BiEncoderShared, self).__init__()
    self.cont_cand_model =BertModel.from_pretrained(model_name)
    try:
      self.dropout = nn.Dropout(config.hidden_dropout_prob)
      self.context_fc = nn.Linear(config.hidden_size, 64)
      self.candidate_fc = nn.Linear(config.hidden_size, 64)
    except:
      self.dropout = nn.Dropout(config.dropout)
      self.context_fc = nn.Linear(config.dim, 64)
      self.candidate_fc = nn.Linear(config.dim, 64)

  def forward(self, context_data=None,candidate_data=None, labels=None,eval=False,get_embedding=False):
    ## only select the first candidate (whose lbl==1)

    if get_embedding and context_data is not None:
        context_input_ids,context_segment_ids, context_input_masks =context_data["context_input_ids"], context_data['context_segment_ids'], context_data["context_input_masks"]
        context_vec = self.cont_cand_model(context_input_ids.unsqueeze(0), context_input_masks.unsqueeze(0), context_segment_ids.unsqueeze(0))[-1]  # [bs,dim]
        context_vec = self.context_fc(self.dropout(context_vec))
        context_vec = F.normalize(context_vec, 2, -1)
        return context_vec
    elif get_embedding and candidate_data is not None:
        candidates_input_ids, candidates_segment_ids,candidates_input_masks =candidate_data["candidate_input_ids"],candidate_data['candidates_segment_ids'],candidate_data["candidate_input_masks"]
        res_cnt, seq_length = candidates_input_ids.shape
        batch_size=1
        candidates_input_ids = candidates_input_ids.view(-1, seq_length)
        candidates_input_masks = candidates_input_masks.view(-1, seq_length)
        candidates_segment_ids = candidates_segment_ids.view(-1, seq_length)
        candidates_vec = self.cont_cand_model(candidates_input_ids, candidates_input_masks, candidates_segment_ids)[-1]  # [bs,dim]
        candidates_vec = candidates_vec.view(batch_size, res_cnt, -1)
        candidates_vec = self.candidate_fc(self.dropout(candidates_vec))
        candidates_vec = F.normalize(candidates_vec, 2, -1)
        return candidates_vec
    context_input_ids,context_segment_ids, context_input_masks =context_data["context_input_ids"], context_data['context_segment_ids'], context_data["context_input_masks"]
    candidates_input_ids, candidates_segment_ids,candidates_input_masks =candidate_data["candidate_input_ids"],candidate_data['candidates_segment_ids'],candidate_data["candidate_input_masks"]
    if labels is not None:
      candidates_input_ids = candidates_input_ids[:, 0, :].unsqueeze(1)
      candidates_segment_ids = candidates_segment_ids[:, 0, :].unsqueeze(1)
      candidates_input_masks = candidates_input_masks[:, 0, :].unsqueeze(1)


    context_vec = self.cont_cand_model(context_input_ids, context_input_masks, context_segment_ids)[-1] 
    batch_size, res_cnt, seq_length = candidates_input_ids.shape
    candidates_input_ids = candidates_input_ids.view(-1, seq_length)
    candidates_input_masks = candidates_input_masks.view(-1, seq_length)
    candidates_segment_ids = candidates_segment_ids.view(-1, seq_length)


    candidates_vec = self.cont_cand_model(candidates_input_ids, candidates_input_masks, candidates_segment_ids)[-1]  # [bs,dim]
    candidates_vec = candidates_vec.view(batch_size, res_cnt, -1)

    context_vec = self.context_fc(self.dropout(context_vec))
    context_vec = F.normalize(context_vec, 2, -1)

    candidates_vec = self.candidate_fc(self.dropout(candidates_vec))
    candidates_vec = F.normalize(candidates_vec, 2, -1)

    if labels is not None:
      candidates_vec = candidates_vec.squeeze(1)
      dot_product = torch.matmul(context_vec, candidates_vec.t())  # [bs, bs]
      mask = torch.eye(context_input_ids.size(0)).to(context_input_ids.device)
      loss = F.log_softmax(dot_product * 5, dim=-1) * mask
      loss = (-loss.sum(dim=1)).mean()

      return loss
    else:
      context_vec = context_vec.unsqueeze(1)
      dot_product = torch.matmul(context_vec, candidates_vec.permute(0, 2, 1))  # take this as logits
      dot_product.squeeze_(1)
      cos_similarity = (dot_product + 1) / 2
      return cos_similarity

