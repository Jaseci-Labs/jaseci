"""Edge class for Jaseci."""
from jaseci.core.object import Object


class Edge(Object):
    """Edge class for Jaseci."""

    def __init__(self: "Edge", *args: list, **kwargs: dict) -> None:
        """Initialize edge."""
        super().__init__(*args, **kwargs)
