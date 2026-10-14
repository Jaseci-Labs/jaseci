"""Actual direct FX export; shared scaffold is in direct_fx.py."""
import torch

def forward(self, x, w, c):
    true_branch = self.true_branch
    false_branch = self.false_branch
    mm_default = torch.ops.aten.mm.default(x, w);  w = None
    cond = torch.ops.higher_order.cond(c, true_branch, false_branch, (mm_default, x));  c = true_branch = false_branch = mm_default = x = None
    getitem = cond[0];  cond = None
    return getitem

# Branch GraphModule: true_branch
def forward(self, h, x):
    add_tensor = torch.ops.aten.add.Tensor(h, x);  h = x = None
    clone_default = torch.ops.aten.clone.default(add_tensor, memory_format = torch.contiguous_format);  add_tensor = None
    return (clone_default,)

# Branch GraphModule: false_branch
def forward(self, h, x):
    sub_tensor = torch.ops.aten.sub.Tensor(h, x);  h = x = None
    clone_default = torch.ops.aten.clone.default(sub_tensor, memory_format = torch.contiguous_format);  sub_tensor = None
    return (clone_default,)
