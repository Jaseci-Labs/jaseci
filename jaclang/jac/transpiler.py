"""Transpilation functions."""
from typing import Type, TypeVar

import jaclang.jac.absyntree as ast
from jaclang.jac.ast_build import jac_file_to_ast_pass
from jaclang.jac.passes import Pass
from jaclang.jac.passes.blue import (
    BluePygenPass,
    pass_schedule,
)


T = TypeVar("T", bound=Pass)


def transpile_jac_file(file_path: str, base_dir: str) -> str:
    """Transpiler Jac file and return python code as string."""
    code = jac_file_to_final_pass(file_path=file_path, base_dir=base_dir).ir
    if isinstance(code, ast.Module):
        return code.meta["py_code"]
    else:
        raise ValueError("Transpilation of Jac file failed.")


def jac_file_to_pass(file_path: str, base_dir: str, target: Type[T]) -> T:
    """Convert a Jac file to an AST."""
    ast_ret = jac_file_to_ast_pass(file_path, base_dir)
    for i in pass_schedule:
        if i == target:
            break
        ast_ret = i(mod_path=file_path, input_ir=ast_ret.ir, base_path=base_dir)
    ast_ret = target(mod_path=file_path, input_ir=ast_ret.ir, base_path=base_dir)
    return ast_ret


def jac_file_to_final_pass(file_path: str, base_dir: str = "") -> Pass:
    """Convert a Jac file to an AST."""
    return jac_file_to_pass(file_path, base_dir, target=BluePygenPass)
