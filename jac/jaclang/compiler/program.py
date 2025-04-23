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
from jaclang.settings import settings
from jaclang.utils.log import logging


logger = logging.getLogger(__name__)


class JacProgram:
    """JacProgram to handle the Jac program-related functionalities."""

    def __init__(self) -> None:
        """Initialize the JacProgram object."""
        self.sem_ir = SemRegistry()
        self.modules: dict[str, Module] = {}
        self.last_imported: list[Module] = []
        self.py_raise_map: dict[str, str] = {}
        self.errors_had: list[Alert] = []
        self.warnings_had: list[Alert] = []

    def get_bytecode(
        self, full_target: str, full_compile: bool = True
    ) -> Optional[types.CodeType]:
        """Get the bytecode for a specific module."""
        if full_target in self.modules:
            codeobj = self.modules[full_target].gen.py_bytecode
            return marshal.loads(codeobj) if isinstance(codeobj, bytes) else None
        if full_compile:
            result = self.jac_file_to_pass(file_path=full_target)
        else:
            result = self.jac_file_to_pass(
                file_path=full_target,
                target=PyBytecodeGenPass,
                schedule=[FuseCommentsPass, JacFormatPass],
            )
        if result.errors_had:
            for alrt in result.errors_had:
                logger.error(alrt.pretty_print())
        if result.ir_out.gen.py_bytecode is not None:
            return marshal.loads(result.ir_out.gen.py_bytecode)
        else:
            return None

    def jac_file_to_pass(
        self,
        file_path: str,
        target: Optional[Type[AstPass]] = None,
        schedule: list[Type[AstPass]] = pass_schedule,
        full_compile: bool = True,
    ) -> Transform:
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
        target: Optional[Type[AstPass]] = None,
        schedule: list[Type[AstPass]] = pass_schedule,
        full_compile: bool = True,
    ) -> Transform:
        """Convert a Jac file to an AST."""
        if not target:
            target = schedule[-1] if schedule else None

        source = ast.Source(jac_str, mod_path=file_path)
        ast_ret: Transform = JacParser(root_ir=source, prog=self)
        return self.run_pass_schedule(
            cur_pass=ast_ret,
            target=target,
            schedule=schedule,
            full_compile=full_compile,
        )

    def py_str_to_pass(
        self,
        py_str: str,
        file_path: str,
        target: Optional[Type[AstPass]] = None,
        schedule: list[Type[AstPass]] = pass_schedule,
    ) -> Transform:
        """Convert a Jac file to an AST."""
        if not target:
            target = schedule[-1] if schedule else None
        parsed_ast = py_ast.parse(py_str)
        py_ast_build_pass = PyastBuildPass(
            ir_in=ast.PythonModuleAst(
                parsed_ast,
                orig_src=ast.Source(py_str, mod_path=file_path),
            ),
            prog=self,
        )
        # TODO: This should go inside the PyastBuildPass
        self.modules[py_ast_build_pass.ir_out.loc.mod_path] = py_ast_build_pass.ir_out
        return self.run_pass_schedule(
            cur_pass=py_ast_build_pass,
            target=target,
            schedule=schedule,
        )

    def run_pass_schedule(
        self,
        cur_pass: Transform,
        target: Optional[Type[AstPass]] = None,
        schedule: list[Type[AstPass]] = pass_schedule,
        full_compile: bool = True,
    ) -> Transform:
        """Convert a Jac file to an AST."""
        # Creating a new JacProgram and attaching it to top module
        self.modules[cur_pass.ir_out.loc.mod_path] = cur_pass.ir_out
        top_mod: ast.Module = cur_pass.ir_out
        self.last_imported.append(cur_pass.ir_out)
        self.annex_impl(cur_pass.ir_out)
        # Only return the parsed module when the schedules are empty
        if len(schedule) == 0:
            return cur_pass

        # Run all passes till PyBytecodeGenPass
        # Here the passes will run one by one on the imported modules instead
        # of running on  a huge AST
        def run_schedule(mod: ast.Module, schedule: list[type[AstPass]]) -> None:
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

        for mod in self.modules.values():
            SymTabBuildPass(ir_in=mod, prog=self)

        # If there is syntax error, no point in processing in further passes.
        if len(cur_pass.errors_had) != 0:
            return cur_pass

        # TODO: we need a elegant way of doing this [should be genaralized].
        if target in (JacImportPass, SymTabBuildPass):
            cur_pass.ir_out = top_mod
            return cur_pass

        # Link all Jac symbol tables created
        for mod in self.modules.values():
            SymTabLinkPass(ir_in=mod, prog=self)

        for mod in self.modules.values():
            run_schedule(mod, schedule=schedule)

        # Check if we need to run without type checking then just return
        if "JAC_NO_TYPECHECK" in os.environ or target in py_code_gen:
            cur_pass.ir_out = top_mod
            return cur_pass

        # Run TypeCheckingPass on the top module
        JacTypeCheckPass(top_mod, prog=self)

        # if "JAC_VSCE" not in os.environ:
        #     ast_ret.ir = top_mod
        #     return ast_ret

        for mod in self.modules.values():
            PyCollectDepsPass(mod, prog=self)

        for mod in self.modules.values():
            self.last_imported.append(mod)
        # Run PyImportPass
        while len(self.last_imported) > 0:
            mod = self.last_imported.pop()
            PyImportPass(mod, prog=self)

        # Link all Jac symbol tables created
        for mod in self.modules.values():
            SymTabLinkPass(ir_in=mod, prog=self)

        for mod in self.modules.values():
            DefUsePass(mod, prog=self)

        for mod in self.modules.values():
            run_schedule(mod, schedule=type_checker_sched)

        cur_pass.ir_out = top_mod
        return cur_pass

    def annex_impl(self, node: ast.Module) -> None:
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
                mod = self.jac_file_to_pass(file_path=cur_file, schedule=[]).ir_out
                if mod:
                    node.add_kids_left(mod.kid, parent_update=True, pos_update=False)
                    node.impl_mod.append(mod)
            if (
                cur_file.startswith(f"{base_path}.")
                or test_folder == os.path.dirname(cur_file)
            ) and cur_file.endswith(".test.jac"):
                mod = self.jac_file_to_pass(file_path=cur_file, schedule=[]).ir_out
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
            source = ast.Source(file.read(), mod_path=file_path)
            prse: Transform = JacParser(root_ir=source, prog=prog)
        for i in [FuseCommentsPass, JacFormatPass]:
            prse = i(ir_in=prse.ir_out, prog=prog)
        prse = target(ir_in=prse.ir_out, prog=prog)
        prse.errors_had = prog.errors_had
        prse.warnings_had = prog.warnings_had
        return prse
