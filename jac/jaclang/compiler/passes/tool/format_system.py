"""Format system for Jac code.

This module implements a Prettier-style formatting architecture for Jac code.
It provides a Doc IR (Intermediate Representation) that abstracts formatting concerns
from the AST structure, allowing for more flexible and powerful formatting strategies.
"""

from typing import List, Optional, Union, Any, Dict


class FormatterOptions:
    """Configuration options for the formatter."""

    def __init__(
        self,
        indent_size: int = 4,
        max_line_length: int = 88,
        use_tabs: bool = False,
        formatter_type: str = "classic",
    ):
        """Initialize formatter options with defaults."""
        self.indent_size = indent_size
        self.max_line_length = max_line_length
        self.use_tabs = use_tabs
        self.formatter_type = formatter_type  # "classic" or "prettier"


class Doc:
    """Base class for document parts."""

    def __str__(self) -> str:
        return self.__class__.__name__


class Text(Doc):
    """Simple text content."""

    def __init__(self, text: str):
        self.text = text

    def __str__(self) -> str:
        return f'Text("{self.text}")'


class Line(Doc):
    """Represents a line break that can be preserved or flattened."""

    def __init__(self, hard: bool = False, literal: bool = False):
        self.hard = hard  # If True, always break
        self.literal = (
            literal  # If True, includes the literal newline in flattened output
        )

    def __str__(self) -> str:
        attrs = []
        if self.hard:
            attrs.append("hard")
        if self.literal:
            attrs.append("literal")
        return f"Line({', '.join(attrs)})"


class Group(Doc):
    """A group that can be printed flat or broken into multiple lines."""

    def __init__(
        self, contents: Doc, break_contiguous: bool = False, id: Optional[str] = None
    ):
        self.contents = contents
        self.break_contiguous = break_contiguous
        self.id = id

    def __str__(self) -> str:
        return f"Group({self.contents})"


class Indent(Doc):
    """Indented content."""

    def __init__(self, contents: Doc):
        self.contents = contents

    def __str__(self) -> str:
        return f"Indent({self.contents})"


class Concat(Doc):
    """A sequence of doc parts."""

    def __init__(self, parts: List[Doc]):
        self.parts = parts

    def __str__(self) -> str:
        return f"Concat({self.parts})"


class IfBreak(Doc):
    """Content that differs based on whether the parent group is broken."""

    def __init__(self, break_contents: Doc, flat_contents: Doc):
        self.break_contents = break_contents
        self.flat_contents = flat_contents

    def __str__(self) -> str:
        return f"IfBreak({self.break_contents}, {self.flat_contents})"


class Align(Doc):
    """Alignment relative to the current indentation level."""

    def __init__(self, contents: Doc, n: Optional[int] = None):
        self.contents = contents
        self.n = n  # Number of spaces, or None to use current indentation level

    def __str__(self) -> str:
        return f"Align({self.n}, {self.contents})"


class JacDocBuilder:
    """Builds a Doc IR from a Jac AST."""

    def __init__(self, options: FormatterOptions):
        """Initialize the Doc builder with options."""
        self.options = options
        self.comments: List[Any] = []

    def build(self, ast: Any) -> Doc:
        """Build a Doc IR from a Jac AST."""
        # This is a placeholder implementation
        # The actual implementation would traverse the AST and build a Doc IR
        return Text("Not implemented")


class JacPrinter:
    """Printer for Doc IR structures into formatted code."""

    def __init__(self, options: FormatterOptions):
        """Initialize the printer with options."""
        self.options = options

    def print(self, doc: Doc) -> str:
        """Print the Doc IR to a formatted string."""
        return self._print_doc(doc, 0, self.options.max_line_length)

    def _print_doc(
        self, doc: Doc, indent_level: int, width_remaining: int, is_broken: bool = False
    ) -> str:
        """Recursively print a Doc node."""
        if isinstance(doc, Text):
            return doc.text

        elif isinstance(doc, Line):
            if is_broken or doc.hard:
                indent_str = " " * (indent_level * self.options.indent_size)
                return "\n" + indent_str
            else:
                return " " if not doc.literal else "\n"

        elif isinstance(doc, Group):
            # Try to print flat first
            flat_contents = self._print_doc(
                doc.contents, indent_level, width_remaining, False
            )

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


class CommentAttacher:
    """Attaches comments to the nearest relevant AST nodes."""

    def __init__(self, ast: Any, comments: List[Any]):
        """Initialize with AST and comments."""
        self.ast = ast
        self.comments = sorted(comments, key=lambda c: c.loc.first_line)
        self.unattached_comments: List[Any] = []

    def run(self) -> Any:
        """Attach comments to nodes and return the modified AST."""
        self.unattached_comments = list(self.comments)
        self._visit_node(self.ast)
        return self.ast

    def _visit_node(self, node: Any) -> None:
        """Visit a node and its children, attaching comments as appropriate."""
        # This is a placeholder implementation
        # The actual implementation would traverse the AST and attach comments
        pass
