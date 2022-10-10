from jaseci.jac.ir.passes.ir_pass import IrPass
from jaseci.jac.jsci_vm.op_codes import JsOp


class CodeGenPass(IrPass):
    def __init__(self, *args):
        super().__init__(*args)
        self.bytecode = b""

    # def run_gen(self, node):
    #     if hasattr(self, f"gen_{node.name}"):
    #         self.bytecode += getattr(self, f"gen_{node.name}")(node)
    #     else:
    #         for i in node.kid:
    #             self.run_gen(i)

    # def before_pass(self):
    #     self.run_gen(self.ir)
    #     return super().before_pass()

    def emit(self, item):
        self.bytecode += bytes(item)

    def enter_node(self, node):
        print("entering", node)
        if hasattr(self, f"enter_{node.name}"):
            self.bytecode += getattr(self, f"enter_{node.name}")(node)

    def exit_node(self, node):
        print("exiting", node)
        if hasattr(self, f"exit_{node.name}"):
            self.bytecode += getattr(self, f"exit_{node.name}")(node)

    def gen_walker_block(self, node):
        self.emit(JsOp.PUSH_SCOPE)
