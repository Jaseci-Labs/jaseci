"""Jaseci Ability class definition."""
from typing import TypeVar

from jaclang.core.element import Element


Node = TypeVar("Node")
Walker = TypeVar("Walker")


class Ability(Element):
    """Ability class for Jaseci."""

    def __init__(
        self, here: "Node" = None, visitor: "Walker" = None, *args: list, **kwargs: dict
    ) -> None:
        """Initialize ability."""
        self.here = here
        self.visitor = visitor
        super().__init__(*args, **kwargs)

    def set_here(self, here: "Node") -> None:
        """Set here ref for ability."""
        self.here = here

    def set_visitor(self, visitor: "Walker") -> None:
        """Set visitor ref for ability."""
        self.visitor = visitor
