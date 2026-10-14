"""Manually built FX graphs: no Jac lowering, tracing, or torch.compile."""
import operator
import torch
from torch import fx, nn

mm = torch.ops.aten.mm.default
add = torch.ops.aten.add.Tensor
sub = torch.ops.aten.sub.Tensor
relu = torch.ops.aten.relu.default


def base(bias=False, condition=False):
    g = fx.Graph()
    x = g.placeholder('x')
    w = g.placeholder('w')
    b = g.placeholder('b') if bias else None
    c = g.placeholder('c') if condition else None
    return g, x, w, b, c


def linear():
    g, x, w, b, _ = base(bias=True)
    h = g.call_function(mm, (x, w))
    y = g.call_function(add, (h, b))
    g.output(y)
    g.lint()
    return fx.GraphModule(nn.Module(), g)


def residual():
    g, x, w, _, _ = base()
    h = g.call_function(mm, (x, w))
    r = g.call_function(relu, (h,))
    y = g.call_function(add, (r, h))
    g.output(y)
    g.lint()
    return fx.GraphModule(nn.Module(), g)


def branch_module(op):
    """Both real extracted branch graphs use explicit operands h and x."""
    branch = fx.Graph()
    h = branch.placeholder('h')
    x = branch.placeholder('x')
    y = branch.call_function(op, (h, x))
    # Match library Cond's fresh contiguous output and HOP no-alias contract.
    y = branch.call_function(torch.ops.aten.clone.default, (y,),
                             {'memory_format': torch.contiguous_format})
    branch.output((y,))
    branch.lint()
    return fx.GraphModule(nn.Module(), branch)


def cond_modules(g, root, true_op, false_op):
    """Construction helper: creates TWO branch GraphModules, not free closures."""
    root.add_module('true_branch', branch_module(true_op))
    root.add_module('false_branch', branch_module(false_op))
    return g.get_attr('true_branch'), g.get_attr('false_branch')


def conditional():
    g, x, w, _, c = base(condition=True)
    root = nn.Module()
    t, f = cond_modules(g, root, add, sub)
    h = g.call_function(mm, (x, w))
    result = g.call_function(torch.ops.higher_order.cond,
                             (c, t, f, (h, x)))
    y = g.call_function(operator.getitem, (result, 0))
    g.output(y)
    g.lint()
    return fx.GraphModule(root, g)
