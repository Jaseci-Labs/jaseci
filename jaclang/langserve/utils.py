"""Utility functions for the language server."""

import asyncio
import logging
from functools import wraps
from typing import Any, Awaitable, Callable, Coroutine, ParamSpec, TypeVar

import jaclang.compiler.absyntree as ast
from jaclang.compiler.symtable import SymbolTable
from jaclang.vendor.pygls.server import LanguageServer

import lsprotocol.types as lspt


def log_error(ls: LanguageServer, message: str) -> None:
    """Log an error message."""
    ls.show_message_log(message, lspt.MessageType.Error)
    ls.show_message(message, lspt.MessageType.Error)


def log(info: str) -> None:
    """Log an info message."""
    logging.warning(info)


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
