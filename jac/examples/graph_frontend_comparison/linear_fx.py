"""Actual direct FX export; shared scaffold is in direct_fx.py."""
import torch

def forward(self, x, w, b):
    mm_default = torch.ops.aten.mm.default(x, w);  x = w = None
    add_tensor = torch.ops.aten.add.Tensor(mm_default, b);  mm_default = b = None
    return add_tensor
