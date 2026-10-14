"""Actual direct FX export; shared scaffold is in direct_fx.py."""
import torch

def forward(self, x, w):
    mm_default = torch.ops.aten.mm.default(x, w);  x = w = None
    relu_default = torch.ops.aten.relu.default(mm_default)
    add_tensor = torch.ops.aten.add.Tensor(relu_default, mm_default);  relu_default = mm_default = None
    return add_tensor
