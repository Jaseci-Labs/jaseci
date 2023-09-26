from jaclang.vendor.lark import Lark, Transformer, v_args


grammar = """
?start: sum

?sum: product
    | sum "+" product   -> add
    | sum "-" product   -> sub

?product: item
    | product "*" item  -> mul
    | product "/" item  -> div

?item: NUMBER           -> num
     | "(" sum ")"

%import common.NUMBER
%import common.WS
%ignore WS
"""


# We define a transformer to process the parsed data
class CalcTransformer(Transformer):
    @v_args(inline=True)
    def num(self, n):
        return float(n[0])

    def add(self, items):
        return sum(items)

    def sub(self, items):
        return items[0] - items[1]

    def mul(self, items):
        return items[0] * items[1]

    def div(self, items):
        return items[0] / items[1]


# We use the grammar and transformer to instantiate the parser
parser = Lark(grammar, parser="lalr", transformer=CalcTransformer())


def evaluate(expression):
    return parser.parse(expression)


# Test the parser
expr1 = "3 + 5 * (2 - 8)"
expr2 = "12.5 / 2.5 + 7"
print(f"{expr1} = {evaluate(expr1)}")
print(f"{expr2} = {evaluate(expr2)}")
