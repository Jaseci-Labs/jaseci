from jaseci.jac.ir.passes.ir_pass import IrPass


class CodeGenPass(IrPass):
    def __init__(self, *args):
        super().__init__(*args)
        self.bytecode = None

    def enter_node(self, node):
        print("entering", node)
        if hasattr(self, f"enter_{node.name}"):
            self.bytecode += getattr(self, f"enter_{node.name}")(node)

    def exit_node(self, node):
        print("exiting", node)
        if hasattr(self, f"exit_{node.name}"):
            self.bytecode += getattr(self, f"exit_{node.name}")(node)
