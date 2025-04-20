"""Jac Machine module."""

from __future__ import annotations

import os
import types

from jaclang.compiler.program import JacProgram
from jaclang.runtimelib.context import ExecutionContext
from jaclang.utils.log import logging


logger = logging.getLogger(__name__)


class JacMachineState:
    """JacMachine to handle the VM-related functionalities and loaded programs."""

    def __init__(self, base_path: str = "", session: str = "", root: str = "") -> None:
        """Initialize the JacMachine object."""
        self.loaded_modules: dict[str, types.ModuleType] = {}
        if not base_path:
            base_path = os.getcwd()
        # Ensure the base_path is a list rather than a string
        self.base_path = base_path
        self.base_path_dir = (
            os.path.dirname(base_path)
            if not os.path.isdir(base_path)
            else os.path.abspath(base_path)
        )
        self.exec_ctx = ExecutionContext(mach=self, session=session, root=root)
        self.jac_program: JacProgram = JacProgram()

    def close_exec_ctx(__jac_mach__) -> None:
        """Close the execution context."""
        __jac_mach__.exec_ctx.close()
        __jac_mach__.loaded_modules.clear()
        __jac_mach__.exec_ctx = ExecutionContext(mach=__jac_mach__)
