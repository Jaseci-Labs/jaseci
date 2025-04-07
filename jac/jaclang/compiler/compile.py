"""Transpilation functions."""

from typing import Optional, Type

import jaclang.compiler.absyntree as ast
from jaclang.compiler.parser import JacParser
from jaclang.compiler.passes import Pass
from jaclang.compiler.passes.main import (
    JacImportPass,
    PyOutPass,
    SubNodeTabPass,
    SymTabBuildPass,
    pass_schedule,
)
from jaclang.compiler.passes.main.sym_tab_link_pass import SymTabLinkPass
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
        assert code.ir.jac_prog is not None
        for _, module in code.ir.jac_prog.modules.items():
            PyOutPass(input_ir=module, prior=code)
    return code


def jac_file_to_pass(
    file_path: str,
    target: Optional[Type[Pass]] = None,
    schedule: list[Type[Pass]] = pass_schedule,
) -> Pass:
    """Convert a Jac file to an AST."""
    with open(file_path, "r", encoding="utf-8") as file:
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
    from jaclang.runtimelib.machine import JacProgram

    from icecream import ic
    ic('inside compile',file_path,'')
    if not target:
        target = schedule[-1] if schedule else None
    source = ast.JacSource(jac_str, mod_path=file_path)
    ast_ret: Pass = JacParser(input_ir=source)
    SubNodeTabPass(ast_ret.ir, ast_ret)

    # Only return the parsed module when the schedules are empty
    if len(schedule) == 0:
        return ast_ret

    assert isinstance(ast_ret.ir, ast.Module)

    top_mod: ast.Module = ast_ret.ir
    top_mod.jac_prog = JacProgram(None, None, None)
    assert isinstance(ast_ret.ir, ast.Module)
    top_mod.jac_prog.last_imported.append(ast_ret.ir)
    top_mod.jac_prog.modules[ast_ret.ir.loc.mod_path] = ast_ret.ir

    while len(top_mod.jac_prog.last_imported) > 0:
        mod = top_mod.jac_prog.last_imported.pop()
        jac_ir_to_pass(ir=mod, schedule=[JacImportPass, SymTabBuildPass])

    # If there is syntax error, no point in processing in further passes.
    if len(ast_ret.errors_had) != 0:
        return ast_ret

    for mod in top_mod.jac_prog.modules.values():
        SymTabLinkPass(input_ir=mod, prior=ast_ret)

    def run_schedule(mod: ast.Module) -> None:
        nonlocal ast_ret
        for i in schedule:
            if i == target:
                break
            ast_ret = i(mod, prior=ast_ret)
        ast_ret = target(mod, prior=ast_ret) if target else ast_ret

    for mod in top_mod.jac_prog.modules.values():
        run_schedule(mod)

    ic('before name',ast_ret.ir.name)
    ic('before loc mod path ',ast_ret.ir.loc.mod_path)
    ast_ret.ir = top_mod
    # ast_ret.ir.loc.mod_path = file_path   # this will make error - set is not possible
    ic('after name',ast_ret.ir.name)
    ic('after loc mod path',ast_ret.ir.loc.mod_path)
    ic(ast_ret.ir.name)
    ic(ast_ret.ir.loc.mod_path)
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
        prse = i(input_ir=prse.ir, prior=prse)
    prse = target(input_ir=prse.ir, prior=prse)
    return prse
