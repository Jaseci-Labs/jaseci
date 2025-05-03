"""This file contains the JacGo runtime, which is a simple implementation of the spawn call concurrency."""

import copy
import threading
import time
from queue import Queue
from typing import Any, Tuple

from jaclang.runtimelib.constructs import (
    NodeAnchor,
    NodeArchitype,
    WalkerAnchor,
    WalkerArchitype,
)

groups: dict[NodeAnchor, WalkerAnchor] = {}


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
    return args[0]  # return same walker if no result is returned


def jacgo_visit(
    func: Any, args: Tuple  # noqa: ANN401
) -> tuple[WalkerArchitype, NodeArchitype | None]:
    """Create a spawn call with the given walker and nodes."""
    result_queue: Queue = Queue()

    def wrapper() -> None:
        try:
            result = func(*args)
            result_queue.put(result)
        except Exception as e:
            result_queue.put(e)

    # thread = threading.Thread(target=wrapper, args=args, daemon=True)
    thread = threading.Thread(target=wrapper, daemon=True)
    thread.start()
    while not thread.is_alive():
        time.sleep(0.5)
    if not result_queue.empty():
        result = result_queue.get_nowait()
        if isinstance(result, Exception):
            raise result
        return result
    return args[0].architype, None  # return same walker if no result is returned


def create_threads(args: list) -> list[WalkerArchitype]:  # noqa: ANN401
    """Create a thread with the given walker and nodes."""
    walker = args[0]
    nodes = args[1]
    global groups
    # groups[nodes[0]] = walker
    for node in nodes:
        walker_new = create_walker(walker, node)
        groups[node] = walker_new
    return [groups[node].architype for node in nodes]  # return all walker anchors


def create_walker(walker: WalkerAnchor, node: NodeAnchor) -> WalkerAnchor:
    """Create a walker."""
    walker_new = copy.deepcopy(walker)
    walker_new.next = [node]
    walker_new.path = []
    walker_new.ignores = []
    # walker_new.parent = walker
    # walker.child.append(walker_new)
    return walker_new


def get_walker(node: NodeAnchor) -> WalkerAnchor:
    """Get the walker for the given node."""
    global groups
    if node in groups:
        walker = groups[node]
        # remove the walker from the groups
        del groups[node]
        return walker
    return None  # type: ignore[return-value]
