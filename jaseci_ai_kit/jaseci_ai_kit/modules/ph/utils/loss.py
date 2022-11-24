import torch.nn.functional as F


def nll_loss(output, target):
    loss = F.nll_loss(output, target)
    return loss


def cross_entropy_loss(output, target):
    loss = F.cross_entropy(output, target)
    return loss


def mse_loss(output, target):
    loss = F.mse_loss(output, target, reduction="mean")
    return loss
