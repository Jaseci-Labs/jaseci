import torch.nn.functional as F
import torch
import importlib


def nll_loss(output, target):
    loss = F.nll_loss(output, target)
    return loss


def cross_entropy_loss(output, target):
    loss = F.cross_entropy(output, target)
    return loss


def mse_loss(output, target):
    loss = F.mse_loss(output, target, reduction="mean")
    return loss


def contrastive_loss(output, target, margin=2.0):
    euclidean_distance = F.pairwise_distance(output[0], output[1], keepdim=True)
    loss_contrastive = torch.mean(
        (1 - target) * torch.pow(euclidean_distance, 2)
        + (target) * torch.pow(torch.clamp(margin - euclidean_distance, min=0.0), 2)
    )
    return loss_contrastive
