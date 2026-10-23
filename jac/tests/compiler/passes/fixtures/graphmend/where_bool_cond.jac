"""Conditions Python can evaluate to a bool rather than a tensor: a boolean
operator, a negation, and a chained comparison. torch.where needs a tensor
predicate, so predication must decline."""
import torch;

@torch.compile()
def flag_gate(x: any, flag: bool) -> any {
    if flag and (x.sum() > 0) {
        return x * 2;
    } else {
        return x * 3;
    }
}

@torch.compile()
def negated(x: any) -> any {
    if not (x.sum() > 0) {
        return x * 2;
    } else {
        return x * 3;
    }
}

@torch.compile()
def chained(x: any) -> any {
    if 0 < x.sum() < 5 {
        return x * 2;
    } else {
        return x * 3;
    }
}
