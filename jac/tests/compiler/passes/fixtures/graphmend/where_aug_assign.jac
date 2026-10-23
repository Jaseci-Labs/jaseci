"""Augmented branch updates keep the old value and their operators, which a
plain torch.where assignment would drop, so predication must decline."""
import torch;

@torch.compile()
def update(y: any, a: any, b: any) -> any {
    if (a.sum() > 0) {
        y += a;
    } else {
        y -= b;
    }
    return y;
}
