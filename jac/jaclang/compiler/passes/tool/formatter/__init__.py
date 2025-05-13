"""Prettier-style formatter infrastructure for Jac.

This package contains the implementation of a prettier-style formatter for the Jac language.
"""

from jaclang.compiler.passes.tool.formatter.doc_builder import DocBuilder
from jaclang.compiler.passes.tool.formatter.doc_ir import (
    Align,
    Concat,
    Doc,
    Group,
    IfBreak,
    Indent,
    Line,
    Text,
)
from jaclang.compiler.passes.tool.formatter.options import FormatterOptions
from jaclang.compiler.passes.tool.formatter.printer import Printer

__all__ = [
    "DocBuilder",
    "Printer",
    "FormatterOptions",
    "Doc",
    "Text",
    "Line",
    "Group",
    "Indent",
    "Concat",
    "IfBreak",
    "Align",
]
