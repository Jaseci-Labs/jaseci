from jaseci.jac.jsci_vm.op_codes import JsOp, JsAttr


def from_bytes(typ, val):
    if typ == str:
        return val.decode("utf-8")
    else:
        return typ.from_bytes(val, "little")


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
            self.print()
        if print_out:
            self.print()

    def offset(self, delta, range=0):
        if range:
            return self.bytecode[self.ip + delta : self.ip + delta + range]
        return self.bytecode[self.ip + delta]

    def cur_op(self):
        return JsOp(self.offset(0)).name

    def print(self):
        for i in self.asm:
            print(*i)

    def dis_LOAD_CONST(self):  # noqa
        typ = JsAttr(self.offset(1))
        byte_len = self.offset(2)
        val = None
        if typ == JsAttr.INT:
            val = from_bytes(int, self.offset(3, byte_len))
        self.asm.append([self.cur_op(), typ.name, byte_len, val])
        self.ip += 2 + byte_len

    def dis_DEBUG_INFO(self):  # noqa
        byte_len_l = self.offset(1)
        line = from_bytes(int, self.offset(2, byte_len_l))
        byte_len_f = self.offset(3)
        jacfile = from_bytes(str, self.offset(4, byte_len_f))
        self.asm.append([self.cur_op(), byte_len_l, line, byte_len_f, jacfile])
        self.ip += 2 + byte_len_l + byte_len_f
