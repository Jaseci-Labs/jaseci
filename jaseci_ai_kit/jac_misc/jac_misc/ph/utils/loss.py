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


class VectorSimilarityLoss(torch.nn.Module):
    def __init__(self, output_dim=128):
        super(VectorSimilarityLoss, self).__init__()
        self.output_dim = output_dim

    def forward(self, output, target):
        output1, output2 = output[:, : self.output_dim], output[:, self.output_dim :]
        similarity = torch.nn.functional.cosine_similarity(output1, output2, dim=1)
        target = target.float()
        loss = torch.nn.functional.cross_entropy(similarity, target)
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
