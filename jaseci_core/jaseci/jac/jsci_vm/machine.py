from jaseci.jac.jsci_vm.op_codes import JsOp, JsAttr
from jaseci.jac.machine.machine_state import MachineState


class Stack(object):
    def __init__(self):
        self.stack = []

    def is_empty(self) -> bool:
        return len(self.stack) == 0

    def pop(self):
        if self.is_empty():
            raise Exception("stack is empty")
        return self.stack.pop()

    def push(self, value):
        self.stack.append(value)

    def peak_stack(self, count=0):
        if not count:
            print(list(reversed(self.stack)))
        else:
            print(list(reversed(self.stack))[0:count])


class BytecodeMachine(MachineState, Stack):
    def __init__(self, *args):
        Stack.__init__(self)
        MachineState.__init__(self, *args)
        self.ip = 0
        self.bytecode = None
        self.op = self.build_op_call()

    def build_op_call(self):
        op_map = {}
        for op in JsOp:
            op_map[op.value] = getattr(self, f"op_{op.name}")
        return op_map

    def run(self, bytecode):
        self.bytecode = bytearray(bytecode)
        while self.ip < len(self.bytecode):
            self.op[self.bytecode[self.ip]]()
            self.ip += 1

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
        typ = JsAttr(self.bytecode[self.ip + 1])
        byte_length = self.bytecode[self.ip + 2]
        if typ == JsAttr.INT:
            val = int.from_bytes(
                self.bytecode[self.ip + 3 : self.ip + 3 + byte_length], "little"
            )
        self.push(val)
        self.ip += 2 + byte_length

    def op_LOAD_NAME(self):  # noqa
        pass

    def op_REPORT(self):  # noqa
        self.report.append(self.pop())

    def op_ACTION_CALL(self):  # noqa
        pass
