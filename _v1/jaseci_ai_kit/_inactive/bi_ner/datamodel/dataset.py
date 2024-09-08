from typing import Iterable
from torch.utils.data import Dataset
from .example import Example


class NERDataset(Dataset[Example]):
    def __init__(self, examples: Iterable[Example]):
        self._examples = list(examples)

    def __getitem__(self, index) -> Example:
        return self._examples[index]

    def __len__(self):
        return len(self._examples)
