"""Jac Machine module."""

from __future__ import annotations

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
    SubNodeTabPass,
    SymTabBuildPass,
    pass_schedule,
    py_code_gen,
    type_checker_sched,
)
from jaclang.compiler.passes.main.sym_tab_link_pass import SymTabLinkPass
from jaclang.compiler.passes.tool import JacFormatPass
from jaclang.compiler.passes.tool.schedules import format_pass
from jaclang.compiler.semtable import SemInfo, SemRegistry, SemScope
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
        ast_ret: Pass = JacParser(root_ir=source)
        # TODO: This function below has tons of tech debt that should go away
        # when these functions become methods of JacProgram.
        SubNodeTabPass(ast_ret.root_ir, ast_ret)  # TODO: Get rid of this one

        # Only return the parsed module when the schedules are empty
        # or the target is SubNodeTabPass
        if len(schedule) == 0 or target == SubNodeTabPass:
            return ast_ret

        assert isinstance(ast_ret.root_ir, ast.Module)

        # Creating a new JacProgram and attaching it to top module
        top_mod: ast.Module = ast_ret.root_ir
        top_mod.jac_prog = self
        top_mod.jac_prog.last_imported.append(ast_ret.root_ir)
        top_mod.jac_prog.modules[ast_ret.root_ir.loc.mod_path] = ast_ret.root_ir

        # Run JacImportPass & SymTabBuildPass on all imported Jac Programs
        while len(top_mod.jac_prog.last_imported) > 0:
            mod = top_mod.jac_prog.last_imported.pop()
            self.jac_ir_to_pass(
                ir=mod, schedule=[JacImportPass, SymTabBuildPass], target=target
            )

        # If there is syntax error, no point in processing in further passes.
        if len(ast_ret.errors_had) != 0:
            return ast_ret

        # TODO: we need a elegant way of doing this [should be genaralized].
        if target in (JacImportPass, SymTabBuildPass):
            ast_ret.root_ir = top_mod
            return ast_ret

        # Link all Jac symbol tables created
        for mod in top_mod.jac_prog.modules.values():
            SymTabLinkPass(ir_root=mod, prior=ast_ret)

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

        for mod in top_mod.jac_prog.modules.values():
            run_schedule(mod, schedule=schedule)

        # Check if we need to run without type checking then just return
        if "JAC_NO_TYPECHECK" in os.environ or target in py_code_gen:
            ast_ret.root_ir = top_mod
            return ast_ret

        # Run TypeCheckingPass on the top module
        JacTypeCheckPass(top_mod, prior=ast_ret)

        # if "JAC_VSCE" not in os.environ:
        #     ast_ret.ir = top_mod
        #     return ast_ret

        for mod in top_mod.jac_prog.modules.values():
            PyCollectDepsPass(mod, prior=ast_ret)

        for mod in top_mod.jac_prog.modules.values():
            top_mod.jac_prog.last_imported.append(mod)
        # Run PyImportPass
        while len(top_mod.jac_prog.last_imported) > 0:
            mod = top_mod.jac_prog.last_imported.pop()
            self.jac_ir_to_pass(ir=mod, schedule=[PyImportPass], target=target)

        # Link all Jac symbol tables created
        for mod in top_mod.jac_prog.modules.values():
            SymTabLinkPass(ir_root=mod, prior=ast_ret)

        for mod in top_mod.jac_prog.modules.values():
            DefUsePass(mod, prior=ast_ret)

        for mod in top_mod.jac_prog.modules.values():
            run_schedule(mod, schedule=type_checker_sched)

        ast_ret.root_ir = top_mod
        return ast_ret

    def jac_pass_to_pass(
        self,
        in_pass: Pass,
        target: Optional[Type[Pass]] = None,
        schedule: list[Type[Pass]] = pass_schedule,
    ) -> Pass:
        """Convert a Jac file to an AST."""
        ast_ret = in_pass

        SubNodeTabPass(ast_ret.root_ir, ast_ret)  # TODO: Get rid of this one

        # Only return the parsed module when the schedules are empty
        # or the target is SubNodeTabPass
        if len(schedule) == 0 or target == SubNodeTabPass:
            return ast_ret

        assert isinstance(ast_ret.root_ir, ast.Module)

        # Creating a new JacProgram and attaching it to top module
        top_mod: ast.Module = ast_ret.root_ir
        top_mod.jac_prog = self
        top_mod.jac_prog.last_imported.append(ast_ret.root_ir)
        top_mod.jac_prog.modules[ast_ret.root_ir.loc.mod_path] = ast_ret.root_ir

        # Run JacImportPass & SymTabBuildPass on all imported Jac Programs
        while len(top_mod.jac_prog.last_imported) > 0:
            mod = top_mod.jac_prog.last_imported.pop()
            self.jac_ir_to_pass(
                ir=mod, schedule=[JacImportPass, SymTabBuildPass], target=target
            )

        # If there is syntax error, no point in processing in further passes.
        if len(ast_ret.errors_had) != 0:
            return ast_ret

        # TODO: we need a elegant way of doing this [should be genaralized].
        if target in (JacImportPass, SymTabBuildPass):
            ast_ret.root_ir = top_mod
            return ast_ret

        # Link all Jac symbol tables created
        for mod in top_mod.jac_prog.modules.values():
            SymTabLinkPass(ir_root=mod, prior=ast_ret)

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

        for mod in top_mod.jac_prog.modules.values():
            run_schedule(mod, schedule=schedule)

        # Check if we need to run without type checking then just return
        if "JAC_NO_TYPECHECK" in os.environ or target in py_code_gen:
            ast_ret.root_ir = top_mod
            return ast_ret

        # Run TypeCheckingPass on the top module
        JacTypeCheckPass(top_mod, prior=ast_ret)

        # if "JAC_VSCE" not in os.environ:
        #     ast_ret.ir = top_mod
        #     return ast_ret

        for mod in top_mod.jac_prog.modules.values():
            PyCollectDepsPass(mod, prior=ast_ret)

        for mod in top_mod.jac_prog.modules.values():
            top_mod.jac_prog.last_imported.append(mod)
        # Run PyImportPass
        while len(top_mod.jac_prog.last_imported) > 0:
            mod = top_mod.jac_prog.last_imported.pop()
            self.jac_ir_to_pass(ir=mod, schedule=[PyImportPass], target=target)

        # Link all Jac symbol tables created
        for mod in top_mod.jac_prog.modules.values():
            SymTabLinkPass(ir_root=mod, prior=ast_ret)

        for mod in top_mod.jac_prog.modules.values():
            DefUsePass(mod, prior=ast_ret)

        for mod in top_mod.jac_prog.modules.values():
            run_schedule(mod, schedule=type_checker_sched)

        ast_ret.root_ir = top_mod
        return ast_ret

    def jac_ir_to_pass(
        self,
        ir: ast.AstNode,
        target: Optional[Type[Pass]] = None,
        schedule: list[Type[Pass]] = pass_schedule,
    ) -> Pass:
        """Convert a Jac file to an AST."""
        if not target:
            target = schedule[-1] if schedule else None
        ast_ret = (
            Pass(ir_root=ir, prior=None)
            if not len(schedule)
            else schedule[0](ir_root=ir, prior=None)
        )
        if schedule[0] == target:
            return ast_ret

        for i in schedule[1:]:
            if i == target:
                break
            ast_ret = i(ir_root=ast_ret.root_ir, prior=ast_ret)
        if target and target in schedule:
            ast_ret = (
                target(ir_root=ast_ret.root_ir, prior=ast_ret) if target else ast_ret
            )
        return ast_ret

    def jac_file_formatter(
        self,
        file_path: str,
        schedule: list[Type[Pass]] = format_pass,
    ) -> JacFormatPass:
        """Convert a Jac file to an AST."""
        target = JacFormatPass
        with open(file_path) as file:
            source = ast.JacSource(file.read(), mod_path=file_path)
            prse: Pass = JacParser(root_ir=source)
        for i in schedule:
            if i == target:
                break
            prse = i(ir_root=prse.root_ir, prior=prse)
        prse = target(ir_root=prse.root_ir, prior=prse)
        return prse

    def get_semstr_type(
        self, scope: str, attr: str, return_semstr: bool
    ) -> Optional[str]:
        """Jac's get_semstr_type feature."""

        _scope = SemScope.get_scope_from_str(scope)
        mod_registry: SemRegistry = self.sem_ir if self is not None else SemRegistry()
        _, attr_seminfo = mod_registry.lookup(_scope, attr)
        if attr_seminfo and isinstance(attr_seminfo, SemInfo):
            return attr_seminfo.semstr if return_semstr else attr_seminfo.type
        return None

    def obj_scope(self, attr: str) -> str:
        """Jac's get_semstr_type feature."""
        mod_registry: SemRegistry = self.sem_ir if self is not None else SemRegistry()

        attr_scope = None
        for x in attr.split("."):
            attr_scope, attr_sem_info = mod_registry.lookup(attr_scope, x)
            if isinstance(attr_sem_info, SemInfo) and attr_sem_info.type not in [
                "class",
                "obj",
                "node",
                "edge",
            ]:
                attr_scope, attr_sem_info = mod_registry.lookup(
                    None, attr_sem_info.type
                )
                if isinstance(attr_sem_info, SemInfo) and isinstance(
                    attr_sem_info.type, str
                ):
                    attr_scope = SemScope(
                        attr_sem_info.name, attr_sem_info.type, attr_scope
                    )
            else:
                if isinstance(attr_sem_info, SemInfo) and isinstance(
                    attr_sem_info.type, str
                ):
                    attr_scope = SemScope(
                        attr_sem_info.name, attr_sem_info.type, attr_scope
                    )
        return str(attr_scope)

    def get_sem_type(self, attr: str) -> tuple[str | None, str | None]:
        """Jac's get_semstr_type feature."""
        mod_registry: SemRegistry = self.sem_ir if self is not None else SemRegistry()

        attr_scope = None
        for x in attr.split("."):
            attr_scope, attr_sem_info = mod_registry.lookup(attr_scope, x)
            if isinstance(attr_sem_info, SemInfo) and attr_sem_info.type not in [
                "class",
                "obj",
                "node",
                "edge",
            ]:
                attr_scope, attr_sem_info = mod_registry.lookup(
                    None, attr_sem_info.type
                )
                if isinstance(attr_sem_info, SemInfo) and isinstance(
                    attr_sem_info.type, str
                ):
                    attr_scope = SemScope(
                        attr_sem_info.name, attr_sem_info.type, attr_scope
                    )
            else:
                if isinstance(attr_sem_info, SemInfo) and isinstance(
                    attr_sem_info.type, str
                ):
                    attr_scope = SemScope(
                        attr_sem_info.name, attr_sem_info.type, attr_scope
                    )
        if isinstance(attr_sem_info, SemInfo) and isinstance(attr_scope, SemScope):
            return attr_sem_info.semstr, attr_scope.as_type_str
        return "", ""
