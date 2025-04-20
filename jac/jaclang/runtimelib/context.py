"""Core constructs for Jac Language."""

from __future__ import annotations

import unittest

from dataclasses import MISSING
from typing import Any, Callable, Optional, TYPE_CHECKING, cast
from uuid import UUID

from .architype import NodeAnchor, Root
from .memory import ShelfStorage

if TYPE_CHECKING:
    from jaclang.runtimelib.machine import JacMachineState

SUPER_ROOT_UUID = UUID("00000000-0000-0000-0000-000000000000")


class ExecutionContext:
    """Execution Context."""

    def __init__(
        self,
        mach: JacMachineState,
        session: Optional[str] = None,
        root: Optional[str] = None,
    ) -> None:
        """Create ExecutionContext."""
        self.mem = ShelfStorage(mach=mach, session=session)
        self.reports: list = []

        __jac_mach__ = mach
        if not isinstance(
            system_root := self.mem.find_by_id(SUPER_ROOT_UUID), NodeAnchor
        ):
            system_root = cast(NodeAnchor, Root().__jac__)
            system_root.id = SUPER_ROOT_UUID
            self.mem.set(system_root.id, system_root)

        self.system_root = system_root

        self.entry_node = self.root = self.init_anchor(root, self.system_root)
        sr_arch = Root()
        self.system_root = sr_arch.__jac__
        self.custom: Any = MISSING
        self.system_root.id = SUPER_ROOT_UUID
        self.system_root.persistent = False

    def init_anchor(
        self,
        anchor_id: str | None,
        default: NodeAnchor,
    ) -> NodeAnchor:
        """Load initial anchors."""
        if anchor_id:
            if isinstance(anchor := self.mem.find_by_id(UUID(anchor_id)), NodeAnchor):
                return anchor
            raise ValueError(f"Invalid anchor id {anchor_id} !")
        return default

    def set_entry_node(self, entry_node: str | None) -> None:
        """Override entry."""
        self.entry_node = self.init_anchor(entry_node, self.root)

    def get_root(self) -> Root:
        """Get current root."""
        return cast(Root, self.root.architype)

    def global_system_root(self) -> NodeAnchor:
        """Get global system root."""
        return self.system_root

    def close(self) -> None:
        """Close the context."""
        self.mem.close()


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
