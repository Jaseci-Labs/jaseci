import os
from pygls.server import LanguageServer
from jaseci.jac.ir.ast_builder import (
    JacAstBuilder,
)
from server.passes import ArchitypePass
from lsprotocol.types import SymbolKind, SymbolInformation, Location, Position, Range
from typing import TypedDict


class ArchitypeInfo(TypedDict):
    name: str
    line: int
    col: int
    block_start: dict
    block_end: dict
    vars: list


def _get_architypes(lsp: LanguageServer, doc_uri: str):
    try:
        mod_name = os.path.basename(doc_uri).split(".")[0]
        doc = lsp.workspace.get_document(doc_uri)
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


def _create_architype_symbol(
    type: str, node: ArchitypeInfo, doc_uri: str
) -> SymbolInformation:
    """Create a symbol for a node or walker"""
    match type:
        case "node":
            kind = SymbolKind.Class
        case "walker":
            kind = SymbolKind.Function
        case _:
            raise ValueError("invalid architype type")

    return SymbolInformation(
        name=node["name"],
        kind=kind,
        location=Location(
            uri=doc_uri,
            range=Range(
                start=Position(line=node["line"] - 1, character=node["col"]),
                end=Position(
                    line=node["block_end"]["line"],
                    character=0,
                ),
            ),
        ),
    )


def get_document_symbols(ls: LanguageServer, doc_uri: str):
    """Return a list of symbols in the document"""
    architypes = _get_architypes(ls, doc_uri)
    symbols = []

    for walker in architypes["walkers"]:
        symbol = _create_architype_symbol("walker", walker, doc_uri)
        symbols.append(symbol)

        for var in walker["vars"]:
            var_symbol = SymbolInformation(
                name=var["name"],
                kind=SymbolKind.Property,
                location=Location(
                    uri=doc_uri,
                    range=Range(
                        start=Position(line=var["line"] - 1, character=var["col"]),
                        end=Position(
                            line=var["line"],
                            character=var["col"] + len(var["name"]),
                        ),
                    ),
                ),
                container_name="testing",
            )

            symbols.append(var_symbol)

    for node in architypes["nodes"]:
        node_symbol = _create_architype_symbol("node", node, doc_uri)

        symbols.append(node_symbol)

        for var in node["vars"]:
            var_symbol = SymbolInformation(
                name=var["name"],
                kind=SymbolKind.Property,
                location=Location(
                    uri=doc_uri,
                    range=Range(
                        start=Position(line=var["line"] - 1, character=var["col"]),
                        end=Position(
                            line=var["line"],
                            character=var["col"] + len(var["name"]),
                        ),
                    ),
                ),
                container_name="testing",
            )

            symbols.append(var_symbol)

    return symbols
