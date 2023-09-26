from jaclang.utils.lark import Lark, Transformer


# Grammar without imports
grammar = """
    start: expr
    expr: expr "+" term -> add
        | term
    term: term "*" factor -> mul
        | factor
    factor: NUMBER -> num
          | "(" expr ")"
    NUMBER: /\d+/
    WS: /\s+/
    %ignore WS
"""

# Lark parser
parser = Lark(grammar)


# Transformer class to handle parsed tree
class ArithmeticTransformer(Transformer):
    def add(self, items):
        print(items[0], items[1])

    def mul(self, items):
        print(items[0], items[1])

    def num(self, items):
        print(int(items[0]))


# Using the parser and transformer
expr = "3 + 5 * 2"
tree = parser.parse(expr)
result = ArithmeticTransformer().transform(tree)
print(result)  # Outputs: 13
