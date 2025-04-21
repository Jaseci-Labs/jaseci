"""Jac Machine module."""

from __future__ import annotations

import ast as py_ast
import marshal
import os
import types
from typing import Optional, Type

import jaclang.compiler.absyntree as ast
from jaclang.compiler.absyntree import Module
from jaclang.compiler.parser import JacParser
from jaclang.compiler.passes import Pass
from jaclang.compiler.passes.main import (
    DefUsePass,
    JacImportPass,
    JacTypeCheckPass,
    PyBytecodeGenPass,
    PyCollectDepsPass,
    PyImportPass,
    PyastBuildPass,
    SymTabBuildPass,
    pass_schedule,
    py_code_gen,
    type_checker_sched,
)
from jaclang.compiler.passes.main.sym_tab_link_pass import SymTabLinkPass
from jaclang.compiler.passes.tool import FuseCommentsPass, JacFormatPass
from jaclang.compiler.semtable import SemRegistry
from jaclang.utils.log import logging


logger = logging.getLogger(__name__)


class JacProgram:
    """JacProgram to handle the Jac program-related functionalities."""

    def __init__(self) -> None:
        """Initialize the JacProgram object."""
        self.sem_ir = SemRegistry()
        self.modules: dict[str, Module] = {}
        self.last_imported: list[Module] = []

    def get_bytecode(self, full_target: str) -> Optional[types.CodeType]:
        """Get the bytecode for a specific module."""
        if full_target in self.modules:
            codeobj = self.modules[full_target].gen.py_bytecode
            return marshal.loads(codeobj) if isinstance(codeobj, bytes) else None

        result = self.compile_jac(full_target)
        if result.errors_had:
            for alrt in result.errors_had:
                logger.error(alrt.pretty_print())
        if result.root_ir.gen.py_bytecode is not None:
            return marshal.loads(result.root_ir.gen.py_bytecode)
        else:
            return None

    def compile_jac(self, file_path: str) -> Pass:
        """Start Compile for Jac file and return python code as string."""
        return self.jac_file_to_pass(
            file_path=file_path,
            schedule=pass_schedule,
        )

    def jac_file_to_pass(
        self,
        file_path: str,
        target: Optional[Type[Pass]] = None,
        schedule: list[Type[Pass]] = pass_schedule,
    ) -> Pass:
        """Convert a Jac file to an AST."""
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
        file_path: str,
        target: Optional[Type[Pass]] = None,
        schedule: list[Type[Pass]] = pass_schedule,
    ) -> Pass:
        """Convert a Jac file to an AST."""
        if not target:
            target = schedule[-1] if schedule else None

        source = ast.JacSource(jac_str, mod_path=file_path)
        ast_ret: Pass = JacParser(root_ir=source, prog=self)
        return self.run_pass_schedule(
            in_pass=ast_ret,
            target=target,
            schedule=schedule,
        )

    def py_str_to_pass(
        self,
        py_str: str,
        file_path: str,
        target: Optional[Type[Pass]] = None,
        schedule: list[Type[Pass]] = pass_schedule,
    ) -> Pass:
        """Convert a Jac file to an AST."""
        if not target:
            target = schedule[-1] if schedule else None
        parsed_ast = py_ast.parse(py_str)
        py_ast_build_pass = PyastBuildPass(
            root_ir=ast.PythonModuleAst(
                parsed_ast,
                orig_src=ast.JacSource(py_str, mod_path=file_path),
            ),
            prog=None,
        )
        return self.run_pass_schedule(
            in_pass=py_ast_build_pass,
            target=target,
            schedule=schedule,
        )

    def run_pass_schedule(
        self,
        in_pass: Pass,
        target: Optional[Type[Pass]] = None,
        schedule: list[Type[Pass]] = pass_schedule,
    ) -> Pass:
        """Convert a Jac file to an AST."""
        ast_ret = in_pass
        assert isinstance(ast_ret.root_ir, ast.Module)
        # Creating a new JacProgram and attaching it to top module
        top_mod: ast.Module = ast_ret.root_ir
        self.last_imported.append(ast_ret.root_ir)
        self.modules[ast_ret.root_ir.loc.mod_path] = ast_ret.root_ir

        # Only return the parsed module when the schedules are empty
        if len(schedule) == 0:
            return ast_ret

        # Run JacImportPass & SymTabBuildPass on all imported Jac Programs
        while len(self.last_imported) > 0:
            mod = self.last_imported.pop()
            JacImportPass(ir_root=mod, prior=ast_ret, prog=self)
            SymTabBuildPass(ir_root=mod, prior=ast_ret, prog=self)

        # If there is syntax error, no point in processing in further passes.
        if len(ast_ret.errors_had) != 0:
            return ast_ret

        # TODO: we need a elegant way of doing this [should be genaralized].
        if target in (JacImportPass, SymTabBuildPass):
            ast_ret.root_ir = top_mod
            return ast_ret

        # Link all Jac symbol tables created
        for mod in self.modules.values():
            SymTabLinkPass(ir_root=mod, prior=ast_ret, prog=self)

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
                ast_ret = current_pass(mod, prior=ast_ret, prog=self)
            if final_pass:
                ast_ret = final_pass(mod, prior=ast_ret, prog=self)

        for mod in self.modules.values():
            run_schedule(mod, schedule=schedule)

        # Check if we need to run without type checking then just return
        if "JAC_NO_TYPECHECK" in os.environ or target in py_code_gen:
            ast_ret.root_ir = top_mod
            return ast_ret

        # Run TypeCheckingPass on the top module
        JacTypeCheckPass(top_mod, prior=ast_ret, prog=self)

        # if "JAC_VSCE" not in os.environ:
        #     ast_ret.ir = top_mod
        #     return ast_ret

        for mod in self.modules.values():
            PyCollectDepsPass(mod, prior=ast_ret, prog=self)

        for mod in self.modules.values():
            self.last_imported.append(mod)
        # Run PyImportPass
        while len(self.last_imported) > 0:
            mod = self.last_imported.pop()
            PyImportPass(mod, prior=ast_ret, prog=self)

        # Link all Jac symbol tables created
        for mod in self.modules.values():
            SymTabLinkPass(ir_root=mod, prior=ast_ret, prog=self)

        for mod in self.modules.values():
            DefUsePass(mod, prior=ast_ret, prog=self)

        for mod in self.modules.values():
            run_schedule(mod, schedule=type_checker_sched)

        ast_ret.root_ir = top_mod
        return ast_ret

    @staticmethod
    def jac_file_formatter(
        file_path: str,
    ) -> JacFormatPass:
        """Convert a Jac file to an AST."""
        target = JacFormatPass
        with open(file_path) as file:
            source = ast.JacSource(file.read(), mod_path=file_path)
            prse: Pass = JacParser(root_ir=source, prog=None)
        for i in [FuseCommentsPass, JacFormatPass]:
            if i == target:
                break
            prse = i(ir_root=prse.root_ir, prior=prse, prog=None)
        prse = target(ir_root=prse.root_ir, prior=prse, prog=None)
        return prse
