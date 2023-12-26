"""Transpilation functions."""
from typing import Optional, Type

import jaclang.compiler.absyntree as ast
from jaclang.compiler.parser import JacParser
from jaclang.compiler.passes import Pass
from jaclang.compiler.passes.main import PyOutPass, pass_schedule
from jaclang.compiler.passes.tool import JacFormatPass
from jaclang.compiler.passes.tool.schedules import format_pass
from jaclang.compiler.passes.transform import Alert


def transpile_jac(file_path: str) -> list[Alert]:
    """Transpiler Jac file and return python code as string."""
    code = jac_file_to_pass(
        file_path=file_path,
        schedule=pass_schedule,
    )
    if isinstance(code.ir, ast.Module) and not code.errors_had:
        print_pass = PyOutPass(input_ir=code.ir, prior=code)
    else:
        return code.errors_had
    return print_pass.errors_had


def jac_file_to_pass(
    file_path: str,
    target: Optional[Type[Pass]] = None,
    schedule: list[Type[Pass]] = pass_schedule,
) -> Pass:
    """Convert a Jac file to an AST."""
    with open(file_path) as file:
        return jac_str_to_pass(
            jac_str=file.read(),
            file_path=file_path,
            target=target,
            schedule=schedule,
        )


def jac_str_to_pass(
    jac_str: str,
    file_path: str,
    target: Optional[Type[Pass]] = None,
    schedule: list[Type[Pass]] = pass_schedule,
) -> Pass:
    """Convert a Jac file to an AST."""
    if not target:
        target = schedule[-1]
    source = ast.JacSource(jac_str, mod_path=file_path)
    ast_ret: Pass = JacParser(input_ir=source)
    for i in schedule:
        if i == target:
            break
        ast_ret = i(input_ir=ast_ret.ir, prior=ast_ret)
    ast_ret = target(input_ir=ast_ret.ir, prior=ast_ret)
    return ast_ret


def jac_pass_to_pass(
    in_pass: Pass,
    target: Optional[Type[Pass]] = None,
    schedule: list[Type[Pass]] = pass_schedule,
) -> Pass:
    """Convert a Jac file to an AST."""
    if not target:
        target = schedule[-1]
    ast_ret = in_pass
    for i in schedule:
        if i == target:
            break
        ast_ret = i(input_ir=ast_ret.ir, prior=ast_ret)
    ast_ret = target(input_ir=ast_ret.ir, prior=ast_ret)
    return ast_ret


def jac_file_formatter(
    file_path: str,
    schedule: list[Type[Pass]] = format_pass,
) -> JacFormatPass:
    """Convert a Jac file to an AST."""
    target = JacFormatPass
    with open(file_path) as file:
        source = ast.JacSource(file.read(), mod_path=file_path)
        prse: Pass = JacParser(input_ir=source)
    for i in schedule:
        if i == target:
            break
        prse = target(input_ir=prse.ir, prior=prse)
    prse = target(input_ir=prse.ir, prior=prse)
    return prse
