"""Transpilation functions."""
from jaclang.jac.parser import JacLexer
from jaclang.jac.parser import JacParser
from jaclang.jac.passes.ast_build_pass import AstBuildPass
from jaclang.jac.passes.blue_pygen_pass import BluePygenPass
from jaclang.jac.passes.ir_pass import parse_tree_to_ast as ptoa


def transpile_jac_file(file_path: str) -> str:
    """Transpiler Jac file and return python code as string."""
    lex = JacLexer()
    prse = JacParser(cur_filename=file_path)
    builder = AstBuildPass(mod_name=file_path)
    pygen = BluePygenPass(mod_name=file_path)

    with open(file_path) as file:
        ptree = prse.parse(lex.tokenize(file.read()), filename=file_path)
        ast = builder.run(node=ptoa(ptree if ptree else ()))
        code = pygen.run(node=ast).meta["py_code"]
        return code
