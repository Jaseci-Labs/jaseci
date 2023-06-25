"""Ast Build Function."""
import jaclang.jac.absyntree as ast
from jaclang.jac.parser import JacLexer
from jaclang.jac.parser import JacParser
from jaclang.jac.passes.ast_build_pass import AstBuildPass


def jac_file_to_ast(file_path: str) -> ast.AstNode:
    """Convert a Jac file to an AST."""
    with open(file_path) as file:
        lex = JacLexer(mod_path=file_path, input_ir=file.read()).ir
        prse = JacParser(mod_path=file_path, input_ir=lex).ir
        ast_ret = AstBuildPass(mod_path=file_path, input_ir=prse).ir
        if not isinstance(ast_ret, ast.AstNode):
            raise ValueError("Parsing of Jac file failed.")
        return ast_ret
