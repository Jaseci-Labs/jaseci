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
        self.assertEqual(8, len(lsp.get_document_symbols(circle_file)))

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
            (2, 16, "datetime.py:0:0-0:0"),
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
            (lspt.Position(37, 16), ["get_color1", "color1", "point1"], 3),
            (
                lspt.Position(51, 12),
                [
                    "get_color1",
                    "color1",
                    "point1",
                    "base_colorred",
                    "pointred",
                    "color2",
                ],
                6,
            ),
            (lspt.Position(52, 19), ["color22", "point22"], 2),
        ]
        for position, expected_completions, expected_length in test_cases:
            completions = lsp.get_completion(
                base_module_file, position, completion_trigger="."
            ).items
            for completion in expected_completions:
                self.assertIn(completion, str(completions))
            self.assertEqual(expected_length, len(completions))

            if position == lspt.Position(47, 12):
                self.assertEqual(
                    1, str(completions).count("kind=<CompletionItemKind.Function: 3>")
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

    def test_update_sem_tok_1(self) -> None:
        """Test when change is in between tokens ."""
        import copy

        # fmt: off
        initial_sem_tokens = [
            1, 10, 4, 0, 2, 3, 4, 14, 12, 1, 0, 15, 6, 7, 1, 0, 8, 5, 2, 1,
            0, 10, 5, 2, 1, 1, 11, 4, 0, 2, 0, 10, 6, 7, 1, 0, 9, 6, 7, 1
        ]
        # fmt: on
        test_cases = [
            (
                lspt.Position(line=0, character=0),
                lspt.Position(line=0, character=0),
                "\n",
                0,
                "Multiline before first token (Basic)",
                "2, 10, 4, 0, 2, 3, 4, 14,",
            ),
            (
                lspt.Position(line=5, character=19),
                lspt.Position(line=5, character=19),
                "\n    ",
                0,
                "Multiline between tokens (Basic)",
                "2, 1, 6, 6, 7, 1, ",
            ),
            (
                lspt.Position(line=4, character=37),
                lspt.Position(line=4, character=37),
                "\n",
                0,
                "Multiline at end of line",
                " 2, 1, 1, 0, 5, 2, 1, ",
            ),
            (
                lspt.Position(line=5, character=20),
                lspt.Position(line=5, character=20),
                " ",
                0,
                "Sameline space between tokens (Basic)",
                " 0, 11, 6, 7, 1,",
            ),
            (
                lspt.Position(line=5, character=20),
                lspt.Position(line=5, character=20),
                "    ",
                0,
                "Sameline tab between tokens (Basic)",
                "0, 14, 6, 7, 1",
            ),
            (
                lspt.Position(line=5, character=21),
                lspt.Position(line=5, character=21),
                "   ",
                0,
                "Tab at start of a token",
                "0, 13, 6, 7, 1, ",
            ),
            (
                lspt.Position(line=5, character=13),
                lspt.Position(line=5, character=13),
                "calculate",
                0,
                "insert inside a token",
                " 1, 11, 13, 0, 2, 0, 19, 6, 7, 1",
            ),
            (
                lspt.Position(line=5, character=12),
                lspt.Position(line=5, character=14),
                "calculate",
                2,
                "insert inside a token in a selected range",
                "1, 11, 11, 0, 2, 0, 17, 6, 7, 1,",
            ),
            (
                lspt.Position(line=5, character=21),
                lspt.Position(line=5, character=21),
                "\n    ",
                0,
                "Newline at start of a token",
                "0, 2, 1, 4, 6, 7, 1, 0",
            ),
            (
                lspt.Position(line=4, character=19),
                lspt.Position(line=4, character=19),
                "\n    ",
                0,
                "Newline after parenthesis ",
                "12, 1, 1, 4, 6, 7, 1, 0, 8",
            ),
            (
                lspt.Position(line=5, character=27),
                lspt.Position(line=5, character=27),
                "\n    ",
                0,
                "Insert Newline at end of a token",
                "7, 1, 1, 7, 6, 7, ",
            ),
            (
                lspt.Position(line=5, character=4),
                lspt.Position(line=5, character=4),
                "",
                4,
                "Deletion Basic ",
                "0, 10, 5, 2, 1, 1, 7, 4, 0, 2, 0",
            ),
            (
                lspt.Position(line=3, character=49),
                lspt.Position(line=4, character=0),
                "",
                4,
                "Multiline Deletion ",
                ", 2, 2, 53, 14, 12, 1, 0",
            ),
            (
                lspt.Position(line=5, character=12),
                lspt.Position(line=5, character=13),
                "",
                1,
                "single Deletion inside token ",
                "1, 1, 11, 3, 0, 2, 0, 9, 6,",
            ),
            (
                lspt.Position(line=4, character=10),
                lspt.Position(line=4, character=15),
                "",
                5,
                "Deletion inside token- selected range ",
                " 4, 9, 12, 1, 0, 10, 6,",
            ),
            (
                lspt.Position(line=4, character=44),
                lspt.Position(line=5, character=4),
                "",
                5,
                "selected Multi line Deletion ",
                " 4, 0, 2, 3, 4, 14, 12, 1, 0, 15, ",
            ),
            (
                lspt.Position(line=4, character=26),
                lspt.Position(line=4, character=27),
                ':= a + a // 2) > 5 {\n        print("b is grater than 5");\n    }',
                1,
                "multi line insert on selected region ",
                " 2, 1, 2, 14, 5, 2, 1, 1, ",
            ),
        ]
        document_lines = [
            "",
            "import:py math;",
            "",
            '"""Function to calculate the area of a circle."""',
            "can calculate_area(radius: float) -> float {",
            "    return math.pi * radius * radius;",
            "}",
            " ",
        ]

        for case_index, case in enumerate(test_cases):
            doc_lines = copy.deepcopy(document_lines)
            if case_index == 0:
                doc_lines.insert(1, "")
            elif case_index == 1:
                doc_lines[5] = "    return math.pi "
                doc_lines.insert(6, "    * radius * radius;")
            elif case_index == 2:
                doc_lines[4] = "can calculate_area(radius: float) -> "
                doc_lines.insert(5, "float {")
            elif case_index == 8:
                doc_lines[5] = "    return math.pi * "
                doc_lines.insert(6, "    radius * radius;")
            elif case_index == 9:
                doc_lines[4] = "can calculate_area("
                doc_lines.insert(5, "    radius: float) -> float {")
            elif case_index == 10:
                doc_lines[5] = "    return math.pi * radius"
                doc_lines.insert(6, "     * radius;")
            elif case_index == 12:
                doc_lines[3] = (
                    '"""Function to calculate the area of a circle."""can calculate_area(radius: float) -> float {'
                )
                del doc_lines[4]
            elif case_index == 15:
                doc_lines[3] = (
                    "can calculate_area(radius: float) -> float {return math.pi * radius * radius;"
                )
                del doc_lines[4]
            elif case_index == 16:
                doc_lines = [
                    "",
                    "import:py math;",
                    "",
                    '"""Function to calculate the area of a circle."""',
                    "can calculate_area(radius::= a + a // 2) > 5 {",
                    '        print("b is grater than 5");',
                    "    }float) -> float {",
                    "    return math.pi * radius * radius;",
                    "}",
                    " ",
                ]

            mod = ModuleInfo.update_sem_tokens(
                "circle_ir",
                lspt.DidChangeTextDocumentParams(
                    text_document=lspt.VersionedTextDocumentIdentifier(
                        version=32,
                        uri="...jaclang/examples/manual_code/circle.jac",
                    ),
                    content_changes=[
                        lspt.TextDocumentContentChangeEvent_Type1(
                            range=lspt.Range(
                                start=case[0],
                                end=case[1],
                            ),
                            text=case[2],
                            range_length=case[3],
                        )
                    ],
                ),
                sem_tokens=copy.deepcopy(initial_sem_tokens),
                document_lines=doc_lines,
            )
            self.assertIn(case[5], str(mod), f"\nFailed for case: {case[4]}")
