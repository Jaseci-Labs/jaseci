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

    cull_able = ["ErrorChar"]

    def enter_node(self, node):
        cull_list = []
        for i in range(len(node.kid)):
            if node.kid[i].name in self.cull_able:
                cull_list.append(node.kid[i])
                continue
            peak = node.kid[i]
            while peak.name in self.prune_able and len(peak.kid) == 1:
                # print("PRUNING:", peak, "from", node.kid, "replacing", peak.kid[0])
                node.kid[i] = peak.kid[0]
                peak = peak.kid[0]
        for i in cull_list:
            node.kid.remove(i)
