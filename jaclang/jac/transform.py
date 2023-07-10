"""Standardized transformation process and error interface."""
from __future__ import annotations

import os
from abc import ABC, ABCMeta, abstractmethod
from typing import Optional


from jaclang.jac.absyntree import AstNode
from jaclang.utils.log import logging
from jaclang.utils.sly.lex import LexerMeta
from jaclang.utils.sly.yacc import ParserMeta


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
        self.errors_had = [] if not prior else prior.errors_had
        self.warnings_had = [] if not prior else prior.warnings_had
        self.cur_line = 0
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
        msg = f"Mod {self.rel_mod_path}: Line {self.cur_line}, " + msg
        self.errors_had.append(msg)
        self.logger.error(msg)

    def log_warning(self, msg: str) -> None:
        """Pass Error."""
        msg = f"Mod {self.rel_mod_path}: Line {self.cur_line}, " + msg
        self.warnings_had.append(msg)
        self.logger.warning(msg)


class ABCLexerMeta(ABCMeta, LexerMeta):
    """Metaclass for Jac Lexer."""

    pass


class ABCParserMeta(ABCMeta, ParserMeta):
    """Metaclass for Jac Lexer."""

    pass
