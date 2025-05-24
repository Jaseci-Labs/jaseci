import os
import runpy
import zipfile
from pathlib import Path

from jaclang.utils.test import TestCase


class TestDocsPlayground(TestCase):
    """Verify generation of playground assets."""

    def setUp(self) -> None:
        self.root = Path(__file__).resolve().parents[2]
        self.docs_root = self.root / "docs"
        self.zip_path = self.docs_root / "docs" / "playground" / "jaclang.zip"
        if self.zip_path.exists():
            self.zip_path.unlink()
        super().setUp()

    def run_pre_build_hook(self) -> None:
        prev = os.getcwd()
        os.chdir(self.docs_root)
        try:
            mod = runpy.run_path(self.docs_root / "scripts" / "handle_jac_compile_data.py")
            mod["pre_build_hook"]()
        finally:
            os.chdir(prev)

    def test_playground_zip_created(self) -> None:
        """pre_build_hook should generate jaclang.zip with expected files."""
        self.run_pre_build_hook()
        self.assertTrue(self.zip_path.exists(), "jaclang.zip was not created")
        with zipfile.ZipFile(self.zip_path) as zf:
            self.assertIn("jaclang/__init__.py", zf.namelist())

    def test_index_contains_title(self) -> None:
        """index.html should have the expected title."""
        index_path = self.docs_root / "docs" / "playground" / "index.html"
        content = index_path.read_text(encoding="utf-8")
        self.assertIn("<title>Jac Playground</title>", content)
