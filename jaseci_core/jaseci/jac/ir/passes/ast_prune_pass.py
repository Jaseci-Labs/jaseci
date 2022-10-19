from jaseci.jac.ir.passes.ir_pass import IrPass
from base64 import b64encode


class AstPrunePass(IrPass):
    def enter_node(self, node):
        if hasattr(node, "bytecode") and node.bytecode:
            node.bytecode = b64encode(node.bytecode).decode()
            node.kid = [] if node.name != "inc_assign" else [node.kid[0]]
