"""Transpilation functions."""
import jaclang.jac.absyntree as ast
from jaclang.jac.ast_build import jac_file_to_ast
from jaclang.jac.passes.ast_enrich_pass import AstEnrichmentPass
from jaclang.jac.passes.blue_pygen_pass import BluePygenPass
from jaclang.jac.passes.import_pass import ImportPass
from jaclang.jac.passes.sub_node_tab_pass import SubNodeTabPass


def transpile_jac_file(file_path: str, base_dir: str) -> str:
    """Transpiler Jac file and return python code as string."""
    code = jac_file_to_final_pass(file_path=file_path, base_dir=base_dir).ir
    if isinstance(code, ast.Module):
        return code.meta["py_code"]
    else:
        raise ValueError("Transpilation of Jac file failed.")


def pass_schedule(file_path: str, base_dir: str) -> ast.AstNode:
    """Convert a Jac file to an AST."""
    ast_ret = jac_file_to_ast(file_path, base_dir)
    ast_ret = SubNodeTabPass(
        mod_path=file_path, input_ir=ast_ret, base_path=base_dir
    ).ir
    ast_ret = ImportPass(mod_path=file_path, input_ir=ast_ret, base_path=base_dir).ir
    ast_ret = AstEnrichmentPass(
        mod_path=file_path, input_ir=ast_ret, base_path=base_dir
    ).ir
    if not isinstance(ast_ret, ast.AstNode):
        raise ValueError("Parsing of Jac file failed.")
    return ast_ret


def jac_file_to_final_pass(file_path: str, base_dir: str) -> BluePygenPass:
    """Convert a Jac file to an AST."""
    return BluePygenPass(
        mod_path=file_path,
        input_ir=pass_schedule(file_path, base_dir),
    )
