import os
import time
from pygls.server import LanguageServer
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from antlr4.TokenStreamRewriter import TokenStreamRewriter

from jaseci.jac.ir.ast_builder import JacAstBuilder, JacTreeBuilder

from jaseci.jac.jac_parse.jacListener import jacListener
from jaseci.jac.jac_parse.jacParser import jacParser
from jaseci.jac.jac_parse.jacLexer import jacLexer

from server.passes import ArchitypePass
from lsprotocol.types import (
    SymbolKind,
    SymbolInformation,
    Location,
    Position,
    Range,
    DidChangeTextDocumentParams,
    TextDocumentContentChangeEvent,
)
from typing import List, TypedDict

from server.utils import debounce


class ArchitypeInfo(TypedDict):
    name: str
    line: int
    col: int
    block_start: dict
    block_end: dict
    vars: list


def _get_architypes(lsp: LanguageServer, doc_uri: str, source: str = None):
    try:
        mod_name = os.path.basename(doc_uri).split(".")[0]
        doc = lsp.workspace.get_document(doc_uri)

        if not source:
            source = doc.source

        tree = JacAstBuilder(mod_name, jac_text=source)
        architype_pass = ArchitypePass(ir=tree.root)
        architype_pass.run()
        # get a dictionary of all architypes in the file
        architypes = architype_pass.output
        # print(architypes)
        return architypes
    except Exception as e:
        print(e)

        return {"nodes": [], "edges": [], "graphs": [], "walkers": []}


def _create_architype_symbol(
    type: str, node: ArchitypeInfo, doc_uri: str, shift_lines: int = 0
) -> SymbolInformation:
    """Create a symbol for a node or walker"""
    match type:
        case "node":
            kind = SymbolKind.Class
        case "walker":
            kind = SymbolKind.Function
        case "edge":
            kind = SymbolKind.Interface
        case "graph":
            kind = SymbolKind.Namespace
        case _:
            raise ValueError("invalid architype type")

    return SymbolInformation(
        name=node["name"],
        kind=kind,
        location=Location(
            uri=doc_uri,
            range=Range(
                start=Position(
                    line=node["line"] - 1 + shift_lines, character=node["col"]
                ),
                end=Position(
                    line=node["block_end"]["line"] + shift_lines,
                    character=0,
                ),
            ),
        ),
    )


def get_document_symbols(
    ls: LanguageServer,
    doc_uri: str,
    architypes: dict[str, list] = None,
    shift_lines: int = 0,
) -> List[SymbolInformation]:
    """Return a list of symbols in the document"""
    if not architypes:
        architypes = _get_architypes(ls, doc_uri)

    symbols: List[SymbolInformation] = []

    try:
        for walker in architypes["walkers"]:
            symbol = _create_architype_symbol(
                "walker", walker, doc_uri, shift_lines=shift_lines
            )
            symbols.append(symbol)

            for var in walker["vars"]:
                var_symbol = SymbolInformation(
                    name=var["name"],
                    kind=SymbolKind.Property,
                    location=Location(
                        uri=doc_uri,
                        range=Range(
                            start=Position(
                                line=var["line"] - 1 + shift_lines, character=var["col"]
                            ),
                            end=Position(
                                line=var["line"] + shift_lines,
                                character=var["col"] + len(var["name"]),
                            ),
                        ),
                    ),
                    container_name=walker["name"],
                )

                symbols.append(var_symbol)
    except Exception as e:
        print(e)

    for node in architypes["nodes"]:
        node_symbol = _create_architype_symbol(
            "node", node, doc_uri, shift_lines=shift_lines
        )

        symbols.append(node_symbol)

        for var in node["vars"]:
            var_symbol = SymbolInformation(
                name=var["name"],
                kind=SymbolKind.Property,
                location=Location(
                    uri=doc_uri,
                    range=Range(
                        start=Position(
                            line=var["line"] - 1 + shift_lines, character=var["col"]
                        ),
                        end=Position(
                            line=var["line"] + shift_lines,
                            character=var["col"] + len(var["name"]),
                        ),
                    ),
                ),
                container_name=node["name"],
            )

            symbols.append(var_symbol)

    for edge in architypes["edges"]:
        symbol = _create_architype_symbol(
            "edge", edge, doc_uri, shift_lines=shift_lines
        )
        symbols.append(symbol)

        for var in edge["vars"]:
            var_symbol = SymbolInformation(
                name=var["name"],
                kind=SymbolKind.Property,
                location=Location(
                    uri=doc_uri,
                    range=Range(
                        start=Position(
                            line=var["line"] - 1 + shift_lines, character=var["col"]
                        ),
                        end=Position(
                            line=var["line"] + shift_lines,
                            character=var["col"] + len(var["name"]),
                        ),
                    ),
                ),
                container_name=edge["name"],
            )

            symbols.append(var_symbol)
    for graph in architypes["graphs"]:
        symbol = _create_architype_symbol(
            "graph", graph, doc_uri, shift_lines=shift_lines
        )
        symbols.append(symbol)

        for var in graph["vars"]:
            var_symbol = SymbolInformation(
                name=var["name"],
                kind=SymbolKind.Property,
                location=Location(
                    uri=doc_uri,
                    range=Range(
                        start=Position(
                            line=var["line"] - 1 + shift_lines, character=var["col"]
                        ),
                        end=Position(
                            line=var["line"] + shift_lines,
                            character=var["col"] + len(var["name"]),
                        ),
                    ),
                ),
                container_name=graph["name"],
            )

            symbols.append(var_symbol)
    return symbols


# def symbol_has_children(symbol: SymbolInformation):
#     """Check if a symbol has children (e.g. a walker with variables)"""
#     if symbol.location.range.end.line > symbol.location.range.start.line:
#         return True
#     return False


# def update_symbol(
#     ls: LanguageServer, doc_uri: str, changes: List[TextDocumentContentChangeEvent]
# ):
#     start = time.time_ns()
#     # get document
#     doc = ls.workspace.get_document(doc_uri)

#     # check if there is a symbol at the line
#     if hasattr(doc, "symbols"):
#         for change in changes:
#             change: TextDocumentContentChangeEvent = change

#             new_symbols = []

#             if (change.text == "\n" and change.range_length == 0) or (
#                 change.text == "" and change.range_length == 1
#             ):
#                 shift = 1

#                 if (
#                     change.text == ""
#                     and (change.range.end.line - change.range.start.line) == -1
#                 ):
#                     shift = -1

#                 # move symbols down one line
#                 retained_symbols = [
#                     s
#                     for s in doc.symbols
#                     if s.location.range.start.line < change.range.start.line
#                 ]
#                 new_symbols = [
#                     s
#                     for s in doc.symbols
#                     if s.location.range.start.line > change.range.start.line
#                 ]
#                 for s in new_symbols:
#                     s.location.range.start.line += shift
#                     s.location.range.end.line += shift

#                 retained_symbols.extend(new_symbols)
#                 doc.symbols = retained_symbols

#             # parse the code block (e.g walker block)
#             # for symbol in doc.symbols:
#             #     parent_symbol: SymbolInformation = symbol

#             #     # check if change is in symbol range
#             #     if (
#             #         parent_symbol.location.range.start.line <= change.range.start.line
#             #         and parent_symbol.location.range.end.line >= change.range.start.line
#             #         and parent_symbol.kind != SymbolKind.Property
#             #     ):
#             #         # get text of parent block
#             #         text_start_line = parent_symbol.location.range.start.line
#             #         text_end_line = parent_symbol.location.range.end.line

#             #         parent_text = "".join(doc.lines[text_start_line:text_end_line])

#             #         # get architypes from parent block
#             #         architypes = _get_architypes(ls, doc_uri, parent_text)

#             #         # create new symbols for the architypes
#             #         new_symbols = get_document_symbols(
#             #             ls, doc_uri, architypes, shift_lines=text_start_line
#             #         )

#             #         # remove old symbols in parent block
#             #         for symbol in doc.symbols:
#             #             if symbol.location.range.start.line < text_start_line:
#             #                 new_symbols.append(symbol)
#             #             elif symbol.location.range.start.line > text_end_line:
#             #                 new_symbols.append(symbol)

#             #         # update the document symbols
#             #         doc.symbols = new_symbols

#             #         print(architypes)

#             if len(new_symbols) == 0:
#                 change_line_num = change.range.start.line
#                 source = doc.lines[change_line_num]

#                 # if source.endswith("{\n"):
#                 #     source = "".join(doc.lines[change_line_num:])

#                 architypes = _get_architypes(ls, doc_uri, source)

#                 new_symbols = get_document_symbols(
#                     ls, doc_uri, architypes, shift_lines=change.range.start.line
#                 )

#                 # remove old symbols to prevent duplicates
#                 for new_symbol in new_symbols:
#                     doc.symbols = [
#                         s
#                         for s in doc.symbols
#                         if s.location.range.start.line
#                         != new_symbol.location.range.start.line
#                     ]
#                 # update the document symbols
#                 doc.symbols.extend(new_symbols)

#     end = time.time_ns()
#     total_time = end - start
#     print("time taken: ", total_time / 1000000, "ms")
