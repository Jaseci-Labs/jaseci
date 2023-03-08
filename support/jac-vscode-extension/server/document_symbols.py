import time
from pygls.server import LanguageServer
from jaseci.jac.ir.ast_builder import JacAstBuilder
from server.builder import JacAstBuilderSLL

from server.passes import ArchitypePass
from lsprotocol.types import (
    SymbolKind,
    SymbolInformation,
    Location,
    Position,
    Range,
    TextDocumentContentChangeEvent,
)
from typing import List, Tuple, TypedDict

from server.architypes_utils import get_architype_class


class ArchitypeInfo(TypedDict):
    name: str
    line: int
    col: int
    block_start: dict
    block_end: dict
    vars: list


def get_architypes_from_tree(tree: JacAstBuilder):
    architype_pass = ArchitypePass(ir=tree.root)
    architype_pass.run()


def _get_architypes(lsp: LanguageServer, doc_uri: str):
    try:
        doc = lsp.workspace.get_document(doc_uri)
        # we need to copy the root because the architype pass modifies the tree
        # and we don't want to modify the tree in the workspace so deps are still valid
        architype_pass = ArchitypePass(
            ir=JacAstBuilder._ast_head_map.get(doc.path).root,
            deps=JacAstBuilder._ast_head_map.get(doc.path).dependencies,
        )
        try:
            architype_pass.run()
        except Exception as e:
            pass

        end = time.time_ns()

        # get a dictionary of all architypes in the file
        architypes = architype_pass.output

        doc.architypes = architypes

        return architypes
    except Exception as e:
        return {"nodes": [], "edges": [], "graphs": [], "walkers": []}


def _create_architype_symbol(
    type: str, node: ArchitypeInfo, doc_uri: str, shift_lines: int = 0
) -> SymbolInformation:
    """Create a symbol for a node or walker"""
    kind = get_architype_class(type)

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
        pass

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
    ast = JacAstBuilderSLL(
        mod_name="architype_tree",
        jac_text=block_text,
        start_rule=start_rule,
    )

    return ast
