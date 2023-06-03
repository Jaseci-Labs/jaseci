"""Object class for Jaseci."""
from jaseci.core.element import Element


class Object(Element):
    """Object class for Jaseci."""

    def __init__(self: "Object", *args: list, **kwargs: dict) -> None:
        """Initialize object."""
        self.context = {}
        super().__init__(*args, **kwargs)
