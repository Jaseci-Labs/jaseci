"""Jaseci Ability class definition."""
from typing import TypeVar

from jaseci.core.element import Element


Node = TypeVar("Node")
Walker = TypeVar("Walker")


class Ability(Element):
    """Ability class for Jaseci."""

    def __init__(
        self: "Ability",
        here: "Node" = None,
        visitor: "Walker" = None,
        *args: list,
        **kwargs: dict
    ) -> None:
        """Initialize ability."""
        self.here = here
        self.visitor = visitor
        super().__init__(*args, **kwargs)

    def set_here(self: "Ability", here: "Node") -> None:
        """Set here ref for ability."""
        self.here = here

    def set_visitor(self: "Ability", visitor: "Walker") -> None:
        """Set visitor ref for ability."""
        self.visitor = visitor
