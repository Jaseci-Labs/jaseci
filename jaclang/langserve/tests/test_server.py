from jaclang.utils.test import TestCase
from jaclang.vendor.pygls import uris
from jaclang.langserve.engine import JacLangServer
from .session import LspSession


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

    def test_diagnostics(self) -> None:
        """Test diagnostics."""
        lsp = JacLangServer("jac-lsp", "v0.1.0")
        # Set up the workspace path to "fixtures/"
        workspace_path = os.path.join(os.path.dirname(__file__), "fixtures")
        workspace = Workspace(workspace_path, lsp)

        # Initialize the server with the workspace
        initialize_params = InitializeParams(
            process_id=None,
            root_uri=f"file://{workspace_path}",
            capabilities={},
            trace="off",
            workspace_folders=None,
        )
        lsp.lsp.bf_initialize(initialize_params)

        # Open a test document from the "fixtures/" directory
        test_file_path = os.path.join(workspace_path, "test_file.jac")
        with open(test_file_path, "r") as f:
            test_file_content = f.read()

        document = TextDocumentItem(
            uri=f"file://{test_file_path}",
            language_id="jac",
            version=1,
            text=test_file_content,
        )

        lsp.lsp.text_document_did_open(
            DidOpenTextDocumentParams(text_document=document)
        )

        # Now you can call the diagnostics method and assert its results
        diagnostics = lsp.get_diagnostics(test_file_path)
        self.assertIsNotNone(diagnostics)
        self.assertGreater(len(diagnostics), 0, "No diagnostics found")
