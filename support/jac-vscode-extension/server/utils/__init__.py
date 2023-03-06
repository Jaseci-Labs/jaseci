import functools
import inspect
import re
import sys
import threading
from typing import Any, Callable, Dict, Optional
from pygls.server import LanguageServer
from server.builder import JacAstBuilder
from server.document_symbols import get_document_symbols
from server.passes import ArchitypePass

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec


def deconstruct_error_message(error_message):
    pattern = re.compile(r"^.*:\sline\s(\d+):(\d+)\s-\s(.+)$")
    bad_import_pattern = re.compile(r"^.*?Line (\d+): (.+)$")

    match = bad_import_pattern.match(error_message)
    if match:
        line_number = match.group(1)
        error_text = match.group(2)

        return (
            int(line_number),
            0,
            error_text,
        )

    match = pattern.match(error_message)

    if match:
        line_number = match.group(1)
        column_number = match.group(2)
        error_text = match.group(3)

        return (
            int(line_number),
            int(column_number),
            error_text,
        )

    return None


P = ParamSpec("P")


def debounce(
    interval_s: int, keyed_by: Optional[str] = None, after=None
) -> Callable[[Callable[P, None]], Callable[P, None]]:
    """Debounce calls to this function until interval_s seconds have passed.
    Decorator copied from https://github.com/python-lsp/python-lsp-
    server
    """

    def wrapper(func: Callable[P, None]) -> Callable[P, None]:
        timers: Dict[Any, threading.Timer] = {}
        lock = threading.Lock()

        @functools.wraps(func)
        def debounced(*args: P.args, **kwargs: P.kwargs) -> None:
            sig = inspect.signature(func)
            call_args = sig.bind(*args, **kwargs)
            key = call_args.arguments[keyed_by] if keyed_by else None

            def run() -> None:
                with lock:
                    del timers[key]
                func(*args, **kwargs)
                if after:
                    after(*args, **kwargs)

                return

            with lock:
                old_timer = timers.get(key)
                if old_timer:
                    old_timer.cancel()

                timer = threading.Timer(interval_s, run)
                timers[key] = timer
                timer.start()

        return debounced

    return wrapper


def get_tree_architypes(tree: JacAstBuilder, pass_deps=False):
    """Get architypes from a tree"""
    if pass_deps:
        architype_pass = ArchitypePass(ir=tree.root, deps=tree.dependencies)
    else:
        architype_pass = ArchitypePass(ir=tree.root)
    architype_pass.run()

    architypes = architype_pass.output

    return architypes


def update_ast_head(ls: LanguageServer, doc_uri: str):
    doc = ls.workspace.get_document(doc_uri)
    JacAstBuilder._ast_head_map.pop(doc.path)

    # update the ast map
    for file, dependencies in ls.dep_table.items():
        if doc.path in dependencies:
            try:
                JacAstBuilder._ast_head_map.pop(file)
            except KeyError:
                pass


# @debounce(2, keyed_by="doc_uri")
def update_doc_deps_debounced(ls: LanguageServer, doc_uri: str):
    update_doc_deps(ls, doc_uri)


def update_doc_deps(ls: LanguageServer, doc_uri: str):
    """Update the document dependencies"""
    doc = ls.workspace.get_document(doc_uri)
    ### UPDATE SYMBOLS
    doc.dependencies = {}
    valid_sources = []

    for dep in get_ast_from_path(doc.path).dependencies:
        for path, tree in get_ast_from_path(doc.path)._ast_head_map.items():
            if path in valid_sources:
                continue

            if dep in tree.root.kid:
                valid_sources.append(path)

    ls.dep_table[doc.path] = [s for s in valid_sources if s != doc.path]

    try:
        for path, dep_tree in get_ast_from_path(doc.path)._ast_head_map.items():
            if path not in valid_sources:
                continue

            if "file://" + path == doc.uri:
                continue

            architypes = get_tree_architypes(dep_tree, pass_deps=True)
            new_symbols = get_document_symbols(
                ls, architypes=architypes, doc_uri="file://" + path
            )
            dependencies = {
                "file://" + path: {"architypes": architypes, "symbols": new_symbols}
            }
            doc.dependencies.update(dependencies)
    except Exception as e:
        pass


def get_ast_from_path(path: str):
    """Given some path, return the ast"""
    return JacAstBuilder._ast_head_map.get(path)
