import functools
import inspect
import re
import sys
import threading
from typing import Any, Callable, Dict, Optional
from lsprotocol.types import SymbolKind

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec


def deconstruct_error_message(error_message):
    pattern = re.compile(r"^.*:\sline\s(\d+):(\d+)\s-\s(.+)$")

    match = pattern.match(error_message)

    if match:
        line_number = match.group(1)
        column_number = match.group(2)
        error_text = match.group(3)

        return (
            int(line_number),
            int(column_number),
            error_text,
        )

    return None


P = ParamSpec("P")


def debounce(
    interval_s: int, keyed_by: Optional[str] = None, after=None
) -> Callable[[Callable[P, None]], Callable[P, None]]:
    """Debounce calls to this function until interval_s seconds have passed.
    Decorator copied from https://github.com/python-lsp/python-lsp-
    server
    """

    def wrapper(func: Callable[P, None]) -> Callable[P, None]:
        timers: Dict[Any, threading.Timer] = {}
        lock = threading.Lock()

        @functools.wraps(func)
        def debounced(*args: P.args, **kwargs: P.kwargs) -> None:
            sig = inspect.signature(func)
            call_args = sig.bind(*args, **kwargs)
            key = call_args.arguments[keyed_by] if keyed_by else None

            def run() -> None:
                with lock:
                    del timers[key]
                func(*args, **kwargs)
                if after:
                    after(*args, **kwargs)

                return

            with lock:
                old_timer = timers.get(key)
                if old_timer:
                    old_timer.cancel()

                timer = threading.Timer(interval_s, run)
                timers[key] = timer
                timer.start()

        return debounced

    return wrapper


def get_architype_class(type: str) -> SymbolKind:
    kind = SymbolKind.Variable
    if type in ["node", "nodes"]:
        kind = SymbolKind.Class
    if type in ["walker", "walkers"]:
        kind = SymbolKind.Function
    if type in ["edge", "edges"]:
        kind = SymbolKind.Interface
    if type in ["graph", "graphs"]:
        kind = SymbolKind.Namespace

    return kind
