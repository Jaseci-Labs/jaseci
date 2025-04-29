"""This file contains the JacGo runtime, which is a simple implementation of the Go concurrency model in Python."""

import threading
from typing import Any, Tuple

from jaclang.runtimelib.constructs import NodeArchitype

groups = []


class Task:
    """Class to represent a task that can be run concurrently."""

    def __init__(self, func: Any | None, args: Tuple) -> None:
        """Initialize the task with a function and its arguments."""
        self.func = func
        self.args = args
        self._thread = threading.Thread(target=self.func, args=self.args)
        self.start()
        self._thread.join()

    def start(self) -> None:
        """Start the task in a separate thread."""
        self._thread.start()


def jacroutine(func: Any | None, args: Tuple) -> Task:
    """Create a task with the given function and arguments."""
    assert len(args) == 2
    return Task(func, args)


def waitgroup(group: list) -> None:
    """Wait group functionality."""
    global groups
    groups = group
    while sum([i[1] for i in groups]) > 0:
        pass


def done(node: NodeArchitype) -> None:
    """Ensure walker reaches the expected node."""
    # from jaclang.runtimelib.machine import JacNode, JacWalker
    # print(groups)
    for group in groups:
        if group[0] == node:
            print("done node", node)
            group[1] -= 1
        if group[1] == 0:
            groups.remove(group)
            print("done", groups)
            print("removed", group[0])
