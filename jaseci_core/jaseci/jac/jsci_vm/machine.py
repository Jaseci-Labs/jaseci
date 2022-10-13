from jaseci.jac.jsci_vm.op_codes import JsOp, JsAttr
from jaseci.jac.machine.machine_state import MachineState


class Stack(object):
    def __init__(self):
        self._stk = []

    def is_empty(self) -> bool:
        return len(self._stk) == 0

    def pop(self):
        if self.is_empty():
            raise Exception("JaseciMachine stack is empty")
        return self._stk.pop()

    def push(self, value):
        self._stk.append(value)

    def peak_stack(self, count=0):
        if not count:
            print(list(reversed(self._stk)))
        else:
            print(list(reversed(self._stk))[0:count])


class VirtualMachine(MachineState, Stack):
    def __init__(self, **kwargs):
        Stack.__init__(self)
        MachineState.__init__(self, **kwargs)
        self._ip = 0
        self._bytecode = None
        self._op = self.build_op_call()

    def build_op_call(self):
        op_map = {}
        for op in JsOp:
            op_map[op.value] = getattr(self, f"op_{op.name}")
        return op_map

    def run(self, bytecode):
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
        typ = JsAttr(self._bytecode[self._ip + 1])
        byte_length = self._bytecode[self._ip + 2]
        if typ == JsAttr.INT:
            val = int.from_bytes(
                self._bytecode[self._ip + 3 : self._ip + 3 + byte_length], "little"
            )
        self.push(val)
        self._ip += 2 + byte_length

    def op_LOAD_NAME(self):  # noqa
        pass

    def op_REPORT(self):  # noqa
        self.report.append(self.pop())

    def op_ACTION_CALL(self):  # noqa
        pass
