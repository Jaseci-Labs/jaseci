"""Jac Machine module."""

from __future__ import annotations

import ast as py_ast
import marshal
import os
import types
from typing import Optional

import jaclang.compiler.unitree as uni
from jaclang.compiler.parser import JacParser
from jaclang.compiler.passes import UniPass
from jaclang.compiler.passes.main import (
    CompilerMode,
    DefUsePass,
    JacImportPass,
    JacTypeCheckPass,
    PyBytecodeGenPass,
    PyCollectDepsPass,
    PyImportPass,
    PyastBuildPass,
    SymTabBuildPass,
    py_code_gen,
    type_checker_sched,
)
from jaclang.compiler.passes.main.sym_tab_link_pass import SymTabLinkPass
from jaclang.compiler.passes.tool import FuseCommentsPass, JacFormatPass
from jaclang.compiler.passes.transform import Alert, Transform
from jaclang.compiler.unitree import Module
from jaclang.settings import settings
from jaclang.utils.log import logging


logger = logging.getLogger(__name__)


class JacProgram:
    """JacProgram to handle the Jac program-related functionalities."""

    def __init__(self, main_mod: Optional[uni.ProgramModule] = None) -> None:
        """Initialize the JacProgram object."""
        self.mod: uni.ProgramModule = main_mod or uni.ProgramModule()
        self.last_imported: list[Module] = []
        self.py_raise_map: dict[str, str] = {}
        self.unexpected_eof: bool = False
        self.errors_had: list[Alert] = []
        self.warnings_had: list[Alert] = []

    def get_bytecode(
        self, full_target: str, full_compile: bool = True
    ) -> Optional[types.CodeType]:
        """Get the bytecode for a specific module."""
        if self.mod and full_target in self.mod.hub:
            codeobj = self.mod.hub[full_target].gen.py_bytecode
            return marshal.loads(codeobj) if isinstance(codeobj, bytes) else None
        result = self.compile(file_path=full_target, full_compile=full_compile)
        if self.errors_had:
            for alrt in self.errors_had:
                logger.error(alrt.pretty_print())
        if result.gen.py_bytecode is not None:
            return marshal.loads(result.gen.py_bytecode)
        else:
            return None

    def compile(
        self,
        file_path: str,
        mode: CompilerMode = CompilerMode.COMPILE,
        full_compile: bool = True,
    ) -> uni.Module:
        """Convert a Jac file to an AST."""
        with open(file_path, "r", encoding="utf-8") as file:
            return self.compile_from_str(
                source_str=file.read(),
                file_path=file_path,
                mode=mode,
                full_compile=full_compile,
            )

    def compile_from_str(
        self,
        source_str: str,
        file_path: str,
        mode: CompilerMode = CompilerMode.COMPILE,
        full_compile: bool = True,
    ) -> uni.Module:
        """Convert a Jac file to an AST."""
        if file_path.endswith(".py"):
            parsed_ast = py_ast.parse(source_str)
            py_ast_ret: Transform[uni.PythonModuleAst, uni.Module] = PyastBuildPass(
                ir_in=uni.PythonModuleAst(
                    parsed_ast,
                    orig_src=uni.Source(source_str, mod_path=file_path),
                ),
                prog=self,
            )
            ast_ret: (
                Transform[uni.PythonModuleAst, uni.Module]
                | Transform[uni.Source, uni.Module]
            ) = py_ast_ret
        else:
            source = uni.Source(source_str, mod_path=file_path)
            jac_ast_ret: Transform[uni.Source, uni.Module] = JacParser(
                root_ir=source, prog=self
            )
            ast_ret = jac_ast_ret
        if ast_ret.errors_had:
            return ast_ret.ir_out
        if self.mod.main.stub_only:
            self.mod = uni.ProgramModule(ast_ret.ir_out)
        self.mod.hub[ast_ret.ir_out.loc.mod_path] = ast_ret.ir_out
        return self.run_pass_schedule(
            mod_targ=ast_ret.ir_out,
            mode=mode,
            full_compile=full_compile,
        )

    def run_pass_schedule(
        self,
        mod_targ: uni.Module,
        mode: CompilerMode = CompilerMode.COMPILE,
        full_compile: bool = True,
    ) -> uni.Module:
        """Convert a Jac file to an AST."""
        self.last_imported.append(mod_targ)
        self.annex_impl(mod_targ)
        SymTabBuildPass(ir_in=mod_targ, prog=self)
        if mode == CompilerMode.PARSE:
            return mod_targ
        if not full_compile:
            self.schedule_runner(mod_targ, mode=mode)
            return mod_targ
        else:
            while len(self.last_imported) > 0:
                mod = self.last_imported.pop()
                JacImportPass(ir_in=mod, prog=self)
        if len(self.errors_had):
            return mod_targ
        else:
            return self.run_whole_program_schedule(
                mod_targ=mod_targ,
                mode=mode,
            )

    def run_whole_program_schedule(
        self,
        mod_targ: uni.Module,
        mode: CompilerMode = CompilerMode.COMPILE,
    ) -> uni.Module:
        """Convert a Jac file to an AST."""
        for mod in self.mod.hub.values():
            SymTabLinkPass(ir_in=mod, prog=self)

        for mod in self.mod.hub.values():
            self.schedule_runner(mod, mode=CompilerMode.COMPILE)

        # Check if we need to run without type checking then just return
        if mode == CompilerMode.COMPILE:
            return mod_targ

        # Run TypeCheckingPass on the top module
        JacTypeCheckPass(mod_targ, prog=self)

        for mod in self.mod.hub.values():
            PyCollectDepsPass(mod, prog=self)

        for mod in self.mod.hub.values():
            self.last_imported.append(mod)
        # Run PyImportPass
        while len(self.last_imported) > 0:
            mod = self.last_imported.pop()
            PyImportPass(mod, prog=self)

        # Link all Jac symbol tables created
        for mod in self.mod.hub.values():
            SymTabLinkPass(ir_in=mod, prog=self)

        for mod in self.mod.hub.values():
            DefUsePass(mod, prog=self)

        for mod in self.mod.hub.values():
            self.schedule_runner(mod, mode=CompilerMode.TYPECHECK)

        return mod_targ

    def annex_impl(self, node: uni.Module) -> None:
        """Annex impl and test modules."""
        if node.stub_only:
            return
        if not node.loc.mod_path:
            logger.error("Module has no path")
        if not node.loc.mod_path.endswith(".jac"):
            return
        base_path = node.loc.mod_path[:-4]
        directory = os.path.dirname(node.loc.mod_path)
        if not directory:
            directory = os.getcwd()
            base_path = os.path.join(directory, base_path)
        impl_folder = base_path + ".impl"
        test_folder = base_path + ".test"
        search_files = [
            os.path.join(directory, impl_file) for impl_file in os.listdir(directory)
        ]
        if os.path.exists(impl_folder):
            search_files += [
                os.path.join(impl_folder, impl_file)
                for impl_file in os.listdir(impl_folder)
            ]
        if os.path.exists(test_folder):
            search_files += [
                os.path.join(test_folder, test_file)
                for test_file in os.listdir(test_folder)
            ]
        for cur_file in search_files:
            if node.loc.mod_path.endswith(cur_file):
                continue
            if (
                cur_file.startswith(f"{base_path}.")
                or impl_folder == os.path.dirname(cur_file)
            ) and cur_file.endswith(".impl.jac"):
                mod = self.compile(file_path=cur_file, mode=CompilerMode.PARSE)
                if mod:
                    node.add_kids_left(mod.kid, parent_update=True, pos_update=False)
                    node.impl_mod.append(mod)
            if (
                cur_file.startswith(f"{base_path}.")
                or test_folder == os.path.dirname(cur_file)
            ) and cur_file.endswith(".test.jac"):
                mod = self.compile(file_path=cur_file, mode=CompilerMode.PARSE)
                if mod and not settings.ignore_test_annex:
                    node.test_mod.append(mod)
                    node.add_kids_right(mod.kid, parent_update=True, pos_update=False)

    def schedule_runner(
        self,
        mod: uni.Module,
        mode: CompilerMode = CompilerMode.COMPILE,
    ) -> None:
        """Run premade passes on the module."""
        final_pass: Optional[type[UniPass]] = None
        passes = py_code_gen if mode == CompilerMode.COMPILE else type_checker_sched
        for current_pass in passes:
            if current_pass == PyBytecodeGenPass:
                final_pass = current_pass
                break
            current_pass(mod, prog=self)
        if final_pass:
            final_pass(mod, prog=self)

    @staticmethod
    def jac_file_formatter(file_path: str) -> str:
        """Convert a Jac file to an AST."""
        target = JacFormatPass
        prog = JacProgram()
        with open(file_path) as file:
            source = uni.Source(file.read(), mod_path=file_path)
            prse: Transform = JacParser(root_ir=source, prog=prog)
        for i in [FuseCommentsPass, JacFormatPass]:
            prse = i(ir_in=prse.ir_out, prog=prog)
        prse = target(ir_in=prse.ir_out, prog=prog)
        prse.errors_had = prog.errors_had
        prse.warnings_had = prog.warnings_had
        return prse.ir_out.gen.jac

    @staticmethod
    def jac_str_formatter(source_str: str, file_path: str) -> str:
        """Convert a Jac file to an AST."""
        prog = JacProgram()
        source = uni.Source(source_str, mod_path=file_path)
        prse: Transform = JacParser(root_ir=source, prog=prog)
        for i in [FuseCommentsPass, JacFormatPass]:
            prse = i(ir_in=prse.ir_out, prog=prog)
        prse.errors_had = prog.errors_had
        prse.warnings_had = prog.warnings_had
        return prse.ir_out.gen.jac if not prse.errors_had else source_str
