"""Ast Build Function."""
from jaclang.jac.parser import JacLexer
from jaclang.jac.parser import JacParser
from jaclang.jac.passes import Pass


def jac_file_to_ast_pass(file_path: str, base_dir: str) -> Pass:
    """Convert a Jac file to an AST."""
    with open(file_path) as file:
        lex = JacLexer(mod_path=file_path, input_ir=file.read(), base_path=base_dir).ir
        prse = JacParser(mod_path=file_path, input_ir=lex, base_path=base_dir)
        return prse
