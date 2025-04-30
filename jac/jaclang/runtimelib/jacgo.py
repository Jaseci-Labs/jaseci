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

    def start(self) -> None:
        """Start the task in a separate thread."""
        self._thread.start()

    def join(self) -> None:
        """Wait for the task to finish."""
        self._thread.join()


def jacroutine(func: Any | None, args: Tuple) -> Task:
    """Create a task with the given function and arguments."""
    return Task(func, args)


def waitgroup(group: list) -> None:
    """Wait group functionality."""
    global groups
    groups.extend(group)


def update(node: NodeArchitype) -> None:
    """Update the wait group with the current node."""
    global groups
    for group in groups:
        if group[0] == node:
            group[1] -= 1
        if group[1] == 0:
            groups.remove(group)


def is_done(node: NodeArchitype) -> bool:
    """Check if the wait group is done."""
    global groups
    nodes = [group[0] for group in groups]
    if node not in nodes:
        return True
    for group in groups:
        if group[0] == node:
            return group[1] == 0
    return False
