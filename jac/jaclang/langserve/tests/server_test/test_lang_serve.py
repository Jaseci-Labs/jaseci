import os
import asyncio
import pytest
import contextlib

from lsprotocol.types import (
    DidOpenTextDocumentParams,
    TextDocumentItem,
    DidSaveTextDocumentParams,
    DidChangeTextDocumentParams,
    TextDocumentContentChangeEvent,
    DocumentFormattingParams,
    CreateFilesParams,
    FileCreate,
    Position,
    VersionedTextDocumentIdentifier,
    TextDocumentIdentifier,
)
from jaclang.langserve.engine import JacLangServer
from jaclang.langserve.server import did_open, did_save, did_change, formatting, did_create_files
from jaclang.vendor.pygls.uris import from_fs_path
from jaclang.vendor.pygls.workspace import Workspace


# Path to a sample Jac file for testing
JAC_FILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../../../examples/manual_code/circle.jac")
)

@pytest.mark.asyncio
async def test_did_open_and_semantic_tokens():
    # Create a fresh instance of the language server
    ls :JacLangServer= JacLangServer()

    uri = from_fs_path(JAC_FILE)

    # Set up workspace so the server can track the document
    ls.lsp._workspace = Workspace(os.path.dirname(JAC_FILE), ls)

    with open(JAC_FILE, "r") as f:
        code = f.read()

    # Create didOpen parameters
    params = DidOpenTextDocumentParams(
        text_document=TextDocumentItem(
            uri=uri,
            language_id="jac",
            version=1,
            text=code,
        )
    )

    # Directly call the `did_open` feature handler
    await did_open(ls, params)

    # Validate diagnostics
    diagnostics = ls.diagnostics.get(uri, [])
    print("Diagnostics:", diagnostics)
    assert isinstance(diagnostics, list)
    assert len(diagnostics) == 0

    # Validate semantic tokens
    sem_tokens = ls.get_semantic_tokens(uri)
    print("Semantic Tokens:", sem_tokens)
    assert hasattr(sem_tokens, "data")
    assert isinstance(sem_tokens.data, list)

@contextlib.contextmanager
def patch_file(filepath, new_content):
    """Temporarily replace file content for testing."""
    with open(filepath, "r") as f:
        original = f.read()
    try:
        with open(filepath, "w") as f:
            f.write(new_content)
        yield
    finally:
        with open(filepath, "w") as f:
            f.write(original)

@pytest.mark.asyncio
async def test_did_open_and_simple_syntax_error():
    ls = JacLangServer()
    uri = from_fs_path(JAC_FILE)
    ls.lsp._workspace = Workspace(os.path.dirname(JAC_FILE), ls)

    from jaclang.langserve.tests.server_test.code_test import get_code
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
        print("Diagnostics:", diagnostics)
        assert isinstance(diagnostics, list)
        assert len(diagnostics) == 1

        sem_tokens = ls.get_semantic_tokens(uri)
        print("Semantic Tokens:", sem_tokens)
        assert hasattr(sem_tokens, "data")
        assert isinstance(sem_tokens.data, list)

@pytest.mark.asyncio
async def test_did_save():
    ls = JacLangServer()
    uri = from_fs_path(JAC_FILE)
    ls.lsp._workspace = Workspace(os.path.dirname(JAC_FILE), ls)
    with open(JAC_FILE, "r") as f:
        code = f.read()
    # Open document first
    await did_open(ls, DidOpenTextDocumentParams(
        text_document=TextDocumentItem(
            uri=uri,
            language_id="jac",
            version=1,
            text=code,
        )
    ))
    # Save event
    params = DidSaveTextDocumentParams(
        text_document=TextDocumentItem(
            uri=uri,
            language_id="jac",
            version=2,
            text=code,
        )
    )
    await did_save(ls, params)
    await asyncio.sleep(1)
    diagnostics = ls.diagnostics.get(uri, [])
    assert isinstance(diagnostics, list)

@pytest.mark.asyncio
async def test_did_change():
    ls = JacLangServer()
    uri = from_fs_path(JAC_FILE)
    ls.lsp._workspace = Workspace(os.path.dirname(JAC_FILE), ls)
    with open(JAC_FILE, "r") as f:
        code = f.read()
    # Open document first
    await did_open(ls, DidOpenTextDocumentParams(
        text_document=TextDocumentItem(
            uri=uri,
            language_id="jac",
            version=1,
            text=code,
        )
    ))
    # Change event
    params = DidChangeTextDocumentParams(
        text_document=VersionedTextDocumentIdentifier(uri=uri, version=2),
        content_changes=[{"text": code + "\n"}]
    )
    await did_change(ls, params)
    await asyncio.sleep(1)
    diagnostics = ls.diagnostics.get(uri, [])
    assert isinstance(diagnostics, list)

def test_formatting():
    ls = JacLangServer()
    uri = from_fs_path(JAC_FILE)
    ls.lsp._workspace = Workspace(os.path.dirname(JAC_FILE), ls)
    # Formatting params
    params = DocumentFormattingParams(
        text_document=TextDocumentIdentifier(uri=uri),
        options={"tabSize": 4, "insertSpaces": True}
    )
    edits = formatting(ls, params)
    assert isinstance(edits, list)

def test_did_create_files():
    ls = JacLangServer()
    uri = from_fs_path(JAC_FILE)
    params = CreateFilesParams(
        files=[FileCreate(uri=uri)]
    )
    # Should not raise
    did_create_files(ls, params)
    print(ls.diagnostics)
