import asyncio
from functools import wraps
import os
import time
import uuid
from typing import Callable, Optional
from jaseci.jac.ir.ast_builder import (
    JacAstBuilder,
)


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
    Location,
    TEXT_DOCUMENT_DID_OPEN,
    TEXT_DOCUMENT_DID_SAVE,
    TEXT_DOCUMENT_HOVER,
    TEXT_DOCUMENT_DEFINITION,
    DiagnosticSeverity,
    DefinitionParams,
)


from lsprotocol.types import (
    CompletionList,
    CompletionOptions,
    CompletionParams,
    ConfigurationItem,
    Diagnostic,
    DidChangeTextDocumentParams,
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
    get_ast_from_path,
    update_ast_head,
    update_doc_deps,
    update_doc_deps_debounced,
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
        super().__init__(*args, max_workers=4)
        self.diagnostics_debounce = None
        self.workspace_filled = False
        # more works = more memory, more memory = more responsive
        self.dep_table = {}

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
            ls.workspace
            ls.workspace.put_document(doc)
            doc = ls.workspace.get_document(doc.uri)
            update_doc_tree(ls, doc_uri=doc.uri)

        # update all dependencies
        for doc in ls.workspace.documents.values():
            update_doc_deps(ls, doc_uri=doc.uri)
        ls.workspace_filled = True
    except Exception as e:
        pass


def get_doc_errors(ls: JacLanguageServer, doc_uri: str, parse_errors: list):
    errors = []

    for error in parse_errors:
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
    try:
        updated = soft_update(ls, params.text_document.uri, params.content_changes[0])
        if not updated:
            update_doc_tree_debounced(ls, params.text_document.uri)
    except Exception as e:
        pass


# @jac_server.thread()
@jac_server.feature(TEXT_DOCUMENT_DID_SAVE)
def did_save(ls: JacLanguageServer, params: DidSaveTextDocumentParams):
    """Text document did save notification."""
    doc = ls.workspace.get_document(params.text_document.uri)
    if doc.version > 1:
        update_ast_head(ls, doc.uri)
        update_doc_tree_debounced(ls, doc.uri)


@jac_server.feature(TEXT_DOCUMENT_DID_OPEN)
def did_open(ls: JacLanguageServer, params: DidOpenTextDocumentParams):
    """Text document did open notification."""

    if ls.workspace_filled is False:
        try:
            fill_workspace(ls)

        except Exception as e:
            pass


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
    """Document symbol request."""
    uri = params.text_document.uri
    doc = ls.workspace.get_document(uri)
    if hasattr(doc, "symbols"):
        return [s for s in doc.symbols if s.location.uri == uri]
    else:
        update_doc_tree(ls, uri)
        doc_symbols = get_document_symbols(ls, doc.uri)
        return [s for s in doc_symbols if s.location.uri == uri]


@jac_server.thread()
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
                architype_pool[key].extend(value)

    for item in architype_pool[architype]:
        if item["name"] == name:
            return item

    return []


def get_symbol_data(ls: JacLanguageServer, uri: str, name: str, architype: str):
    """Returns the symbol data for the given architype."""
    doc = ls.workspace.get_document(uri)
    if not hasattr(doc, "symbols"):
        return None
        doc.symbols = get_document_symbols(ls, doc.uri)

    symbols_pool = doc.symbols
    if not hasattr(doc, "dependencies"):
        update_doc_deps(ls, doc.uri)

    for dep in doc.dependencies.values():
        symbols = dep["symbols"]
        symbols_pool.extend(symbols)

    for symbol in symbols_pool[::-1]:
        # we want to consider dependencies first because the dependencies are in doc.symbols with the wrong uri
        # doc.dependencies have the correct uri
        if symbol.name == name and symbol.kind == get_architype_class(architype):
            return symbol

    return None


def handle_go_to_file(ls: JacLanguageServer, uri: str, position: Position):
    """Handles the go to file request."""
    doc = ls.workspace.get_document(uri)
    line = doc.lines[position.line]
    tokens = line.split()

    try:
        if (
            tokens[0] == "import"
            and tokens[2] == "with"
            and (line.endswith(";\n") or line.endswith(";"))
        ):
            relative_path = tokens[3].strip("\"';")
            base_path = os.path.dirname(doc.path)
            file_path = os.path.abspath(os.path.join(base_path, relative_path))

            if os.path.exists(file_path):
                location = Location(
                    uri="file://" + file_path,
                    range=Range(
                        start=Position(line=0, character=0),
                        end=Position(line=0, character=0),
                    ),
                )
                return location

    except IndexError:
        return None

    return None


# @jac_server.thread()
@jac_server.feature(TEXT_DOCUMENT_DEFINITION)
def definition(ls: JacLanguageServer, params: DefinitionParams):
    try:
        doc_uri = params.text_document.uri
        doc = ls.workspace.get_document(doc_uri)

        position = params.position
        file_location = handle_go_to_file(ls, doc_uri, position)
        if file_location is not None:
            return file_location

        # get symbols under cursor
        if JacAstBuilder._ast_head_map.get(doc.path):
            ref_table_pass = ReferencePass(
                ir=get_ast_from_path(doc.path).root,
                deps=get_ast_from_path(doc.path).dependencies,
            )
            try:
                ref_table_pass.run()
            except Exception:
                return None

            ref_table = ref_table_pass.output

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
    except Exception as e:
        pass


# @jac_server.thread()
@jac_server.feature(TEXT_DOCUMENT_HOVER)
def hover(ls: JacLanguageServer, params: HoverParams):
    """Hover request."""
    try:
        uri = params.text_document.uri
        position = params.position

        doc = ls.workspace.get_document(uri)
        source = doc.source
        line = source.splitlines()[position.line]

        # Get the word at the position and the word before it
        word_at_position = doc.word_at_position(position)
        before_word = (
            line[: position.character]
            .strip()
            .split(".")[0]
            .split(" ")[-1]
            .strip("=+-*<>!")
        )

        # Check if the word is a builtin action and return the docstring
        if before_word in action_modules.keys():
            action = get_builtin_action(word_at_position, before_word)
            if action:
                args = ", ".join(action["args"])
                doc = f'_action({before_word})_: **{action["name"]}({args})**'
                if action["doc"]:
                    doc += f'\n\n{action["doc"]}'

                return Hover(
                    contents=MarkupContent(kind=MarkupKind.Markdown, value=doc)
                )

        # handle hover for architypes
        if JacAstBuilder._ast_head_map.get(doc.path):
            hover_pass = ReferencePass(
                ir=get_ast_from_path(doc.path).root,
                deps=get_ast_from_path(doc.path).dependencies,
            )
            try:
                hover_pass.run()
            except Exception as e:
                pass

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
    except Exception as e:
        pass


# @jac_server.thread()
@jac_server.feature(
    TEXT_DOCUMENT_COMPLETION, CompletionOptions(trigger_characters=[".", ":"])
)
def handle_completions(params: Optional[CompletionParams] = None) -> CompletionList:
    try:
        return completions(jac_server, params)
    except Exception as e:
        pass


def soft_update(
    ls: JacLanguageServer, doc_uri: str, change: TextDocumentContentChangeEvent
):
    """Update the document tree if certain conditions are met."""
    doc = ls.workspace.get_document(doc_uri)
    if change.text == ";" or change.text == "{" or doc.version % 20 == 0:
        update_doc_tree(ls, doc_uri)
        return True


@jac_server.thread()
def update_doc_tree_debounced(ls: JacLanguageServer, doc_uri: str):
    update_doc_tree(ls, doc_uri)


@jac_server.thread()
def update_doc_tree(ls: JacLanguageServer, doc_uri: str):
    """Update the document tree"""
    start = time.time_ns()
    doc = ls.workspace.get_document(doc_uri)

    tree = JacAstBuilder(
        mod_name=doc.filename,
        jac_text=doc.source,
        mod_dir=os.path.dirname(doc.path) + "/",
    )
    if tree._parse_errors:
        errors = get_doc_errors(ls, doc_uri, tree._parse_errors)

        ls.publish_diagnostics(doc_uri, errors)
        return
    else:
        errors = get_doc_errors(ls, doc_uri, [])
        ls.publish_diagnostics(doc_uri, errors)

    doc = ls.workspace.get_document(doc_uri)
    doc.symbols = [
        s for s in get_document_symbols(ls, doc.uri) if s.location.uri == doc_uri
    ]

    try:
        if doc.version > 1:
            update_doc_deps_debounced(ls, doc_uri)
        else:
            update_doc_deps(ls, doc_uri)
    except Exception as e:
        pass

    end = time.time_ns()
    time_ms = (end - start) / 1000000

    return tree
