"""Standardized transformation process and error interface."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Optional

from jaclang.compiler.absyntree import AstNode, T
from jaclang.compiler.codeloc import CodeLocInfo
from jaclang.utils.log import logging


class Alert:
    """Alert interface."""

    def __init__(self, msg: str, loc: CodeLocInfo) -> None:
        """Initialize alert."""
        self.msg = msg
        self.loc: CodeLocInfo = loc

    def __str__(self) -> str:
        """Return string representation of alert."""
        return (
            f"{self.loc.mod_path}, line {self.loc.first_line},"
            f" col {self.loc.col_start}: {self.msg}"
        )

    def __repr__(self) -> str:
        """Return string representation of alert."""
        return self.__str__()


class Transform(ABC, Generic[T]):
    """Abstract class for IR passes."""

    def __init__(
        self,
        input_ir: T,
        prior: Optional[Transform] = None,
    ) -> None:
        """Initialize pass."""
        self.logger = logging.getLogger(self.__class__.__module__)
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
        alrt = Alert(msg, self.cur_node.loc if not node_override else node_override.loc)
        self.errors_had.append(alrt)
        self.logger.error(str(alrt))

    def log_warning(self, msg: str, node_override: Optional[AstNode] = None) -> None:
        """Pass Error."""
        alrt = Alert(msg, self.cur_node.loc if not node_override else node_override.loc)
        self.warnings_had.append(alrt)
        self.logger.warning(str(alrt))
