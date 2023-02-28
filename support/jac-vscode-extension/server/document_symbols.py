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
from typing import List, Tuple, TypedDict

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
        start = time.time_ns()
        tree = JacAstBuilder(
            mod_name, jac_text=source, prediction_mode=PredictionMode.SLL
        )
        # keep a reference to the root node for passes
        doc.ir = tree.root
        end = time.time_ns()
        print(f"parsing tree took {(end - start) / 1000000} ms")

        start = time.time_ns()
        architype_pass = ArchitypePass(ir=tree.root)
        architype_pass.run()

        end = time.time_ns()
        print(f"architype pass took {(end - start) / 1000000} ms")

        # get a dictionary of all architypes in the file
        architypes = architype_pass.output
        doc.architypes = architypes

        # print(architypes)
        return architypes
    except Exception as e:
        print(e)

        return {"nodes": [], "edges": [], "graphs": [], "walkers": []}


def get_tree_architypes(tree: JacAstBuilder):
    """Get architypes from a tree"""
    architype_pass = ArchitypePass(ir=tree.root)
    architype_pass.run()

    architypes = architype_pass.output

    return architypes


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

    symbol = SymbolInformation(
        name=node["name"],
        kind=kind,
        location=Location(
            uri=doc_uri,
            range=Range(
                start=Position(
                    line=(node["line"] - 1) + shift_lines, character=node["col"]
                ),
                end=Position(
                    line=node["block_end"]["line"] + shift_lines,
                    character=0,
                ),
            ),
        ),
    )
    return symbol


def get_document_symbols(
    ls: LanguageServer,
    doc_uri: str,
    architypes: dict[str, list] = None,
    shift_lines: int = 0,
) -> List[SymbolInformation]:
    """Return a list of symbols in the document"""
    if not architypes:
        start = time.time_ns()
        architypes = _get_architypes(ls, doc_uri)
        end = time.time_ns()
        print(f"_get_architypes took {(end - start) / 1000000} ms")

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


def get_change_block_text(
    ls: LanguageServer, doc_uri: str, change: TextDocumentContentChangeEvent
) -> Tuple[int, int, str]:
    """Get the text of the block that was changed"""
    doc = ls.workspace.get_document(doc_uri)
    change_line = change.range.start.line
    change_line_text = doc.source.splitlines()[change_line]

    # if the change is a new line, return the whole document
    if change_line_text.split()[0] in [
        "node",
        "walker",
        "graph",
        "edge",
    ] and change_line_text[-1] in ["{", ";"]:
        return [0, 0, doc.source]

    # find any symbols that are above the change
    doc_symbols = doc.symbols

    symbols_above = [
        symbol
        for symbol in doc_symbols
        if symbol.location.range.start.line < change_line
        # only architypes
        and (
            symbol.kind == SymbolKind.Class
            or symbol.kind == SymbolKind.Namespace
            or symbol.kind == SymbolKind.Function
        )
    ]

    # sort the symbols by line number
    symbols_above.sort(key=lambda symbol: symbol.location.range.start.line)

    # get the text of the block that was changed
    if symbols_above:
        # get the start of the block
        symbol_above: SymbolInformation = symbols_above[-1]
        block_start = symbol_above.location.range.start.line

        # get the end of the block (symbol ends at the closing brace)
        block_end = symbol_above.location.range.end.line

        lines = doc.source.splitlines(keepends=True)

        block_text = "".join(lines[block_start : block_end + 1])
        return [block_start, block_end, block_text]

    # if there are no symbols above the change, return the whole document
    if not symbols_above:
        return [0, 0, doc.source]


def remove_symbols_in_range(
    start_line: int, end_line: int, symbols: List[SymbolInformation]
):
    all_symbols = symbols.copy()
    ## get rid of symbols that are in the range
    symbols_in_range = [
        symbol
        for symbol in all_symbols
        if symbol.location.range.start.line >= start_line
        and symbol.location.range.end.line <= end_line
    ]

    for symbol in symbols_in_range:
        symbols.remove(symbol)

    return symbols


def get_architype_ast(block_text: str, start_rule="architype"):
    ast = JacAstBuilder(
        mod_name="architype_tree",
        jac_text=block_text,
        prediction_mode=PredictionMode.SLL,
        start_rule=start_rule,
    )

    return ast
