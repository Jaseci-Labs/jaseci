import torch
from torch import nn
from torch.nn.utils.rnn import pad_sequence,pack_padded_sequence
from torch.utils.data import Dataset
import json
from typing import Iterable,Dict,Optional
from torch import Tensor, LongTensor, BoolTensor
from jac_nlp.bi_ner.model.ph_func import BI_P_Head,prepare_inputs
from jac_nlp.bi_ner.model.loss import ContrastiveThresholdLoss
from jac_nlp.bi_ner.model.tokenize_data import get_datasets
from jac_nlp.bi_ner.datamodel.utils import get_category_id_mapping,invert,pad_images
from jac_nlp.bi_ner.datamodel.example import Example
from jac_nlp.bi_ner.datamodel import example
from functools import partial
from transformers import AutoTokenizer
### Inference related Classes ###
# class PHClassifier(Module):
#     def __init__(
#         self,
#         bi_ner_model
#         embedding_length=768,
#         ph_nhead=12,
#         ph_ff_dim=128,
#         batch_first=True,
#         ph_nlayers=1,
#     ):
#         super().__init__()
#         self.bi_ner_model=bi_ner_model
#         encoder_layer = nn.TransformerEncoderLayer(
#             d_model=embedding_length,
#             nhead=ph_nhead,
#             dim_feedforward=ph_ff_dim,
#             batch_first=batch_first,
#         )
#         cand_encoder_layer = nn.TransformerEncoderLayer(
#             d_model=embedding_length,
#             nhead=ph_nhead,
#             dim_feedforward=30,
#             batch_first=batch_first,
#         )
#         self.con_encoder = nn.TransformerEncoder(
#             encoder_layer=encoder_layer, num_layers=ph_nlayers
#         )
#         self.cand_encoder = nn.TransformerEncoder(
#             encoder_layer=cand_encoder_layer, num_layers=ph_nlayers
#         )
        

#     def forward(self, batch):
#         ent_emb,token_emb=bi_ner_model(**batch)
#         token_emb = self.con_encoder(token_emb)
#         ent_emb = self.cand_encoder(ent_emb)
#         comb_emb = torch.cat((token_emb, ent_emb), dim=1)
#         return comb_emb

# class CustomPreProcessor:
#     def __init__(self):
#         pass
#     def process(self, x):
#         # x if List[List[Float]]
#         x = torch.tensor(x)
#         return x
# class CustomPostProcessor:
#     def __init__(self):
#         pass
#     def process(self, x):
#         x = x.tolist()
#         return x
### Training Related Classes ###

# class CustomDataset(Dataset):
#     def __init__(self, input_file):
#         from jaseci_ai_kit.use_enc import encode
#         self.input_file = input_file
#         dirname = os.path.dirname(__file__)
#         m_config_fname = os.path.join(dirname, "config/m_config.json")
#         with open(m_config_fname, "r") as jsonfile:
#             model_args = json.load(jsonfile)
#         with open(input_file, "r") as f:
#             dataset = json.load(f)
#         category_name = list(
#             set(ele["entity_type"] for val in dataset["annotations"] for ele in val)
#         )
#         category_id_mapping = get_category_id_mapping(model_args, category_name)
#         model_args["descriptions"] = category_name
#         self.model = BI_Enc_NER(model_args)
#         example_encoder = partial(
#             self.model.prepare_inputs,
#             category_mapping=invert(category_id_mapping),
#             no_entity_category=model_args["unk_category"],
#         )
#         return get_datasets(dataset, example_encoder)

        
class CustomLoss(torch.nn.Module):
    def __init__(self, n_classes=2, beta=0.6):
        super(CustomLoss, self).__init__()
        self._loss_fn = ContrastiveThresholdLoss(n_classes=n_classes,ignore_id=-100,
            reduction="mean",
            beta=beta)
    def forward(self, output, labels):
        _span_coef=0.6
        _start_coef=0.2
        _end_coef=0.2
        _max_entity_length=30
        
        span_loss = self._loss_fn(output[0], labels)
        start_loss = self._loss_fn(
            output[1].unsqueeze(-2).repeat(1, 1, _max_entity_length, 1), labels
        )
        end_loss = self._loss_fn(
            output[2].unsqueeze(-2).repeat(1, 1, _max_entity_length, 1), labels
        )

        return (
        _span_coef * span_loss
        + _start_coef * start_loss
        + _end_coef * end_loss
    )


class CustomModel(nn.Module):
    def __init__(self, model_args) -> None:
        super(CustomModel, self).__init__()
        category_id_mapping = get_category_id_mapping(model_args, model_args["descriptions"])
        self.model = BI_P_Head(model_args)
        print(f"in custom model{model_args}")
        con_encoder_layer = nn.TransformerEncoderLayer(
            d_model=768,
            nhead=12,
            dim_feedforward=128,
            batch_first=True,
        )
        cand_encoder_layer = nn.TransformerEncoderLayer(
            d_model=768,
            nhead=12,
            dim_feedforward=30,
            batch_first=True,
        )
        self.con_encoder = nn.TransformerEncoder(
            encoder_layer=con_encoder_layer, num_layers=1
        )
        self.cand_encoder = nn.TransformerEncoder(
            encoder_layer=cand_encoder_layer, num_layers=1
        )
        
    def forward(self,x):
        ent_emb,token_emb = self.model(x)
        token_emb = self.con_encoder(token_emb)
        ent_emb = self.cand_encoder(ent_emb)
        scores=self.model.get_scores(token_emb,ent_emb,"test")
        return scores

def collate_fn(
     examples: Iterable[Example], _max_sequence_length=128,return_batch_examples: bool = False,
) -> Dict[str, Optional[LongTensor]]:
    print("custom collate fucntions")
    # print(examples)
    return example.collate_examples(
        examples,
        padding_token_id=100,
        pad_length=_max_sequence_length,
        return_batch_examples=return_batch_examples,
    )


class CustomDataset(Dataset):
    def __init__(self,train_args) -> None:
        super(CustomDataset, self).__init__()
        self.data =  {
            "text": [
                "Japan began the defence of their Asian Cup title with a lucky 2-1 win against Syria in a Group C championship match on Friday.",
                "But China saw their luck desert them in the second match of the group crashing to a surprise 2-0 defeat to newcomers Uzbekistan."
                ],
                "annotations": [
                    [
                        {
                            "start_index": 0,
                            "end_index": 5,
                            "entity_type": "LOC"
                        },
                        {
                            "start_index": 78,
                            "end_index": 83,
                            "entity_type": "LOC"
                        }
                    ],
                    [
                        {
                            "start_index": 4,
                            "end_index": 9,
                            "entity_type": "LOC"
                        },
                        {
                            "start_index": 117,
                            "end_index": 127,
                            "entity_type": "LOC"
                        }
                    ]
                ]
            }
        category_id_mapping = get_category_id_mapping(train_args, train_args["descriptions"])
        self.example_encoder = partial(
            prepare_inputs,
            category_mapping=invert(category_id_mapping),
            no_entity_category=train_args["unk_category"],
        )
        self.pad_length=train_args["max_sequence_length"]
        _token_tokenizer=AutoTokenizer.from_pretrained(
            train_args.get("context_bert_model"))
        self.padding_token_id=_token_tokenizer.pad_token_id
        self.dataset = get_datasets(self.data, self.example_encoder)
        self._max_sequence_length = 0
        for example in self.dataset:
            _,_,input_ids,_,_,_ = example
            self._max_sequence_length = max(
                self._max_sequence_length, len(input_ids)
            )
        print(f"max sequence length {self._max_sequence_length}")

    def __len__(self):
        return len(self.dataset)
    def __getitem__(self, idx):
        # print(self.dataset[idx])
        return self.dataset[idx]
        # print(input_ids.shape)
        # print(labels.shape)
        # input_ids = nn.ConstantPad1d((0,self._max_sequence_length - input_ids.shape[0]), 0)(input_ids)
        # input_ids = pad_sequence([input_ids],batch_first=True)
        # # input_ids=  pad_images(
        # #         [input_ids], padding_value=self.padding_token_id, padding_length=(self._max_sequence_length, None))
        # labels= pad_images(
        #         [labels], padding_value=-100, padding_length=(self.pad_length, None)
        #     )
        # # print(input_ids)
        # print(input_ids.size())
        # print(labels.size())

class CustomPreProcessor:
    def __init__(self):
        pass

    def process(self, x):
        # tokenization and data transformation
        pass

class CustomPostProcessor:
    def __init__(self):
        pass

    def process(self, x):
        pass
