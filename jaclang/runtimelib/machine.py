"""Jac Machine module."""

import os
import types
from typing import Dict


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
