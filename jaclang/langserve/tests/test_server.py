from jaclang.utils.test import TestCase
from jaclang.vendor.pygls import uris
from jaclang.vendor.pygls.workspace import Workspace
from jaclang.langserve.engine import JacLangServer
from .session import LspSession

import lsprotocol.types as lspt


class TestJacLangServer(TestCase):

    def test_formatting(self) -> None:
        with LspSession() as s:
            s.initialize()
            with open(self.fixture_abs_path("hello.jac"), "w") as f:
                f.write('with entry {print("Hello, World!");}')
            with open(self.fixture_abs_path("hello.jac"), "r") as f:
                self.assertEqual(f.read(), 'with entry {print("Hello, World!");}')
            params_json = {
                "textDocument": {
                    "uri": uris.from_fs_path(self.fixture_abs_path("hello.jac")),
                    "languageId": "jac",
                    "version": 1,
                    "text": "with entry {print('Hello, World!');}",
                },
                "options": {"tabSize": 4, "insertSpaces": True},
            }
            text_edits = s.text_document_formatting(params_json)
            self.assertEqual(
                text_edits,
                [
                    {
                        "range": {
                            "start": {"line": 0, "character": 0},
                            "end": {"line": 2, "character": 0},
                        },
                        "newText": 'with entry {\n    print("Hello, World!");\n}\n',
                    }
                ],
            )

    def test_syntax_diagnostics(self) -> None:
        """Test diagnostics."""
        lsp = JacLangServer()
        # Set up the workspace path to "fixtures/"
        workspace_path = self.fixture_abs_path("")
        workspace = Workspace(workspace_path, lsp)
        lsp.lsp._workspace = workspace
        circle_file = uris.from_fs_path(self.fixture_abs_path("circle_err.jac"))
        lsp.quick_check(circle_file)
        self.assertEqual(len(lsp.modules), 1)
        self.assertEqual(lsp.modules[circle_file].diagnostics[0].range.start.line, 22)

    def test_doesnt_run_if_syntax_error(self) -> None:
        """Test that the server doesn't run if there is a syntax error."""
        lsp = JacLangServer()
        # Set up the workspace path to "fixtures/"
        workspace_path = self.fixture_abs_path("")
        workspace = Workspace(workspace_path, lsp)
        lsp.lsp._workspace = workspace
        circle_file = uris.from_fs_path(self.fixture_abs_path("circle_err.jac"))
        lsp.quick_check(circle_file)
        self.assertEqual(len(lsp.modules), 1)
        self.assertEqual(lsp.modules[circle_file].diagnostics[0].range.start.line, 22)
        lsp.deep_check(circle_file)
        self.assertEqual(len(lsp.modules), 1)
        self.assertEqual(lsp.modules[circle_file].diagnostics[0].range.start.line, 22)
        lsp.type_check(circle_file)
        self.assertEqual(len(lsp.modules), 1)
        self.assertEqual(lsp.modules[circle_file].diagnostics[0].range.start.line, 22)

    def test_impl_stay_connected(self) -> None:
        """Test that the server doesn't run if there is a syntax error."""
        lsp = JacLangServer()
        # Set up the workspace path to "fixtures/"
        workspace_path = self.fixture_abs_path("")
        workspace = Workspace(workspace_path, lsp)
        lsp.lsp._workspace = workspace
        circle_file = uris.from_fs_path(self.fixture_abs_path("circle_pure.jac"))
        circle_impl_file = uris.from_fs_path(
            self.fixture_abs_path("circle_pure.impl.jac")
        )
        lsp.quick_check(circle_file)
        lsp.deep_check(circle_file)
        lsp.type_check(circle_file)
        pos = lspt.Position(20, 8)
        self.assertIn(
            "Circle class inherits from Shape.",
            lsp.get_hover_info(circle_file, pos).contents.value,
        )
        lsp.type_check(circle_impl_file, force=True)
        pos = lspt.Position(8, 11)
        self.assertIn(
            "ability) calculate_area: float",
            lsp.get_hover_info(circle_impl_file, pos).contents.value,
        )

    def test_impl_auto_discover(self) -> None:
        """Test that the server doesn't run if there is a syntax error."""
        lsp = JacLangServer()
        # Set up the workspace path to "fixtures/"
        workspace_path = self.fixture_abs_path("")
        workspace = Workspace(workspace_path, lsp)
        lsp.lsp._workspace = workspace
        circle_impl_file = uris.from_fs_path(
            self.fixture_abs_path("circle_pure.impl.jac")
        )
        lsp.quick_check(circle_impl_file, force=True)
        lsp.deep_check(circle_impl_file, force=True)
        lsp.type_check(circle_impl_file, force=True)
        pos = lspt.Position(8, 11)
        self.assertIn(
            "ability) calculate_area: float",
            lsp.get_hover_info(circle_impl_file, pos).contents.value,
        )

    def test_show_type_impl(self) -> None:
        """Test that the server doesn't run if there is a syntax error."""
        lsp = JacLangServer()
        # Set up the workspace path to "fixtures/"
        workspace_path = self.fixture_abs_path("")
        workspace = Workspace(workspace_path, lsp)
        lsp.lsp._workspace = workspace
        target = uris.from_fs_path(
            self.fixture_abs_path("../../../../examples/guess_game/guess_game4.jac")
        )
        lsp.quick_check(target)
        lsp.deep_check(target)
        lsp.type_check(target)
        pos = lspt.Position(43, 18)
        self.assertIn(
            "attempts: int",
            lsp.get_hover_info(target, pos).contents.value,
        )
