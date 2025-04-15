"""Jac Machine module."""

from __future__ import annotations

import marshal
import os
import types
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
from jaclang.compiler.semtable import SemRegistry
from jaclang.utils.log import logging

logger = logging.getLogger(__name__)


class JacProgram:
    """Jac Program class.

    This class is used to represent a Jac program and its associated
    components, such as the abstract syntax tree (AST), bytecode, and
    semantic registry. It provides methods for compiling Jac files,
    generating bytecode, and managing the program's modules.
    """

    def __init__(self, main_file: str, mod_bundle: Optional[ast.Module] = None) -> None:
        """Initialize the JacProgram object."""
        self.main_file = main_file
        self.mod_bundle = mod_bundle
        self.sem_ir = SemRegistry()
        self.modules: dict[str, ast.Module] = {}
        self.last_imported: list[ast.Module] = []

    @property
    def main_module(self) -> Optional[ast.Module]:
        """Return the main module of the Jac program."""
        return self.modules[self.main_file]

    def get_bytecode(self, full_target: str) -> Optional[types.CodeType]:
        """Get the bytecode for a specific module."""
        if self.mod_bundle and isinstance(self.mod_bundle, ast.Module):
            codeobj = self.modules[full_target].gen.py_bytecode
            return marshal.loads(codeobj) if isinstance(codeobj, bytes) else None
        result = self.compile_jac(full_target)
        if result.errors_had:
            for alrt in result.errors_had:
                # We're not logging here, it already gets logged as the errors were added to the errors_had list.
                # Regardless of the logging, this needs to be sent to the end user, so we'll printing it to stderr.
                logger.error(alrt.pretty_print())
        ret_code = self.modules[full_target]
        if ret_code.gen.py_bytecode is not None:
            return marshal.loads(ret_code.gen.py_bytecode)
        else:
            return None

    def compile_jac(self, file_path: str) -> Pass:  # TODO: Come back and nix file_path
        """Start Compile for Jac file and return python code as string."""
        code = self.jac_file_to_pass(
            file_path=file_path,
            schedule=pass_schedule,
        )
        return code

    def jac_file_to_pass(
        self,
        file_path: Optional[str] = None,
        target: Optional[Type[Pass]] = None,
        schedule: list[Type[Pass]] = pass_schedule,
    ) -> Pass:
        """Convert a Jac file to an AST."""
        file_path = file_path or self.main_file
        with open(file_path, "r", encoding="utf-8") as file:
            return self.jac_str_to_pass(
                jac_str=file.read(),
                file_path=file_path,
                target=target,
                schedule=schedule,
            )

    def jac_str_to_pass(
        self,
        jac_str: str,
        file_path: Optional[str] = None,
        target: Optional[Type[Pass]] = None,
        schedule: list[Type[Pass]] = pass_schedule,
    ) -> Pass:
        """Convert a Jac file to an AST."""
        if not file_path:
            file_path = self.main_file
        if not target:
            target = schedule[-1] if schedule else None
        source = ast.JacSource(jac_str, mod_path=file_path)
        ast_ret: Pass = JacParser(input_ir=source)
        assert isinstance(ast_ret.ir, ast.Module)
        ast_ret.ir.jac_prog = self
        # TODO: This function below has tons of tech debt that should go away
        # when these functions become methods of JacProgram.
        SubNodeTabPass(ast_ret.ir, ast_ret)  # TODO: Get rid of this one

        # Only return the parsed module when the schedules are empty
        # or the target is SubNodeTabPass
        if len(schedule) == 0 or target == SubNodeTabPass:
            return ast_ret

        assert isinstance(ast_ret.ir, ast.Module)

        # Creating a new JacProgram and attaching it to top module
        self.last_imported.append(ast_ret.ir)
        self.modules[ast_ret.ir.loc.mod_path] = ast_ret.ir

        # Run JacImportPass & SymTabBuildPass on all imported Jac Programs
        while len(self.last_imported) > 0:
            mod = self.last_imported.pop()
            JacProgram.jac_ir_to_pass(
                ir=mod, schedule=[JacImportPass, SymTabBuildPass], target=target
            )

        # If there is syntax error, no point in processing in further passes.
        if len(ast_ret.errors_had) != 0:
            return ast_ret

        # TODO: we need a elegant way of doing this [should be genaralized].
        if target in (JacImportPass, SymTabBuildPass):
            return ast_ret

        # Link all Jac symbol tables created
        for mod in self.modules.values():
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
                ast_ret = current_pass(mod, prior=ast_ret)
            if final_pass:
                ast_ret = final_pass(mod, prior=ast_ret)

        for mod in self.modules.values():
            run_schedule(mod, schedule=schedule)

        # Check if we need to run without type checking then just return
        if "JAC_NO_TYPECHECK" in os.environ or target in py_code_gen:
            return ast_ret

        # Run TypeCheckingPass on the top module
        JacTypeCheckPass(ast_ret.ir, prior=ast_ret)

        # if "JAC_VSCE" not in os.environ:
        #     return ast_ret

        for mod in self.modules.values():
            run_schedule(mod, schedule=type_checker_sched)

        return ast_ret

    def jac_pass_to_pass(
        self,
        in_pass: Pass,
        target: Optional[Type[Pass]] = None,
        schedule: list[Type[Pass]] = pass_schedule,
    ) -> Pass:
        """Convert a Jac file to an AST."""
        from jaclang.runtimelib.machine import JacProgram

        ast_ret = in_pass
        assert isinstance(ast_ret.ir, ast.Module)
        ast_ret.ir.jac_prog = self
        SubNodeTabPass(ast_ret.ir, ast_ret)  # TODO: Get rid of this one
        # Only return the parsed module when the schedules are empty
        # or the target is SubNodeTabPass
        if len(schedule) == 0 or target == SubNodeTabPass:
            return ast_ret

        assert isinstance(ast_ret.ir, ast.Module)

        # Creating a new JacProgram and attaching it to top module
        self.last_imported.append(ast_ret.ir)
        self.modules[ast_ret.ir.loc.mod_path] = ast_ret.ir

        # Run JacImportPass & SymTabBuildPass on all imported Jac Programs
        while len(self.last_imported) > 0:
            mod = self.last_imported.pop()
            JacProgram.jac_ir_to_pass(
                ir=mod, schedule=[JacImportPass, SymTabBuildPass], target=target
            )

        # If there is syntax error, no point in processing in further passes.
        # if len(ast_ret.errors_had) != 0:
        #     return ast_ret

        # TODO: we need a elegant way of doing this [should be genaralized].
        if target in (JacImportPass, SymTabBuildPass):
            return ast_ret
        # Link all Jac symbol tables created
        for mod in self.modules.values():
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
                ast_ret = current_pass(mod, prior=ast_ret)
            if final_pass:
                ast_ret = final_pass(mod, prior=ast_ret)

        for mod in self.modules.values():
            run_schedule(mod, schedule=schedule)

        # Check if we need to run without type checking then just return
        if "JAC_NO_TYPECHECK" in os.environ or target in py_code_gen:
            return ast_ret

        # Run TypeCheckingPass on the top module
        JacTypeCheckPass(ast_ret.ir, prior=ast_ret)

        # if "JAC_VSCE" not in os.environ:
        #     return ast_ret

        for mod in self.modules.values():
            run_schedule(mod, schedule=type_checker_sched)
        return ast_ret

    @staticmethod
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

    @staticmethod
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
