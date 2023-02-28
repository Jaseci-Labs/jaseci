############################################################################
# Copyright(c) Open Law Library. All rights reserved.                      #
# See ThirdPartyNotices.txt in the project root for additional notices.    #
#                                                                          #
# Licensed under the Apache License, Version 2.0 (the "License")           #
# you may not use this file except in compliance with the License.         #
# You may obtain a copy of the License at                                  #
#                                                                          #
#     http: // www.apache.org/licenses/LICENSE-2.0                         #
#                                                                          #
# Unless required by applicable law or agreed to in writing, software      #
# distributed under the License is distributed on an "AS IS" BASIS,        #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. #
# See the License for the specific language governing permissions and      #
# limitations under the License.                                           #
############################################################################
import asyncio
from functools import partial
import os
import time
import uuid
from typing import Optional
from jaseci.jac.ir.ast_builder import (
    JacAstBuilder,
)
from jaseci.utils.utils import logger

from server.passes import ReferencePass
from .utils import debounce


from lsprotocol.types import (
    TEXT_DOCUMENT_DOCUMENT_SYMBOL,
    TEXT_DOCUMENT_COMPLETION,
    WORKSPACE_SYMBOL,
    TEXT_DOCUMENT_DID_CLOSE,
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_SAVE,
    TEXT_DOCUMENT_HOVER,
    DiagnosticSeverity,
)

from pygls.workspace import Workspace

from lsprotocol.types import (
    CompletionItem,
    CompletionList,
    CompletionOptions,
    CompletionParams,
    ConfigurationItem,
    Diagnostic,
    DidChangeTextDocumentParams,
    DidCloseTextDocumentParams,
    DidSaveTextDocumentParams,
    MarkedString,
    DidOpenTextDocumentParams,
    MessageType,
    Position,
    Range,
    TextDocumentItem,
    Registration,
    RegistrationParams,
    WorkspaceConfigurationParams,
    DocumentSymbolParams,
    WorkspaceSymbolParams,
    Hover,
    HoverParams,
    MarkupContent,
    MarkupKind,
)
from pygls.server import LanguageServer
from server.document_symbols import (
    get_architype_ast,
    get_change_block_text,
    get_document_symbols,
    get_tree_architypes,
    remove_symbols_in_range,
)

from server.utils import deconstruct_error_message

COUNT_DOWN_START_IN_SECONDS = 10
COUNT_DOWN_SLEEP_IN_SECONDS = 1


class JacLanguageServer(LanguageServer):
    CMD_COUNT_DOWN_BLOCKING = "countDownBlocking"
    CMD_COUNT_DOWN_NON_BLOCKING = "countDownNonBlocking"
    CMD_PROGRESS = "progress"
    CMD_REGISTER_COMPLETIONS = "registerCompletions"
    CMD_SHOW_CONFIGURATION_ASYNC = "showConfigurationAsync"
    CMD_SHOW_CONFIGURATION_CALLBACK = "showConfigurationCallback"
    CMD_SHOW_CONFIGURATION_THREAD = "showConfigurationThread"
    CMD_UNREGISTER_COMPLETIONS = "unregisterCompletions"

    CONFIGURATION_SECTION = "jacServer"

    def __init__(self, *args):
        super().__init__(*args)
        self.diagnostics_debounce = None
        self.workspace_filled = False


def fill_workspace(ls):
    """Fills the workspace with documents."""
    # get all files in the workspace
    files = [
        os.path.join(root, name)
        for root, dirs, files in os.walk(ls.workspace.root_path)
        for name in files
        if name.endswith(".jac")
    ]

    try:
        for file in files:
            with open(file, "r") as f:
                text = f.read()

            doc = TextDocumentItem(
                uri="file://" + file, text=text, language_id="jac", version=0
            )
            ls.workspace.put_document(doc)

            _diagnose(ls, doc.uri)

        ls.workspace_filled = True
    except Exception as e:
        logger.error(e)

    # def on_text_document_did_open(self, text_document: TextDocumentItem):
    #     self.show_message("file opened")
    #     jac_server.show_message("testing")
    #     self.workspace[text_document.uri] = text_document

    #     diagnostics = self._diagnose(text_document.uri)

    #     self.publish_diagnostics(text_document.uri, diagnostics)

    # def on_text_document_did_change(self, text_document: TextDocumentItem):
    #     self.workspace[text_document.uri] = text_document

    # diagnostics = self._diagnose(text_document.uri)

    # self.publish_diagnostics(text_document.uri, diagnostics)


@debounce(0.5, keyed_by="doc_uri")
def _diagnose(ls: JacLanguageServer, doc_uri: str):
    doc = ls.workspace.get_document(doc_uri)
    source = doc.source
    mod_name = os.path.basename(doc.uri).split(".")[0]
    tree = JacAstBuilder(mod_name, jac_text=source)

    errors = []

    for error in tree._parse_errors:
        unformatted_error = deconstruct_error_message(error)

        if unformatted_error is None:
            continue

        line, col, message = unformatted_error

        diagnostic = Diagnostic(
            range=Range(
                start=Position(line=line - 1, character=col),
                end=Position(line=line - 1, character=col),
            ),
            message=message,
            severity=DiagnosticSeverity.Error,
        )

        errors.append(diagnostic)

    ls.publish_diagnostics(doc.uri, errors)


jac_server = JacLanguageServer("jac-lsp", "v0.1")


@jac_server.feature(
    TEXT_DOCUMENT_COMPLETION, CompletionOptions(trigger_characters=[","])
)
def completions(params: Optional[CompletionParams] = None) -> CompletionList:
    """Returns completion items."""
    return CompletionList(
        is_incomplete=False,
        items=[
            CompletionItem(label='"'),
            CompletionItem(label="["),
            CompletionItem(label="]"),
            CompletionItem(label="{"),
            CompletionItem(label="}"),
        ],
    )


@jac_server.command(JacLanguageServer.CMD_COUNT_DOWN_BLOCKING)
def count_down_10_seconds_blocking(ls, *args):
    """Starts counting down and showing message synchronously.
    It will `block` the main thread, which can be tested by trying to show
    completion items.
    """
    for i in range(COUNT_DOWN_START_IN_SECONDS):
        ls.show_message(f"Counting down... {COUNT_DOWN_START_IN_SECONDS - i}")
        time.sleep(COUNT_DOWN_SLEEP_IN_SECONDS)


@jac_server.command(JacLanguageServer.CMD_COUNT_DOWN_NON_BLOCKING)
async def count_down_10_seconds_non_blocking(ls, *args):
    """Starts counting down and showing message asynchronously.
    It won't `block` the main thread, which can be tested by trying to show
    completion items.
    """
    for i in range(COUNT_DOWN_START_IN_SECONDS):
        ls.show_message(f"Counting down... {COUNT_DOWN_START_IN_SECONDS - i}")
        await asyncio.sleep(COUNT_DOWN_SLEEP_IN_SECONDS)


# traverse the current ast line where character was changes


# @jac_server.feature(TEXT_DOCUMENT_DID_CHANGE)
async def did_change(ls, params: DidChangeTextDocumentParams):
    """Text document did change notification."""
    _diagnose(ls, params.text_document.uri)


#     try:
#         start = time.time_ns()
#         doc = ls.workspace.get_document(params.text_document.uri)
#         [start_line, end_line, block_text] = get_change_block_text(
#             ls, params.text_document.uri, params.content_changes[0]
#         )

#         # handle whole document
#         if start_line == 0 and end_line == 0:
#             doc.symbols = get_document_symbols(ls, doc.uri)
#             return

#         change_tree = get_architype_ast(block_text)
#         architypes = get_tree_architypes(change_tree)

#         new_symbols = get_document_symbols(
#             ls,
#             params.text_document.uri,
#             architypes=architypes,
#             shift_lines=start_line,
#         )

#         retained_symbols = remove_symbols_in_range(
#             start_line, end_line, symbols=doc.symbols
#         )

#         doc.symbols = retained_symbols + new_symbols

#         print("block text", block_text)
#         end = time.time_ns()

#         print("Time to symbols changes: (ms)", (end - start) / 1000000)
#     except Exception as e:
#         print(e)


@jac_server.feature(TEXT_DOCUMENT_DID_CLOSE)
def did_close(server: JacLanguageServer, params: DidCloseTextDocumentParams):
    """Text document did close notification."""
    server.show_message("Text Document Did Close")


@jac_server.feature(TEXT_DOCUMENT_DID_SAVE)
def did_save(server: JacLanguageServer, params: DidSaveTextDocumentParams):
    """Text document did save notification."""
    _diagnose(server, params.text_document.uri)


@jac_server.feature(TEXT_DOCUMENT_DID_OPEN)
async def did_open(ls: LanguageServer, params: DidOpenTextDocumentParams):
    """Text document did open notification."""

    if ls.workspace_filled is False:
        fill_workspace(ls)
        return

    doc = ls.workspace.get_document(params.text_document.uri)

    _diagnose(ls, doc.uri)


def get_word_at_position(text: str, position: int) -> str:
    """
    Given some text and the position of a starting character,
    returns the word containing the starting character.
    """
    word_start = None
    word_end = None
    for i in range(position, -1, -1):
        if not text[i].isalnum() and text[i] not in ["_", "$"]:
            word_start = i + 1
            break
    if word_start is None:
        word_start = 0
    for i in range(position, len(text)):
        if not text[i].isalnum() and text[i] not in ["_", "$"]:
            word_end = i
            break
    if word_end is None:
        word_end = len(text)
    return text[word_start:word_end]


# show message when client connects

# @json_server.feature(
#     TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
#     SemanticTokensLegend(token_types=["operator"], token_modifiers=[]),
# )
# def semantic_tokens(ls: JacLanguageServer, params: SemanticTokensParams):
#     """See https://microsoft.github.io/language-server-protocol/specification#textDocument_semanticTokens
#     for details on how semantic tokens are encoded."""

#     TOKENS = ["test_walker", "another_walker"]

#     uri = params.text_document.uri
#     doc = ls.workspace.get_document(uri)

#     last_line = 0
#     last_start = 0

#     data = []

#     for lineno, line in enumerate(doc.lines):
#         last_start = 0

#         for match in TOKENS.finditer(line):
#             start, end = match.span()
#             data += [(lineno - last_line), (start - last_start), (end - start), 0, 0]

#             last_line = lineno
#             last_start = start

#     return SemanticTokens(data=data)


@jac_server.command(JacLanguageServer.CMD_PROGRESS)
async def progress(ls: JacLanguageServer, *args):
    """Create and start the progress on the client."""
    sources = ls.workspace.documents
    ls.show_message("Starting progress...")


@jac_server.command(JacLanguageServer.CMD_REGISTER_COMPLETIONS)
async def register_completions(ls: JacLanguageServer, *args):
    """Register completions method on the client."""

    params = RegistrationParams(
        registrations=[
            Registration(
                id=str(uuid.uuid4()),
                method=TEXT_DOCUMENT_COMPLETION,
                register_options={"triggerCharacters": "[':']"},
            )
        ]
    )

    response = await ls.register_capability_async(params)

    if response is None:
        ls.show_message("Successfully registered completions method")
    else:
        ls.show_message(
            "Error happened during completions registration.", MessageType.Error
        )


@jac_server.command(JacLanguageServer.CMD_SHOW_CONFIGURATION_ASYNC)
async def show_configuration_async(ls: JacLanguageServer, *args):
    """Gets exampleConfiguration from the client settings using coroutines."""
    try:
        config = await ls.get_configuration_async(
            WorkspaceConfigurationParams(
                items=[
                    ConfigurationItem(
                        scope_uri="", section=JacLanguageServer.CONFIGURATION_SECTION
                    )
                ]
            )
        )

        example_config = config[0].get("pythonPath")

        ls.show_message(f"jsonServer.exampleConfiguration value: {example_config}")
        ls.show_message(f"testing 123!!")

    except Exception as e:
        ls.show_message_log(f"Error ocurred: {e}")


@jac_server.command(JacLanguageServer.CMD_SHOW_CONFIGURATION_CALLBACK)
def show_configuration_callback(ls: JacLanguageServer, *args):
    """Gets exampleConfiguration from the client settings using callback."""

    def _config_callback(config):
        try:
            example_config = config[0].get("pythonPath")

            ls.show_message(f"jsonServer.exampleConfiguration value: {example_config}")

        except Exception as e:
            ls.show_message_log(f"Error ocurred: {e}")

    ls.get_configuration(
        WorkspaceConfigurationParams(
            items=[
                ConfigurationItem(
                    scope_uri="", section=JacLanguageServer.CONFIGURATION_SECTION
                )
            ]
        ),
        _config_callback,
    )


@jac_server.feature(WORKSPACE_SYMBOL)
async def workspace_symbol(ls: JacLanguageServer, params: WorkspaceSymbolParams):
    """Workspace symbol request."""
    symbols = []
    for doc in ls.workspace.documents.values():
        if hasattr(doc, "symbols"):
            symbols += doc.symbols
            continue

        doc.symbols = get_document_symbols(ls, doc.uri)

    return symbols


@jac_server.feature(TEXT_DOCUMENT_DOCUMENT_SYMBOL)
async def document_symbol(ls: JacLanguageServer, params: DocumentSymbolParams):
    start = time.time_ns()
    """Document symbol request."""
    uri = params.text_document.uri

    doc = ls.workspace.get_document(uri)

    # if hasattr(doc, "symbols"):
    # return doc.symbols

    doc.symbols = get_document_symbols(ls, doc.uri)

    end = time.time_ns()

    logger.info(f"Symbols Retrieved - Time: {(end - start) / 1000000}ms")

    return doc.symbols


def provide_hover(doc_uri: str, position: Position):
    pass


def get_architype_variables(ls: JacLanguageServer, uri: str, name: str, architype: str):
    """Get the variables for the given architype."""
    doc = ls.workspace.get_document(uri)

    for item in doc.architypes[architype]:
        if item["name"] == name:
            return item["vars"]

    return []


@jac_server.feature(TEXT_DOCUMENT_HOVER)
async def hover(ls: JacLanguageServer, params: HoverParams):
    """Hover request."""
    uri = params.text_document.uri
    position = params.position

    doc = ls.workspace.get_document(uri)
    source = doc.source
    line = source.split()[position.line]

    if doc.ir:
        hover_pass = ReferencePass(ir=doc.ir)
        hover_pass.run()

        ref_table = hover_pass.output

        for ref in ref_table:
            if (
                ref["line"] == position.line + 1
                and ref["start"] <= position.character <= ref["end"]
            ):
                vars = get_architype_variables(ls, uri, ref["name"], ref["architype"])
                vars = [var["name"] for var in vars]
                return Hover(
                    contents=MarkupContent(
                        kind=MarkupKind.Markdown,
                        value=f"_{ref['architype'][:-1]}_::{ref['name']}({', '.join(vars)})",
                    )
                )

    return None
