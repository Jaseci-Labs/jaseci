"""Jac Machine module."""

from __future__ import annotations

import marshal
import os
import types
from typing import Optional

from jaclang.compiler.absyntree import Module
from jaclang.compiler.compile import compile_jac
from jaclang.compiler.constant import Constants as Con
from jaclang.compiler.semtable import SemRegistry
from jaclang.utils.log import logging


logger = logging.getLogger(__name__)


class JacProgram:
    """Class to hold the mod_bundle bytecode and sem_ir for Jac modules."""

    def __init__(
        self,
        mod_bundle: Optional[Module],
        bytecode: Optional[dict[str, bytes]],
        sem_ir: Optional[SemRegistry],
    ) -> None:
        """Initialize the JacProgram object."""
        self.mod_bundle = mod_bundle
        self.bytecode = bytecode or {}
        self.sem_ir = sem_ir if sem_ir else SemRegistry()
        self.modules: dict[str, Module] = {}
        self.last_imported: list[Module] = []

    def get_bytecode(
        self,
        module_name: str,
        full_target: str,
        caller_dir: str,
        cachable: bool = True,
        reload: bool = False,
    ) -> Optional[types.CodeType]:
        """Get the bytecode for a specific module."""
        if self.mod_bundle and isinstance(self.mod_bundle, Module):
            codeobj = self.mod_bundle.mod_deps[full_target].gen.py_bytecode
            return marshal.loads(codeobj) if isinstance(codeobj, bytes) else None
        gen_dir = os.path.join(caller_dir, Con.JAC_GEN_DIR)
        pyc_file_path = os.path.join(gen_dir, module_name + ".jbc")
        if cachable and os.path.exists(pyc_file_path) and not reload:
            with open(pyc_file_path, "rb") as f:
                return marshal.load(f)

        result = compile_jac(full_target, cache_result=cachable)
        if result.errors_had:
            for alrt in result.errors_had:
                # We're not logging here, it already gets logged as the errors were added to the errors_had list.
                # Regardless of the logging, this needs to be sent to the end user, so we'll printing it to stderr.
                logger.error(alrt.pretty_print())
        if result.ir.gen.py_bytecode is not None:
            return marshal.loads(result.ir.gen.py_bytecode)
        else:
            return None
