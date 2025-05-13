"""Doc IR classes for the new formatter infrastructure.

This module contains the Doc IR (Intermediate Representation) classes used
by the prettier-style formatter.
"""

from typing import List, Optional, Union


class Doc:
    """Base class for document parts."""

    def __str__(self):
        return self.__class__.__name__


class Text(Doc):
    """Simple text content."""

    def __init__(self, text: str):
        self.text = text

    def __str__(self):
        return f'Text("{self.text}")'


class Line(Doc):
    """Represents a line break that can be preserved or flattened."""

    def __init__(self, hard: bool = False, literal: bool = False):
        self.hard = hard  # If True, always break
        self.literal = (
            literal  # If True, includes the literal newline in flattened output
        )

    def __str__(self):
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

    def __str__(self):
        return f"Group({self.contents})"


class Indent(Doc):
    """Indented content."""

    def __init__(self, contents: Doc):
        self.contents = contents

    def __str__(self):
        return f"Indent({self.contents})"


class Concat(Doc):
    """A sequence of doc parts."""

    def __init__(self, parts: List[Doc]):
        self.parts = parts

    def __str__(self):
        return f"Concat({self.parts})"


class IfBreak(Doc):
    """Content that differs based on whether the parent group is broken."""

    def __init__(self, break_contents: Doc, flat_contents: Doc):
        self.break_contents = break_contents
        self.flat_contents = flat_contents

    def __str__(self):
        return f"IfBreak({self.break_contents}, {self.flat_contents})"


class Align(Doc):
    """Alignment relative to the current indentation level."""

    def __init__(self, contents: Doc, n: Optional[int] = None):
        self.contents = contents
        self.n = n  # Number of spaces, or null to use current indentation level

    def __str__(self):
        return f"Align({self.n}, {self.contents})"


DocType = Union[Doc, Text, Line, Group, Indent, Concat, IfBreak, Align]
