from transformers import prune_layer
from jaseci.jac.ir.passes.ir_pass import IrPass


class PrunePass(IrPass):
    prune_able = [
        "expression",
        "connect",
        "logical",
        "compare",
        "arithmetic",
        "term",
        "factor",
    ]

    def enter_node(self, node):
        if node.name in self.prune_able and len(node.kid) == 1:
            node.kid = node.kid[0].kid

    def exit_node(self, node):
        pass
