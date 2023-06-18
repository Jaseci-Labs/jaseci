"""Utility functions and classes for Jac compilation toolchain."""
import re

import jaclang.jac.ast as ast
from jaclang.jac.parser import JacLexer
from jaclang.jac.parser import JacParser
from jaclang.jac.passes.ast_build_pass import AstBuildPass
from jaclang.jac.passes.ir_pass import parse_tree_to_ast as ptoa


def get_all_jac_keywords() -> str:
    """Get all Jac keywords as an or string."""
    ret = ""
    for k in JacLexer._remapping["NAME"].keys():
        ret += f"{k}|"
    return ret[:-1]


if __name__ == "__main__":
    print(get_all_jac_keywords())


def pascal_to_snake(pascal_string: str) -> str:
    """Convert pascal case to snake case."""
    snake_string = re.sub(r"(?<!^)(?=[A-Z])", "_", pascal_string).lower()
    return snake_string


def jac_file_to_ast(mod_path: str, base_path: str = None) -> ast.AstNode:
    """Convert a Jac file to an AST."""
    if base_path is None:
        base_path = ""
    lex = JacLexer()
    prse = JacParser()
    builder = AstBuildPass(mod_path=mod_path)
    prse.cur_file = mod_path
    ptree = prse.parse(
        lex.tokenize(open(base_path + mod_path).read()), filename=mod_path
    )
    return builder.run(node=ptoa(ptree))
