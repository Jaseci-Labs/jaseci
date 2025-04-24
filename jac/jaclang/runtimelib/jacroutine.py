import copy
import threading
from typing import Any, List, Tuple

from jaclang.runtimelib.constructs import NodeArchitype, WalkerArchitype


class Task:
    def __init__(self, func: Any | None, args: Tuple) -> None:
        self.func = func
        self.args = args
        self._thread = threading.Thread(target=self.func, args=self.args)

    def start(self) -> None:
        self._thread.start()

    def converge(self, timeout: float | None = None) -> None:
        self._thread.join(timeout)

    def get_walker(self) -> WalkerArchitype | None:
        if isinstance(self.args[0], WalkerArchitype):
            return self.args[0]
        elif isinstance(self.args[1], WalkerArchitype):
            return self.args[1]
        return None

    def get_node(self) -> NodeArchitype | None:
        if isinstance(self.args[0], NodeArchitype):
            return self.args[0]
        elif isinstance(self.args[1], NodeArchitype):
            return self.args[1]
        return None


class Group:
    def __init__(self, *tasks: Task) -> None:
        self.tasks: List[Task] = list(tasks)

    def append(self, task: Task) -> None:
        self.tasks.append(task)

    def remove(self, task: Task) -> None:
        self.tasks.remove(task)

    def start(self, policy: str | None = None) -> None:
        if policy is None:
            for task in self.tasks:
                task.start()
        elif policy == "parallel":
            for task in self.tasks:
                task.start()
            for task in self.tasks:
                task.converge()
        elif policy == "serial":
            for task in self.tasks:
                task.start()
                task.converge()
        else:
            raise ValueError("Invalid policy. Use 'parallel' or 'serial'.")

    def converge(self, timeout: float | None = None) -> None:
        for task in self.tasks:
            task.converge(timeout)

    def get_walkers(self) -> list[WalkerArchitype]:
        walkers = []
        for task in self.tasks:
            walker = task.get_walker()
            assert isinstance(walker, WalkerArchitype)
            walkers.append(walker)
        return walkers

    def get_nodes(self) -> list[NodeArchitype]:
        nodes = []
        for task in self.tasks:
            node = task.get_node()
            assert isinstance(node, NodeArchitype)
            nodes.append(node)
        return nodes


def create_jacroutine(func: Any | None, args: Tuple) -> Task | Group:
    assert len(args) == 2
    if isinstance(args[0], list):
        assert isinstance(args[1], WalkerArchitype)
        group = Group()
        for arg in args[0]:
            assert isinstance(arg, NodeArchitype)
            group.append(Task(func, (copy.deepcopy(args[1]), arg)))
        return group
    elif isinstance(args[1], list):
        assert isinstance(args[0], WalkerArchitype)
        group = Group()
        for arg in args[1]:
            assert isinstance(arg, NodeArchitype)
            group.append(Task(func, (copy.deepcopy(args[0]), arg)))
        return group
    else:
        return Task(func, args)
