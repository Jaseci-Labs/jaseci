from jaseci.jac.ir.passes.ir_pass import IrPass
from jaseci.jac.jsci_vm.op_codes import JsOp, JsAttr


class CodeGenPass(IrPass):
    def __init__(self, *args):
        super().__init__(*args)
        self.bytecode = bytearray()

    def emit(self, *items):
        for i in items:
            if type(i) is bytes:
                self.bytecode += bytearray(i)
            else:
                self.bytecode.append(i)

    def enter_node(self, node):
        if hasattr(self, f"enter_{node.name}"):
            getattr(self, f"enter_{node.name}")(node)

    def exit_node(self, node):
        if hasattr(self, f"exit_{node.name}"):
            getattr(self, f"exit_{node.name}")(node)

    def enter_walker_block(self, node):
        self.emit(JsOp.PUSH_SCOPE)

    def exit_walker_block(self, node):
        self.emit(JsOp.PUSH_SCOPE)

    def exit_arithmetic(self, node):
        self.emit(JsOp.ADD if node.kid[1].name == "PLUS" else JsOp.SUB)

    def exit_report_action(self, node):
        self.emit(JsOp.REPORT)

    def exit_INT(self, node):  # noqa
        val = int(node.token_text())
        self.emit(
            JsOp.LOAD_CONST,
            JsAttr.INT,
            val.bit_length(),
            val.to_bytes(length=val.bit_length(), byteorder="little"),
        )
