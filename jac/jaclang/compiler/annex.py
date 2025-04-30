"""JacAnnexManager handles the loading of annex modules."""

import os
from typing import TYPE_CHECKING

from jaclang.compiler import unitree as uni
from jaclang.settings import settings
from jaclang.utils.log import logging

if TYPE_CHECKING:
    from jaclang.compiler.program import JacProgram

logger = logging.getLogger(__name__)


class JacAnnexManager:
    """Handles loading and attaching of annex files (.impl.jac and .test.jac)."""

    def __init__(self, mod_path: str) -> None:
        """Initialize JacAnnexManager with the module path."""
        self.mod_path = mod_path
        self.base_path = mod_path[:-4]
        self.impl_folder = self.base_path + ".impl"
        self.test_folder = self.base_path + ".test"
        self.directory = os.path.dirname(mod_path) or os.getcwd()

    def find_annex_paths(self) -> list[str]:
        """Return list of .impl.jac and .test.jac files related to base module."""
        paths = [os.path.join(self.directory, f) for f in os.listdir(self.directory)]
        for folder in [self.impl_folder, self.test_folder]:
            if os.path.exists(folder):
                paths += [os.path.join(folder, f) for f in os.listdir(folder)]
        return paths

    def load_annexes(self, jac_program: "JacProgram", node: uni.Module) -> None:
        """Parse and attach annex modules to the node."""
        from jaclang.compiler.program import CompilerMode

        if node.stub_only or not self.mod_path.endswith(".jac"):
            return
        if not self.mod_path:
            logger.error("Module path is empty.")
            return

        for path in self.find_annex_paths():
            if path == self.mod_path:
                continue

            if path.endswith(".impl.jac") and (
                path.startswith(f"{self.base_path}.")
                or os.path.dirname(path) == self.impl_folder
            ):
                mod = jac_program.compile(file_path=path, mode=CompilerMode.PARSE)
                if mod:
                    node.add_kids_left(mod.kid, parent_update=True, pos_update=False)
                    node.impl_mod.append(mod)

            elif (
                path.endswith(".test.jac")
                and not settings.ignore_test_annex
                and (
                    path.startswith(f"{self.base_path}.")
                    or os.path.dirname(path) == self.test_folder
                )
            ):
                mod = jac_program.compile(file_path=path, mode=CompilerMode.PARSE)
                if mod:
                    node.test_mod.append(mod)
                    node.add_kids_right(mod.kid, parent_update=True, pos_update=False)
