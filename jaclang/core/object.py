"""Object class for Jaseci."""
from jaclang.core.element import Element


class Object(Element):
    """Object class for Jaseci."""

    def __init__(self, *args: list, **kwargs: dict) -> None:
        """Initialize object."""
        self.context = {}
        super().__init__(*args, **kwargs)
