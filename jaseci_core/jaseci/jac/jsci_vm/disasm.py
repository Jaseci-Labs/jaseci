from jaseci.jac.jsci_vm.op_codes import JsOp, JsAttr


class DisAsm:
    def __init__(self):
        self.ip = 0
        self.bytecode = None
        self.asm = []

    def disassemble(self, bytecode, print_out=True):
        self.bytecode = bytearray(bytecode)
        while self.ip < len(self.bytecode):
            op = JsOp(self.bytecode[self.ip])
            if hasattr(self, f"dis_{op.name}"):
                getattr(self, f"dis_{op.name}")()
            else:
                self.asm.append([op.name])
            self.ip += 1
        if print_out:
            self.print()

    def print(self):
        for i in self.asm:
            print(*i)

    def dis_LOAD_CONST(self):  # noqa
        op = JsOp(self.bytecode[self.ip]).name
        typ = JsAttr(self.bytecode[self.ip + 1])
        byte_length = self.bytecode[self.ip + 2]
        val = None
        if typ == JsAttr.INT:
            val = int.from_bytes(
                self.bytecode[self.ip + 3 : self.ip + 3 + byte_length], "little"
            )
        self.asm.append([op, typ.name, byte_length, val])
        self.ip += 2 + byte_length
