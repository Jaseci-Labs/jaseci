"""Standardized transformation process and error interface."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Generic, Optional, TYPE_CHECKING, Type, TypeVar

from jaclang.compiler.absyntree import AstNode
from jaclang.compiler.codeloc import CodeLocInfo
from jaclang.settings import settings
from jaclang.utils.helpers import pretty_print_source_location
from jaclang.utils.log import logging

if TYPE_CHECKING:
    from jaclang.compiler.program import JacProgram

T = TypeVar("T", bound=AstNode)
R = TypeVar("R", bound=AstNode)


class Alert:
    """Alert interface."""

    def __init__(self, msg: str, loc: CodeLocInfo, from_pass: Type[Transform]) -> None:
        """Initialize alert."""
        self.msg = msg
        self.loc: CodeLocInfo = loc
        self.from_pass: Type[Transform] = from_pass

    def __str__(self) -> str:
        """Return string representation of alert."""
        return (
            f" {self.loc.mod_path}, line {self.loc.first_line},"
            f" col {self.loc.col_start}: {self.msg}"
        )

    def __repr__(self) -> str:
        """Return string representation of alert."""
        return self.as_log()

    def as_log(self) -> str:
        """Return the alert as a single line log as opposed to the pretty print."""
        file_path: str = self.loc.mod_path
        if file_path == "":
            return self.msg  # There are error messages without file references.

        line: int = self.loc.first_line
        column: int = self.loc.col_start
        return f"{file_path}:{line}:{column} {self.msg}"

    def pretty_print(self) -> str:
        """Pretty pritns the Alert to show the alert with source location."""
        pretty_dump = pretty_print_source_location(
            self.loc.mod_path,
            self.loc.orig_src.code,
            self.loc.first_line,
            self.loc.pos_start,
            self.loc.pos_end,
        )
        if pretty_dump != "":
            pretty_dump = "\n" + pretty_dump
        return self.as_log() + pretty_dump


class Transform(ABC, Generic[T, R]):
    """Abstract class for IR passes."""

    def __init__(
        self,
        ir_in: T,
        prior: Optional[Transform],
        prog: Optional[JacProgram],
    ) -> None:
        """Initialize pass."""
        from jaclang.compiler.program import JacProgram

        self.logger = logging.getLogger(self.__class__.__name__)
        self.errors_had: list[Alert] = [] if not prior else prior.errors_had
        self.warnings_had: list[Alert] = [] if not prior else prior.warnings_had
        self.cur_node: AstNode = ir_in  # tracks current node during traversal
        self.prog = prog or JacProgram()
        self.time_taken = 0.0
        self.ir_in: T = ir_in
        self.ir_out: R = self.timed_transform(ir=ir_in)

    def timed_transform(
        self,
        ir: T,
    ) -> R:
        """Transform with time tracking."""
        start_time = time.time()
        ret = self.transform(ir=ir)
        self.time_taken = time.time() - start_time
        if settings.pass_timer:
            self.log_info(
                f"Time taken in {self.__class__.__name__}: {self.time_taken:.4f} seconds"
            )
        return ret

    @abstractmethod
    def transform(self, ir: T) -> R:
        """Transform interface."""
        pass

    def log_error(self, msg: str, node_override: Optional[AstNode] = None) -> None:
        """Pass Error."""
        alrt = Alert(
            msg,
            self.cur_node.loc if not node_override else node_override.loc,
            self.__class__,
        )
        self.errors_had.append(alrt)
        self.logger.error(alrt.as_log())

    def log_warning(self, msg: str, node_override: Optional[AstNode] = None) -> None:
        """Pass Error."""
        alrt = Alert(
            msg,
            self.cur_node.loc if not node_override else node_override.loc,
            self.__class__,
        )
        self.warnings_had.append(alrt)
        self.logger.warning(alrt.as_log())

    def log_info(self, msg: str) -> None:
        """Log info."""
        self.logger.info(msg)

    def ice(self, msg: str = "Something went horribly wrong!") -> RuntimeError:
        """Pass Error."""
        self.log_error(f"ICE: Pass {self.__class__.__name__} - {msg}")
        return RuntimeError(
            f"Internal Compiler Error: Pass {self.__class__.__name__} - {msg}"
        )
