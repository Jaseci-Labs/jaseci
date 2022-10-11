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

    def __call__(self, cmd):
        self.codes = cmd
        while self.instruction_pointer < len(self.codes["instruction"]):
            (opcode, oparg) = self.codes["instruction"][self.instruction_pointer]
            # branching statements for multiple opcode
            self.instruction_pointer += 1
