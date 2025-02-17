"""Core constructs for Jac Language."""

from __future__ import annotations

import unittest
from contextvars import ContextVar
from dataclasses import MISSING
from typing import Any, Callable, ClassVar, Optional, cast
from uuid import UUID

from .architype import NodeAnchor, Root
from .memory import Memory, ShelfStorage


EXECUTION_CONTEXT = ContextVar[Optional["ExecutionContext"]]("ExecutionContext")
SUPER_ROOT_UUID = UUID("00000000-0000-0000-0000-000000000000")


class ExecutionContext:
    """Execution Context."""

    mem: Memory
    reports: list[Any]
    custom: Any = MISSING
    system_root: NodeAnchor
    root: NodeAnchor
    entry_node: NodeAnchor

    # A context change event subscription list, those who want to listen ctx change will register here.
    on_ctx_change: ClassVar[list[Callable[[ExecutionContext | None], None]]] = []

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

    def close(self) -> None:
        """Close current ExecutionContext."""
        self.mem.close()
        EXECUTION_CONTEXT.set(None)
        for func in ExecutionContext.on_ctx_change:
            func(EXECUTION_CONTEXT.get(None))

    @staticmethod
    def create(
        session: Optional[str] = None,
        root: Optional[str] = None,
        auto_close: bool = True,
    ) -> ExecutionContext:
        """Create ExecutionContext."""
        from jaclang import Root

        ctx = ExecutionContext()
        ctx.mem = ShelfStorage(session)
        ctx.reports = []

        if not isinstance(
            system_root := ctx.mem.find_by_id(SUPER_ROOT_UUID), NodeAnchor
        ):
            system_root = cast(NodeAnchor, Root().__jac__)  # type: ignore[attr-defined]
            system_root.id = SUPER_ROOT_UUID
            ctx.mem.set(system_root.id, system_root)

        ctx.system_root = system_root

        ctx.entry_node = ctx.root = ctx.init_anchor(root, ctx.system_root)

        if auto_close and (old_ctx := EXECUTION_CONTEXT.get(None)):
            old_ctx.close()

        EXECUTION_CONTEXT.set(ctx)
        for func in ExecutionContext.on_ctx_change:
            func(EXECUTION_CONTEXT.get(None))

        return ctx

    @staticmethod
    def get() -> ExecutionContext:
        """Get current ExecutionContext."""
        if ctx := EXECUTION_CONTEXT.get(None):
            return ctx
        raise Exception("ExecutionContext is not yet available!")

    @staticmethod
    def get_root() -> Root:
        """Get current root."""
        if ctx := EXECUTION_CONTEXT.get(None):
            return cast(Root, ctx.root.architype)

        return cast(Root, ExecutionContext.global_system_root().architype)

    @staticmethod
    def global_system_root() -> NodeAnchor:
        """Get global system root."""
        from jaclang import Root

        if not (sr_anch := getattr(ExecutionContext, "system_root", None)):
            sr_arch = Root()
            sr_anch = sr_arch.__jac__  # type: ignore[attr-defined]
            sr_anch.id = SUPER_ROOT_UUID
            sr_anch.persistent = False
            ExecutionContext.system_root = sr_anch
        return sr_anch


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
