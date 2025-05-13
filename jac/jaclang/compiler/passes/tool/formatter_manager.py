"""Formatter manager for Jac code.

This module provides a manager for selecting between different formatter implementations.
"""

from enum import Enum, auto
from typing import Optional, Type

import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import UniPass
from jaclang.compiler.passes.tool.jac_formatter_pass import JacFormatPass
from jaclang.compiler.passes.tool.prettier_formatter_pass import PrettierFormatPass
from jaclang.compiler.program import JacProgram


class FormatterStyle(Enum):
    """Enumeration of available formatter styles."""

    CLASSIC = auto()  # The original formatter
    PRETTIER = auto()  # The prettier-style formatter


class FormatterManager:
    """Manager for selecting and applying formatters to Jac code."""

    @staticmethod
    def get_formatter_class(
        style: FormatterStyle = FormatterStyle.CLASSIC,
    ) -> Type[UniPass]:
        """Get the formatter class for the specified style.

        Args:
            style: The formatter style to use

        Returns:
            The formatter class
        """
        if style == FormatterStyle.CLASSIC:
            return JacFormatPass
        elif style == FormatterStyle.PRETTIER:
            return PrettierFormatPass
        else:
            raise ValueError(f"Unknown formatter style: {style}")

    @staticmethod
    def format_jac_file(
        file_path: str, style: FormatterStyle = FormatterStyle.CLASSIC
    ) -> str:
        """Format a Jac file using the specified formatter style.

        Args:
            file_path: Path to the Jac file to format
            style: The formatter style to use

        Returns:
            The formatted Jac code
        """
        formatter_class = FormatterManager.get_formatter_class(style)
        return JacProgram.jac_file_formatter(file_path, formatter_class=formatter_class)

    @staticmethod
    def format_jac_str(
        source_str: str, file_path: str, style: FormatterStyle = FormatterStyle.CLASSIC
    ) -> str:
        """Format a Jac string using the specified formatter style.

        Args:
            source_str: The Jac code to format
            file_path: A file path for reference (used for error reporting)
            style: The formatter style to use

        Returns:
            The formatted Jac code
        """
        formatter_class = FormatterManager.get_formatter_class(style)
        return JacProgram.jac_str_formatter(
            source_str, file_path, formatter_class=formatter_class
        )
