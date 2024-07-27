from jaclang.utils.test import TestCase
from jaclang.vendor.pygls import uris
from jaclang.vendor.pygls.workspace import Workspace
from jaclang.langserve.engine import JacLangServer, ModuleInfo
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
        lsp.deep_check(circle_file)
        pos = lspt.Position(20, 8)
        self.assertIn(
            "Circle class inherits from Shape.",
            lsp.get_hover_info(circle_file, pos).contents.value,
        )
        lsp.deep_check(circle_impl_file)
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
        lsp.deep_check(circle_impl_file)
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
        target = uris.from_fs_path(self.examples_abs_path("guess_game/guess_game4.jac"))
        lsp.deep_check(target)
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
        lsp.deep_check(circle_file)
        self.assertEqual(8, len(lsp.get_outline(circle_file)))

    def test_go_to_definition(self) -> None:
        """Test that the go to definition is correct."""
        lsp = JacLangServer()
        workspace_path = self.fixture_abs_path("")
        workspace = Workspace(workspace_path, lsp)
        lsp.lsp._workspace = workspace
        circle_file = uris.from_fs_path(self.fixture_abs_path("circle_pure.jac"))
        lsp.deep_check(circle_file)
        self.assertIn(
            "fixtures/circle_pure.impl.jac:8:0-8:19",
            str(lsp.get_definition(circle_file, lspt.Position(9, 16))),
        )
        self.assertIn(
            "fixtures/circle_pure.jac:13:11-13:16",
            str(lsp.get_definition(circle_file, lspt.Position(20, 16))),
        )

    def test_go_to_definition_method(self) -> None:
        """Test that the go to definition is correct."""
        lsp = JacLangServer()
        workspace_path = self.fixture_abs_path("")
        workspace = Workspace(workspace_path, lsp)
        lsp.lsp._workspace = workspace
        guess_game_file = uris.from_fs_path(
            self.examples_abs_path("guess_game/guess_game4.jac")
        )
        lsp.deep_check(guess_game_file)
        self.assertIn(
            "guess_game4.jac:27:8-27:21",
            str(lsp.get_definition(guess_game_file, lspt.Position(46, 45))),
        )

    def test_go_to_definition_method_manual_impl(self) -> None:
        """Test that the go to definition is correct."""
        lsp = JacLangServer()
        workspace_path = self.fixture_abs_path("")
        workspace = Workspace(workspace_path, lsp)
        lsp.lsp._workspace = workspace
        decldef_file = uris.from_fs_path(
            self.examples_abs_path("micro/decl_defs_impl.jac")
        )
        lsp.deep_check(decldef_file)
        self.assertNotIn(
            "decl_defs_main.jac:8:8-8:17",
            str(lsp.get_definition(decldef_file, lspt.Position(2, 24))),
        )
        decldef_main_file = uris.from_fs_path(
            self.examples_abs_path("micro/decl_defs_main.jac")
        )
        lsp.deep_check(decldef_main_file)
        lsp.deep_check(decldef_file)
        self.assertIn(
            "decl_defs_main.jac:8:8-8:17",
            str(lsp.get_definition(decldef_file, lspt.Position(2, 24))),
        )

    def test_test_annex(self) -> None:
        """Test that the server doesn't run if there is a syntax error."""
        lsp = JacLangServer()
        # Set up the workspace path to "fixtures/"
        workspace_path = self.fixture_abs_path("")
        workspace = Workspace(workspace_path, lsp)
        lsp.lsp._workspace = workspace
        circle_file = uris.from_fs_path(self.fixture_abs_path("circle_pure.test.jac"))
        lsp.deep_check(circle_file)
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
        lsp.deep_check(import_file)
        positions = [
            (2, 24, "datetime.py:0:0-0:0"),
            (3, 17, "base_module_structure.jac:0:0-0:0"),
            (3, 87, "base_module_structure.jac:23:0-23:5"),
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
        lsp.deep_check(circle_file)
        sem_list = lsp.get_semantic_tokens(circle_file).data
        expected_counts = [
            ("<JacSemTokenType.VARIABLE: 8>, <JacSemTokenModifier.READONLY: 4>", 12),
            (
                "<JacSemTokenType.PROPERTY: 9>, <JacSemTokenModifier.DEFINITION: 2>,",
                19,
            ),
            (
                "<JacSemTokenType.PARAMETER: 7>, <JacSemTokenModifier.DECLARATION: 1>,",
                5,
            ),
            (
                "<JacSemTokenType.FUNCTION: 12>, <JacSemTokenModifier.DECLARATION: 1>,",
                9,
            ),
            ("<JacSemTokenType.METHOD: 13>, <JacSemTokenModifier.DECLARATION: 1>", 6),
            ("<JacSemTokenType.ENUM: 3>, <JacSemTokenModifier.DECLARATION: 1>,", 4),
            ("<JacSemTokenType.CLASS: 2>, <JacSemTokenModifier.DECLARATION: ", 12),
            (
                "<JacSemTokenType.NAMESPACE: 0>, <JacSemTokenModifier.DEFINITION: 2>,",
                3,
            ),
        ]
        for token_type, expected_count in expected_counts:
            self.assertEqual(str(sem_list).count(token_type), expected_count)

    def test_completion(self) -> None:
        """Test that the completions are correct."""
        lsp = JacLangServer()
        workspace_path = self.fixture_abs_path("")
        workspace = Workspace(workspace_path, lsp)
        lsp.lsp._workspace = workspace
        base_module_file = uris.from_fs_path(
            self.fixture_abs_path("base_module_structure.jac")
        )
        lsp.deep_check(base_module_file)
        test_cases = [
            (lspt.Position(38, 16), ["get_color1", "color1", "point1"], 3),
            (lspt.Position(42, 22), ["RED", "GREEN", "BLUE"], 3),
            (lspt.Position(42, 34), ["RED", "GREEN", "BLUE"], 3),
            (lspt.Position(42, 45), ["REsD", "GREEN", "BLUE"], 3),
            (lspt.Position(46, 20), ["RED22", "GREEN22", "BLUE22"], 3),
            (lspt.Position(46, 30), ["RED22", "GREEN22", "BLUE22"], 3),
            (lspt.Position(46, 41), ["RED22", "GREEN22", "BLUE22"], 3),
            (
                lspt.Position(52, 32),
                ["RED22", "GREEN22", "BLUE22"],
                3,
            ),
            (
                lspt.Position(66, 13),
                [
                    "get_color1",
                    "color1",
                    "point1",
                    "base_colorred",
                    "pointred",
                    "inner_red",
                    "doubleinner",
                    "apply_red",
                ],
                8,
            ),
            (
                lspt.Position(66, 23),
                ["color22", "doublepoint22", "point22", "apply_inner_red", "enum_red"],
                5,
            ),
            (
                lspt.Position(66, 31),
                ["RED22", "GREEN22", "BLUE22"],
                3,
            ),
            (
                lspt.Position(73, 12),
                [
                    "get_color1",
                    "color1",
                    "point1",
                    "base_colorred",
                    "pointred",
                    "inner_red",
                    "doubleinner",
                    "apply_red",
                ],
                8,
            ),
            (
                lspt.Position(74, 22),
                ["color22", "doublepoint22", "apply_inner_red", "point22", "enum_red"],
                5,
            ),
            (
                lspt.Position(37, 12),
                ["self", "add", "subtract", "x", "Colorenum", "Colour1", "red", "r"],
                8,
                None,
            ),
        ]
        default_trigger = "."
        for case in test_cases:
            position, expected_completions, expected_length = case[:3]
            completion_trigger = case[3] if len(case) > 3 else default_trigger
            completions = lsp.get_completion(
                base_module_file, position, completion_trigger=completion_trigger
            ).items
            for completion in expected_completions:
                self.assertIn(completion, str(completions))
            self.assertEqual(expected_length, len(completions))

            if position == lspt.Position(73, 12):
                self.assertEqual(
                    2, str(completions).count("kind=<CompletionItemKind.Function: 3>")
                )
                self.assertEqual(
                    4, str(completions).count("kind=<CompletionItemKind.Field: 5>")
                )

    def test_go_to_reference(self) -> None:
        """Test that the go to reference is correct."""
        lsp = JacLangServer()
        workspace_path = self.fixture_abs_path("")
        workspace = Workspace(workspace_path, lsp)
        lsp.lsp._workspace = workspace

        circle_file = uris.from_fs_path(self.fixture_abs_path("circle.jac"))
        lsp.deep_check(circle_file)
        test_cases = [
            (47, 12, ["circle.jac:47:8-47:14", "69:8-69:14", "74:8-74:14"]),
            (54, 66, ["54:62-54:76", "65:28-65:42"]),
            (62, 14, ["65:49-65:62", "70:38-70:51"]),
        ]
        for line, char, expected_refs in test_cases:
            references = str(lsp.get_references(circle_file, lspt.Position(line, char)))
            for expected in expected_refs:
                self.assertIn(expected, references)
