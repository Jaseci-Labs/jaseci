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
from jaclang.langserve.tests.server_test.utils import (
    create_temp_jac_file,
    get_code,
    get_jac_file_path,
    create_ls_with_workspace,  # new helper
)
from jaclang.vendor.pygls.uris import from_fs_path
from jaclang.vendor.pygls.workspace import Workspace
from jaclang import JacMachineInterface as _

JacLangServer = _.py_jac_import(
    "....langserve.engine", __file__, items={"JacLangServer": None}
)[0]
(did_open, did_save, did_change, formatting) = _.py_jac_import(    "....langserve.server", __file__, items={"did_open": None, "did_save": None, "did_change": None, "formatting": None})

JAC_FILE = get_jac_file_path()

class TestLangServe:
    """Test class for Jac language server features."""

    @pytest.mark.asyncio
    async def test_open_valid_file_no_diagnostics(self):
        """Test opening a Jac file with a syntax error."""
        ls = JacLangServer()

        code = get_code("")
        temp_file_path = create_temp_jac_file(code)
        uri = from_fs_path(temp_file_path)
        ls.lsp._workspace = Workspace(os.path.dirname(temp_file_path), ls)

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
        ls.shutdown()
        assert len(diagnostics) == 0

        os.remove(temp_file_path)

    @pytest.mark.asyncio
    async def test_open_with_syntax_error(self):
        """Test opening a Jac file with a syntax error."""
        ls = JacLangServer()

        code = get_code("error")
        temp_file_path = create_temp_jac_file(code)
        uri = from_fs_path(temp_file_path)
        ls.lsp._workspace = Workspace(os.path.dirname(temp_file_path), ls)

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
        ls.shutdown()
        assert len(diagnostics) == 1
        assert diagnostics[0].message == "Syntax Error"
        assert str(diagnostics[0].range) == "66:0-66:1"

        os.remove(temp_file_path)

    @pytest.mark.asyncio
    async def test_did_open_and_simple_syntax_error(self):
        """Test diagnostics for a Jac file with a syntax error."""
        ls = JacLangServer()

        code = get_code("")
        temp_file_path = create_temp_jac_file(code)
        uri = from_fs_path(temp_file_path)
        ls.lsp._workspace = Workspace(os.path.dirname(temp_file_path), ls)
    
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

        broken_code = get_code("error")
        with open(temp_file_path, "w") as f:
            f.write(broken_code)
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
        print(sem_tokens)
        ls.shutdown()
        assert hasattr(sem_tokens, "data")
        assert isinstance(sem_tokens.data, list)
        assert len(sem_tokens.data) == 0 # TODO: we should retain the sem tokens, will be fixed in next PR 

        os.remove(temp_file_path)

    @pytest.mark.asyncio
    async def test_did_save(self):
        """Test saving a Jac file triggers diagnostics."""
        code = get_code("")
        temp_file_path = create_temp_jac_file(code)
        uri, ls = create_ls_with_workspace(temp_file_path)

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

        # Now simulate a syntax error by updating the workspace and saving
        broken_code = get_code("error")
        ls.workspace.put_text_document(TextDocumentItem(
            uri=uri,
            language_id="jac",
            version=3,
            text=broken_code,
        ))
        params = DidSaveTextDocumentParams(
            text_document=TextDocumentItem(
                uri=uri,
                language_id="jac",
                version=3,
                text=broken_code,
            )
        )
        await did_save(ls, params)
        diagnostics = ls.diagnostics.get(uri, [])
        assert isinstance(diagnostics, list)
        assert len(diagnostics) == 1
        assert diagnostics[0].message == "Syntax Error"

        ls.shutdown()
        os.remove(temp_file_path)

    @pytest.mark.asyncio
    async def test_did_change(self):
        """Test changing a Jac file triggers diagnostics."""
        code = get_code("")
        temp_file_path = create_temp_jac_file(code)
        uri, ls = create_ls_with_workspace(temp_file_path)

        await did_open(ls, DidOpenTextDocumentParams(
            text_document=TextDocumentItem(
                uri=uri,
                language_id="jac",
                version=1,
                text=code,
            )
        ))

        # No error, should be no diagnostics
        params = DidChangeTextDocumentParams(
            text_document=VersionedTextDocumentIdentifier(uri=uri, version=2),
            content_changes=[{"text": "\n" + code}]
        )
        ls.workspace.put_text_document(TextDocumentItem(
            uri=uri,
            language_id="jac",
            version=2,
            text="\n" + code,
        ))
        await did_change(ls, params)
        diagnostics = ls.diagnostics.get(uri, [])
        assert isinstance(diagnostics, list)
        assert len(diagnostics) == 0

        # Now add a syntax error and update workspace
        # This should trigger diagnostics with a syntax error
        error_code = "\nerror"
        params = DidChangeTextDocumentParams(
            text_document=VersionedTextDocumentIdentifier(uri=uri, version=3),
            content_changes=[{"text": error_code + code}]
        )
        ls.workspace.put_text_document(TextDocumentItem(
            uri=uri,
            language_id="jac",
            version=3,
            text=error_code + code,
        ))
        await did_change(ls, params)
        diagnostics = ls.diagnostics.get(uri, [])
        assert isinstance(diagnostics, list)
        assert len(diagnostics) == 1
        assert diagnostics[0].message == "Syntax Error"

        ls.shutdown()
        os.remove(temp_file_path)

    def test_vsce_formatting(self):
        """Test formatting a Jac file returns edits."""
        code = get_code("")
        temp_file_path = create_temp_jac_file(code)
        uri, ls = create_ls_with_workspace(temp_file_path)
        params = DocumentFormattingParams(
            text_document=TextDocumentIdentifier(uri=uri),
            options={"tabSize": 4, "insertSpaces": True}
        )
        edits = formatting(ls, params)
        assert isinstance(edits, list)
        assert isinstance(edits[0], TextEdit)
        assert len(edits[0].new_text) > 100  # it is a random number to check if the text is changed
        print(edits[0].new_text)
        ls.shutdown()
        os.remove(temp_file_path)