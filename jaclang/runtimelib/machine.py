"""Jac Machine module."""

import marshal
import os
import types
from typing import Dict, Optional

from jaclang.compiler.absyntree import Module
from jaclang.compiler.compile import compile_jac
from jaclang.compiler.constant import Constants as Con
from jaclang.utils.log import logging

logger = logging.getLogger(__name__)


class JacMachine:
    """JacMachine to handle the VM-related functionalities and loaded programs."""

    def __init__(self, base_path: str = "") -> None:
        """Initialize the JacMachine object."""
        self.loaded_modules: Dict[str, types.ModuleType] = {}
        if not base_path:
            base_path = os.getcwd()
        self.base_path = base_path
        self.base_path_dir = (
            os.path.dirname(base_path)
            if not os.path.isdir(base_path)
            else os.path.abspath(base_path)
        )
        self.jac_program: Optional[JacProgram] = None

    def attach_program(self, jac_program: "JacProgram") -> None:
        """Attach a JacProgram to the machine."""
        self.jac_program = jac_program

    def get_mod_bundle(self) -> Optional[Module]:
        """Retrieve the mod_bundle from the attached JacProgram."""
        if self.jac_program:
            return self.jac_program.mod_bundle
        return None

    def get_bytecode(
        self,
        module_name: str,
        full_target: str,
        caller_dir: str,
        cachable: bool = True,
    ) -> Optional[types.CodeType]:
        """Retrieve bytecode from the attached JacProgram."""
        if self.jac_program:
            return self.jac_program.get_bytecode(
                module_name, full_target, caller_dir, cachable
            )
        return None


class JacProgram:
    """Class to hold the mod_bundle and bytecode for Jac modules."""

    def __init__(
        self, mod_bundle: Optional[Module], bytecode: Optional[dict[str, bytes]]
    ) -> None:
        """Initialize the JacProgram object."""
        self.mod_bundle = mod_bundle
        self.bytecode = bytecode or {}

    def get_bytecode(
        self,
        module_name: str,
        full_target: str,
        caller_dir: str,
        cachable: bool = True,
    ) -> Optional[types.CodeType]:
        """Get the bytecode for a specific module."""
        if self.mod_bundle and isinstance(self.mod_bundle, Module):
            codeobj = self.mod_bundle.mod_deps[full_target].gen.py_bytecode
            return marshal.loads(codeobj) if isinstance(codeobj, bytes) else None
        gen_dir = os.path.join(caller_dir, Con.JAC_GEN_DIR)
        pyc_file_path = os.path.join(gen_dir, module_name + ".jbc")
        if cachable and os.path.exists(pyc_file_path):
            with open(pyc_file_path, "rb") as f:
                return marshal.load(f)

        result = compile_jac(full_target, cache_result=cachable)
        if result.errors_had or not result.ir.gen.py_bytecode:
            logger.error(
                f"While importing {len(result.errors_had)} errors"
                f" found in {full_target}"
            )
            return None
        if result.ir.gen.py_bytecode is not None:
            return marshal.loads(result.ir.gen.py_bytecode)
        else:
            return None
