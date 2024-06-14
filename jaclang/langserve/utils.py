"""Utility functions for the language server."""

import asyncio
from functools import wraps
from typing import Any, Awaitable, Callable, Coroutine, Optional, ParamSpec, TypeVar

import jaclang.compiler.absyntree as ast
from jaclang.compiler.symtable import SymbolTable

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


def find_deepest_node_at_pos(
    node: ast.AstNode, line: int, character: int
) -> Optional[ast.AstSymbolNode]:
    """Return the deepest node that contains the given position."""
    if position_within_node(node, line, character):
        for i in [n for n in node.kid if n.loc.mod_path == node.loc.mod_path]:
            if position_within_node(i, line, character):
                return find_deepest_node_at_pos(i, line, character)
        return (
            node
            if isinstance(node, ast.AstSymbolNode)
            else node.find_parent_of_type(ast.AstSymbolNode)
        )
    return None


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


def collect_symbols(node: ast.AstNode) -> list[lspt.DocumentSymbol]:
    """Recursively collect symbols from the AST."""
    symbols = []
    for child in node.kid:
        if isinstance(
            child, (ast.Architype, ast.Ability, ast.GlobalVars, ast.ParamVar)
        ):
            symbol_kind = (
                lspt.SymbolKind.Class
                if isinstance(child, ast.Architype)
                else (
                    lspt.SymbolKind.Method
                    if isinstance(child, ast.Ability)
                    else (
                        lspt.SymbolKind.Variable
                        if isinstance(child, ast.GlobalVars)
                        else lspt.SymbolKind.Field
                    )
                )
            )
            node_range = lspt.Range(
                start=lspt.Position(
                    line=node.loc.first_line - 1, character=node.loc.col_start - 1
                ),
                end=lspt.Position(
                    line=node.loc.last_line - 1, character=node.loc.col_end - 1
                ),
            )
            symbol = lspt.DocumentSymbol(
                name=child.sym_name if isinstance(child, ast.AstSymbolNode) else "name",
                kind=symbol_kind,
                range=node_range,
                selection_range=node_range,
                children=[],
            )
            symbol.children = collect_symbols(child)
            symbols.append(symbol)
        elif hasattr(child, "kid") and child.kid:
            symbols.extend(collect_symbols(child))
    return symbols
