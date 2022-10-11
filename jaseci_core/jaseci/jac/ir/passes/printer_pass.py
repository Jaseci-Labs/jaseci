from jaseci.jac.ir.passes.ir_pass import IrPass


class PrinterPass(IrPass):
    def __init__(self, *args):
        super().__init__(*args)

    def enter_node(self, node):
        print("Entering", node.name)

    def exit_node(self, node):
        print("Exiting", node.name)
