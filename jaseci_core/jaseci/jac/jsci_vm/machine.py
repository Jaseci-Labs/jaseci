from jaseci.jac.jsci_vm.op_codes import JsOp, JsAttr


class Stack(object):
    def __init__(self):
        self.stack = []

    def is_empty(self) -> bool:
        return len(self.stack) == 0

    def pop(self):
        if self.is_empty():
            raise Exception("stack is empty")
        return self.stack.pop()

    def push(self, value) -> None:
        self.stack.append(value)


class JaseciMachine(Stack):
    def __init__(self):
        Stack.__init__(self)
        self.ip = 0
        self.bytecode = None
        self.op = self.build_op_call()

    def build_op_call(self):
        op_map = {}
        for op in JsOp:
            op_map[op.value] = getattr(self, f"op_{op.name}")
        return op_map

    def run(self, bytecode):
        self.bytecode = bytecode
        while self.ip < len(self.bytecode):
            (opcode, oparg) = self.codes["instruction"][self.instruction_pointer]
            # branching statements for multiple opcode
            self.instruction_pointer += 1

    def op_PUSH_SCOPE(self):
        pass

    def op_POP_SCOPE(self):
        pass

    def op_PUSH(self):
        pass

    def op_ADD(self):
        pass

    def op_SUB(self):
        pass

    def op_LOAD_CONST(self):
        pass

    def op_LOAD_NAME(self):
        pass

    def op_REPORT(self):
        pass

    def op_ACTION_CALL(self):
        pass
