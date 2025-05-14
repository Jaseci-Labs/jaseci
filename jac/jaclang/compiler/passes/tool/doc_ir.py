from __future__ import annotations

from typing import Optional, Union

# Define DocType for self-referential typing
DocType = Union["Doc", "Text", "Line", "Group", "Indent", "Concat", "IfBreak", "Align"]
DocContent = Union[DocType, list[DocType]]


class Doc:
    """Base class for document parts."""

    def __str__(self) -> str:
        return self.__class__.__name__


class Text(Doc):
    """Simple text content."""

    def __init__(self, text: str) -> None:
        self.text: str = text

    def __str__(self) -> str:
        return f'Text("{self.text}")'


class Line(Doc):
    """Represents a line break that can be preserved or flattened."""

    def __init__(self, hard: bool = False, literal: bool = False) -> None:
        self.hard: bool = hard  # If True, always break
        self.literal: bool = (
            literal  # If True, includes the literal newline in flattened output
        )

    def __str__(self) -> str:
        attrs: list[str] = []
        if self.hard:
            attrs.append("hard")
        if self.literal:
            attrs.append("literal")
        return f"Line({', '.join(attrs)})"


class Group(Doc):
    """A group that can be printed flat or broken into multiple lines."""

    def __init__(
        self,
        contents: DocContent,
        break_contiguous: bool = False,
        id: Optional[str] = None,
    ) -> None:
        self.contents: DocContent = contents
        self.break_contiguous: bool = break_contiguous
        self.id: Optional[str] = id

    def __str__(self) -> str:
        return f"Group({self.contents})"


class Indent(Doc):
    """Indented content."""

    def __init__(self, contents: DocContent) -> None:
        self.contents: DocContent = contents

    def __str__(self) -> str:
        return f"Indent({self.contents})"


class Concat(Doc):
    """A sequence of doc parts."""

    def __init__(self, parts: list[DocType]) -> None:
        self.parts: list[DocType] = parts

    def __str__(self) -> str:
        return f"Concat({self.parts})"


class IfBreak(Doc):
    """Content that differs based on whether the parent group is broken."""

    def __init__(self, break_contents: DocContent, flat_contents: DocContent) -> None:
        self.break_contents: DocContent = break_contents
        self.flat_contents: DocContent = flat_contents

    def __str__(self) -> str:
        return f"IfBreak({self.break_contents}, {self.flat_contents})"


class Align(Doc):
    """Alignment relative to the current indentation level."""

    def __init__(self, contents: DocContent, n: Optional[int] = None) -> None:
        self.contents: DocContent = contents
        self.n: Optional[int] = (
            n  # Number of spaces, or null to use current indentation level
        )

    def __str__(self) -> str:
        return f"Align({self.n}, {self.contents})"
