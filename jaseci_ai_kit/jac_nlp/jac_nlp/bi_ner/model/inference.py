from collections import defaultdict
from copy import deepcopy
from functools import partial
from os import cpu_count
from typing import Dict, List, Set, TypeVar, Optional
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


class Bi_NER_Infer(Base_BI_enc):
    def __init__(
        self,
        span_classifier: BI_Enc_NER,
        category_mapping: Dict[str, int],
        no_entity_category: str,
        max_sequence_length: int,
        max_entity_length: int,
        model_args,
    ):
        super(Bi_NER_Infer, self).__init__(model_args)
        self._classifier = deepcopy(span_classifier)
        self._classifier.eval()
        self._classifier.drop_descriptions_encoder()
        self._classifier.train = None
        self._encoded_descriptions = self._classifier._encoded_descriptions
        self._category_mapping = deepcopy(category_mapping)
        self._category_id_mapping = invert(self._category_mapping)
        self._no_entity_category = no_entity_category
        self._max_sequence_length = max_sequence_length
        self._max_entity_length = max_entity_length
        self._text_length: List[Optional[int]] = None
        self._no_entity_category_id = None
        self._stride_length = None

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
            predictions: LongTensor = self._classifier(**batch)

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
                (text_length // self._stride_length)
                + (text_length % self._stride_length > 0)
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
                    ((strided_text_length - entity_token_start) // self._stride_length)
                    + 1,
                )
                if count_preds >= total_predictions // 2:
                    all_entities[text_id].add(entity)

        return all_entities
