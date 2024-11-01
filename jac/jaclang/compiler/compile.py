"""Transpilation functions."""

from typing import Optional, Type

import jaclang.compiler.absyntree as ast
from jaclang.compiler.parser import JacParser
from jaclang.compiler.passes import Pass
from jaclang.compiler.passes.main import PyOutPass, pass_schedule
from jaclang.compiler.passes.tool import JacFormatPass
from jaclang.compiler.passes.tool.schedules import format_pass


def compile_jac(file_path: str, cache_result: bool = False) -> Pass:
    """Start Compile for Jac file and return python code as string."""
    code = jac_file_to_pass(
        file_path=file_path,
        schedule=pass_schedule,
    )
    # If there is syntax error, the code will be an instance of JacParser as there is
    # no more passes were processed, in that case we can ignore it.
    had_syntax_error = isinstance(code, JacParser) and len(code.errors_had) != 0
    if cache_result and (not had_syntax_error) and isinstance(code.ir, ast.Module):
        print_pass = PyOutPass(input_ir=code.ir, prior=code)
        return print_pass
    return code


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
        target = schedule[-1] if schedule else None
    source = ast.JacSource(jac_str, mod_path=file_path)
    ast_ret: Pass = JacParser(input_ir=source)

    # If there is syntax error, no point in processing in further passes.
    if len(ast_ret.errors_had) != 0:
        return ast_ret

    for i in schedule:
        if i == target:
            break
        ast_ret = i(input_ir=ast_ret.ir, prior=ast_ret)
    ast_ret = target(input_ir=ast_ret.ir, prior=ast_ret) if target else ast_ret
    return ast_ret


def jac_ir_to_pass(
    ir: ast.AstNode,
    target: Optional[Type[Pass]] = None,
    schedule: list[Type[Pass]] = pass_schedule,
) -> Pass:
    """Convert a Jac file to an AST."""
    if not target:
        target = schedule[-1] if schedule else None
    ast_ret = (
        Pass(input_ir=ir, prior=None)
        if not len(schedule)
        else schedule[0](input_ir=ir, prior=None)
    )
    for i in schedule[1:]:
        if i == target:
            break
        ast_ret = i(input_ir=ast_ret.ir, prior=ast_ret)
    ast_ret = target(input_ir=ast_ret.ir, prior=ast_ret) if target else ast_ret
    return ast_ret


def jac_pass_to_pass(
    in_pass: Pass,
    target: Optional[Type[Pass]] = None,
    schedule: list[Type[Pass]] = pass_schedule,
) -> Pass:
    """Convert a Jac file to an AST."""
    if not target:
        target = schedule[-1] if schedule else None
    ast_ret = in_pass
    for i in schedule:
        if i == target:
            break
        ast_ret = i(input_ir=ast_ret.ir, prior=ast_ret)
    ast_ret = target(input_ir=ast_ret.ir, prior=ast_ret) if target else ast_ret
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
