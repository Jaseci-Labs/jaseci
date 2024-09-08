class IrPass:
    def __init__(self, ir=None):
        self.ir = ir

    def before_pass(self):
        pass

    def after_pass(self):
        pass

    def enter_node(self, node):
        pass

    def exit_node(self, node):
        pass

    def run(self):
        self.before_pass()
        self.traverse()
        self.after_pass()
        return self

    def traverse(self, node=None):
        if node is None:
            node = self.ir
        self.enter_node(node)
        for i in node.kid:
            self.traverse(i)
        self.exit_node(node)
