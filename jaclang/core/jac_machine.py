"""Jac Machine module."""

import os


class JacMachine:
    """JacMachine to handle the VM-related functionalities and loaded programs."""

    def initialize_base_dir(self, base_path: str) -> str:
        """Compute and set the main base directory."""
        if not os.path.isdir(base_path):
            return os.path.dirname(base_path)
        elif os.path.isfile(base_path):
            return base_path
        else:
            return os.path.abspath(base_path)

    def __init__(self, base_path: str = "") -> None:
        """Initialize the JacMachine object."""
        # self.loaded_modules: Dict[str, types.ModuleType] = {}
        self.base_path = base_path
        self.base_path_dir = self.initialize_base_dir(base_path)
