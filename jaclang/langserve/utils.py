"""Utility functions for the language server."""

import asyncio
from functools import wraps
from typing import Any, Awaitable, Callable, Coroutine, Optional, ParamSpec, TypeVar

import jaclang.compiler.absyntree as ast
from jaclang.compiler.symtable import Symbol , SymbolTable

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


def collect_symbols(node: SymbolTable, ls) -> list[lspt.DocumentSymbol]:
    """Recursively collect symbols from the AST."""
    import builtins
    symbols = []
    if node is None:
        return symbols
    ls.log_py(f'kidsss: {node.kid}')
    for key, item in node.tab.items():
        if key in dir(builtins):
            continue
        ls.log_py(f'key: {key}   \n{item}   \n type ->{type(item)}  typ ---{item.typ}')
        if isinstance(item.defn[0], (ast.Architype, ast.Ability, ast.GlobalVars)):
            # Process as a SymbolTable
            ls.log_py(f'item: {item}')
            symbol_kind = (
                lspt.SymbolKind.Class if isinstance(item.defn[0], ast.Architype) else (
                    lspt.SymbolKind.Method if isinstance(item.defn[0], ast.Ability) else (
                        lspt.SymbolKind.Variable if isinstance(item.defn[0], ast.GlobalVars) else (
                            lspt.SymbolKind.Field
                        )
                    )
                )
            )

            s1 = item.defn[0].loc.first_line - 1
            s2 = item.defn[0].loc.col_start - 1
            s3 = item.defn[0].loc.last_line - 1
            s4 = item.defn[0].loc.col_end - 1

            try:
                node_range = lspt.Range(
                    start=lspt.Position(
                        line=int(s1) if s1 >= 0 else 0, character=int(s2) if s2 >= 0 else 0
                    ),
                    end=lspt.Position(
                        line=int(s3) if s3 >= 0 else 0, character=int(s4) if s4 >= 0 else 0
                    ),
                )
            except Exception as e:
                ls.log_py(f'Error11: {e}')
                node_range = lspt.Range(
                    start=lspt.Position(line=0, character=0),
                    end=lspt.Position(line=0, character=0),
                )

            symbol = lspt.DocumentSymbol(
                name=key,
                kind=symbol_kind,
                range=node_range,
                selection_range=node_range,
                children=[],
            )
            for kid in node.kid:
                if kid.name == key:
                    symbol.children = collect_symbols(kid, ls)
            symbols.append(symbol)
        elif isinstance(item, Symbol) :
            ls.log_py(f'item: {item}  \n{type(item)}')
            # Process as a Symbol
            symbol_kind = lspt.SymbolKind.Field

            s1 = item.defn[0].loc.first_line - 1
            s2 = item.defn[0].loc.col_start - 1
            s3 = item.defn[0].loc.last_line - 1
            s4 = item.defn[0].loc.col_end - 1

            try:
                node_range = lspt.Range(
                    start=lspt.Position(
                        line=int(s1) if s1 >= 0 else 0, character=int(s2) if s2 >= 0 else 0
                    ),
                    end=lspt.Position(
                        line=int(s3) if s3 >= 0 else 0, character=int(s4) if s4 >= 0 else 0
                    ),
                )
            except Exception as e:
                ls.log_py(f'Error: {e}')
                node_range = lspt.Range(
                    start=lspt.Position(line=0, character=0),
                    end=lspt.Position(line=0, character=0),
                )

            symbol = lspt.DocumentSymbol(
                name=item.sym_name,
                kind=symbol_kind,
                range=node_range,
                selection_range=node_range,
                children=[],
            )
            symbols.append(symbol)

    ls.log_py(f'collect_symbols: {symbols}')
    return symbols
