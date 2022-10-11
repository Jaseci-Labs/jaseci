from jaseci.jac.ir.passes.ir_pass import IrPass
from jaseci.jac.jsci_vm.op_codes import JsOp, JsAttr


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

    def emit(self, *items):
        for i in items:
            self.bytecode += bytes(i)

    def enter_node(self, node):
        print("entering", node)
        if hasattr(self, f"enter_{node.name}"):
            getattr(self, f"enter_{node.name}")(node)

    def exit_node(self, node):
        print("exiting", node)
        if hasattr(self, f"exit_{node.name}"):
            getattr(self, f"exit_{node.name}")(node)

    def enter_walker_block(self, node):
        self.emit(JsOp.PUSH_SCOPE)

    def exit_walker_block(self, node):
        self.emit(JsOp.PUSH_SCOPE)

    def exit_arithmetic(self, node):
        self.emit(JsOp.ADD if node.kid[1] == "PLUS" else JsOp.SUB)

    def exit_report_action(self, node):
        self.emit(JsOp.REPORT)

    def exit_INT(self, node):  # noqa
        self.emit(JsOp.LOAD_CONST, JsAttr.INT, int(node.token_text()))
