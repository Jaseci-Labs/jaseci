from jaseci.jac.jsci_vm.op_codes import JsCmp, JsOp, JsType, type_map
from jaseci.jac.jsci_vm.inst_ptr import InstPtr, from_bytes
from jaseci.utils.utils import logger
from base64 import b64decode


class DisAsm(InstPtr):
    def __init__(self):
        InstPtr.__init__(self)
        self._asm = []

    def disassemble(self, bytecode, to_screen=True, log_out=False):
        if type(bytecode) == str:
            bytecode = b64decode(bytecode.encode())
        self._bytecode = bytearray(bytecode)
        try:
            while self._ip < len(self._bytecode):
                op = JsOp(self._bytecode[self._ip])
                if hasattr(self, f"dis_{op.name}"):
                    getattr(self, f"dis_{op.name}")()
                else:
                    self._asm.append([op.name])
                self._ip += 1
            self.print() if to_screen else None
            self.log() if log_out else None
            return self._asm
        except Exception:
            logger.error(f"Disassembly Failed on Following Bytecode: {self._bytecode}")
            self.print() if to_screen else None
            self.log() if log_out else None

    def print(self):
        for i in self._asm:
            print(*i)

    def log(self):
        for i in self._asm:
            logger.info(str(i))

    def op_COMPARE(self):  # noqa
        ctyp = JsCmp(self.offset(1))
        self._asm.append([self.cur_op(), ctyp.name])
        self._ip += 1

    def op_INCREMENT(self):  # noqa
        ityp = JsCmp(self.offset(1))
        self._asm.append([self.cur_op(), ityp.name])
        self._ip += 1

    def dis_LOAD_CONST(self):  # noqa
        typ = JsType(self.offset(1))
        operand2 = self.offset(2)
        val = None
        if typ in [JsType.TYPE]:
            self._asm.append([self.cur_op(), typ.name, JsType(operand2).name])
            self._ip += 2
        elif typ in [JsType.INT]:
            val = from_bytes(type_map[typ], self.offset(3, operand2))
            self._asm.append([self.cur_op(), typ.name, operand2, val])
            self._ip += 2 + operand2
        elif typ in [JsType.STRING]:
            str_len = from_bytes(type_map[JsType.INT], self.offset(3, operand2))
            val = from_bytes(type_map[typ], self.offset(3 + operand2, str_len))
            self._asm.append([self.cur_op(), typ.name, operand2, str_len, val])
            self._ip += 2 + operand2 + str_len
        elif typ in [JsType.FLOAT]:
            val = from_bytes(float, self.offset(2, 8))
            self._asm.append([self.cur_op(), typ.name, val])
            self._ip += 1 + 8
        elif typ in [JsType.BOOL]:
            val = bool(self.offset(2))
            self._asm.append([self.cur_op(), typ.name, val])
            self._ip += 1 + 1

    def dis_LOAD_VAR(self):  # noqa
        name = from_bytes(str, self.offset(2, self.offset(1)))
        self._asm.append([self.cur_op(), self.offset(1), name])
        self._ip += 1 + self.offset(1)

    def dis_CREATE_VAR(self):  # noqa
        name = from_bytes(str, self.offset(2, self.offset(1)))
        self._asm.append([self.cur_op(), self.offset(1), name])
        self._ip += 1 + self.offset(1)

    def dis_DEBUG_INFO(self):  # noqa
        byte_len_l = self.offset(1)
        line = from_bytes(int, self.offset(2, byte_len_l))
        f_offset = byte_len_l + 2
        byte_len_f = self.offset(f_offset)
        jacfile = (
            from_bytes(str, self.offset(f_offset + 1, byte_len_f)) if byte_len_f else 0
        )
        self._asm.append([self.cur_op(), byte_len_l, line, byte_len_f, jacfile])
        self._ip += 2 + byte_len_l + byte_len_f
