"""Standardized transformation process and error interface."""
from abc import ABC, abstractmethod
from typing import Generator, Sequence, Union

from jaclang.jac.absyntree import AstNode
from jaclang.utils.log import logging

IRType = Union[AstNode, Generator, Sequence, str]


class Transform(ABC):
    """Abstract class for IR passes."""

    def __init__(self, mod_path: str, input_ir: IRType, base_path: str = "") -> None:
        """Initialize pass."""
        self.logger = logging.getLogger(self.__class__.__module__)
        self.mod_path = mod_path
        self.rel_mod_path = mod_path.replace(base_path, "")
        self.ir: IRType = self.transform(ir=input_ir)

    @abstractmethod
    def transform(self, ir: IRType) -> IRType:
        """Transform interface."""
        pass

    @abstractmethod
    def err_line(self) -> int:
        """Get line number for error current line."""
        pass

    def log_error(self, msg: str) -> None:
        """Pass Error."""
        self.logger.error(f"Mod {self.rel_mod_path}, Line {self.err_line()}, " + msg)

    def log_warning(self, msg: str) -> None:
        """Pass Error."""
        self.logger.warning(f"Mod {self.rel_mod_path}, Line {self.err_line()}, " + msg)
