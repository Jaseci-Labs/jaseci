"""Transpilation functions."""
from typing import Type, TypeVar

import jaclang.jac.absyntree as ast
from jaclang.jac.parser import JacParser
from jaclang.jac.passes import Pass
from jaclang.jac.passes.blue import (
    BluePygenPass,
    JacFormatPass,
    PyOutPass,
    pass_schedule,
)
from jaclang.jac.passes.blue.schedules import format_pass
from jaclang.jac.passes.transform import Alert


T = TypeVar("T", bound=Pass)


def transpile_jac_blue(file_path: str) -> list[Alert]:
    """Transpiler Jac file and return python code as string."""
    code = jac_file_to_pass(
        file_path=file_path,
        target=BluePygenPass,
        schedule=pass_schedule,
    )
    if isinstance(code.ir, ast.Module) and not code.errors_had:
        print_pass = PyOutPass(input_ir=code.ir, prior=code)
    else:
        return code.errors_had
    return print_pass.errors_had


def transpile_jac_purple(file_path: str) -> list[Alert]:
    """Transpiler Jac file and return python code as string."""
    from jaclang.jac.passes.purple import pass_schedule, PurplePygenPass

    code = jac_file_to_pass(
        file_path=file_path,
        target=PurplePygenPass,
        schedule=pass_schedule,
    )
    if isinstance(code.ir, ast.Module) and not code.errors_had:
        print_pass = PyOutPass(input_ir=code.ir, prior=code)
    else:
        return code.errors_had
    return print_pass.errors_had


def jac_file_to_pass(
    file_path: str,
    target: Type[T] = BluePygenPass,
    schedule: list[Type[T]] = pass_schedule,
) -> T:
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
    target: Type[T] = BluePygenPass,
    schedule: list[Type[T]] = pass_schedule,
) -> T:
    """Convert a Jac file to an AST."""
    source = ast.JacSource(jac_str, mod_path=file_path)
    ast_ret = JacParser(input_ir=source)
    for i in schedule:
        if i == target:
            break
        ast_ret = i(input_ir=ast_ret.ir, prior=ast_ret)
    ast_ret = target(input_ir=ast_ret.ir, prior=ast_ret)
    return ast_ret


def jac_file_formatter(
    file_path: str,
    schedule: list[Type[T]] = format_pass,
) -> JacFormatPass:
    """Convert a Jac file to an AST."""
    target = JacFormatPass
    with open(file_path) as file:
        source = ast.JacSource(file.read(), mod_path=file_path)
        prse = JacParser(input_ir=source)
        comments = prse.comments

    for i in schedule:
        if i == target:
            break
        prse = i(input_ir=prse.ir, prior=prse)
    prse = target(input_ir=prse.ir, prior=prse, comments=comments)
    return prse
