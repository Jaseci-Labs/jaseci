"""Ast Build Function."""
from os import path

import jaclang.jac.absyntree as ast
from jaclang.jac.parser import JacLexer
from jaclang.jac.parser import JacParser
from jaclang.jac.passes.ast_build_pass import AstBuildPass


def jac_file_to_ast(file_path: str, base_dir: str) -> ast.AstNode:
    """Convert a Jac file to an AST."""
    target = path.normpath(path.join(base_dir, file_path))
    with open(target) as file:
        lex = JacLexer(mod_path=file_path, input_ir=file.read(), base_path=base_dir).ir
        prse = JacParser(mod_path=file_path, input_ir=lex, base_path=base_dir).ir
        ast_ret = AstBuildPass(mod_path=file_path, input_ir=prse, base_path=base_dir).ir
        if not isinstance(ast_ret, ast.AstNode):
            raise ValueError("Parsing of Jac file failed.")
        return ast_ret
