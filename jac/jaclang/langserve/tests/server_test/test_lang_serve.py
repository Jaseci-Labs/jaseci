"""Test for Jac language server[VSCE] features"""
import os
import pytest

from lsprotocol.types import (
    DidOpenTextDocumentParams,
    TextDocumentItem,
    DidSaveTextDocumentParams,
    DidChangeTextDocumentParams,
    DocumentFormattingParams,
    TextEdit,
    VersionedTextDocumentIdentifier,
    TextDocumentIdentifier,
)
from jaclang.langserve.engine import JacLangServer
from jaclang.langserve.server import (
    did_open,
    did_save,
    did_change,
    formatting,
)
from jaclang.langserve.tests.server_test.utils import get_code, patch_file, get_jac_file_path
from jaclang.vendor.pygls.uris import from_fs_path
from jaclang.vendor.pygls.workspace import Workspace

JAC_FILE = get_jac_file_path()

class TestLangServe:
    @pytest.mark.asyncio
    async def test_did_open_and_semantic_tokens(self):
        """Test opening a Jac file and retrieving semantic tokens."""
        ls: JacLangServer = JacLangServer()
        uri = from_fs_path(JAC_FILE)
        ls.lsp._workspace = Workspace(os.path.dirname(JAC_FILE), ls)

        code = get_code("error")
        params = DidOpenTextDocumentParams(
            text_document=TextDocumentItem(
                uri=uri,
                language_id="jac",
                version=1,
                text=code,
            )
        )
        await did_open(ls, params)

        diagnostics = ls.diagnostics.get(uri, [])
        assert isinstance(diagnostics, list)
        assert len(diagnostics) == 0

        sem_tokens = ls.get_semantic_tokens(uri)
        assert hasattr(sem_tokens, "data")
        assert isinstance(sem_tokens.data, list)
        assert len(sem_tokens.data) == 300

    @pytest.mark.asyncio
    async def test_did_open_and_simple_syntax_error(self):
        """Test diagnostics for a Jac file with a syntax error."""
        ls = JacLangServer()
        uri = from_fs_path(JAC_FILE)
        ls.lsp._workspace = Workspace(os.path.dirname(JAC_FILE), ls)

        broken_code = get_code("error")

        with patch_file(JAC_FILE, broken_code):
            params = DidOpenTextDocumentParams(
                text_document=TextDocumentItem(
                    uri=uri,
                    language_id="jac",
                    version=1,
                    text=broken_code,
                )
            )
            await did_open(ls, params)
            diagnostics = ls.diagnostics.get(uri, [])
            assert isinstance(diagnostics, list)
            assert len(diagnostics) == 1

            sem_tokens = ls.get_semantic_tokens(uri)
            assert hasattr(sem_tokens, "data")
            assert isinstance(sem_tokens.data, list)

    @pytest.mark.asyncio
    async def test_did_save(self):
        """Test saving a Jac file triggers diagnostics."""
        ls = JacLangServer()
        uri = from_fs_path(JAC_FILE)
        ls.lsp._workspace = Workspace(os.path.dirname(JAC_FILE), ls)

        code = get_code("")

        await did_open(ls, DidOpenTextDocumentParams(
            text_document=TextDocumentItem(
                uri=uri,
                language_id="jac",
                version=1,
                text=code,
            )
        ))

        params = DidSaveTextDocumentParams(
            text_document=TextDocumentItem(
                uri=uri,
                language_id="jac",
                version=2,
                text=code,
            )
        )

        await did_save(ls, params)
        diagnostics = ls.diagnostics.get(uri, [])
        assert isinstance(diagnostics, list)
        assert len(diagnostics) == 0

        broken_code = get_code("error")
        with patch_file(JAC_FILE, broken_code):
            params = DidOpenTextDocumentParams(
                text_document=TextDocumentItem(
                    uri=uri,
                    language_id="jac",
                    version=1,
                    text=broken_code,
                )
            )

            await did_open(ls, params)
            diagnostics = ls.diagnostics.get(uri, [])
            assert isinstance(diagnostics, list)
            assert len(diagnostics) == 1

    @pytest.mark.asyncio
    async def test_did_change(self):
        """Test changing a Jac file triggers diagnostics."""
        ls = JacLangServer()
        uri = from_fs_path(JAC_FILE)
        ls.lsp._workspace = Workspace(os.path.dirname(JAC_FILE), ls)
        with open(JAC_FILE, "r") as f:
            code = f.read()

        await did_open(ls, DidOpenTextDocumentParams(
            text_document=TextDocumentItem(
                uri=uri,
                language_id="jac",
                version=1,
                text=code,
            )
        ))

        params = DidChangeTextDocumentParams(
            text_document=VersionedTextDocumentIdentifier(uri=uri, version=2),
            content_changes=[{"text": "\n"+ code }]
        )
        await did_change(ls, params)
        diagnostics = ls.diagnostics.get(uri, [])
        uri = from_fs_path(JAC_FILE)
        assert isinstance(diagnostics, list)
        assert len(diagnostics) == 0

    def test_vsce_formatting(self):
        """Test formatting a Jac file returns edits."""
        ls = JacLangServer()
        uri = from_fs_path(JAC_FILE)
        ls.lsp._workspace = Workspace(os.path.dirname(JAC_FILE), ls)
        params = DocumentFormattingParams(
            text_document=TextDocumentIdentifier(uri=uri),
            options={"tabSize": 4, "insertSpaces": True}
        )
        edits = formatting(ls, params)
        assert isinstance(edits, list)
        assert isinstance(edits[0], TextEdit)
        assert len(edits[0].new_text) > 100 # it is a random number to check if the text is changed