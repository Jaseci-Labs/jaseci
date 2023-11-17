"""Standardized transformation process and error interface."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from jaclang.jac.absyntree import AstNode
from jaclang.jac.codeloc import CodeLocInfo
from jaclang.jac.constant import Constants as Con, Values as Val
from jaclang.utils.helpers import add_line_numbers, clip_code_section
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


class TransformError(Exception):
    """Error during transformation."""

    def __init__(
        self, message: str, errors: list[Alert], warnings: list[Alert]
    ) -> None:
        """Initialize error."""
        self.errors = errors
        self.warnings = warnings
        if len(errors):
            message += "\nErrors:"
            for i in self.errors:
                message += "\n" + str(i)
        if len(warnings):
            message += "\nWarnings:"
            for i in self.warnings:
                message += "\n" + str(i)
        if len(errors) or len(warnings):
            jac_err_line = (
                errors[0].loc.first_line if len(errors) else warnings[0].loc.first_line
            )
            with open(errors[0].loc.mod_path, "r") as file:
                jac_code_string = file.read()
            message += f"\n{Con.JAC_ERROR_PREAMBLE}\n" + clip_code_section(
                add_line_numbers(jac_code_string),
                jac_err_line,
                Val.JAC_ERROR_LINE_RANGE,
            )
        super().__init__(message)


class Transform(ABC):
    """Abstract class for IR passes."""

    def __init__(
        self,
        input_ir: AstNode,
        prior: Optional[Transform] = None,
    ) -> None:
        """Initialize pass."""
        self.logger = logging.getLogger(self.__class__.__module__)
        self.errors_had: list[Alert] = [] if not prior else prior.errors_had
        self.warnings_had: list[Alert] = [] if not prior else prior.warnings_had
        self.cur_node = input_ir  # tracks current node during traversal
        self.ir: AstNode = self.transform(ir=input_ir)

    @abstractmethod
    def transform(self, ir: AstNode) -> AstNode:
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

    def gen_exception(
        self, msg: str = "Error in code transform, see above for details."
    ) -> TransformError:
        """Raise error."""
        return TransformError(msg, self.errors_had, self.warnings_had)
