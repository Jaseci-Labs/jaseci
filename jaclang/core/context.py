"""Core constructs for Jac Language."""

from __future__ import annotations

import unittest
from contextvars import ContextVar
from typing import Callable, Optional
from uuid import UUID

from .architype import Architype, Root
from .memory import Memory, ShelveStorage


class ExecutionContext:
    """Default Execution Context implementation."""

    mem: Optional[Memory]
    root: Optional[Root]

    def __init__(self) -> None:
        """Create execution context."""
        super().__init__()
        self.mem = ShelveStorage()
        self.root = None

    def init_memory(self, session: str = "") -> None:
        """Initialize memory."""
        if session:
            self.mem = ShelveStorage(session)
        else:
            self.mem = Memory()

    def get_root(self) -> Root:
        """Get the root object."""
        if self.mem is None:
            raise ValueError("Memory not initialized")

        if not self.root:
            root = self.mem.get_obj(UUID(int=0))
            if root is None:
                self.root = Root()
                self.mem.save_obj(self.root, persistent=self.root._jac_.persistent)
            elif not isinstance(root, Root):
                raise ValueError(f"Invalid root object: {root}")
            else:
                self.root = root
        return self.root

    def get_obj(self, obj_id: UUID) -> Architype | None:
        """Get object from memory."""
        if self.mem is None:
            raise ValueError("Memory not initialized")

        return self.mem.get_obj(obj_id)

    def save_obj(self, item: Architype, persistent: bool) -> None:
        """Save object to memory."""
        if self.mem is None:
            raise ValueError("Memory not initialized")

        self.mem.save_obj(item, persistent)

    def reset(self) -> None:
        """Reset the execution context."""
        if self.mem:
            self.mem.close()
        self.mem = None
        self.root = None


exec_context: ContextVar[ExecutionContext | None] = ContextVar(
    "ExecutionContext", default=None
)


class JacTestResult(unittest.TextTestResult):
    """Jac test result class."""

    def __init__(
        self,
        stream,  # noqa
        descriptions,  # noqa
        verbosity: int,
        max_failures: Optional[int] = None,
    ) -> None:
        """Initialize FailFastTestResult object."""
        super().__init__(stream, descriptions, verbosity)  # noqa
        self.failures_count = JacTestCheck.failcount
        self.max_failures = max_failures

    def addFailure(self, test, err) -> None:  # noqa
        """Count failures and stop."""
        super().addFailure(test, err)
        self.failures_count += 1
        if self.max_failures is not None and self.failures_count >= self.max_failures:
            self.stop()

    def stop(self) -> None:
        """Stop the test execution."""
        self.shouldStop = True


class JacTextTestRunner(unittest.TextTestRunner):
    """Jac test runner class."""

    def __init__(self, max_failures: Optional[int] = None, **kwargs) -> None:  # noqa
        """Initialize JacTextTestRunner object."""
        self.max_failures = max_failures
        super().__init__(**kwargs)

    def _makeResult(self) -> JacTestResult:  # noqa
        """Override the method to return an instance of JacTestResult."""
        return JacTestResult(
            self.stream,
            self.descriptions,
            self.verbosity,
            max_failures=self.max_failures,
        )


class JacTestCheck:
    """Jac Testing and Checking."""

    test_case = unittest.TestCase()
    test_suite = unittest.TestSuite()
    breaker = False
    failcount = 0

    @staticmethod
    def reset() -> None:
        """Clear the test suite."""
        JacTestCheck.test_case = unittest.TestCase()
        JacTestCheck.test_suite = unittest.TestSuite()

    @staticmethod
    def run_test(xit: bool, maxfail: int | None, verbose: bool) -> None:
        """Run the test suite."""
        verb = 2 if verbose else 1
        runner = JacTextTestRunner(max_failures=maxfail, failfast=xit, verbosity=verb)
        result = runner.run(JacTestCheck.test_suite)
        if result.wasSuccessful():
            print("Passed successfully.")
        else:
            fails = len(result.failures)
            JacTestCheck.failcount += fails
            JacTestCheck.breaker = (
                (JacTestCheck.failcount >= maxfail) if maxfail else True
            )

    @staticmethod
    def add_test(test_fun: Callable) -> None:
        """Create a new test."""
        JacTestCheck.test_suite.addTest(unittest.FunctionTestCase(test_fun))

    def __getattr__(self, name: str) -> object:
        """Make convenient check.Equal(...) etc."""
        return getattr(JacTestCheck.test_case, name)
