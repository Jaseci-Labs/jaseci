"""Jac Machine module."""

from __future__ import annotations

import ast as py_ast
import marshal
import os
import types
from typing import Optional, Type

import jaclang.compiler.unitree as uni
from jaclang.compiler.parser import JacParser
from jaclang.compiler.passes import AstPass
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
from jaclang.compiler.passes.transform import Alert, Transform
from jaclang.compiler.semtable import SemRegistry
from jaclang.compiler.unitree import Module
from jaclang.settings import settings
from jaclang.utils.log import logging


logger = logging.getLogger(__name__)


class JacProgram:
    """JacProgram to handle the Jac program-related functionalities."""

    def __init__(self, main_mod: Optional[uni.ProgramModule] = None) -> None:
        """Initialize the JacProgram object."""
        self.sem_ir = SemRegistry()
        self.mod: uni.ProgramModule = main_mod if main_mod else uni.ProgramModule()
        self.last_imported: list[Module] = []
        self.py_raise_map: dict[str, str] = {}
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
        if result.errors_had:
            for alrt in result.errors_had:
                logger.error(alrt.pretty_print())
        if result.ir_out.gen.py_bytecode is not None:
            return marshal.loads(result.ir_out.gen.py_bytecode)
        else:
            return None

    def compile(
        self,
        file_path: str,
        target: Optional[Type[AstPass]] = None,
        schedule: list[Type[AstPass]] = pass_schedule,
        full_compile: bool = True,
    ) -> Transform:
        """Convert a Jac file to an AST."""
        with open(file_path, "r", encoding="utf-8") as file:
            return self.compile_from_str(
                source_str=file.read(),
                file_path=file_path,
                target=target,
                schedule=schedule,
                full_compile=full_compile,
            )

    def compile_from_str(
        self,
        source_str: str,
        file_path: str,
        target: Optional[Type[AstPass]] = None,
        schedule: list[Type[AstPass]] = pass_schedule,
        full_compile: bool = True,
    ) -> Transform:
        """Convert a Jac file to an AST."""
        if not target:
            target = schedule[-1] if schedule else None
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
            return ast_ret
        return self.run_pass_schedule(
            cur_pass=ast_ret,
            target=target,
            schedule=schedule,
            full_compile=full_compile,
        )

    def run_pass_schedule(
        self,
        cur_pass: Transform,
        target: Optional[Type[AstPass]] = None,
        schedule: list[Type[AstPass]] = pass_schedule,
        full_compile: bool = True,
    ) -> Transform:
        """Convert a Jac file to an AST."""
        top_mod = cur_pass.ir_out
        if self.mod.main.stub_only:
            self.mod = uni.ProgramModule(top_mod)
        # Creating a new JacProgram and attaching it to top module
        self.mod.hub[cur_pass.ir_out.loc.mod_path] = cur_pass.ir_out

        self.last_imported.append(cur_pass.ir_out)
        self.annex_impl(cur_pass.ir_out)
        # Only return the parsed module when the schedules are empty
        if len(schedule) == 0:
            return cur_pass

        # Run all passes till PyBytecodeGenPass
        # Here the passes will run one by one on the imported modules instead
        # of running on  a huge AST
        def run_schedule(mod: uni.Module, schedule: list[type[AstPass]]) -> None:
            nonlocal cur_pass
            final_pass: Optional[type[AstPass]] = None
            for current_pass in schedule:
                if current_pass in (target, PyBytecodeGenPass):
                    final_pass = current_pass
                    break
                cur_pass = current_pass(mod, prog=self)
            if final_pass:
                cur_pass = final_pass(mod, prog=self)

        if not full_compile:
            cur_pass = SymTabBuildPass(ir_in=top_mod, prog=self)
            run_schedule(top_mod, schedule=schedule)
            cur_pass.ir_out = top_mod
            return cur_pass

        # Run JacImportPass & SymTabBuildPass on all imported Jac Programs
        while len(self.last_imported) > 0:
            mod = self.last_imported.pop()
            JacImportPass(ir_in=mod, prog=self)

        for mod in self.mod.hub.values():
            SymTabBuildPass(ir_in=mod, prog=self)

        # If there is syntax error, no point in processing in further passes.
        if len(cur_pass.errors_had) != 0:
            return cur_pass

        # TODO: we need a elegant way of doing this [should be genaralized].
        if target in (JacImportPass, SymTabBuildPass):
            cur_pass.ir_out = top_mod
            return cur_pass

        # Link all Jac symbol tables created
        for mod in self.mod.hub.values():
            SymTabLinkPass(ir_in=mod, prog=self)

        for mod in self.mod.hub.values():
            run_schedule(mod, schedule=schedule)

        # Check if we need to run without type checking then just return
        if target in py_code_gen:
            cur_pass.ir_out = top_mod
            return cur_pass

        # Run TypeCheckingPass on the top module
        JacTypeCheckPass(top_mod, prog=self)

        # if "JAC_VSCE" not in os.environ:
        #     ast_ret.ir = top_mod
        #     return ast_ret

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
            run_schedule(mod, schedule=type_checker_sched)

        cur_pass.ir_out = top_mod
        return cur_pass

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
                mod = self.compile(file_path=cur_file, schedule=[]).ir_out
                if mod:
                    node.add_kids_left(mod.kid, parent_update=True, pos_update=False)
                    node.impl_mod.append(mod)
            if (
                cur_file.startswith(f"{base_path}.")
                or test_folder == os.path.dirname(cur_file)
            ) and cur_file.endswith(".test.jac"):
                mod = self.compile(file_path=cur_file, schedule=[]).ir_out
                if mod and not settings.ignore_test_annex:
                    node.test_mod.append(mod)
                    node.add_kids_right(mod.kid, parent_update=True, pos_update=False)

    @staticmethod
    def jac_file_formatter(
        file_path: str,
    ) -> JacFormatPass:
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
        return prse
