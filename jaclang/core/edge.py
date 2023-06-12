"""Edge class for Jaseci."""
from enum import Enum, auto

from jaclang.core.object import Object


class EdgeDir(Enum):
    """Edge direction indicator."""

    IN = auto()
    OUT = auto()
    BOTH = auto()


class Edge(Object):
    """Edge class for Jaseci."""

    def __init__(self: "Edge", *args: list, **kwargs: dict) -> None:
        """Initialize edge."""
        super().__init__(*args, **kwargs)
