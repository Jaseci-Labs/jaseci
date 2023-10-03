"""Living Workspace of Jac project."""
from __future__ import annotations

import os
from typing import Optional


import jaclang.jac.absyntree as ast
from jaclang.jac.passes.blue import SemanticCheckPass
from jaclang.jac.transpiler import Alert, jac_file_to_pass


class ModuleInfo:
    """Module IR and Stats."""

    def __init__(
        self, ir: Optional[ast.Module], errors: list[Alert], warnings: list[Alert]
    ) -> None:
        """Initialize module info."""
        self.ir = ir
        self.errors = errors
        self.warnings = warnings


class Workspace:
    """Class for managing workspace."""

    def __init__(self, path: str) -> None:
        """Initialize workspace."""
        self.path = path
        self.modules: dict[str, ModuleInfo] = {}
        self.rebuild_workspace()

    def rebuild_workspace(self) -> None:
        """Rebuild workspace."""
        self.modules = {}
        for file in [
            os.path.normpath(os.path.join(root, name))
            for root, _, files in os.walk(self.path)
            for name in files
            if name.endswith(".jac")
        ]:
            if file in self.modules:
                continue
            build = jac_file_to_pass(
                file_path=file, base_dir=self.path, target=SemanticCheckPass
            )
            self.modules[file] = ModuleInfo(
                ir=build.ir if isinstance(build.ir, ast.Module) else None,
                errors=build.errors_had,
                warnings=build.warnings_had,
            )
            if build.ir:
                for sub in build.ir.meta["sub_import_tab"]:
                    self.modules[sub] = ModuleInfo(
                        ir=build.ir.meta["sub_import_tab"][sub],
                        errors=build.errors_had,
                        warnings=build.warnings_had,
                    )

    def rebuild_file(self, file_path: str, deep: bool = False) -> None:
        """Rebuild a file."""
        build = jac_file_to_pass(
            file_path=file_path, base_dir=self.path, target=SemanticCheckPass
        )
        self.modules[file_path] = ModuleInfo(
            ir=build.ir if isinstance(build.ir, ast.Module) else None,
            errors=build.errors_had,
            warnings=build.warnings_had,
        )
        if deep:
            for sub in build.ir.meta["sub_import_tab"]:
                self.modules[sub] = ModuleInfo(
                    ir=build.ir.meta["sub_import_tab"][sub],
                    errors=build.errors_had,
                    warnings=build.warnings_had,
                )

    def add_file(self, file_path: str) -> None:
        """Add a file to the workspace."""
        self.rebuild_file(file_path)

    def del_file(self, file_path: str) -> None:
        """Delete a file from the workspace."""
        del self.modules[file_path]

    def file_list(self) -> list[str]:
        """Return a list of files in the workspace."""
        return list(self.modules.keys())
