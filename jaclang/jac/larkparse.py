import os

from jaclang.vendor.lark import Lark, Transformer, v_args

with open(os.path.join(os.path.dirname(__file__), "jac.lark"), "r") as f:
    c_like_grammar = f.read()

parser = Lark(c_like_grammar)

test_code = """
int main() {
    int a;
    a = 5;
    if (a == 5) {
        return 1;
    } else {
        return 0;
    }
}

int add(int x, int y) {
    return x + y;
}
"""

tree = parser.parse(test_code)
print(tree.pretty())
