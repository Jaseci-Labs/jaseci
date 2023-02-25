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
import os
import sys
import time
import uuid
from typing import Optional
from jaseci.jac.ir.ast_builder import (
    JacAstBuilder,
)


from lsprotocol.types import (
    TEXT_DOCUMENT_DOCUMENT_SYMBOL,
    TEXT_DOCUMENT_COMPLETION,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_DID_CLOSE,
    TEXT_DOCUMENT_DID_OPEN,
    DiagnosticSeverity,
)
from lsprotocol.types import (
    CompletionItem,
    CompletionList,
    CompletionOptions,
    CompletionParams,
    ConfigurationItem,
    Diagnostic,
    DidChangeTextDocumentParams,
    DidCloseTextDocumentParams,
    DidOpenTextDocumentParams,
    MessageType,
    Position,
    Range,
    TextDocumentItem,
    Registration,
    RegistrationParams,
    WorkspaceConfigurationParams,
    DocumentSymbolParams,
)
from pygls.server import LanguageServer
from server.document_symbols import get_document_symbols

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

    def on_text_document_did_open(self, text_document: TextDocumentItem):
        self.show_message("file opened")
        jac_server.show_message("testing")
        self.workspace[text_document.uri] = text_document

        diagnostics = self._diagnose(text_document.uri)

        self.publish_diagnostics(text_document.uri, diagnostics)

    def on_text_document_did_change(self, text_document: TextDocumentItem):
        self.workspace[text_document.uri] = text_document

        diagnostics = self._diagnose(text_document.uri)

        self.publish_diagnostics(text_document.uri, diagnostics)


def _diagnose(lsp: LanguageServer, doc_uri: str):
    doc = lsp.workspace.get_document(doc_uri)
    errors = []
    source = doc.source
    mod_name = os.path.basename(doc_uri).split(".")[0]
    tree = JacAstBuilder(mod_name, jac_text=source)

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
    return errors


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


@jac_server.feature(TEXT_DOCUMENT_DID_CHANGE)
def did_change(ls, params: DidChangeTextDocumentParams):
    """Text document did change notification."""
    doc = params.text_document
    ls.show_message("changed")
    try:
        diagnostics = _diagnose(ls, doc.uri)
    except Exception as e:
        print("an error", e)
    print(diagnostics)
    ls.publish_diagnostics(doc.uri, diagnostics)


@jac_server.feature(TEXT_DOCUMENT_DID_CLOSE)
def did_close(server: JacLanguageServer, params: DidCloseTextDocumentParams):
    """Text document did close notification."""
    server.show_message("Text Document Did Close")


@jac_server.feature(TEXT_DOCUMENT_DID_OPEN)
async def did_open(ls: LanguageServer, params: DidOpenTextDocumentParams):
    """Text document did open notification."""
    doc = params.text_document
    ls.show_message(f"Text Document Did Open Called (uri: {doc.uri})")
    try:
        diagnostics = _diagnose(ls, doc.uri)
        ls.publish_diagnostics(doc.uri, diagnostics)
    except Exception as e:
        print("an error", e)
    # ls.show_message_log("result")
    # result_2 = _diagnose(ls, params)


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

        example_config = config[0].get("exampleConfiguration")

        ls.show_message(f"jsonServer.exampleConfiguration value: {example_config}")
        ls.show_message(f"testing 123!!")

    except Exception as e:
        ls.show_message_log(f"Error ocurred: {e}")


@jac_server.command(JacLanguageServer.CMD_SHOW_CONFIGURATION_CALLBACK)
def show_configuration_callback(ls: JacLanguageServer, *args):
    """Gets exampleConfiguration from the client settings using callback."""

    def _config_callback(config):
        try:
            example_config = config[0].get("exampleConfiguration")

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


@jac_server.feature(TEXT_DOCUMENT_DOCUMENT_SYMBOL)
def document_symbol(ls: JacLanguageServer, params: DocumentSymbolParams):
    """Document symbol request."""
    uri = params.text_document.uri
    doc = ls.workspace.get_document(uri)
    symbols = get_document_symbols(ls, doc.uri)

    return symbols
