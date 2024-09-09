import unittest
from .architype import Architype as Architype, Root as Root
from .machine import JacMachine as JacMachine
from .memory import Memory as Memory, ShelveStorage as ShelveStorage
from _typeshed import Incomplete
from contextvars import ContextVar
from typing import Callable
from uuid import UUID

class ExecutionContext:
    mem: Memory | None
    root: Root | None
    jac_machine: Incomplete
    def __init__(self) -> None: ...
    def init_memory(self, base_path: str = "", session: str = "") -> None: ...
    def get_root(self) -> Root: ...
    def get_obj(self, obj_id: UUID) -> Architype | None: ...
    def save_obj(self, item: Architype, persistent: bool) -> None: ...
    def reset(self) -> None: ...

exec_context: ContextVar[ExecutionContext | None]

class JacTestResult(unittest.TextTestResult):
    failures_count: Incomplete
    max_failures: Incomplete
    def __init__(
        self, stream, descriptions, verbosity: int, max_failures: int | None = None
    ) -> None: ...
    def addFailure(self, test, err) -> None: ...
    shouldStop: bool
    def stop(self) -> None: ...

class JacTextTestRunner(unittest.TextTestRunner):
    max_failures: Incomplete
    def __init__(self, max_failures: int | None = None, **kwargs) -> None: ...

class JacTestCheck:
    test_case: Incomplete
    test_suite: Incomplete
    breaker: bool
    failcount: int
    @staticmethod
    def reset() -> None: ...
    @staticmethod
    def run_test(xit: bool, maxfail: int | None, verbose: bool) -> None: ...
    @staticmethod
    def add_test(test_fun: Callable) -> None: ...
    def __getattr__(self, name: str) -> object: ...
