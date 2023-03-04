import asyncio
from functools import wraps
import os
import time
from threading import Timer
import uuid
from typing import Callable, Optional
from jaseci.jac.ir.ast_builder import (
    JacAstBuilder,
)
from jaseci.utils.utils import logger

from server.architypes_utils import get_architype_class
from server.passes.semantic_token_pass import SemanticTokenPass
from .completions import completions, action_modules, get_builtin_action
from server.passes import ReferencePass

# from .utils import debounce


from lsprotocol.types import (
    TEXT_DOCUMENT_DOCUMENT_SYMBOL,
    TEXT_DOCUMENT_DID_CHANGE,
    TEXT_DOCUMENT_COMPLETION,
    WORKSPACE_SYMBOL,
    TEXT_DOCUMENT_DID_CLOSE,
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_SAVE,
    TEXT_DOCUMENT_HOVER,
    TEXT_DOCUMENT_DEFINITION,
    DiagnosticSeverity,
    DefinitionParams,
    TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
    SemanticTokensLegend,
    SemanticTokensParams,
    SemanticTokens,
    SemanticTokens,
)


from lsprotocol.types import (
    CompletionList,
    CompletionOptions,
    CompletionParams,
    ConfigurationItem,
    Diagnostic,
    DidChangeTextDocumentParams,
    DidCloseTextDocumentParams,
    DidSaveTextDocumentParams,
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
    TextDocumentContentChangeEvent,
)
from pygls.server import LanguageServer
from server.document_symbols import (
    get_document_symbols,
)
from server.utils import (
    deconstruct_error_message,
    update_doc_deps,
)


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
        self._max_workers = 4

    def catch(self, log=False):
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if log:
                        self.show_message_log(str(e), MessageType.Error)
                    else:
                        self.show_message(str(e), MessageType.Error)

            return wrapper

        return decorator


def fill_workspace(ls):
    """Fills the workspace with documents."""
    # get all files in the workspace
    files = [
        os.path.join(root, name)
        for root, _dirs, files in os.walk(ls.workspace.root_path)
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
            doc = ls.workspace.get_document(doc.uri)
            update_doc_tree(ls, doc_uri=doc.uri)
            logger.info("Processing ..." + doc.uri)

        for doc in ls.workspace.documents.values():
            # architypes are present for all files at this point
            # so we can update the dependencies
            update_doc_deps(ls, doc.uri)
            # tree = JacAstBuilder(
            #     mod_name=doc.filename,
            #     mod_dir=os.path.dirname(doc.path) + "/",
            #     jac_text=doc.source,
            # )
            # doc._tree = tree
            # doc.architypes = get_tree_architypes(tree.root)
            # doc.symbols = get_document_symbols(
            #     ls, architypes=doc.architypes, doc_uri=doc.uri
            # )
            # doc.dependencies = {}
            # update_doc_deps(ls, doc.uri)

            # _diagnose(ls, doc.uri)

        ls.workspace_filled = True
    except Exception as e:
        logger.error(e)


# @debounce(0.5, keyed_by="doc_uri")
def _diagnose(ls: JacLanguageServer, doc_uri: str):
    tree = update_doc_tree(ls, doc_uri)

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

    ls.publish_diagnostics(doc_uri, errors)


jac_server = JacLanguageServer("jac-lsp", "v0.1")


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


@jac_server.feature(TEXT_DOCUMENT_DID_CHANGE)
async def did_change(ls, params: DidChangeTextDocumentParams):
    """Text document did change notification."""
    updated = soft_update(ls, params.text_document.uri, params.content_changes[0])
    if not updated:
        update_doc_tree_debounced(ls, params.text_document.uri)


@jac_server.feature(TEXT_DOCUMENT_DID_CLOSE)
def did_close(server: JacLanguageServer, params: DidCloseTextDocumentParams):
    """Text document did close notification."""
    server.show_message("Jac document closed")


@jac_server.thread()
@jac_server.feature(TEXT_DOCUMENT_DID_SAVE)
def did_save(ls: JacLanguageServer, params: DidSaveTextDocumentParams):
    """Text document did save notification."""
    # doc = ls.workspace.get_document(params.text_document.uri)
    # tree = JacAstBuilder(
    #     "test",
    #     mod_dir=os.dirname(doc.path),
    #     jac_text=doc.source,
    #     start_rule="import_module",
    # )
    # imports = ImportPass(ir=tree.root)
    # imports.run()

    _diagnose(ls, params.text_document.uri)


@jac_server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: JacLanguageServer, params: DidOpenTextDocumentParams):
    """Text document did open notification."""
    if ls.workspace_filled is False:
        fill_workspace(ls)
        try:
            ls.semantic_tokens_refresh()
        except Exception as e:
            logger.error(e)

    # _diagnose(ls, doc.uri)


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


# @jac_server.feature(
#     TEXT_DOCUMENT_SEMANTIC_TOKENS_FULL,
#     SemanticTokensLegend(token_types=["operator", "keyword"], token_modifiers=[]),
# )
# def semantic_tokens(ls: JacLanguageServer, params: SemanticTokensParams):
#     doc = ls.workspace.get_document(params.text_document.uri)
#     token_pass = SemanticTokenPass(ir=doc._tree.root)
#     token_pass.run()
#     data = token_pass.tokens

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
@jac_server.catch()
def workspace_symbol(ls: JacLanguageServer, params: WorkspaceSymbolParams):
    """Workspace symbol request."""
    symbols = []
    for doc in ls.workspace.documents.values():
        if hasattr(doc, "symbols"):
            symbols.extend(doc.symbols)
        else:
            doc_symbols = get_document_symbols(ls, doc.uri)
            symbols.extend(doc_symbols)

    return symbols


@jac_server.feature(TEXT_DOCUMENT_DOCUMENT_SYMBOL)
def document_symbol(ls: JacLanguageServer, params: DocumentSymbolParams):
    print("Retrieving Symbols...")
    start = time.time_ns()
    """Document symbol request."""
    uri = params.text_document.uri
    doc = ls.workspace.get_document(uri)
    if hasattr(doc, "symbols"):
        return doc.symbols
    else:
        update_doc_tree(ls, uri)
        doc_symbols = get_document_symbols(ls, doc.uri)
        return doc_symbols

    logger.info(f"Symbols Retrieved - Time: {(end - start) / 1000000}ms")

    return doc.symbols


def get_architype_data(ls: JacLanguageServer, uri: str, name: str, architype: str):
    """Get the variables for the given architype."""
    doc = ls.workspace.get_document(uri)
    if not hasattr(doc, "architypes"):
        return []

    architype_pool = doc.architypes

    for dep in doc.dependencies.values():
        architypes = dep["architypes"]
        for key, value in architypes.items():
            if key == architype:
                architype_pool[key].extend([value])

    for item in architype_pool[architype]:
        if item["name"] == name:
            return item

    return []


def get_symbol_data(ls: JacLanguageServer, uri: str, name: str, architype: str):
    """Get the variables for the given architype."""
    doc = ls.workspace.get_document(uri)
    if not hasattr(doc, "symbols"):
        return None
        doc.symbols = get_document_symbols(ls, doc.uri)

    symbols_pool = doc.symbols
    if not hasattr(doc, "dependencies"):
        doc.dependencies = update_doc_deps(ls, doc.uri)

    for dep in doc.dependencies.values():
        symbols = dep["symbols"]
        symbols_pool.extend(symbols)

    for symbol in symbols_pool:
        if symbol.name == name and symbol.kind == get_architype_class(architype):
            return symbol

    return None


@jac_server.feature(TEXT_DOCUMENT_DEFINITION)
def definition(ls: JacLanguageServer, params: DefinitionParams):
    doc_uri = params.text_document.uri
    doc = ls.workspace.get_document(doc_uri)

    position = params.position

    # handle hover for architypes
    if hasattr(doc, "_tree"):
        hover_pass = ReferencePass(
            ir=doc._tree.root, dependencies=doc._tree.dependencies
        )
        hover_pass.run()

        ref_table = hover_pass.output

        # we reverse the table so nodes that are in the current file are prioritized
        for ref in ref_table[::-1]:
            if (
                ref["line"] == position.line + 1
                and ref["start"] <= position.character <= ref["end"]
            ):
                symbol = get_symbol_data(ls, doc_uri, ref["name"], ref["architype"])

                if symbol is None:
                    return None

                return symbol.location

    else:
        return None

    return


@jac_server.thread()
@jac_server.feature(TEXT_DOCUMENT_HOVER)
@jac_server.catch()
def hover(ls: JacLanguageServer, params: HoverParams):
    """Hover request."""
    uri = params.text_document.uri
    position = params.position

    doc = ls.workspace.get_document(uri)
    source = doc.source
    line = source.splitlines()[position.line]

    # Get the word at the position and the word before it
    word_at_position = doc.word_at_position(position)
    before_word = line[: position.character].strip().split(".")[0].split(" ")[-1]

    # Check if the word is a builtin action and return the docstring
    if before_word in action_modules.keys():
        action = get_builtin_action(word_at_position, before_word)
        if action:
            args = ", ".join(action["args"])
            doc = f'_action({before_word})_: **{action["name"]}({args})**'
            if action["doc"]:
                doc += f'\n\n{action["doc"]}'

            return Hover(contents=MarkupContent(kind=MarkupKind.Markdown, value=doc))

    # handle hover for architypes
    if hasattr(doc, "_tree"):
        hover_pass = ReferencePass(ir=doc._tree.root)
        hover_pass.run()

        ref_table = hover_pass.output

        for ref in ref_table:
            if (
                ref["line"] == position.line + 1
                and ref["start"] <= position.character <= ref["end"]
            ):
                arch = get_architype_data(ls, uri, ref["name"], ref["architype"])
                vars = [var["name"] for var in arch["vars"]]
                return Hover(
                    contents=MarkupContent(
                        kind=MarkupKind.Markdown,
                        value=f"_{ref['architype'][:-1]}_::{ref['name']}({', '.join(vars)})",
                    )
                )
    else:
        return None


@jac_server.thread()
@jac_server.feature(
    TEXT_DOCUMENT_COMPLETION, CompletionOptions(trigger_characters=[".", ":"])
)
@jac_server.catch()
def handle_completions(params: Optional[CompletionParams] = None) -> CompletionList:
    return completions(jac_server, params)


def soft_update(
    ls: JacLanguageServer, doc_uri: str, change: TextDocumentContentChangeEvent
):
    """Update the document tree if certain conditions are met."""
    doc = ls.workspace.get_document(doc_uri)
    if change.text == ";" or change.text == "{" or doc.version % 10 == 0:
        update_doc_tree(ls, doc_uri)
        return True


def update_doc_tree_debounced(ls: JacLanguageServer, doc_uri: str):
    doc = ls.workspace.get_document(doc_uri)
    if hasattr(doc, "_tree_timer"):
        doc._tree_timer.cancel()

    doc._tree_timer = Timer(0.8, update_doc_tree, args=(ls, doc_uri, True))
    doc._tree_timer.start()


# @jac_server.thread()
def update_doc_tree(ls: JacLanguageServer, doc_uri: str, debounced: bool = False):
    """Update the document tree"""
    start = time.time_ns()
    doc = ls.workspace.get_document(doc_uri)
    # JacAstBuilder._ast_head_map = {}

    if doc.path in JacAstBuilder._ast_head_map.keys():
        JacAstBuilder._ast_head_map.pop(doc.path)

    tree = JacAstBuilder(
        mod_name=doc.filename,
        jac_text=doc.source,
        mod_dir=os.path.dirname(doc.path) + "/",
    )
    doc = ls.workspace.get_document(doc_uri)
    doc._tree = tree
    doc.symbols = get_document_symbols(ls, doc.uri)
    doc.dependencies = {}
    update_doc_deps(ls, doc_uri)

    end = time.time_ns()
    time_ms = (end - start) / 1000000

    if debounced:
        logger.info(f"Debounced: Updated Document Tree - Time: {time_ms}ms")
    else:
        logger.info(f"Updated Document Tree - Time: {time_ms}ms")

    return tree
