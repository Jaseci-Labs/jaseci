import torch.nn.functional as F
import torch
import importlib.util


def nll_loss(output, target):
    loss = F.nll_loss(output, target)
    return loss


def cross_entropy_loss(output, target):
    loss = F.cross_entropy(output, target)
    return loss


def mse_loss(output, target):
    loss = F.mse_loss(output, target, reduction="mean")
    return loss


class CustomLoss(torch.nn.Module):
    def __init__(self, python_file: str = "heads/custom.py", **kwargs):
        super().__init__()
        # import the python file
        spec = importlib.util.spec_from_file_location("module.name", python_file)
        foo = importlib.util.module_from_spec(spec)  # type: ignore
        spec.loader.exec_module(foo)  # type: ignore
        self.loss = foo.CustomLoss(**kwargs)

    def forward(self, output, target):
        loss = self.loss(output, target)
        return loss
