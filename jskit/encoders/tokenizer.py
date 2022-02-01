import torch
from torch.utils.data import Dataset
from tqdm import tqdm
import os

import pickle



class SelectionSequentialTransform(object):
  def __init__(self, tokenizer, max_len=128, max_history=10, pair_last=False):
    self.tokenizer = tokenizer
    self.max_len = max_len
    self.max_history = max_history
    self.pair_last = pair_last

  def __call__(self, texts):
    input_ids_list, segment_ids_list, input_masks_list, contexts_masks_list = [], [], [], []
    if self.max_history is not None:
      texts = texts[-self.max_history:]
    last_context = None
    if self.pair_last:
      last_context = texts[-1]
    for text in texts:
      tokenized_dict = self.tokenizer.encode_plus(text,
                                                  text_pair=last_context,
                                                  add_special_tokens=True,
                                                  max_length=self.max_len,
                                                  pad_to_max_length=True)
      input_ids, segment_ids, input_masks = tokenized_dict['input_ids'], tokenized_dict['token_type_ids'], \
                                            tokenized_dict['attention_mask']
      assert len(input_ids) == self.max_len
      assert len(segment_ids) == self.max_len
      assert len(input_masks) == self.max_len
      input_ids_list.append(input_ids)
      segment_ids_list.append(segment_ids)
      input_masks_list.append(input_masks)
    contexts_masks_list = [1] * len(input_ids_list)
    if self.max_history is not None:
      tokenized_dict = self.tokenizer.encode_plus('',
                                                  text_pair='',
                                                  add_special_tokens=True,
                                                  max_length=self.max_len,
                                                  pad_to_max_length=True)
      input_ids, segment_ids, input_masks = tokenized_dict['input_ids'], tokenized_dict['token_type_ids'], \
                                            tokenized_dict['attention_mask']
      for _ in range(self.max_history - len(texts)):
        input_ids_list.append(input_ids[:])
        segment_ids_list.append(segment_ids[:])
        input_masks_list.append(input_masks[:])
      contexts_masks_list += [0] * (self.max_history - len(texts))

    return input_ids_list, segment_ids_list, input_masks_list, contexts_masks_list

  def __str__(self) -> str:
    return 'maxlen%d_maxhistory%d_pairlast%s' % (self.max_len, self.max_history, str(self.pair_last))


class SelectionJoinTransform(object):
  def __init__(self, tokenizer, max_len=512, max_history=10):
    self.tokenizer = tokenizer
    self.max_len = max_len
    self.max_history = max_history

    self.cls_id = self.tokenizer.convert_tokens_to_ids(['[CLS]'])[0]
    self.sep_id = self.tokenizer.convert_tokens_to_ids(['[SEP]'])[0]
    self.pad_id = 0

  def __call__(self, texts):
    input_ids_list, segment_ids_list, input_masks_list = [], [], []

    for text in texts[::-1][:self.max_history]: 
      tokenized_dict = self.tokenizer.encode_plus(text,
                                                  text_pair=None,
                                                  add_special_tokens=True,
                                                  max_length=self.max_len,
                                                  pad_to_max_length=False)
      input_ids, input_masks = tokenized_dict['input_ids'], tokenized_dict['attention_mask']
      segment_ids = [1] * len(input_ids)
      if len(input_ids_list) > 0:
        input_ids = input_ids[1:]
        segment_ids = segment_ids[1:]
        input_masks = input_masks[1:]
      input_ids_list.extend(input_ids)
      segment_ids_list.extend(segment_ids)
      input_masks_list.extend(input_masks)

      if len(input_ids_list) >= self.max_len:
        input_ids_list = input_ids_list[:self.max_len - 1] + [self.sep_id]
        segment_ids_list = segment_ids_list[:self.max_len]
        input_masks_list = input_masks_list[:self.max_len]
        break
    input_ids_list += [self.pad_id] * (self.max_len - len(input_ids_list))
    segment_ids_list += [0] * (self.max_len - len(segment_ids_list))
    input_masks_list += [0] * (self.max_len - len(input_masks_list))

    assert len(input_ids_list) == self.max_len
    assert len(segment_ids_list) == self.max_len
    assert len(input_masks_list) == self.max_len

    return input_ids_list, segment_ids_list, input_masks_list

  def __str__(self) -> str:
    return '[join_str]maxlen%d_maxhis%d' % (self.max_len, self.max_history)


class SelectionResponelTransform(object):
  def __init__(self, tokenizer, max_len=128):
    self.tokenizer = tokenizer
    self.max_len = max_len

  def __call__(self, text):
    input_ids_list, segment_ids_list, input_masks_list, contexts_masks_list = [], [], [], []

    tokenized_dict = self.tokenizer.encode_plus(text,
                                                add_special_tokens=True,
                                                max_length=self.max_len,
                                                pad_to_max_length=True)
    input_ids, segment_ids, input_masks = tokenized_dict['input_ids'], tokenized_dict['token_type_ids'], \
                                          tokenized_dict['attention_mask']

    return input_ids, segment_ids, input_masks

  def __str__(self) -> str:
    return 'maxlen%d_maxhistory%d_pairlast%s' % (self.max_len, self.max_history, str(self.pair_last))




def pickle_dump(data, file_path):
  f_write = open(file_path, 'wb')
  pickle.dump(data, f_write, True)


def pickle_load(file_path):
  f_read = open(file_path, 'rb')
  data = pickle.load(f_read)

  return data

class SelectionDataset(Dataset):
  def __init__(self,contexts,candidates, context_transform, candidate_transform, sample_cnt=None):
    self.context_transform = context_transform
    self.candidate_transform = candidate_transform
    self.candidate_list=[]
    self.data_source = []
    self.transformed_data = {}

    for context,candidate in zip(contexts,candidates):
        lbl=1
        group = {
        'context': None,
        'candidates': [],
        'labels': []
        }
        group['candidates'].append(candidate)
        group['labels'].append(lbl)
        group['context'] = context
        self.data_source.append(group)
        if len(candidates)>1:
            lbl=0
            for value in candidates:
                if value not in candidate: 
                    group['candidates'].append(value)
                    group['labels'].append(lbl)
                    group['context'] = context
    for idx in tqdm(range(len(self.data_source))):
        self.__get_single_item__(idx)
    #   pickle_dump(self.transformed_data, cache_path)
    self.data_source = [0] * len(self.transformed_data)
    #   self.candidate_transform(candidate_list)
    def __len__(self):
        return len(self.data_source)

  def __len__(self):
    return len(self.data_source)

  def __getitem__(self, indices):
    if isinstance(indices, (tuple, list)):
      return [self.__get_single_item__(index) for index in indices]
    return self.__get_single_item__(indices)

  def __get_single_item__(self, index):
    if index in self.transformed_data:
      key_data = self.transformed_data[index]
      return key_data
    else:
      group = self.data_source[index]
      context, candidates, labels = group['context'], group['candidates'], group['labels']
      transformed_context = self.context_transform(context)  # [token_ids],[seg_ids],[masks]
      transformed_candidates = self.candidate_transform(candidates)  # [token_ids],[seg_ids],[masks]
      key_data = transformed_context, transformed_candidates, labels
      self.transformed_data[index] = key_data

      return key_data

  def batchify(self, batch):
    contexts_token_ids_list_batch, contexts_segment_ids_list_batch, contexts_input_masks_list_batch, contexts_masks_batch, \
    candidates_token_ids_list_batch, candidates_segment_ids_list_batch, candidates_input_masks_list_batch = [], [], [], [], [], [], []
    labels_batch = []
    for sample in batch:
      (contexts_token_ids_list, contexts_segment_ids_list, contexts_input_masks_list, contexts_masks_list), \
      (candidates_token_ids_list, candidates_segment_ids_list, candidates_input_masks_list, _) = sample[:2]

      contexts_token_ids_list_batch.append(contexts_token_ids_list)
      contexts_segment_ids_list_batch.append(contexts_segment_ids_list)
      contexts_input_masks_list_batch.append(contexts_input_masks_list)
      contexts_masks_batch.append(contexts_masks_list)

      candidates_token_ids_list_batch.append(candidates_token_ids_list)
      candidates_segment_ids_list_batch.append(candidates_segment_ids_list)
      candidates_input_masks_list_batch.append(candidates_input_masks_list)

      labels_batch.append(sample[-1])

    long_tensors = [contexts_token_ids_list_batch, contexts_segment_ids_list_batch, contexts_input_masks_list_batch,
                    contexts_masks_batch,
                    candidates_token_ids_list_batch, candidates_segment_ids_list_batch, candidates_input_masks_list_batch]

    contexts_token_ids_list_batch, contexts_segment_ids_list_batch, contexts_input_masks_list_batch, contexts_masks_batch, \
    candidates_token_ids_list_batch, candidates_segment_ids_list_batch, candidates_input_masks_list_batch = (
      torch.tensor(t, dtype=torch.long) for t in long_tensors)

    labels_batch = torch.tensor(labels_batch, dtype=torch.long)
    return contexts_token_ids_list_batch, contexts_segment_ids_list_batch, contexts_input_masks_list_batch, contexts_masks_batch, \
           candidates_token_ids_list_batch, candidates_segment_ids_list_batch, candidates_input_masks_list_batch, labels_batch

  def batchify_join_str(self, batch):
    contexts_token_ids_list_batch, contexts_segment_ids_list_batch, contexts_input_masks_list_batch, \
    candidates_token_ids_list_batch, candidates_segment_ids_list_batch, candidates_input_masks_list_batch = [], [], [], [], [], []
    labels_batch = []
    for sample in batch:
      (contexts_token_ids_list, contexts_segment_ids_list, contexts_input_masks_list), \
      (candidates_token_ids_list, candidates_segment_ids_list, candidates_input_masks_list, _) = sample[:2]

      contexts_token_ids_list_batch.append(contexts_token_ids_list)
      contexts_segment_ids_list_batch.append(contexts_segment_ids_list)
      contexts_input_masks_list_batch.append(contexts_input_masks_list)

      candidates_token_ids_list_batch.append(candidates_token_ids_list)
      candidates_segment_ids_list_batch.append(candidates_segment_ids_list)
      candidates_input_masks_list_batch.append(candidates_input_masks_list)

      labels_batch.append(sample[-1])

    long_tensors = [contexts_token_ids_list_batch, contexts_segment_ids_list_batch, contexts_input_masks_list_batch,
                    candidates_token_ids_list_batch, candidates_segment_ids_list_batch, candidates_input_masks_list_batch]

    contexts_token_ids_list_batch, contexts_segment_ids_list_batch, contexts_input_masks_list_batch, \
    candidates_token_ids_list_batch, candidates_segment_ids_list_batch, candidates_input_masks_list_batch = (
      torch.tensor(t, dtype=torch.long) for t in long_tensors)

    labels_batch = torch.tensor(labels_batch, dtype=torch.long)
    return contexts_token_ids_list_batch, contexts_segment_ids_list_batch, contexts_input_masks_list_batch, \
           candidates_token_ids_list_batch, candidates_segment_ids_list_batch, candidates_input_masks_list_batch, labels_batch


class SelectionData():
  def __init__(self, text,intent, context_transform, candidate_transform):
    self.context_transform = context_transform
    self.candidate_transform = candidate_transform
    self.candidate_list=[]
    self.data_source = []
    self.transformed_data = None
    context=text
    candidates= []
    labels= None
    for resp in intent:
        candidates.append(resp)
    transformed_context = self.context_transform(context)  # [token_ids],[seg_ids],[masks]
    transformed_candidates = self.candidate_transform(candidates)
    self.transformed_data = (transformed_context,transformed_candidates)
    # print(self.transformed_data) 

  def get_data(self):


    (contexts_token_ids_list, contexts_segment_ids_list, contexts_input_masks_list), \
    (candidates_token_ids_list, candidates_segment_ids_list, candidates_input_masks_list, _) = self.transformed_data[:2]


    long_tensors = [contexts_token_ids_list, contexts_segment_ids_list, contexts_input_masks_list,
                    candidates_token_ids_list, candidates_segment_ids_list, candidates_input_masks_list]

    contexts_token_ids_list_batch, contexts_segment_ids_list_batch, contexts_input_masks_list_batch, \
    candidates_token_ids_list_batch, candidates_segment_ids_list_batch, candidates_input_masks_list_batch = (
      torch.tensor(t, dtype=torch.long) for t in long_tensors)

    labels_batch = None
    return contexts_token_ids_list_batch, contexts_segment_ids_list_batch, contexts_input_masks_list_batch, \
           candidates_token_ids_list_batch, candidates_segment_ids_list_batch, candidates_input_masks_list_batch

class ContextData():
  def __init__(self, text, context_transform):
    self.context_transform = context_transform
    self.candidate_list=[]
    self.data_source = []
    self.transformed_data = None
    context=text

    transformed_context = self.context_transform(context)  # [token_ids],[seg_ids],[masks]
    self.transformed_data = (transformed_context)
    # print(self.transformed_data) 

  def get_data(self):
    # print(self.transformed_data)
    (contexts_token_ids_list, contexts_segment_ids_list, contexts_input_masks_list) = self.transformed_data
    long_tensors = [contexts_token_ids_list, contexts_segment_ids_list, contexts_input_masks_list]
    contexts_token_ids_list, contexts_segment_ids_list, contexts_input_masks_list= (
      torch.tensor(t, dtype=torch.long) for t in long_tensors)
    return contexts_token_ids_list, contexts_segment_ids_list, contexts_input_masks_list
    
class CandidateData():
  def __init__(self, candidates, candidate_transform):
    self.candidate_transform = candidate_transform
    self.candidate_list=[]
    self.transformed_data = None
    for resp in candidates:
        self.candidate_list.append(resp)
    transformed_candidate = self.candidate_transform(self.candidate_list)  # [token_ids],[seg_ids],[masks]
    self.transformed_data = (transformed_candidate)
    # print(self.transformed_data) 

  def get_data(self):
    # print(self.transformed_data)
    (candidate_token_ids_list, candidate_segment_ids_list, candidate_input_masks_list,_) = self.transformed_data
    long_tensors = [candidate_token_ids_list, candidate_segment_ids_list, candidate_input_masks_list]
    [candidate_token_ids_list, candidate_segment_ids_list, candidate_input_masks_list] = (torch.tensor(t, dtype=torch.long) for t in long_tensors)
    return [candidate_token_ids_list, candidate_segment_ids_list, candidate_input_masks_list]