import marshal
import os
import types

from jaclang.compiler.absyntree import Module
from jaclang.compiler.compile import compile_jac
from jaclang.compiler.constant import Constants as Con
from jaclang.compiler.passes.main import PyOutPass
from jaclang.compiler.semtable import SemRegistry
from jaclang.utils.log import logging

logger = logging.getLogger(__name__)


class JacProgram:
    """The jac program is the output of a jac source file.

    It is a representation of the program that can be executed by the jac machine.
    The program is a list of instructions that are executed in order. The program
    is created by the jac compiler when it compiles a jac source file. And every
    include modules will be compiled along with it and cached.
    """

    def __init__(
        self,
        mod_bundle: Module | None,
        sem_ir: SemRegistry | None,
    ) -> None:
        """Initialize the JacProgram object."""
        self.mod_bundle = mod_bundle
        self.sem_ir = sem_ir or SemRegistry()
        self.modules: dict[str, Module] = {}

    def compile(self, filepath: str) -> Module | None:
        """Compile the jac source code from the given filepath.

        Returns the compiled module and store it in the modules dict.
        """
        filepath = os.path.abspath(filepath)
        result = compile_jac(filepath, False)
        for alrt in result.errors_had:
            logger.error(alrt.pretty_print())
        if isinstance(result.ir, Module):
            self.modules[filepath] = result.ir
            return result.ir
        return None

    def dump_files(self, module: Module) -> None:
        """Dump the bytecode and python files for the given module."""
        PyOutPass(input_ir=module, prior=None)

    def get_bytecode(
        self,
        module_name: str,
        filepth: str,
        caller_dir: str,
        cachable: bool = True,
        reload: bool = False,
    ) -> types.CodeType | None:
        """Get the bytecode for a specific module."""
        if self.mod_bundle and isinstance(self.mod_bundle, Module):
            codeobj = self.mod_bundle.mod_deps[filepth].gen.py_bytecode
            return marshal.loads(codeobj) if isinstance(codeobj, bytes) else None
        gen_dir = os.path.join(caller_dir, Con.JAC_GEN_DIR)
        pyc_file_path = os.path.join(gen_dir, module_name + ".jbc")
        if cachable and os.path.exists(pyc_file_path) and not reload:
            with open(pyc_file_path, "rb") as f:
                return marshal.load(f)

        if mod := self.compile(filepth):
            if cachable:
                self.dump_files(mod)
            if mod.gen.py_bytecode is not None:
                return marshal.loads(mod.gen.py_bytecode)
        return None
