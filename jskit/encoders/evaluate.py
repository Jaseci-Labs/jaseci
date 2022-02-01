import torch

from tokenizer import SelectionJoinTransform, SelectionSequentialTransform,SelectionData,ContextData,CandidateData
import configparser
config = configparser.ConfigParser()
config.read('config.cfg')

max_history = int(config['TRAIN_PARAMETERS']['MAX_HISTORY'])
max_contexts_length = int(config['TRAIN_PARAMETERS']['MAX_CONTEXTS_LENGTH'])
max_candidate_length = int(config['TRAIN_PARAMETERS']['MAX_RESPONSE_LENGTH'])


def get_inference(model,tokenizer,context,candidate):

    context_transform = SelectionJoinTransform(tokenizer=tokenizer, max_len=max_contexts_length,
                                            max_history=max_history)
    candidate_transform = SelectionSequentialTransform(tokenizer=tokenizer, max_len=max_candidate_length,
                                                max_history=None, pair_last=False)

    test_data = SelectionData(context,candidate,context_transform, candidate_transform)
    
    context_token_ids_list_batch, context_segment_ids_list_batch, context_input_masks_list_batch, \
    candidate_token_ids_list_batch, candidate_segment_ids_list_batch, candidate_input_masks_list_batch= test_data.get_data()
    with torch.no_grad():
      context_data={"context_input_ids":context_token_ids_list_batch,"context_segment_ids": context_segment_ids_list_batch,"context_input_masks": context_input_masks_list_batch}
      candidate_data={"candidate_input_ids":candidate_token_ids_list_batch,"candidates_segment_ids":candidate_segment_ids_list_batch,"candidate_input_masks": candidate_input_masks_list_batch}
      logits = model(context_data, candidate_data,eval=True)
    _, prediction = torch.max(logits, dim=1)
    print(candidate[prediction])
    return candidate[prediction]

def get_context_embedding(model,tokenizer,context):

    context_transform = SelectionJoinTransform(tokenizer=tokenizer, max_len=max_contexts_length,
                                            max_history=max_history)

    context_data = ContextData(context,context_transform)
    context_token_ids_list_batch, context_segment_ids_list_batch, context_input_masks_list_batch= context_data.get_data()
    with torch.no_grad():
      embedding_data={"context_input_ids":context_token_ids_list_batch,"context_segment_ids": context_segment_ids_list_batch,"context_input_masks": context_input_masks_list_batch}
      embeddings = model(context_data=embedding_data,eval=True,get_embedding=True)
    # print(embeddings)
    return embeddings
    
def get_candidate_embedding(model,tokenizer, candidate):

    candidate_transform = SelectionSequentialTransform(tokenizer=tokenizer, max_len=max_candidate_length,
                                                max_history=None, pair_last=False)

    candidate_data = CandidateData(candidate,candidate_transform)
    
    candidate_token_ids_list, candidate_segment_ids_list, candidate_input_masks_list= candidate_data.get_data()
    with torch.no_grad():
      embedding_data={"candidate_input_ids":candidate_token_ids_list,"candidates_segment_ids": candidate_segment_ids_list,"candidate_input_masks": candidate_input_masks_list}
      embeddings = model(candidate_data=embedding_data,eval=True,get_embedding=True)
    # print(embeddings)
    return embeddings