"""Jac Machine module."""

from __future__ import annotations

import ast as py_ast
import marshal
import types
from typing import Optional

import jaclang.compiler.unitree as uni
from jaclang.compiler.parser import JacParser
from jaclang.compiler.passes.main import (
    Alert,
    CFGBuildPass,
    CompilerMode,
    DeclImplMatchPass,
    DefUsePass,
    InheritancePass,
    JacAnnexPass,
    JacImportDepsPass,
    PyBytecodeGenPass,
    PyImportDepsPass,
    PyJacAstLinkPass,
    PyastBuildPass,
    PyastGenPass,
    SymTabBuildPass,
    SymTabLinkPass,
    Transform,
)
from jaclang.compiler.passes.tool import (
    DocIRGenPass,
    FuseCommentsPass,
    JacFormatPass,
)
from jaclang.utils.log import logging


logger = logging.getLogger(__name__)

ir_gen_sched = [
    DeclImplMatchPass,
    DefUsePass,
    CFGBuildPass,
    InheritancePass,
]
py_code_gen = [
    PyastGenPass,
    PyJacAstLinkPass,
    PyBytecodeGenPass,
]
format_sched = [FuseCommentsPass, DocIRGenPass, JacFormatPass]


class JacProgram:
    """JacProgram to handle the Jac program-related functionalities."""

    def __init__(self, main_mod: Optional[uni.ProgramModule] = None) -> None:
        """Initialize the JacProgram object."""
        self.mod: uni.ProgramModule = main_mod if main_mod else uni.ProgramModule()
        self.py_raise_map: dict[str, str] = {}
        self.errors_had: list[Alert] = []
        self.warnings_had: list[Alert] = []

    def get_bytecode(
        self, full_target: str, full_compile: bool = True
    ) -> Optional[types.CodeType]:
        """Get the bytecode for a specific module."""
        if full_target in self.mod.hub:
            codeobj = self.mod.hub[full_target].gen.py_bytecode
            return marshal.loads(codeobj) if isinstance(codeobj, bytes) else None
        result = self.compile(
            file_path=full_target,
            mode=CompilerMode.COMPILE if full_compile else CompilerMode.COMPILE_SINGLE,
        )
        return marshal.loads(result.gen.py_bytecode) if result.gen.py_bytecode else None

    def compile(
        self,
        file_path: str,
        mode: CompilerMode = CompilerMode.COMPILE,
    ) -> uni.Module:
        """Convert a Jac file to an AST."""
        with open(file_path, "r", encoding="utf-8") as file:
            return self.compile_from_str(
                source_str=file.read(), file_path=file_path, mode=mode
            )

    def compile_from_str(
        self,
        source_str: str,
        file_path: str,
        mode: CompilerMode = CompilerMode.COMPILE,
    ) -> uni.Module:
        """Convert a Jac file to an AST."""
        had_error = False
        if file_path.endswith(".py"):
            parsed_ast = py_ast.parse(source_str)
            py_ast_ret = PyastBuildPass(
                ir_in=uni.PythonModuleAst(
                    parsed_ast,
                    orig_src=uni.Source(source_str, mod_path=file_path),
                ),
                prog=self,
            )
            had_error = len(py_ast_ret.errors_had) > 0
            mod = py_ast_ret.ir_out
        else:
            source = uni.Source(source_str, mod_path=file_path)
            jac_ast_ret: Transform[uni.Source, uni.Module] = JacParser(
                root_ir=source, prog=self
            )
            had_error = len(jac_ast_ret.errors_had) > 0
            mod = jac_ast_ret.ir_out
        if had_error:
            return mod
        if self.mod.main.stub_only:
            self.mod = uni.ProgramModule(mod)
        self.mod.hub[mod.loc.mod_path] = mod
        return self.run_pass_schedule(mod_targ=mod, mode=mode)

    def run_pass_schedule(
        self,
        mod_targ: uni.Module,
        mode: CompilerMode = CompilerMode.COMPILE,
    ) -> uni.Module:
        """Convert a Jac file to an AST."""
        JacAnnexPass(ir_in=mod_targ, prog=self)
        SymTabBuildPass(ir_in=mod_targ, prog=self)
        if mode == CompilerMode.PARSE:
            return mod_targ
        elif mode in (CompilerMode.COMPILE_SINGLE, CompilerMode.NO_CGEN_SINGLE):
            self.schedule_runner(mod_targ, mode=mode)
            return mod_targ
        JacImportDepsPass(ir_in=mod_targ, prog=self)
        if len(self.errors_had):
            return mod_targ
        SymTabLinkPass(ir_in=mod_targ, prog=self)
        for mod in self.mod.hub.values():
            self.schedule_runner(mod, mode=CompilerMode.COMPILE)
        if mode == CompilerMode.COMPILE:
            return mod_targ
        PyImportDepsPass(mod_targ, prog=self)
        SymTabLinkPass(ir_in=mod_targ, prog=self)
        for mod in self.mod.hub.values():
            DefUsePass(mod, prog=self)
        for mod in self.mod.hub.values():
            self.schedule_runner(mod, mode=CompilerMode.TYPECHECK)
        return mod_targ

    def schedule_runner(
        self,
        mod: uni.Module,
        mode: CompilerMode = CompilerMode.COMPILE,
    ) -> None:
        """Run premade passes on the module."""
        match mode:
            case CompilerMode.NO_CGEN | CompilerMode.NO_CGEN_SINGLE:
                passes = ir_gen_sched
            case CompilerMode.COMPILE | CompilerMode.COMPILE_SINGLE:
                passes = [*ir_gen_sched, *py_code_gen]
            case CompilerMode.TYPECHECK:
                passes = []
            case _:
                raise ValueError(f"Invalid mode: {mode}")
        self.run_schedule(mod, passes)

    def run_schedule(
        self,
        mod: uni.Module,
        passes: list[type[Transform[uni.Module, uni.Module]]],
    ) -> None:
        """Run the passes on the module."""
        final_pass: Optional[type[Transform[uni.Module, uni.Module]]] = None
        for current_pass in passes:
            if current_pass == PyBytecodeGenPass:
                final_pass = current_pass
                break
            current_pass(ir_in=mod, prog=self)  # type: ignore
        if final_pass:
            final_pass(mod, prog=self)

    @staticmethod
    def jac_file_formatter(file_path: str) -> str:
        """Convert a Jac file to an AST."""
        prog = JacProgram()
        with open(file_path) as file:
            source = uni.Source(file.read(), mod_path=file_path)
            prse: Transform = JacParser(root_ir=source, prog=prog)
        for i in format_sched:
            prse = i(ir_in=prse.ir_out, prog=prog)
        prse.errors_had = prog.errors_had
        prse.warnings_had = prog.warnings_had
        return prse.ir_out.gen.jac

    @staticmethod
    def jac_str_formatter(source_str: str, file_path: str) -> str:
        """Convert a Jac file to an AST."""
        prog = JacProgram()
        source = uni.Source(source_str, mod_path=file_path)
        prse: Transform = JacParser(root_ir=source, prog=prog)
        for i in format_sched:
            prse = i(ir_in=prse.ir_out, prog=prog)
        prse.errors_had = prog.errors_had
        prse.warnings_had = prog.warnings_had
        return prse.ir_out.gen.jac if not prse.errors_had else source_str
