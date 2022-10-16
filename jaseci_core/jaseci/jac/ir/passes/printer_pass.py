from jaseci.jac.ir.passes.ir_pass import IrPass
from jaseci.jac.jsci_vm.disasm import DisAsm


class PrinterPass(IrPass):
    def __init__(self, *args):
        super().__init__(*args)

    def enter_node(self, node):
        print("Entering", node)
        if hasattr(node, "bytecode"):
            DisAsm().disassemble(node.bytecode)

    def exit_node(self, node):
        print("Exiting", node)
