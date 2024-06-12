"""Utility functions for the language server."""

import asyncio
from functools import wraps
from typing import Any, Awaitable, Callable, Coroutine, Optional, ParamSpec, TypeVar

import jaclang.compiler.absyntree as ast
from jaclang.compiler.symtable import SymbolTable


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
) -> Optional[ast.AstNode]:
    """Return the deepest node that contains the given position."""
    if position_within_node(node, line, character):
        for i in node.kid:
            if position_within_node(i, line, character):
                return find_deepest_node_at_pos(i, line, character)
        return node
    else:
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
