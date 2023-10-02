"""Living Workspace of Jac project."""
from __future__ import annotations

import os


from jaclang.jac.passes.blue import AstBuildPass, SemanticCheckPass
from jaclang.jac.transpiler import jac_file_to_pass


class Workspace:
    """Class for managing workspace."""

    def __init__(self, path: str) -> None:
        """Initialize workspace."""
        self.path = path
        self.modules: dict[str, tuple[AstBuildPass, SemanticCheckPass]] = {}
        self.rebuild_workspace()

    def rebuild_workspace(self) -> None:
        """Rebuild workspace."""
        jac_files = [
            os.path.join(root, name)
            for root, _, files in os.walk(self.path)
            for name in files
            if name.endswith(".jac")
        ]
        self.modules = {
            file: (
                jac_file_to_pass(
                    file_path=file, base_dir=self.path, target=AstBuildPass
                ),
                jac_file_to_pass(
                    file_path=file, base_dir=self.path, target=SemanticCheckPass
                ),
            )
            for file in jac_files
        }

    def rebuild_file(self, file_path: str) -> None:
        """Rebuild a file."""
        self.modules[file_path] = (
            jac_file_to_pass(
                file_path=file_path, base_dir=self.path, target=AstBuildPass
            ),
            jac_file_to_pass(
                file_path=file_path, base_dir=self.path, target=SemanticCheckPass
            ),
        )

    def add_file(self, file_path: str) -> None:
        """Add a file to the workspace."""
        self.modules[file_path] = (
            jac_file_to_pass(
                file_path=file_path, base_dir=self.path, target=AstBuildPass
            ),
            jac_file_to_pass(
                file_path=file_path, base_dir=self.path, target=SemanticCheckPass
            ),
        )

    def del_file(self, file_path: str) -> None:
        """Delete a file from the workspace."""
        del self.modules[file_path]
