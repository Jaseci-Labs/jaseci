"""JacAnnexManager handles the loading of annex modules."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from jaclang.compiler import unitree as uni
from jaclang.compiler.passes import Transform
from jaclang.settings import settings

if TYPE_CHECKING:
    from jaclang.compiler.program import JacProgram


class JacAnnexPass(Transform[uni.Module, uni.Module]):
    """Handles loading and attaching of annex files (.impl.jac and .test.jac)."""

    def transform(self, ir_in: uni.Module) -> uni.Module:
        """Initialize JacAnnexPass with the module path."""
        self.mod_path = ir_in.loc.mod_path
        self.base_path = self.mod_path[:-4]
        self.impl_folder = self.base_path + ".impl"
        self.test_folder = self.base_path + ".test"
        self.directory = os.path.dirname(self.mod_path) or os.getcwd()
        self.load_annexes(jac_program=self.prog, node=ir_in)
        return ir_in

    def find_annex_paths(self) -> list[str]:
        """Return list of .impl.jac and .test.jac files related to base module."""
        paths = [os.path.join(self.directory, f) for f in os.listdir(self.directory)]
        for folder in [self.impl_folder, self.test_folder]:
            if os.path.exists(folder):
                paths += [os.path.join(folder, f) for f in os.listdir(folder)]
        return paths

    def load_annexes(self, jac_program: JacProgram, node: uni.Module) -> None:
        """Parse and attach annex modules to the node."""
        from jaclang.compiler.program import CompilerMode

        if node.stub_only or not self.mod_path.endswith(".jac"):
            return
        if not self.mod_path:
            self.log_error("Module path is empty.")
            return

        for path in self.find_annex_paths():
            if path == self.mod_path:
                continue

            if path.endswith(".impl.jac") and (
                path.startswith(f"{self.base_path}.")
                or os.path.dirname(path) == self.impl_folder
            ):
                mod = jac_program.compile(
                    file_path=path, full_compile=False, mode=CompilerMode.COMPILE
                )
                if mod:
                    node.impl_mod.append(mod)

            elif (
                path.endswith(".test.jac")
                and not settings.ignore_test_annex
                and (
                    path.startswith(f"{self.base_path}.")
                    or os.path.dirname(path) == self.test_folder
                )
            ):
                mod = jac_program.compile(
                    file_path=path, full_compile=False, mode=CompilerMode.COMPILE
                )
                if mod:
                    node.test_mod.append(mod)
