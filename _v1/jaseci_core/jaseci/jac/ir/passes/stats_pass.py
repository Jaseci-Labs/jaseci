from jaseci.jac.ir.passes.ir_pass import IrPass
import sys


class StatsPass(IrPass):
    def __init__(self, *args):
        super().__init__(*args)
        self.stats = {"node_count": 0, "ir_size_kb": 0}

    def enter_node(self, node):
        self.stats["node_count"] += 1
        self.stats["ir_size_kb"] += sys.getsizeof(node) / 1024

    def after_pass(self):
        self.stats["ir_size_kb"] = round(self.stats["ir_size_kb"], 2)
        print(self.stats, "\n")
