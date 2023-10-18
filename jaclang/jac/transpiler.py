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


def transpile_jac_blue(file_path: str, base_dir: str) -> list[Alert]:
    """Transpiler Jac file and return python code as string."""
    code = jac_file_to_pass(
        file_path=file_path,
        base_dir=base_dir,
        target=BluePygenPass,
        schedule=pass_schedule,
    )
    if isinstance(code.ir, ast.Module) and not code.errors_had:
        print_pass = PyOutPass(
            mod_path=file_path, input_ir=code.ir, base_path=base_dir, prior=code
        )
    else:
        return code.errors_had
    return print_pass.errors_had


def transpile_jac_purple(file_path: str, base_dir: str) -> list[Alert]:
    """Transpiler Jac file and return python code as string."""
    from jaclang.jac.passes.purple import pass_schedule, PurplePygenPass

    code = jac_file_to_pass(
        file_path=file_path,
        base_dir=base_dir,
        target=PurplePygenPass,
        schedule=pass_schedule,
    )
    if isinstance(code.ir, ast.Module) and not code.errors_had:
        print_pass = PyOutPass(
            mod_path=file_path, input_ir=code.ir, base_path=base_dir, prior=code
        )
    else:
        return code.errors_had
    return print_pass.errors_had


def jac_file_to_pass(
    file_path: str,
    base_dir: str = "",
    target: Type[T] = BluePygenPass,
    schedule: list[Type[T]] = pass_schedule,
) -> T:
    """Convert a Jac file to an AST."""
    with open(file_path) as file:
        return jac_str_to_pass(file.read(), file_path, base_dir, target, schedule)


def jac_str_to_pass(
    jac_str: str,
    file_path: str,
    base_dir: str = "",
    target: Type[T] = BluePygenPass,
    schedule: list[Type[T]] = pass_schedule,
) -> T:
    """Convert a Jac file to an AST."""
    source = ast.SourceString(jac_str)
    ast_ret = JacParser(
        mod_path=file_path, input_ir=source, base_path=base_dir, prior=None
    )
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


def jac_file_formatter(
    file_path: str,
    base_dir: str = "",
    schedule: list[Type[T]] = format_pass,
) -> JacFormatPass:
    """Convert a Jac file to an AST."""
    target = JacFormatPass
    with open(file_path) as file:
        source = ast.SourceString(file.read())
        prse = JacParser(
            mod_path=file_path, input_ir=source, base_path=base_dir, prior=None
        )
        comments = prse.comments

    for i in schedule:
        if i == target:
            break
        prse = i(
            mod_path=file_path,
            input_ir=prse.ir,
            base_path=base_dir,
            prior=prse,
        )
    prse = target(
        mod_path=file_path,
        input_ir=prse.ir,
        base_path=base_dir,
        prior=prse,
        comments=comments,
    )
    return prse
