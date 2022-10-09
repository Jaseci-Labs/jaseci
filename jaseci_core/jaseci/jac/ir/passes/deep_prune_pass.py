from jaseci.jac.ir.passes.ir_pass import IrPass


class DeepPrunePass(IrPass):
    direct_prune = [
        "SEMI",
    ]

    def __init__(self, *args):
        super().__init__(*args)
        self.count = 0

    def enter_node(self, node):
        node.kid = [x for x in node.kid if x.name not in self.direct_prune]
        self.view_prune_candidate(node)

    def view_prune_candidate(self, node):
        for i in range(len(node.kid)):
            peak = node.kid[i]
            if len(peak.kid) == 1:
                # print("Pruneable? - ", peak, "from", node.kid, "with", peak.kid[0])
                self.count += 1

    def after_pass(self):
        # print(self.count)
        return super().after_pass()
