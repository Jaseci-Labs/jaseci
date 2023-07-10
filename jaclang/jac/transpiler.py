"""Transpilation functions."""
from typing import Type, TypeVar

import jaclang.jac.absyntree as ast
from jaclang.jac.parser import JacLexer
from jaclang.jac.parser import JacParser
from jaclang.jac.passes import Pass
from jaclang.jac.passes.blue import BluePygenPass, pass_schedule
from jaclang.jac.transform import Transform


T = TypeVar("T", bound=Pass)


def jac_file_to_parse_tree(file_path: str, base_dir: str) -> Transform:
    """Convert a Jac file to an AST."""
    with open(file_path) as file:
        lex = JacLexer(mod_path=file_path, input_ir=file.read(), base_path=base_dir)
        prse = JacParser(
            mod_path=file_path, input_ir=lex.ir, base_path=base_dir, prior=lex
        )
        return prse


def transpile_jac_blue(file_path: str, base_dir: str) -> str:
    """Transpiler Jac file and return python code as string."""
    code = jac_file_to_pass(
        file_path=file_path, base_dir=base_dir, target=BluePygenPass
    )
    if isinstance(code.ir, ast.Module):
        return code.ir.meta["py_code"]
    else:
        raise ValueError("Transpilation of Jac file failed.")


def transpile_jac_purple(file_path: str, base_dir: str) -> str:
    """Transpiler Jac file and return python code as string."""
    from jaclang.jac.passes.purple import pass_schedule, PurplePygenPass

    code = jac_file_to_pass(
        file_path=file_path,
        base_dir=base_dir,
        target=PurplePygenPass,
        schedule=pass_schedule,
    )
    if isinstance(code.ir, ast.Module):
        return code.ir.meta["py_code"]
    else:
        raise ValueError("Transpilation of Jac file failed.")


def jac_file_to_pass(
    file_path: str,
    base_dir: str = "",
    target: Type[T] = BluePygenPass,
    schedule: list[Type[T]] = pass_schedule,
) -> T:
    """Convert a Jac file to an AST."""
    ast_ret = jac_file_to_parse_tree(file_path, base_dir)
    for i in schedule:
        if i == target:
            break
        ast_ret = i(
            mod_path=file_path, input_ir=ast_ret.ir, base_path=base_dir, prior=ast_ret
        )
    ast_ret = target(
        mod_path=file_path, input_ir=ast_ret.ir, base_path=base_dir, prior=ast_ret
    )
    return ast_ret
