"""Standardized transformation process and error interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Optional, Type

from jaclang.compiler.absyntree import AstNode, T
from jaclang.compiler.codeloc import CodeLocInfo
from jaclang.utils.helpers import pretty_print_source_location
from jaclang.utils.log import logging


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


class Transform(ABC, Generic[T]):
    """Abstract class for IR passes."""

    def __init__(
        self,
        input_ir: T,
        prior: Optional[Transform] = None,
    ) -> None:
        """Initialize pass."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self.errors_had: list[Alert] = [] if not prior else prior.errors_had
        self.warnings_had: list[Alert] = [] if not prior else prior.warnings_had
        self.cur_node: AstNode = input_ir  # tracks current node during traversal
        self.ir = self.transform(ir=input_ir)

    @abstractmethod
    def transform(self, ir: T) -> AstNode:
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
