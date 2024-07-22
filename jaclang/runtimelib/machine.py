"""Jac Machine module."""

import os
import types
from typing import Dict, Optional, Union


class JacMachine:
    """JacMachine to handle the VM-related functionalities and loaded programs."""

    loaded_modules: Dict[str, types.ModuleType] = {}

    def __init__(self, base_path: str = "") -> None:
        """Initialize the JacMachine object."""
        if not base_path:
            base_path = os.getcwd()
        self.base_path = base_path
        self.base_path_dir = (
            os.path.dirname(base_path)
            if not os.path.isdir(base_path)
            else os.path.abspath(base_path)
        )

    @classmethod
    def get_modules(
        cls, module_name: Optional[str] = None
    ) -> Union[types.ModuleType, Dict[str, types.ModuleType], None]:
        """Get a module from the loaded programs or all modules if no module name is provided."""
        if module_name:
            return cls.loaded_modules.get(module_name)
        else:
            return cls.loaded_modules
