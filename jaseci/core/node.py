"""Node class for Jaseci."""
from jaseci.core.object import object


class Node(object):
    """Node class for Jaseci."""

    def __init__(self: "Node", *args: list, **kwargs: dict) -> None:
        """Initialize node."""
        super().__init__(*args, **kwargs)
