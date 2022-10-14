from jaseci.jac.ir.passes.ir_pass import IrPass


class AstPrunePass(IrPass):
    def enter_node(self, node):
        if hasattr(node, "bytecode") and node.bytecode:
            node.kid = []
