"""Jac Machine module."""

import os


class JacMachine:
    """JacMachine to handle the VM-related functionalities and loaded programs."""

    def __init__(self, base_path: str = "") -> None:
        """Initialize the JacMachine object."""
        # self.loaded_modules: Dict[str, types.ModuleType] = {}
        self.base_path = base_path
        self.base_path_dir = (
            os.path.dirname(base_path) if not os.path.isdir(base_path) else base_path
        )
