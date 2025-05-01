"""This file contains the JacGo runtime, which is a simple implementation of the spawn call concurrency."""

import copy
import threading
import time
from queue import Queue
from typing import Any, Tuple

from jaclang.runtimelib.constructs import (
    NodeAnchor,
    # NodeArchitype,
    WalkerAnchor,
    WalkerArchitype,
)


def jacgo_spawn(func: Any, args: Tuple) -> WalkerArchitype:  # noqa: ANN401
    """Create a spawn call with the given walker and nodes."""
    result_queue: Queue = Queue()

    def wrapper() -> None:
        try:
            result = func(*args)
            result_queue.put(result)
        except Exception as e:
            result_queue.put(e)

    thread = threading.Thread(target=wrapper, daemon=True)
    thread.start()
    while not thread.is_alive():
        time.sleep(0.5)
    if not result_queue.empty():
        result = result_queue.get_nowait()
        if isinstance(result, Exception):
            raise result
        return result
    return args[0].__jac__  # return same walker if no result is returned


def create_walker(walker: WalkerAnchor, node: NodeAnchor) -> WalkerAnchor:
    """Create a walker."""
    walker_new = copy.deepcopy(walker)
    walker_new.next = [node]
    walker_new.path = []
    walker_new.ignores = []
    walker_new.parent = walker
    walker.child.append(walker_new)
    return walker_new
