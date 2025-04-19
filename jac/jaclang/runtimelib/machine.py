"""Jac Machine module."""

from __future__ import annotations

import os
import types
from contextvars import ContextVar

from jaclang.compiler.program import JacProgram
from jaclang.utils.log import logging


logger = logging.getLogger(__name__)


JACMACHINE_CONTEXT = ContextVar["JacMachineState | None"]("JacMachineState")


class JacMachineState:
    """JacMachine to handle the VM-related functionalities and loaded programs."""

    def __init__(self, base_path: str = "") -> None:
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
        self.jac_program: JacProgram = JacProgram(
            mod_bundle=None, bytecode=None, sem_ir=None
        )

        JACMACHINE_CONTEXT.set(self)

    @staticmethod
    def get(base_path: str = "") -> "JacMachineState":
        """Get current jac machine."""
        if (jac_machine := JACMACHINE_CONTEXT.get(None)) is None:
            jac_machine = JacMachineState(base_path)
        return jac_machine

    @staticmethod
    def detach_machine() -> None:
        """Detach current jac machine."""
        JACMACHINE_CONTEXT.set(None)
