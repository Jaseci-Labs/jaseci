"""A deferrable logger call before one that must stay eager: deferring the first
would emit it after the second, so the function keeps both eager."""
import torch;
import logging;

glob logger = logging.getLogger("gm_order");

@torch.compile()
def f(x: any) -> any {
    x = torch.relu(x);
    logger.warning("first");
    logger.warning("second", stack_info=True);
    return x * 2.0;
}
