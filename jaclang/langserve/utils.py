"""Utility functions for the language server."""

import asyncio
import builtins
from functools import wraps
from typing import Any, Awaitable, Callable, Coroutine, Optional, ParamSpec, TypeVar

import jaclang.compiler.absyntree as ast
from jaclang.compiler.codeloc import CodeLocInfo
from jaclang.compiler.symtable import Symbol, SymbolTable

import lsprotocol.types as lspt

T = TypeVar("T", bound=Callable[..., Coroutine[Any, Any, Any]])
P = ParamSpec("P")


def debounce(wait: float) -> Callable[[T], Callable[..., Awaitable[None]]]:
    """Debounce decorator for async functions."""

    def decorator(fn: T) -> Callable[..., Awaitable[None]]:
        @wraps(fn)
        async def debounced(*args: P.args, **kwargs: P.kwargs) -> None:
            async def call_it() -> None:
                await fn(*args, **kwargs)

            if hasattr(debounced, "_task"):
                debounced._task.cancel()

            async def debounced_coro() -> None:
                try:
                    await asyncio.sleep(wait)
                    await call_it()
                except asyncio.CancelledError:
                    pass

            setattr(  # noqa: B010
                debounced, "_task", asyncio.create_task(debounced_coro())
            )

        return debounced

    return decorator


def sym_tab_list(sym_tab: SymbolTable, file_path: str) -> list[SymbolTable]:
    """Iterate through symbol table."""
    sym_tabs = (
        [sym_tab]
        if not (
            isinstance(sym_tab.owner, ast.Module)
            and sym_tab.owner.loc.mod_path != file_path
        )
        else []
    )
    for i in sym_tab.kid:
        sym_tabs += sym_tab_list(i, file_path=file_path)
    return sym_tabs


def find_deepest_symbol_node_at_pos(
    node: ast.AstNode, line: int, character: int
) -> Optional[ast.AstSymbolNode]:
    """Return the deepest symbol node that contains the given position."""
    last_symbol_node = None

    if position_within_node(node, line, character):
        if isinstance(node, ast.AstSymbolNode):
            last_symbol_node = node

        for child in node.kid:
            if position_within_node(child, line, character):
                deeper_node = find_deepest_symbol_node_at_pos(child, line, character)
                if deeper_node is not None:
                    last_symbol_node = deeper_node

    return last_symbol_node


def position_within_node(node: ast.AstNode, line: int, character: int) -> bool:
    """Check if the position falls within the node's location."""
    if node.loc.first_line < line + 1 < node.loc.last_line:
        return True
    if (
        node.loc.first_line == line + 1
        and node.loc.col_start <= character + 1
        and (
            node.loc.last_line == line + 1
            and node.loc.col_end >= character + 1
            or node.loc.last_line > line + 1
        )
    ):
        return True
    if (
        node.loc.last_line == line + 1
        and node.loc.col_start <= character + 1 <= node.loc.col_end
    ):
        return True
    return False


def collect_symbols(node: SymbolTable) -> list[lspt.DocumentSymbol]:
    """Recursively collect symbols from the AST."""
    symbols = []
    if node is None:
        return symbols

    for key, item in node.tab.items():
        if key in dir(builtins):
            continue
        if item in [owner_sym(tab) for tab in node.kid]:
            continue
        else:

            pos = create_range(item.defn[0].loc)
            symbol = lspt.DocumentSymbol(
                name=key,
                kind=kind_map(item.defn[0]),
                range=pos,
                selection_range=pos,
                children=[],
            )
            symbols.append(symbol)

    for sub_tab in node.kid:
        sub_symbols = collect_symbols(sub_tab)

        if isinstance(
            sub_tab.owner,
            (ast.IfStmt, ast.ElseStmt, ast.WhileStmt, ast.IterForStmt, ast.InForStmt),
        ):
            symbols.extend(sub_symbols)
        else:
            sub_pos = create_range(sub_tab.owner.loc)
            symbol = lspt.DocumentSymbol(
                name=sub_tab.name,
                kind=kind_map(sub_tab.owner),
                range=sub_pos,
                selection_range=sub_pos,
                children=sub_symbols,
            )
            symbols.append(symbol)

    return symbols


def owner_sym(table: SymbolTable) -> Optional[Symbol]:
    """Get owner sym."""
    if table.has_parent() and isinstance(table.owner, ast.AstSymbolNode):
        return table.parent.lookup(table.owner.sym_name)
    return None


def create_range(loc: CodeLocInfo) -> lspt.Range:
    """Create an lspt.Range from a location object."""
    return lspt.Range(
        start=lspt.Position(line=loc.first_line - 1, character=loc.col_start - 1),
        end=lspt.Position(line=loc.last_line - 1, character=loc.col_end - 1),
    )


def kind_map(sub_tab: ast.AstNode) -> lspt.SymbolKind:
    """Map the symbol node to an lspt.SymbolKind."""
    return (
        lspt.SymbolKind.Function
        if isinstance(sub_tab, (ast.Ability, ast.AbilityDef))
        else (
            lspt.SymbolKind.Class
            if isinstance(sub_tab, (ast.Architype, ast.ArchDef))
            else (
                lspt.SymbolKind.Module
                if isinstance(sub_tab, ast.Module)
                else (
                    lspt.SymbolKind.Enum
                    if isinstance(sub_tab, (ast.Enum, ast.EnumDef))
                    else lspt.SymbolKind.Variable
                )
            )
        )
    )
