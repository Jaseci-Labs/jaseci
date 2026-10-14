"""Identical CPU float64 values; w is [in, out] in both frontends."""
import torch


def tensors():
    return dict(x=torch.tensor([[1., -2.], [.5, 3.]], dtype=torch.float64),
                w=torch.tensor([[.75, -1.], [2., .25]], dtype=torch.float64),
                b=torch.tensor([.1, -.2], dtype=torch.float64))
