from enum import Enum
from typing import TypeVar, Dict, List, Any, Optional, Tuple

# from sklearn.metrics import f1_score, recall_score, precision_score
# from transformers import EvalPrediction
import numpy as np
import torch
from torch import Tensor
from torch.nn.functional import pad

_K = TypeVar("_K")
_V = TypeVar("_V")


def invert(d: Dict[_K, _V]) -> Dict[_V, _K]:
    return {v: k for k, v in d.items()}


_Tensor = TypeVar("_Tensor", bound=Tensor)


def pad_images(
    images: List[_Tensor],
    *,
    padding_value: Any = 0.0,
    padding_length: Tuple[Optional[int], Optional[int]],
) -> _Tensor:
    """Pad images to equal length (maximum height and width)."""
    max_height, max_width = padding_length

    shapes = torch.tensor(
        list(map(lambda t: t.shape, images)), dtype=torch.long
    ).transpose(0, 1)
    max_height = shapes[-2].max() if max_height is None else max_height
    max_width = shapes[-1].max() if max_width is None else max_width

    ignore_dims = len(images[0].shape) - 2

    image_batch = [
        # The needed padding is the difference between the
        # max width/height and the image's actual width/height.
        pad(
            img,
            [
                *([0, 0] * ignore_dims),
                0,
                max_width - img.shape[-1],
                0,
                max_height - img.shape[-2],
            ],
            value=padding_value,
        )
        for img in images
    ]
    return torch.stack(image_batch)


def to_numpy(tensor: Tensor) -> np.ndarray:
    return tensor.detach().cpu().numpy()


class DatasetType(str, Enum):
    TRAIN = "train"
    DEV = "dev"
    TEST = "test"


# def compute_metrics(
#     evaluation_results: EvalPrediction,
#     category_id_mapping: Dict[int, str],
#     no_entity_category_id: int,
# ) -> Dict[str, float]:

#     padding_mask = evaluation_results.label_ids != -100

#     label_ids = evaluation_results.label_ids[padding_mask]
#     predictions = evaluation_results.predictions[padding_mask]

#     unique_label_ids = set(np.unique(label_ids[label_ids != no_entity_category_id]))

#     labels = sorted(category_id_mapping.keys())
#     f1_category_scores = f1_score(
#         label_ids, predictions, average=None, labels=labels, zero_division=0
#     )
#     recall_category_scores = recall_score(
#         label_ids, predictions, average=None, labels=labels, zero_division=0
#     )
#     precision_category_scores = precision_score(
#         label_ids, predictions, average=None, labels=labels, zero_division=0
#     )
#     results: Dict[str, float] = {}
#     sum_f1 = 0
#     sum_recall = 0
#     sum_precision = 0
#     for category_id, f1, recall, precision in zip(
#         labels, f1_category_scores, recall_category_scores, precision_category_scores
#     ):
#         if category_id == no_entity_category_id:
#             # logger.info(f'O: {f1}, {recall}, {precision}')
#             continue

#         if category_id not in unique_label_ids:
#             # logger.info(f'Skipping {category_id}: {f1}, {recall}, {precision}')
#             continue

#         category = category_id_mapping[category_id]
#         results[f"F1_{category}"] = f1
#         results[f"Recall_{category}"] = recall
#         results[f"Precision_{category}"] = precision
#         sum_f1 += f1
#         sum_recall += recall
#         sum_precision += precision

#     num_categories = len(category_id_mapping) - 1

#     results["F1_macro"] = sum_f1 / num_categories
#     results["Recall_macro"] = sum_recall / num_categories
#     results["Precision_macro"] = sum_precision / num_categories
#     return results


def get_category_id_mapping(model_args: Dict, category_name=None):
    category_names = sorted(category_name)
    category_id_mapping = dict(enumerate(category_names))
    category_id_mapping[model_args["unk_entity_type_id"]] = model_args["unk_category"]
    return category_id_mapping
