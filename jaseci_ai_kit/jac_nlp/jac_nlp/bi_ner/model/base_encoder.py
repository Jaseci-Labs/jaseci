import os
import torch
import shutil
from pathlib import Path
from functools import partial
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
from ..datamodel.example import Example, strided_split, TypedSpan, collate_examples


_Model = TypeVar("_Model", bound="BI_Enc_NER")


class Base_BI_enc(Module):
    def __init__(self, param) -> None:
        super(Base_BI_enc, self).__init__()
        self._context_encoder: PreTrainedModel = AutoModel.from_pretrained(
            param.get("context_bert_model")
        )
        self._candidate_encoder: PreTrainedModel = AutoModel.from_pretrained(
            param.get("candidate_bert_model")
        )
        self._dummy_param = Parameter(torch.empty(0))

    @property
    def device(self) -> torch.device:
        return self._dummy_param.device

    def get_context_embeddings(self, context_inputs):
        return self._context_encoder(**context_inputs).last_hidden_state[:, 0]

    def get_candidate_embeddings(self, candidate_inputs):
        return self._candidate_encoder(**candidate_inputs).last_hidden_state[:, 0]

    def forward(self, context_inputs, candidate_inputs=None, **kwargs):
        cont_emb = self.get_context_embeddings(context_inputs)
        if candidate_inputs:
            cand_emb = self.get_candidate_embeddings(candidate_inputs)
            return cont_emb, cand_emb
        return cont_emb

    def save(self, save_path):
        pass

    def load(self, load_path):
        pass


class BI_Enc_NER(Base_BI_enc):
    def __init__(self, param) -> None:
        super(BI_Enc_NER, self).__init__(param)

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
        self._descriptions_encoder = self._candidate_encoder
        self._descriptions_tokenizer: PreTrainedTokenizer = (
            AutoTokenizer.from_pretrained(param.get("candidate_bert_model"))
        )
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
        super(BI_Enc_NER, self).eval()
        self.freeze_descriptions()
        return self

    def train(self: _Model, mode: bool = True) -> _Model:
        super(BI_Enc_NER, self).train(mode)
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

    def prepare_inputs(
        self,
        texts: List[str],
        entities: List[Optional[Set[TypedSpan]]],
        *,
        stride: float = 1 / 8,
        category_mapping: Dict[str, int],
        no_entity_category: str,
        text_lengths: Optional[List] = None,
    ) -> Iterable[Example]:
        encodings: Optional[List[EncodingFast]] = self._token_tokenizer(
            texts,
            truncation=False,
            add_special_tokens=False,
            return_offsets_mapping=True,
        ).encodings
        if encodings is None:
            raise ValueError(
                f"Tokenizer {self._token_tokenizer} is not fast! Use fast tokenizer!"
            )

        if text_lengths is not None:
            for i in range(len(texts)):
                text_lengths[i] = len(encodings[i].ids)

        for text_idx, (encoding, entities) in enumerate(zip(encodings, entities)):
            yield from strided_split(
                text_idx,
                encoding,
                entities,
                stride=int(self._max_sequence_length * stride),
                max_sequence_length=self._max_sequence_length,
                max_entity_length=self._max_entity_length,
                category_mapping=category_mapping,
                no_entity_category=no_entity_category,
                cls_token_id=self._token_tokenizer.cls_token_id,
            )

    def collate_examples(
        self, examples: Iterable[Example], return_batch_examples: bool = False
    ) -> Dict[str, Optional[LongTensor]]:
        return collate_examples(
            examples,
            padding_token_id=self._token_tokenizer.pad_token_id,
            pad_length=self._max_sequence_length,
            return_batch_examples=return_batch_examples,
        )

    def forward(
        self, input_ids: LongTensor, labels: Optional[LongTensor] = None, **_
    ) -> Union[LongTensor, Tuple[Tensor, LongTensor]]:
        """Predicts entity type ids. If true label ids are given,
        calculates loss as well."""

        batch_size, sequence_length = input_ids.shape
        input_ids = pad(
            input_ids,
            [0, self._max_sequence_length - sequence_length],
            value=self._token_tokenizer.pad_token_id,
        )

        token_representations = self._token_encoder(
            input_ids=input_ids.to(self.device)
        )[
            "last_hidden_state"
        ]  # (B, S, E)
        entity_representations = self._get_entity_representations()  # (C, E)

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
        labels = labels.to(self.device)

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

        start_scores = self._compute_sim_scores(
            token_start_representations, entity_start_representations, span_level=False
        )
        end_scores = self._compute_sim_scores(
            token_end_representations, entity_end_representations, span_level=False
        )

        span_loss = self._loss_fn(span_scores, labels)
        start_loss = self._loss_fn(
            start_scores.unsqueeze(-2).repeat(1, 1, self._max_entity_length, 1), labels
        )
        end_loss = self._loss_fn(
            end_scores.unsqueeze(-2).repeat(1, 1, self._max_entity_length, 1), labels
        )

        return (
            self._span_coef * span_loss
            + self._start_coef * start_loss
            + self._end_coef * end_loss,
            predictions,
        )

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
