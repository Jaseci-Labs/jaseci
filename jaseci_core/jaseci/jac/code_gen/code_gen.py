"""
Code generator for jac code in AST form
"""


class code_gen():
    """Shared code generator class across both sentinels and walkers"""

    def __init__(self):
        self.machine_code = []

    def g_ins(self, ins):
        """Generates op with specified parameters"""
        self.machine_code.append(ins)

    def g_lab(self, name):
        """Inserts label in code"""
        self.machine_code.append(name)
