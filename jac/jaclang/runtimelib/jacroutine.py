import threading
from typing import Any, List, Tuple


class Task:
    def __init__(self, func: Any | None, args: Tuple) -> None:
        self.func = func
        self.args = args
        self._thread = threading.Thread(target=self.func, args=self.args)

    def start(self) -> None:
        self._thread.start()

    def converge(self, timeout: float | None = None) -> None:
        self._thread.join(timeout)


class Group:
    def __init__(self, *tasks: Task) -> None:
        self.tasks: List[Task] = list(tasks)

    def append(self, task: Task) -> None:
        self.tasks.append(task)

    def remove(self, task: Task) -> None:
        self.tasks.remove(task)

    def start(self) -> None:
        for task in self.tasks:
            task.start()

    def converge(self, timeout: float | None = None) -> None:
        for task in self.tasks:
            task.converge(timeout)
