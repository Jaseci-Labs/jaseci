"""Printer for the Doc IR to formatted code.

This module contains the printer that transforms Doc IR into formatted code.
"""

from typing import Optional

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


class Printer:
    """Printer for Doc IR structures into formatted code."""

    def __init__(self, options: FormatterOptions):
        self.options = options

    def print(self, doc: Doc) -> str:
        """Print the Doc IR to a formatted string."""
        return self._print_doc(doc, 0, self.options.max_line_length)

    def _print_doc(
        self, doc: Doc, indent_level: int, width_remaining: int, is_broken: bool = False
    ) -> str:
        """Recursively print a Doc node.

        Args:
            doc: The Doc IR node to print
            indent_level: Current indentation level
            width_remaining: Remaining characters on the current line
            is_broken: Whether the parent group is broken

        Returns:
            The formatted string
        """
        if isinstance(doc, Text):
            return doc.text

        elif isinstance(doc, Line):
            if is_broken or doc.hard:
                return "\n" + " " * (indent_level * self.options.indent_size)
            else:
                return " " if not doc.literal else "\n"

        elif isinstance(doc, Group):
            # Try to print flat first
            flat_contents = self._print_doc(doc.contents, indent_level, width_remaining)

            # If it fits, use flat version
            if (
                len(flat_contents.splitlines()[-1]) <= width_remaining
                and "\n" not in flat_contents
            ):
                return flat_contents

            # Otherwise, print broken
            return self._print_doc(doc.contents, indent_level, width_remaining, True)

        elif isinstance(doc, Indent):
            return self._print_doc(
                doc.contents,
                indent_level + 1,
                width_remaining - self.options.indent_size,
                is_broken,
            )

        elif isinstance(doc, Concat):
            result = ""
            current_width = width_remaining

            for part in doc.parts:
                part_str = self._print_doc(part, indent_level, current_width, is_broken)
                result += part_str

                # Update remaining width
                if "\n" in part_str:
                    lines = part_str.splitlines()
                    current_width = width_remaining - len(lines[-1] if lines else "")
                else:
                    current_width -= len(part_str)

            return result

        elif isinstance(doc, IfBreak):
            if is_broken:
                return self._print_doc(
                    doc.break_contents, indent_level, width_remaining, is_broken
                )
            else:
                return self._print_doc(
                    doc.flat_contents, indent_level, width_remaining, is_broken
                )

        elif isinstance(doc, Align):
            align_size = self.options.indent_size if doc.n is None else doc.n
            return self._print_doc(
                doc.contents,
                indent_level + align_size // self.options.indent_size,
                width_remaining - align_size,
                is_broken,
            )

        # Default case
        return str(doc)
