from abc import abstractmethod, ABCMeta

from torch import Tensor
from torch.nn import CosineSimilarity, Module


class Metric(Module, metaclass=ABCMeta):
    @abstractmethod
    def forward(self, x: Tensor, y: Tensor) -> Tensor:
        pass


class CosSimilarity(Module):
    def __init__(self, scale: float):
        super().__init__()
        self._scale = scale
        self._metric = CosineSimilarity(dim=-1)

    def forward(self, x: Tensor, y: Tensor) -> Tensor:
        return self._metric(x, y) / self._scale
