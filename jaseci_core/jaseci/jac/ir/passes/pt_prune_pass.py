from jaseci.jac.ir.passes.ir_pass import IrPass


class ParseTreePrunePass(IrPass):
    prune_able = [
        "connect",
        "logical",
        "compare",
        "arithmetic",
        "term",
        "factor",
        "power",
    ]

    def enter_node(self, node):
        for i in range(len(node.kid)):
            peak = node.kid[i]
            while peak.name in self.prune_able and len(peak.kid) == 1:
                # print("PRUNING:", peak, "from", node.kid, "replacing", peak.kid[0])
                node.kid[i] = peak.kid[0]
                peak = peak.kid[0]
