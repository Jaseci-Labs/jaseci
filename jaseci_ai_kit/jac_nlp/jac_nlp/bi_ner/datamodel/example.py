import logging
from dataclasses import dataclass, fields
from typing import Tuple, Iterable, Optional, Union, Dict, List, Set, Callable
import torch
from torch import LongTensor
from torch.nn.utils.rnn import pad_sequence
from transformers.tokenization_utils_base import EncodingFast
from .utils import pad_images, invert


logger = logging.getLogger(__name__)


@dataclass
class TupleLike:
    def __iter__(self):  # so it behaves like a NamedTuple
        return iter(self.as_tuple())

    def as_tuple(self):
        return tuple(self.__getattribute__(field.name) for field in fields(self))


@dataclass(repr=True, eq=True, order=True, frozen=True)
class TypedSpan:
    start: int
    end: int
    type: str

    def __iter__(self):  # so it behaves like a NamedTuple
        return iter(self.as_tuple())

    def as_tuple(self):
        return tuple(self.__getattribute__(field.name) for field in fields(self))


@dataclass
class Example(TupleLike):
    text_id: int
    example_start: int
    input_ids: LongTensor  # shape: (LENGTH)
    start_offset: LongTensor
    end_offset: LongTensor
    target_label_ids: Optional[LongTensor]  # shape: (LENGTH, MAX_ENTITY_LENGTH)


@dataclass
class BatchedExamples(TupleLike):
    text_ids: Tuple[int, ...]
    example_starts: Tuple[int, ...]
    input_ids: LongTensor  # shape: (BATCH_SIZE, LENGTH)
    start_offset: LongTensor
    end_offset: LongTensor


def collate_examples(
    examples: Iterable[Example],
    *,
    padding_token_id: int,
    pad_length: Optional[int] = None,
    return_batch_examples: bool = True,
) -> Dict[str, Union[BatchedExamples, Optional[LongTensor]]]:
    all_text_ids: List[int] = []
    all_example_starts: List[int] = []
    all_input_ids: List[LongTensor] = []
    all_start_offsets: List[LongTensor] = []
    all_end_offsets: List[LongTensor] = []
    target_label_ids: Optional[List[LongTensor]] = None

    no_target_label_ids: Optional[bool] = None

    for example in examples:
        all_text_ids.append(example.text_id)
        all_example_starts.append(example.example_start)
        all_input_ids.append(example.input_ids)
        all_start_offsets.append(example.start_offset)
        all_end_offsets.append(example.end_offset)

        if no_target_label_ids is None:
            no_target_label_ids = example.target_label_ids is None
            if not no_target_label_ids:
                target_label_ids: List[LongTensor] = []

        if (example.target_label_ids is None) != no_target_label_ids:
            raise RuntimeError("Inconsistent examples at collate_examples!")

        if example.target_label_ids is not None:
            target_label_ids.append(example.target_label_ids)

    res = {
        "input_ids": pad_sequence(
            all_input_ids, batch_first=True, padding_value=padding_token_id
        ).long(),
        "labels": pad_images(
            target_label_ids, padding_value=-100, padding_length=(pad_length, None)
        )
        if not no_target_label_ids
        else None,
    }

    if return_batch_examples:
        res["examples"] = BatchedExamples(
            tuple(all_text_ids),
            tuple(all_example_starts),
            pad_sequence(
                all_input_ids, batch_first=True, padding_value=padding_token_id
            ).long(),
            pad_sequence(
                all_start_offsets, batch_first=True, padding_value=-100
            ).long(),
            pad_sequence(all_end_offsets, batch_first=True, padding_value=-100).long(),
        )
    return res


def batch_examples(
    examples: Iterable[Example],
    *,
    collate_fn: Callable[
        [Iterable[Example]], Dict[str, Union[BatchedExamples, LongTensor]]
    ],
    batch_size: int = 1,
) -> Iterable[Dict[str, Union[BatchedExamples, LongTensor]]]:
    """Groups examples into batches."""
    curr_batch = []
    for example in examples:
        if len(curr_batch) == batch_size:
            yield collate_fn(curr_batch)
            curr_batch = []

        curr_batch.append(example)

    if len(curr_batch):
        yield collate_fn(curr_batch)


def strided_split(
    text_id: int,
    encoding: EncodingFast,
    entities: Optional[Set[TypedSpan]] = None,
    *,
    category_mapping: Dict[str, int],
    no_entity_category: str,
    stride: int,
    max_sequence_length: int,
    max_entity_length: int,
    cls_token_id: int,
) -> Iterable[Example]:
    assert 0 < stride <= max_sequence_length

    sequence_length = len(encoding.ids)
    offset = torch.tensor(encoding.offsets, dtype=torch.long)

    target_label_ids: Optional[LongTensor] = None
    if entities is not None:
        token_start_mapping = {}
        token_end_mapping = {}
        for token_idx, (token_start, token_end) in enumerate(encoding.offsets):
            token_start_mapping[token_start] = token_idx
            token_end_mapping[token_end] = token_idx

        no_entity_category_id = category_mapping[no_entity_category]
        category_id_mapping = invert(category_mapping)

        text_length = len(encoding.ids)
        target_label_ids = torch.full(
            (text_length, max_entity_length),
            fill_value=no_entity_category_id,
            dtype=torch.long,
        ).long()
        for start, end, category in entities:
            try:
                token_start = token_start_mapping[start]
            except KeyError:
                if start + 1 in token_start_mapping:
                    logger.warning(f"changing {start} to {start + 1}")
                    token_start = token_start_mapping[start + 1]
                elif start - 1 in token_start_mapping:
                    logger.warning(f"changing {start} to {start - 1}")
                    token_start = token_start_mapping[start - 1]
                else:
                    logger.warning(
                        f"Skipped entity {category} at ({start} {end}) -- weird span"
                    )
                    continue

            try:
                token_end = token_end_mapping[end]
            except KeyError:  # for some reason some ends are shifted by one
                if end + 1 in token_end_mapping:
                    logger.warning(f"changing {end} to {end + 1}")
                    token_end = token_end_mapping[end + 1]
                elif end - 1 in token_end_mapping:
                    logger.warning(f"changing {end} to {end - 1}")
                    token_end = token_end_mapping[end - 1]
                else:
                    logger.warning(
                        f"Skipped entity {category} at ({start} {end}) -- weird span"
                    )
                    continue

            token_length = token_end - token_start
            if token_length >= max_entity_length:
                logger.warning(
                    f"Skipped entity {category} at ({start} {end}) -- too long"
                )
                continue

            prev_label = target_label_ids[token_start][token_length].item()

            if prev_label != no_entity_category_id:
                from_category = category_id_mapping[prev_label]
                logger.warning(
                    f"""rewriting entity of category
                     {from_category} with {category} at ({start} {end}) span"""
                )

            target_label_ids[token_start][token_length] = category_mapping[category]

    # split encoding into max_length-token chunks

    chunk_start = 0
    chunk_end = 0
    while chunk_start < sequence_length and chunk_end != sequence_length:
        chunk_end = min(
            chunk_start + max_sequence_length - 1, sequence_length
        )  # -1 for cls token
        ex = Example(
            text_id,
            chunk_start,
            torch.tensor(
                [cls_token_id] + encoding.ids[chunk_start:chunk_end], dtype=torch.long
            ).long(),
            torch.tensor(
                [-100] + offset[chunk_start:chunk_end, 0].tolist(), dtype=torch.long
            ).long(),
            torch.tensor(
                [-100] + offset[chunk_start:chunk_end, 1].tolist(), dtype=torch.long
            ).long(),
            torch.tensor(
                [[-100] * max_entity_length]
                + target_label_ids[chunk_start:chunk_end].tolist(),
                dtype=torch.long,
            ).long()
            if target_label_ids is not None
            else None,
        )
        yield ex
        chunk_start += stride
