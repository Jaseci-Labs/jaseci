"""Transpilation functions."""

import os
from typing import Optional, Type

import jaclang.compiler.absyntree as ast
from jaclang.compiler.parser import JacParser
from jaclang.compiler.passes import Pass
from jaclang.compiler.passes.main import (
    JacImportPass,
    JacTypeCheckPass,
    PyBytecodeGenPass,
    SubNodeTabPass,
    SymTabBuildPass,
    pass_schedule,
    py_code_gen,
    type_checker_sched,
)
from jaclang.compiler.passes.main.sym_tab_link_pass import SymTabLinkPass
from jaclang.compiler.passes.tool import JacFormatPass
from jaclang.compiler.passes.tool.schedules import format_pass
from jaclang.settings import settings


def __debug_print(args: str = "") -> None:
    if settings.compile_debug:
        if args == "":
            print()
        else:
            print("[JAC_COMPILE]", args)


def compile_jac(file_path: str, cache_result: bool = False) -> Pass:
    """Start Compile for Jac file and return python code as string."""
    return jac_file_to_pass(
        file_path=file_path,
        schedule=pass_schedule,
    )


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
    from jaclang.compiler.program import JacProgram

    if not target:
        target = schedule[-1] if schedule else None

    source = ast.JacSource(jac_str, mod_path=file_path)
    ast_ret: Pass = JacParser(input_ir=source)
    # TODO: This function below has tons of tech debt that should go away
    # when these functions become methods of JacProgram.
    SubNodeTabPass(ast_ret.ir, ast_ret)  # TODO: Get rid of this one

    # Only return the parsed module when the schedules are empty
    # or the target is SubNodeTabPass
    if len(schedule) == 0 or target == SubNodeTabPass:
        return ast_ret

    assert isinstance(ast_ret.ir, ast.Module)

    # Creating a new JacProgram and attaching it to top module
    top_mod: ast.Module = ast_ret.ir
    top_mod.jac_prog = JacProgram(None, None, None)
    top_mod.jac_prog.last_imported.append(ast_ret.ir)
    top_mod.jac_prog.modules[ast_ret.ir.loc.mod_path] = ast_ret.ir

    # Run JacImportPass & SymTabBuildPass on all imported Jac Programs
    while len(top_mod.jac_prog.last_imported) > 0:
        mod = top_mod.jac_prog.last_imported.pop()
        __debug_print(f"Parsing {mod.name}")
        jac_ir_to_pass(ir=mod, schedule=[JacImportPass, SymTabBuildPass], target=target)

    # If there is syntax error, no point in processing in further passes.
    if len(ast_ret.errors_had) != 0:
        return ast_ret

    # TODO: we need a elegant way of doing this [should be genaralized].
    if target in (JacImportPass, SymTabBuildPass):
        ast_ret.ir = top_mod
        return ast_ret

    # Link all Jac symbol tables created
    for mod in top_mod.jac_prog.modules.values():
        SymTabLinkPass(input_ir=mod, prior=ast_ret)

    # Run all passes till PyBytecodeGenPass
    # Here the passes will run one by one on the imported modules instead
    # of running on  a huge AST
    def run_schedule(mod: ast.Module, schedule: list[type[Pass]]) -> None:
        nonlocal ast_ret
        final_pass: Optional[type[Pass]] = None
        for current_pass in schedule:
            if current_pass in (target, PyBytecodeGenPass):
                final_pass = current_pass
                break
            __debug_print(f"\tRunning {current_pass} on {mod.name}")
            ast_ret = current_pass(mod, prior=ast_ret)
        if final_pass:
            __debug_print(f"\tRunning {final_pass} on {mod.name}")
            ast_ret = final_pass(mod, prior=ast_ret)

    for mod in top_mod.jac_prog.modules.values():
        __debug_print(f"### Running first layer of schdules on {mod.name} ####")
        run_schedule(mod, schedule=schedule)

    # Check if we need to run without type checking then just return
    if "JAC_NO_TYPECHECK" in os.environ or target in py_code_gen:
        ast_ret.ir = top_mod
        return ast_ret

    # Run TypeCheckingPass on the top module
    __debug_print()
    __debug_print(f"Running JacTypeCheckPass on {top_mod.name}")
    __debug_print()
    JacTypeCheckPass(top_mod, prior=ast_ret)

    # if "JAC_VSCE" not in os.environ:
    #     ast_ret.ir = top_mod
    #     return ast_ret

    for mod in top_mod.jac_prog.modules.values():
        __debug_print(f"### Running second layer of schdules on {mod.name} ####")
        run_schedule(mod, schedule=type_checker_sched)

    ast_ret.ir = top_mod
    return ast_ret


def jac_pass_to_pass(
    in_pass: Pass,
    target: Optional[Type[Pass]] = None,
    schedule: list[Type[Pass]] = pass_schedule,
) -> Pass:
    """Convert a Jac file to an AST."""
    from jaclang.compiler.program import JacProgram

    ast_ret = in_pass

    SubNodeTabPass(ast_ret.ir, ast_ret)  # TODO: Get rid of this one
    # Only return the parsed module when the schedules are empty
    # or the target is SubNodeTabPass
    if len(schedule) == 0 or target == SubNodeTabPass:
        return ast_ret

    assert isinstance(ast_ret.ir, ast.Module)

    # Creating a new JacProgram and attaching it to top module
    top_mod: ast.Module = ast_ret.ir
    top_mod.jac_prog = JacProgram(None, None, None)
    top_mod.jac_prog.last_imported.append(ast_ret.ir)
    top_mod.jac_prog.modules[ast_ret.ir.loc.mod_path] = ast_ret.ir

    # Run JacImportPass & SymTabBuildPass on all imported Jac Programs
    while len(top_mod.jac_prog.last_imported) > 0:
        mod = top_mod.jac_prog.last_imported.pop()
        __debug_print(f"Parsing {mod.name}")
        jac_ir_to_pass(ir=mod, schedule=[JacImportPass, SymTabBuildPass], target=target)

    # If there is syntax error, no point in processing in further passes.
    # if len(ast_ret.errors_had) != 0:
    #     return ast_ret

    # TODO: we need a elegant way of doing this [should be genaralized].
    if target in (JacImportPass, SymTabBuildPass):
        ast_ret.ir = top_mod
        return ast_ret
    # Link all Jac symbol tables created
    for mod in top_mod.jac_prog.modules.values():
        SymTabLinkPass(input_ir=mod, prior=ast_ret)

    # Run all passes till PyBytecodeGenPass
    # Here the passes will run one by one on the imported modules instead
    # of running on  a huge AST
    def run_schedule(mod: ast.Module, schedule: list[type[Pass]]) -> None:
        nonlocal ast_ret
        final_pass: Optional[type[Pass]] = None
        for current_pass in schedule:
            if current_pass in (target, PyBytecodeGenPass):
                final_pass = current_pass
                break
            __debug_print(f"\tRunning {current_pass} on {mod.name}")
            ast_ret = current_pass(mod, prior=ast_ret)
        if final_pass:
            __debug_print(f"\tRunning {final_pass} on {mod.name}")
            ast_ret = final_pass(mod, prior=ast_ret)

    for mod in top_mod.jac_prog.modules.values():
        __debug_print(f"### Running first layer of schdules on {mod.name} ####")
        run_schedule(mod, schedule=schedule)

    # Check if we need to run without type checking then just return
    if "JAC_NO_TYPECHECK" in os.environ or target in py_code_gen:
        ast_ret.ir = top_mod
        return ast_ret

    # Run TypeCheckingPass on the top module
    __debug_print()
    __debug_print(f"Running JacTypeCheckPass on {top_mod.name}")
    __debug_print()
    JacTypeCheckPass(top_mod, prior=ast_ret)

    # if "JAC_VSCE" not in os.environ:
    #     ast_ret.ir = top_mod
    #     return ast_ret

    for mod in top_mod.jac_prog.modules.values():
        __debug_print(f"### Running second layer of schdules on {mod.name} ####")
        run_schedule(mod, schedule=type_checker_sched)
    ast_ret.ir = top_mod
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
    if schedule[0] == target:
        return ast_ret

    for i in schedule[1:]:
        if i == target:
            break
        ast_ret = i(input_ir=ast_ret.ir, prior=ast_ret)
    if target and target in schedule:
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
