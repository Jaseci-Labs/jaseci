from jaseci.jac.jsci_vm.op_codes import JsOp, JsAttr
from jaseci.jac.jsci_vm.inst_ptr import InstPtr, from_bytes


class DisAsm(InstPtr):
    def __init__(self):
        InstPtr.__init__(self)
        self._asm = []

    def disassemble(self, bytecode, print_out=True):
        self._bytecode = bytearray(bytecode)
        while self._ip < len(self._bytecode):
            op = JsOp(self._bytecode[self._ip])
            if hasattr(self, f"dis_{op.name}"):
                getattr(self, f"dis_{op.name}")()
            else:
                self._asm.append([op.name])
            self._ip += 1
        if print_out:
            self.print()

    def print(self):
        for i in self._asm:
            print(*i)

    def dis_LOAD_CONST(self):  # noqa
        typ = JsAttr(self.offset(1))
        byte_len = self.offset(2)
        val = None
        if typ == JsAttr.INT:
            val = from_bytes(int, self.offset(3, byte_len))
        self._asm.append([self.cur_op(), typ.name, byte_len, val])
        self._ip += 2 + byte_len

    def dis_DEBUG_INFO(self):  # noqa
        byte_len_l = self.offset(1)
        line = from_bytes(int, self.offset(2, byte_len_l))
        byte_len_f = self.offset(3)
        jacfile = from_bytes(str, self.offset(4, byte_len_f)) if byte_len_f else 0
        self._asm.append([self.cur_op(), byte_len_l, line, byte_len_f, jacfile])
        self._ip += 2 + byte_len_l + byte_len_f
