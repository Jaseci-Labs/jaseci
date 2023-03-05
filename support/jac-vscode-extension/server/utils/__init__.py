import functools
import inspect
import os
import re
import sys
import threading
from typing import Any, Callable, Dict, Optional
from pygls.server import LanguageServer
from server.builder import JacAstBuilderSLL
from server.document_symbols import get_document_symbols
from server.passes import ArchitypePass

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec


def deconstruct_error_message(error_message):
    pattern = re.compile(r"^.*:\sline\s(\d+):(\d+)\s-\s(.+)$")

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


def get_tree_architypes(tree: JacAstBuilderSLL):
    """Get architypes from a tree"""
    architype_pass = ArchitypePass(ir=tree)
    architype_pass.run()

    architypes = architype_pass.output

    return architypes


def update_doc_deps(ls: LanguageServer, doc_uri: str):
    """Update the document dependencies"""
    doc = ls.workspace.get_document(doc_uri)
    # get architypes for dependencies
    for dep in doc._tree.dependencies:
        mod_name = dep.loc[2]
        if mod_name not in doc.dependencies:
            doc.dependencies[mod_name] = {
                "architypes": {"nodes": [], "edges": [], "walkers": [], "graphs": []},
                "symbols": [],
            }

        new_architypes = get_tree_architypes(dep)

        for key, value in new_architypes.items():
            doc.dependencies[mod_name]["architypes"][key].extend(value)

    ### UPDATE SYMBOLS
    # find a uri that end with the module name and is not the current document and create symbols
    for mod_name in doc.dependencies.keys():
        uri_matches = [
            uri
            for uri in ls.workspace.documents.keys()
            if os.path.basename(uri) == mod_name and uri != doc.uri
        ]

        for uri in uri_matches:
            matched_architypes = {"nodes": [], "edges": [], "walkers": [], "graphs": []}
            uri_doc = ls.workspace.get_document(uri)
            # some dependencies might not have been parsed yet
            if not hasattr(uri_doc, "architypes"):
                continue

            match_architypes = uri_doc.architypes

            # compare architypes in the current document with the architypes in the dependency
            for slot, value in match_architypes.items():
                try:
                    for architype in value:
                        # some architypes are lists and idk why, gotta investigate
                        if not isinstance(architype, dict):
                            continue
                        if list(
                            filter(
                                lambda x: x["name"] == architype["name"],
                                doc.dependencies[architype["src"]]["architypes"][slot],
                            )
                        ):
                            matched_architypes[slot].extend([architype])
                except Exception as e:
                    # we gotta keep going
                    print(e)
            new_symbols = get_document_symbols(
                ls, architypes=matched_architypes, doc_uri=uri
            )
            doc.dependencies[mod_name]["symbols"].extend(new_symbols)
