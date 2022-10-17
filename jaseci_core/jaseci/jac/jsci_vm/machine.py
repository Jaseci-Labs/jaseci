from jaseci.jac.jsci_vm.op_codes import JsOp, JsAttr, type_map
from jaseci.jac.machine.machine_state import MachineState
from jaseci.jac.jsci_vm.inst_ptr import InstPtr, from_bytes
from jaseci.jac.machine.jac_value import JacValue
from jaseci.jac.jsci_vm.disasm import DisAsm


class Stack(object):
    def __init__(self):
        self._stk = []

    def stack_is_empty(self) -> bool:
        return len(self._stk) == 0

    def pop(self):
        if self.stack_is_empty():
            raise Exception("JaseciMachine stack is empty")
        return self._stk.pop()

    def push(self, value):
        self._stk.append(value)

    def peak_stack(self, count=0):
        if not count:
            print(list(reversed(self._stk)))
        else:
            print(list(reversed(self._stk))[0:count])


class VirtualMachine(MachineState, Stack, InstPtr):
    def __init__(self, **kwargs):
        Stack.__init__(self)
        InstPtr.__init__(self)
        MachineState.__init__(self, **kwargs)
        self._op = self.build_op_call()
        self._cur_loc = None

    def reset_vm(self):
        Stack.__init__(self)
        InstPtr.__init__(self)
        self._cur_loc = None
        self._op = self.build_op_call()

    def build_op_call(self):
        op_map = {}
        for op in JsOp:
            op_map[op] = getattr(self, f"op_{op.name}")
        return op_map

    def run_bytecode(self, bytecode):
        self.reset_vm()
        self._bytecode = bytearray(bytecode)
        try:
            while self._ip < len(self._bytecode):
                self._op[self._bytecode[self._ip]]()
                self._ip += 1
        except Exception as e:
            self.disassemble(print_out=False, log_out=True)
            raise e

    def disassemble(self, print_out=True, log_out=False):
        return DisAsm().disassemble(self._bytecode, print_out, log_out)

    def op_PUSH_SCOPE(self):  # noqa
        pass

    def op_POP_SCOPE(self):  # noqa
        pass

    def op_ADD(self):  # noqa
        val = self.pop()
        val.value = val.value + self.pop().value
        self.push(val)

    def op_SUB(self):  # noqa
        val = self.pop()
        val.value = val.value - self.pop().value
        self.push(val)

    def op_LOAD_CONST(self):  # noqa
        typ = JsAttr(self.offset(1))
        operand2 = self.offset(2)
        if typ in [JsAttr.TYPE]:
            val = type_map[JsAttr(operand2)]
            self._ip += 2
        elif typ in [JsAttr.INT, JsAttr.STRING]:
            val = from_bytes(type_map[typ], self.offset(3, operand2))
            self._ip += 2 + operand2
        elif typ in [JsAttr.FLOAT]:
            val = from_bytes(float, self.offset(2, 8))
            self._ip += 2 + 8
        elif typ in [JsAttr.BOOL]:
            val = bool(self.offset(2))
            self._ip += 2 + 1
        self.push(JacValue(self, value=val))

    def op_LOAD_VAR(self):  # noqa
        name = from_bytes(str, self.offset(2, self.offset(1)))
        self.load_variable(name)
        self._ip += 1 + self.offset(1)

    def op_REPORT(self):  # noqa
        self.report.append(self.pop())

    def op_ACTION_CALL(self):  # noqa
        pass

    def op_DEBUG_INFO(self):  # noqa
        byte_len_l = self.offset(1)
        line = from_bytes(int, self.offset(2, byte_len_l))
        f_offset = byte_len_l + 2
        byte_len_f = self.offset(f_offset)
        jacfile = (
            from_bytes(str, self.offset(f_offset + 1, byte_len_f)) if byte_len_f else 0
        )
        self._cur_loc = [line, jacfile]
        self._ip += 2 + byte_len_l + byte_len_f
