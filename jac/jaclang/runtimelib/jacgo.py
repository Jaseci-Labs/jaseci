"""This file contains the JacGo runtime, which is a simple implementation of the Go concurrency model in Python."""

import copy
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Tuple

from jaclang.runtimelib.constructs import (
    NodeAnchor,
    NodeArchitype,
    WalkerAnchor,
)

groups = []

pool = ThreadPoolExecutor(max_workers=10)


class Task:
    """Class to represent a task that can be run concurrently."""

    def __init__(self, func: Any | None, args: Tuple) -> None:
        """Initialize the task with a function and its arguments."""
        self.func = func
        self.args = args
        self.t = self.start()

    def start(self) -> Any:  # noqa: ANN401
        """Start the task in a separate thread."""
        global pool
        if self.func is not None:
            t1 = pool.submit(self.func, *self.args)
        return t1.result()


def jacroutine(func: Any | None, args: Tuple) -> Task:
    """Create a task with the given function and arguments."""
    task = Task(func, args)
    return task.t


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


def create_walker(walker: WalkerAnchor, node: NodeAnchor) -> WalkerAnchor:
    """Create a walker."""
    walker_new = copy.deepcopy(walker)
    walker_new.next = [node]
    walker_new.path = []
    walker_new.ignores = []
    # walker_new.parent = walker
    # walker.child.append(walker_new)
    return walker_new
