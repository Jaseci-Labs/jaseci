from jaseci.jac.jsci_vm.op_codes import JsOp, JsAttr
from jaseci.jac.machine.machine_state import MachineState
from jaseci.jac.jsci_vm.inst_ptr import InstPtr, from_bytes


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

    def build_op_call(self):
        op_map = {}
        for op in JsOp:
            op_map[op.value] = getattr(self, f"op_{op.name}")
        return op_map

    def run_bytecode(self, bytecode):
        self._bytecode = bytearray(bytecode)
        while self._ip < len(self._bytecode):
            self._op[self._bytecode[self._ip]]()
            self._ip += 1

    def op_PUSH_SCOPE(self):  # noqa
        pass

    def op_POP_SCOPE(self):  # noqa
        pass

    def op_ADD(self):  # noqa
        self.push(self.pop() + self.pop())

    def op_SUB(self):  # noqa
        rhs = self.pop()
        self.push(self.pop() - rhs)

    def op_LOAD_CONST(self):  # noqa
        typ = JsAttr(self.offset(1))
        byte_len = self.offset(2)
        if typ == JsAttr.INT:
            val = from_bytes(int, self.offset(3, byte_len))
        self.push(val)
        self._ip += 2 + byte_len

    def op_REPORT(self):  # noqa
        self.report.append(self.pop())

    def op_ACTION_CALL(self):  # noqa
        pass

    def op_DEBUG_INFO(self):  # noqa
        byte_len_l = self.offset(1)
        line = from_bytes(int, self.offset(2, byte_len_l))
        byte_len_f = self.offset(3)
        jacfile = from_bytes(str, self.offset(4, byte_len_f)) if byte_len_f else 0
        self._cur_loc = [line, jacfile]
        self._ip += 2 + byte_len_l + byte_len_f
