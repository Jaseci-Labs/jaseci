"""Utility functions for the language server."""

import asyncio
import logging
from functools import wraps
from typing import Any, Callable, Coroutine, TypeVar

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


def debounce(wait: float) -> Callable[[T], T]:
    """Debounce decorator for async functions."""

    def decorator(fn: T) -> T:  # noqa: ANN401
        @wraps(fn)
        def debounced(*args: Any, **kwargs: Any) -> None:  # noqa: ANN401
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

            debounced._task = asyncio.create_task(debounced_coro())  # type: ignore

        return debounced  # type: ignore

    return decorator
