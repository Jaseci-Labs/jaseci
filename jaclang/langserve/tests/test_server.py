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
        # self.assertEqual(len(lsp.modules), 1)
        self.assertEqual(lsp.modules[circle_file].diagnostics[0].range.start.line, 22)
        lsp.type_check(circle_file)
        # self.assertEqual(len(lsp.modules), 1)
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
        lsp.type_check(circle_impl_file)
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
        lsp.quick_check(circle_impl_file)
        lsp.deep_check(circle_impl_file)
        lsp.type_check(circle_impl_file)
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

    def test_outline_symbols(self) -> None:
        """Test that the outline symbols are correct."""
        lsp = JacLangServer()
        workspace_path = self.fixture_abs_path("")
        workspace = Workspace(workspace_path, lsp)
        lsp.lsp._workspace = workspace
        circle_file = uris.from_fs_path(self.fixture_abs_path("circle_pure.jac"))
        lsp.quick_check(circle_file)
        lsp.deep_check(circle_file)
        lsp.type_check(circle_file)
        self.assertEqual(8, len(lsp.get_document_symbols(circle_file)))

    def test_go_to_definition(self) -> None:
        """Test that the go to definition is correct."""
        lsp = JacLangServer()
        workspace_path = self.fixture_abs_path("")
        workspace = Workspace(workspace_path, lsp)
        lsp.lsp._workspace = workspace
        circle_file = uris.from_fs_path(self.fixture_abs_path("circle_pure.jac"))
        lsp.quick_check(circle_file)
        lsp.deep_check(circle_file)
        lsp.type_check(circle_file)
        self.assertIn(
            "fixtures/circle_pure.impl.jac:8:0-8:19",
            str(lsp.get_definition(circle_file, lspt.Position(9, 16))),
        )
        self.assertIn(
            "fixtures/circle_pure.jac:13:11-13:16",
            str(lsp.get_definition(circle_file, lspt.Position(20, 17))),
        )

    def test_go_to_definition_method(self) -> None:
        """Test that the go to definition is correct."""
        lsp = JacLangServer()
        workspace_path = self.fixture_abs_path("")
        workspace = Workspace(workspace_path, lsp)
        lsp.lsp._workspace = workspace
        guess_game_file = uris.from_fs_path(
            self.fixture_abs_path("../../../../examples/guess_game/guess_game4.jac")
        )
        lsp.quick_check(guess_game_file)
        lsp.deep_check(guess_game_file)
        lsp.type_check(guess_game_file)
        self.assertIn(
            "guess_game4.jac:27:8-27:21",
            str(lsp.get_definition(guess_game_file, lspt.Position(46, 45))),
        )

    def test_test_annex(self) -> None:
        """Test that the server doesn't run if there is a syntax error."""
        lsp = JacLangServer()
        # Set up the workspace path to "fixtures/"
        workspace_path = self.fixture_abs_path("")
        workspace = Workspace(workspace_path, lsp)
        lsp.lsp._workspace = workspace
        circle_file = uris.from_fs_path(self.fixture_abs_path("circle_pure.test.jac"))
        lsp.quick_check(circle_file)
        lsp.deep_check(circle_file)
        lsp.type_check(circle_file)
        pos = lspt.Position(13, 29)
        self.assertIn(
            "shape_type: circle_pure.ShapeType",
            lsp.get_hover_info(circle_file, pos).contents.value,
        )

    def test_go_to_defintion_import(self) -> None:
        """Test that the go to definition is correct."""
        lsp = JacLangServer()
        workspace_path = self.fixture_abs_path("")
        workspace = Workspace(workspace_path, lsp)
        lsp.lsp._workspace = workspace
        import_file = uris.from_fs_path(
            self.fixture_abs_path("import_include_statements.jac")
        )
        lsp.quick_check(import_file)
        lsp.deep_check(import_file)
        lsp.type_check(import_file)
        positions = [
            (2, 16, "datetime.py:0:0-0:0"),
            (3, 17, "base_module_structure.jac:0:0-0:0"),
            (3, 74, "base_module_structure.jac:23:0-23:5"),
            (5, 65, "py_import.py:12:0-20:5"),
            (5, 35, "py_import.py:3:0-4:5"),
        ]

        for line, char, expected in positions:
            with self.subTest(line=line, char=char):
                self.assertIn(
                    expected,
                    str(lsp.get_definition(import_file, lspt.Position(line, char))),
                )

    def test_sem_tokens(self) -> None:
        """Test that the Semantic Tokens are generated correctly."""
        lsp = JacLangServer()
        workspace_path = self.fixture_abs_path("")
        workspace = Workspace(workspace_path, lsp)
        lsp.lsp._workspace = workspace
        circle_file = uris.from_fs_path(self.fixture_abs_path("circle.jac"))
        lsp.quick_check(circle_file)
        lsp.deep_check(circle_file)
        lsp.type_check(circle_file)
        sem_list = lsp.get_semantic_tokens(circle_file).data
        expected_counts = [
            ("<JacSemTokenType.VARIABLE: 8>, <JacSemTokenModifier.READONLY: 4>", 206),
            (
                "<JacSemTokenType.PROPERTY: 9>, <JacSemTokenModifier.DEFINITION: 2>,",
                112,
            ),
            (
                "<JacSemTokenType.PARAMETER: 7>, <JacSemTokenModifier.DECLARATION: 1>,",
                56,
            ),
            (
                "<JacSemTokenType.FUNCTION: 12>, <JacSemTokenModifier.DECLARATION: 1>,",
                25,
            ),
            ("<JacSemTokenType.METHOD: 13>, <JacSemTokenModifier.DECLARATION: 1>", 12),
            ("<JacSemTokenType.ENUM: 3>, <JacSemTokenModifier.DECLARATION: 1>,", 37),
            ("<JacSemTokenType.CLASS: 2>, <JacSemTokenModifier.DECLARATION: ", 162),
            (
                "<JacSemTokenType.NAMESPACE: 0>, <JacSemTokenModifier.DEFINITION: 2>,",
                10,
            ),
            ("0, 0, 4,", 22),
            ("0, 0, 3,", 192),
            ("0, 0, 6, ", 65),
            (" 0, 7, 3,", 3),
        ]
        for token_type, expected_count in expected_counts:
            self.assertEqual(str(sem_list).count(token_type), expected_count)
