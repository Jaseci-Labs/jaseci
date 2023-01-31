import os
import torch
import shutil
from pathlib import Path
from functools import partial
from torch import nn
from torch.nn import Module, Parameter
from torch.nn import Linear, Embedding
from torch import Tensor, LongTensor, BoolTensor
from transformers.tokenization_utils_base import EncodingFast
from typing import List, Tuple, Union, Optional, TypeVar, Iterable, Set, Dict
from torch.nn.functional import pad
from transformers import (
    PreTrainedModel,
    AutoModel,
    AutoTokenizer,
    PreTrainedTokenizer,
    BatchEncoding,
)
from .metric import CosSimilarity
from .loss import ContrastiveThresholdLoss
from ..datamodel.example import Example, strided_split, TypedSpan
from ..datamodel import example
from torch.utils.data import DataLoader
from tqdm.autonotebook import trange
from transformers.optimization import AdamW, get_linear_schedule_with_warmup
import math
from .base_encoder import Base_BI_enc
_Model = TypeVar("_Model", bound="BI_P_Head")

class PHClassifier(Module):
    def __init__(
        self,
        embedding_length=768,
        ph_nhead=12,
        ph_ff_dim=128,
        batch_first=True,
        ph_nlayers=1,
    ):
        super().__init__()
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embedding_length,
            nhead=ph_nhead,
            dim_feedforward=ph_ff_dim,
            batch_first=batch_first,
        )
        cand_encoder_layer = nn.TransformerEncoderLayer(
            d_model=embedding_length,
            nhead=ph_nhead,
            dim_feedforward=30,
            batch_first=batch_first,
        )
        self.con_encoder = nn.TransformerEncoder(
            encoder_layer=encoder_layer, num_layers=ph_nlayers
        )
        self.cand_encoder = nn.TransformerEncoder(
            encoder_layer=cand_encoder_layer, num_layers=ph_nlayers
        )
        # self.decoder = nn.Linear(embedding_length, n_classes)
        # nn.init.xavier_uniform_(self.decoder.weight)

    def forward(self, emb1, emb2):
        x = self.con_encoder(emb1)
        y = self.cand_encoder(emb2)
        return x, y


class BI_P_Head(Base_BI_enc):
    def __init__(self, param) -> None:

        super(BI_P_Head, self).__init__(param)
        global _token_tokenizer
        self._metric = CosSimilarity(scale=0.07)
        self._unk_entity_label_id = param.get("unk_entity_type_id")
        self._loss_fn_factory = partial(
            ContrastiveThresholdLoss,
            ignore_id=-100,
            reduction="mean",
            beta=param.get("loss_beta"),
        )
        self._token_encoder = self._context_encoder
        self._token_tokenizer: PreTrainedTokenizer = AutoTokenizer.from_pretrained(
            param.get("context_bert_model")
        )
        _token_tokenizer=self._token_tokenizer
        self._descriptions_encoder = self._candidate_encoder
        self._descriptions_tokenizer: PreTrainedTokenizer = (
            AutoTokenizer.from_pretrained(param.get("candidate_bert_model"))
        )
        # self._head=PHClassifier()
        self._loss_fn: Optional[ContrastiveThresholdLoss] = None
        self._start_coef = param.get("start_coef")
        self._end_coef = param.get("end_coef")
        self._span_coef = param.get("span_coef")

        self._hidden_size = param.get("hidden_size")
        self._encoder_hidden = self._token_encoder.config.hidden_size
        self._max_sequence_length = min(
            param.get("max_sequence_length"), self._token_tokenizer.model_max_length
        )
        self._max_entity_length = param.get("max_entity_length")

        self._entity_projection = Linear(self._encoder_hidden, self._hidden_size)
        self._encoded_descriptions: Optional[BatchEncoding] = None
        self._frozen_entity_representations: Optional[Tensor] = None
        self.add_descriptions(param.get("descriptions"))

        self._length_embedding = Embedding(self._max_entity_length, self._hidden_size)
        self._span_projection = Linear(
            self._encoder_hidden * 2 + self._hidden_size, self._hidden_size
        )
        self._token_start_projection = Linear(self._encoder_hidden, self._hidden_size)
        self._token_end_projection = Linear(self._encoder_hidden, self._hidden_size)
        self._entity_start_projection = Linear(self._encoder_hidden, self._hidden_size)
        self._entity_end_projection = Linear(self._encoder_hidden, self._hidden_size)

    def freeze_descriptions(self):
        if self._frozen_entity_representations is not None:
            return

        with torch.no_grad():
            self._frozen_entity_representations = self._descriptions_encoder(
                self._encoded_descriptions.to(self.device)
            ).last_hidden_state[
                :, 0
            ]  # TODO: split into batches

    def drop_descriptions_encoder(self):
        self._descriptions_encoder = None

    def add_descriptions(self, descriptions: List[str]) -> None:
        self._encoded_descriptions = self._descriptions_tokenizer(
            descriptions,
            return_tensors="pt",
            truncation=True,
            max_length=self._descriptions_encoder.config.max_length,
            add_special_tokens=True,
            padding=True,
        )["input_ids"]
        self._loss_fn = self._loss_fn_factory(len(descriptions))
        self._frozen_entity_representations = None

    def eval(self: _Model) -> _Model:
        super(BI_P_Head, self).eval()
        self.freeze_descriptions()
        return self

    def train(self: _Model, mode: bool = True) -> _Model:
        super(BI_P_Head, self).train(mode)
        self._frozen_entity_representations = None
        return self

    def _get_entity_representations(self) -> Tensor:
        if self._frozen_entity_representations is not None:
            return self._frozen_entity_representations.to(self.device)
        return self._descriptions_encoder(
            self._encoded_descriptions.to(self.device)
        ).last_hidden_state[
            :, 0
        ]  # TODO: split into batches

    def _get_length_representations(self, token_representations: Tensor) -> Tensor:
        batch_size, sequence_length, representation_dims = token_representations.shape

        length_embeddings = self._length_embedding(
            torch.arange(self._max_entity_length, device=self.device)
        )
        return length_embeddings.reshape(
            1, 1, self._max_entity_length, self._hidden_size
        ).repeat(batch_size, sequence_length, 1, 1)

    def _get_span_representations(
        self, token_representations: Tensor
    ) -> Tuple[Tensor, BoolTensor]:
        batch_size, sequence_length, representation_dims = token_representations.shape

        padding_masks: List[BoolTensor] = []
        span_end_representations: List[Tensor] = []

        for shift in range(
            self._max_entity_length
        ):  # self._max_entity_length ~ 20-30, so it is fine to not vectorize this
            span_end_representations.append(
                torch.roll(token_representations, -shift, 1).unsqueeze(-2)
            )

            padding_mask = torch.ones(
                (batch_size, sequence_length), dtype=torch.bool, device=self.device
            )
            padding_mask[:, -shift:] = False
            padding_masks.append(padding_mask.unsqueeze(-1))

        padding_mask = torch.concat(padding_masks, dim=-1).bool()
        span_end_representation = torch.concat(span_end_representations, dim=-2)
        span_start_representation = token_representations.unsqueeze(-2).repeat(
            1, 1, self._max_entity_length, 1
        )

        span_length_embedding = self._get_length_representations(token_representations)

        span_representation = torch.concat(
            [span_start_representation, span_end_representation, span_length_embedding],
            dim=-1,
        )
        return self._span_projection(span_representation), padding_mask

    def _compute_sim_scores(
        self,
        representations: Tensor,
        entity_representations: Tensor,
        *,
        span_level: bool = True,
    ) -> Tensor:
        n_classes = len(self._encoded_descriptions)

        representations = representations.unsqueeze(
            -2
        )  # (B, S, M, 1, H) or (B, S, 1, H)
        new_shape = (
            (1, 1, 1, n_classes, self._hidden_size)
            if span_level
            else (1, 1, n_classes, self._hidden_size)
        )
        entity_representations = entity_representations.reshape(*new_shape)
        return self._metric(representations, entity_representations)

    

    def forward(
        self, input_ids: LongTensor, labels: Optional[LongTensor] = None, **_
    ) -> Union[LongTensor, Tuple[Tensor, LongTensor]]:
        """Predicts entity type ids. If true label ids are given,
        calculates loss as well."""
        # print(input_ids.shape)
        # input_ids=input_ids.squeeze(0)
        # print(input_ids.shape)
        batch_size,sequence_length = input_ids
        # input_ids = pad(
        #     input_ids,
        #     [0, self._max_sequence_length - sequence_length],
        #     value=self._token_tokenizer.pad_token_id,
        # )

        token_representations = self._token_encoder(
            input_ids=input_ids.to(self.device)
        )[
            "last_hidden_state"
        ]  # (B, S, E)
        entity_representations = self._get_entity_representations()  # (C, E)

        return entity_representations,token_representations

    def get_scores(self,token_representations,entity_representations,labels=None):
        # token_representations,entity_representations = self._head(token_representations,entity_representations)
        span_representations, span_padding = self._get_span_representations(
            token_representations
        )
        span_scores = self._compute_sim_scores(
            span_representations, self._entity_projection(entity_representations)
        )
        batch_size, _, _, n_classes = span_scores.shape

        entity_threshold = span_scores[:, 0, 0].reshape(
            batch_size, 1, 1, n_classes
        )  # is a sim score with [CLS] token and entities
        mask = span_scores > entity_threshold
        scores_mask = torch.full_like(span_scores, fill_value=-torch.inf)
        scores_mask[mask] = 0  # set to -inf scores that did not pass the threshold

        values, predictions = torch.max(span_scores + scores_mask, dim=-1)
        predictions[values == -torch.inf] = self._unk_entity_label_id

        if labels is None:
            return predictions

        # (C, H)
        entity_start_representations = self._entity_start_projection(
            entity_representations
        )
        entity_end_representations = self._entity_end_projection(entity_representations)

        # (B, S, H)
        token_start_representations = self._token_start_projection(
            token_representations
        )
        token_end_representations = self._token_start_projection(token_representations)
        # labels = labels.to(self.device)?
        start_scores = self._compute_sim_scores(
            token_start_representations, entity_start_representations, span_level=False
        )
        end_scores = self._compute_sim_scores(
            token_end_representations, entity_end_representations, span_level=False
        )
        return (span_scores,start_scores,end_scores)


    def save(self, save_path):
        super().save(save_path)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        cand_bert_path = os.path.join(save_path + "/cand_bert")
        cont_bert_path = os.path.join(save_path + "/cont_bert")
        if not os.path.exists(cand_bert_path):
            os.makedirs(cand_bert_path)
        if not os.path.exists(cont_bert_path):
            os.makedirs(cont_bert_path)
        self._context_encoder.save_pretrained(cont_bert_path)
        self._context_encoder.save_pretrained(cand_bert_path)
        self._descriptions_tokenizer.save_vocabulary(cand_bert_path)
        self._token_tokenizer.save_vocabulary(cont_bert_path)
        print(f"Saving non-shared model to : {save_path}")
        shutil.copyfile(
            os.path.join(
                Path(os.path.dirname(__file__)).parent, "config/t_config.json"
            ),
            os.path.join(save_path, "t_config.json"),
        )
        shutil.copyfile(
            os.path.join(
                Path(os.path.dirname(__file__)).parent, "config/m_config.json"
            ),
            os.path.join(save_path, "m_config.json"),
        )
        return f"[Saved model at] : {save_path}"

    def load(self, load_path) -> _Model:
        super().load(load_path)
        cand_bert_path = os.path.join(load_path, "cand_bert")
        cont_bert_path = os.path.join(load_path, "cont_bert")
        print(f"Loading non-shared model from : {load_path}")
        self._token_encoder: PreTrainedModel = AutoModel.from_pretrained(
            cont_bert_path, local_files_only=True
        )
        self._descriptions_encoder: PreTrainedModel = AutoModel.from_pretrained(
            cand_bert_path, local_files_only=True
        )
        self._token_tokenizer = AutoTokenizer.from_pretrained(
            cont_bert_path, local_files_only=True
        )
        self._descriptions_tokenizer = AutoTokenizer.from_pretrained(
            cand_bert_path, local_files_only=True
        )
        return self

_loss_fn=ContrastiveThresholdLoss(n_classes=2,ignore_id=-100,
            reduction="mean",
            beta=0.6)
def get_loss(output, labels):
    _span_coef=0.6
    _start_coef=0.2
    _end_coef=0.2
    _max_entity_length=30
    
    span_loss = _loss_fn(output[0], labels)
    start_loss = _loss_fn(
        output[1].unsqueeze(-2).repeat(1, 1, _max_entity_length, 1), labels
    )
    end_loss = _loss_fn(
        output[2].unsqueeze(-2).repeat(1, 1, _max_entity_length, 1), labels
    )

    return (
        _span_coef * span_loss
        + _start_coef * start_loss
        + _end_coef * end_loss
    )


def collate_examples(
     examples: Iterable[Example], _max_sequence_length,return_batch_examples: bool = False,
) -> Dict[str, Optional[LongTensor]]:
    return example.collate_examples(
        examples,
        padding_token_id=_token_tokenizer.pad_token_id,
        pad_length=_max_sequence_length,
        return_batch_examples=return_batch_examples,
    )



def train_ph(model, train_dataset, train_config):
    train_dataloader = DataLoader(
        train_dataset,
        batch_size=train_config["train_batch_size"],
        shuffle=True,collate_fn=partial(
                    collate_examples,_max_sequence_length=128,return_batch_examples=True
                )
    )
    t_total = (
        len(train_dataloader)
        // train_config["gradient_accumulation_steps"]
        * (max(5, train_config["num_train_epochs"]))
    )

    global_step = 0
    if not os.path.exists(train_config["logpath"]):
        os.makedirs(train_config["logpath"])
    log_wf = open(
        os.path.join(train_config["logpath"], "log.txt"), "w", encoding="utf-8"
    )  # will be used in for logging
    no_decay = ["bias", "LayerNorm.weight"]
    optimizer_grouped_parameters = [
        {
            "params": [
                p
                for n, p in model.named_parameters()
                if not any(nd in n for nd in no_decay)
            ],
            "weight_decay": train_config["weight_decay"],
        },
        {
            "params": [
                p
                for n, p in model.named_parameters()
                if any(nd in n for nd in no_decay)
            ],
            "weight_decay": 0.0,
        },
    ]
    optimizer = AdamW(
        optimizer_grouped_parameters,
        lr=train_config["learning_rate"],
    )
    warmup_steps = math.ceil(
        len(train_dataset)
        * train_config["num_train_epochs"]
        / train_config["train_batch_size"]
        * 0.1
    )
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=warmup_steps, num_training_steps=t_total
    )
    for name, param in model.named_parameters():
        if '_candidate_encoder' in name or "_context_encoder" in name:
        # if '_head' not in name:
        #     continue
            param.requires_grad = False
    for name, param in model.named_parameters():
      if param.requires_grad:
        print(name, param.size())
    for epoch in trange(
        train_config["num_train_epochs"], desc="Epoch", disable=False, unit="batch"
    ):
        tr_loss = 0
        nb_tr_steps = 0
        with trange(len(train_dataloader), unit="it") as bar:
            for step, batch in enumerate(train_dataloader, start=1):
                model.train()
                optimizer.zero_grad()
                entity_representations,token_representations = model(**batch)
                output = model.get_scores(token_representations,entity_representations,batch["labels"])
                loss=get_loss(output,batch["labels"])
                tr_loss += loss.item()
                nb_tr_steps += 1
                if (step + 1) % train_config["gradient_accumulation_steps"] == 0:

                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(
                        model.parameters(), train_config["max_grad_norm"]
                    )

                    optimizer.step()
                    scheduler.step()
                    model.zero_grad()   
                    global_step += 1
                    bar.update()

        print(
            f"""\n
            Epoch : {epoch+1}
            loss : {tr_loss/nb_tr_steps}
            LR : {optimizer.param_groups[0]['lr']}\n"""
        )
        log_wf.write(f"{epoch+1}\t{tr_loss/nb_tr_steps}\n")
    log_wf.close()
    return model


from collections import defaultdict
from copy import deepcopy
from functools import partial
from os import cpu_count
from typing import Dict, List, Set, TypeVar, Optional, Iterable, Tuple

import numpy as np
import torch
from torch import LongTensor
from torch.nn import Module
from torch.nn.functional import pad
from tqdm import tqdm

from ..datamodel.example import TypedSpan, batch_examples, BatchedExamples
from ..datamodel.utils import invert
from .base_encoder import Base_BI_enc, BI_Enc_NER

torch.set_num_threads(cpu_count() // 2)


_Model = TypeVar("_Model", bound=Module)


class PH_infer(Base_BI_enc):
    def __init__(
        self,
        span_classifier: BI_Enc_NER,
        category_mapping: Dict[str, int],
        no_entity_category: str,
        max_sequence_length: int,
        max_entity_length: int,
        model_args,
    ):
        super(PH_infer, self).__init__(model_args)
        self._classifier = span_classifier
        self._classifier.eval()
        self._classifier.drop_descriptions_encoder()
        self._classifier.train = None
        self._encoded_descriptions=self._classifier._encoded_descriptions
        self._category_mapping = deepcopy(category_mapping)
        self._category_id_mapping = invert(self._category_mapping)
        self._no_entity_category = no_entity_category
        self._max_sequence_length = max_sequence_length
        self._max_entity_length = max_entity_length
        self._text_length: List[Optional[int]]=None
        self._no_entity_category_id=None
        self._stride_length=None

    def train(self: _Model, mode: bool = True) -> _Model:
        raise NotImplementedError

    @torch.no_grad()
    def add_entity_types(self, descriptions: Dict[str, str]) -> None:
        names, texts = map(list, zip(*descriptions.items()))
        entity_representations = self._classifier._description_encoder(texts)
        self._encoded_descriptions.update(zip(names, entity_representations))

    @torch.no_grad()
    def forward(self, texts: List[str]) -> List[Set[TypedSpan]]:
        stride = 0.9
        self._stride_length = int(self._max_sequence_length * stride)

        self._text_length: List[Optional[int]] = [None] * len(texts)
        examples = list(
            self._classifier.prepare_inputs(
                texts,
                [None] * len(texts),
                category_mapping=self._category_mapping,
                no_entity_category=self._no_entity_category,
                stride=stride,
                text_lengths=self._text_length,
            )
        )

        self._no_entity_category_id = self._category_mapping[self._no_entity_category]

        predictions_collector = [defaultdict(int) for _ in texts]
        
        for batch in tqdm(
            batch_examples(
                examples,
                batch_size=1,
                collate_fn=partial(
                    self._classifier.collate_examples, return_batch_examples=True
                ),
            ),
            total=len(examples),
        ):
            entity_representations,token_representations = self._classifier(**batch)
            # token_representations,entity_representations = self._classifier.get_head_emb(token_representations,entity_representations)
            predictions: LongTensor = self._classifier.get_head_emb(entity_representations,token_representations)
           
            batched_examples: BatchedExamples = batch["examples"]

            batch_size, length = batched_examples.start_offset.shape
            span_start = (
                pad(
                    batched_examples.start_offset,
                    [0, self._max_sequence_length - length],
                    value=-100,
                )
                .view(batch_size, self._max_sequence_length, 1)
                .repeat(1, 1, self._max_entity_length)
                .to(self.device)
            )

            end_offset = pad(
                batched_examples.end_offset,
                [0, self._max_sequence_length - length],
                value=-100,
            ).to(self.device)

            padding_masks = []
            span_end = []
            for shift in range(
                self._max_entity_length
            ):  # self._max_entity_length ~ 20-30, so it is fine to not vectorize this
                span_end.append(torch.roll(end_offset, -shift, 1).unsqueeze(-1))
                padding_mask = torch.roll(end_offset != -100, -shift, 1)
                padding_mask[:, -shift:] = False
                padding_masks.append(padding_mask.unsqueeze(-1))

            span_end = torch.concat(span_end, dim=-1)
            padding_mask = torch.concat(padding_masks, dim=-1)

            entities_mask = (
                (predictions != self._no_entity_category_id)
                & padding_mask
                & (span_end != -100)
                & (span_start != -100)
            )
            entity_token_start = (
                torch.arange(self._max_sequence_length)
                .reshape(1, self._max_sequence_length, 1)
                .repeat(batch_size, 1, self._max_entity_length)
                .to(self.device)
            )

            entity_text_ids = (
                torch.tensor(batched_examples.text_ids)
                .view(batch_size, 1, 1)
                .repeat(1, self._max_sequence_length, self._max_entity_length)
                .to(self.device)
            )

            chosen_text_ids = entity_text_ids[entities_mask]
            chosen_category_ids = predictions[entities_mask]
            chosen_span_starts = span_start[entities_mask]
            chosen_span_ends = span_end[entities_mask]
            chosen_token_starts = entity_token_start[entities_mask]
            for text_id, category_id, start, end, token_start in zip(
                chosen_text_ids,
                chosen_category_ids,
                chosen_span_starts,
                chosen_span_ends,
                chosen_token_starts,
            ):
                predictions_collector[text_id][
                    (
                        TypedSpan(
                            start.item(),
                            end.item(),
                            self._category_id_mapping[category_id.item()],
                        ),
                        token_start.item(),
                    )
                ] += 1

        all_entities = [set() for _ in texts]
        for text_id, preds in enumerate(predictions_collector):
            text_length = self._text_length[text_id]
            strided_text_length = (
                (text_length // self._stride_length) + (text_length % self._stride_length > 0)
            ) * self._stride_length
            for (entity, entity_token_start), count_preds in preds.items():
                # [1, 2, 3, ..., MAX, MAX, ..., MAX, MAX - 1, ..., 3, 2, 1]
                #  bin sizes are stride_length except for the last bin
                total_predictions = min(
                    (entity_token_start // self._stride_length) + 1,
                    (
                        max(strided_text_length - self._max_sequence_length, 0)
                        // self._stride_length
                    )
                    + 1,
                    ((strided_text_length - entity_token_start) // self._stride_length) + 1,
                )
                if count_preds >= total_predictions // 2:
                    all_entities[text_id].add(entity)

        return all_entities


def prepare_inputs(
        texts: List[str],
        entities: List[Optional[Set[TypedSpan]]],
        *,
        stride: float = 1 / 8,
        category_mapping: Dict[str, int],
        no_entity_category: str,
        text_lengths: Optional[List] = None,
        _max_sequence_length=128,
        _max_entity_length=30


    ) -> Iterable[Example]:

        encodings: Optional[List[EncodingFast]] = _token_tokenizer(
            texts,
            truncation=False,
            add_special_tokens=False,
            return_offsets_mapping=True,
        ).encodings
        if encodings is None:
            raise ValueError(
                f"Tokenizer {_token_tokenizer} is not fast! Use fast tokenizer!"
            )

        if text_lengths is not None:
            for i in range(len(texts)):
                text_lengths[i] = len(encodings[i].ids)

        for text_idx, (encoding, entities) in enumerate(zip(encodings, entities)):
            yield from strided_split(
                text_idx,
                encoding,
                entities,
                stride=int(_max_sequence_length * stride),
                max_sequence_length=_max_sequence_length,
                max_entity_length=_max_entity_length,
                category_mapping=category_mapping,
                no_entity_category=no_entity_category,
                cls_token_id=_token_tokenizer.cls_token_id,
            )
