from jaseci.jac.ir.passes.ir_pass import IrPass
from jaseci.jac.jsci_vm.disasm import DisAsm


class PrinterPass(IrPass):
    def __init__(self, to_screen=True, with_exit=False, **kwargs):
        super().__init__(**kwargs)
        self.to_screen = to_screen
        self.with_exit = with_exit
        self.output = []

    def enter_node(self, node):
        out = "Entering " if self.with_exit else "Encountering " + str(node)
        print(out) if self.to_screen else None
        self.output.append(out)
        if hasattr(node, "bytecode"):
            self.output += DisAsm().disassemble(node.bytecode, to_screen=self.to_screen)

    def exit_node(self, node):
        if self.with_exit:
            out = "Exiting " + str(node)
            print(out) if self.to_screen else None
            self.output.append(out)
