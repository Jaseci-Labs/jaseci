"""Standardized transformation process and error interface."""
from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Optional

from jaclang.jac.absyntree import AstNode
from jaclang.jac.constant import Constants as Con, Values as Val
from jaclang.utils.helpers import add_line_numbers, clip_code_section
from jaclang.utils.log import logging


class Alert:
    """Alert interface."""

    def __init__(
        self, msg: str, mod: str, line: int, col_start: int, col_end: int
    ) -> None:
        """Initialize alert."""
        self.msg = msg
        self.mod = mod
        self.line = line
        self.col_start = col_start
        self.col_end = col_end

    def __str__(self) -> str:
        """Return string representation of alert."""
        try:
            mod_path = os.path.relpath(self.mod, start=os.getcwd())
        except ValueError:
            mod_path = "<code_string>"
        return f"{mod_path}, line {self.line}, col {self.col_start}: {self.msg}"


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
            jac_err_line = errors[0].line if len(errors) else warnings[0].line
            with open(errors[0].mod, "r") as file:
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
        mod_path: str,
        input_ir: AstNode,
        base_path: str = "",
        prior: Optional[Transform] = None,
    ) -> None:
        """Initialize pass."""
        self.logger = logging.getLogger(self.__class__.__module__)
        self.errors_had: list[Alert] = [] if not prior else prior.errors_had
        self.warnings_had: list[Alert] = [] if not prior else prior.warnings_had
        self.cur_node = input_ir  # tracks current node during traversal
        self.mod_path = mod_path
        self.rel_mod_path = (
            mod_path.replace(base_path, "") if base_path else mod_path.split(os.sep)[-1]
        )
        self.ir = self.transform(ir=input_ir)

    @abstractmethod
    def transform(self, ir: AstNode) -> AstNode:
        """Transform interface."""
        pass

    def log_error(self, msg: str) -> None:
        """Pass Error."""
        alrt = Alert(
            msg,
            self.mod_path,
            self.cur_node.line if self.cur_node else 0,
            self.cur_node.col_start if self.cur_node else 0,
            self.cur_node.col_end if self.cur_node else 0,
        )
        self.errors_had.append(alrt)
        self.logger.error(str(alrt))

    def log_warning(self, msg: str) -> None:
        """Pass Error."""
        alrt = Alert(
            msg,
            self.mod_path,
            self.cur_node.line if self.cur_node else 0,
            self.cur_node.col_start if self.cur_node else 0,
            self.cur_node.col_end if self.cur_node else 0,
        )
        self.warnings_had.append(alrt)
        self.logger.warning(str(alrt))

    def gen_exception(
        self, msg: str = "Error in code transform, see above for details."
    ) -> TransformError:
        """Raise error."""
        return TransformError(msg, self.errors_had, self.warnings_had)
