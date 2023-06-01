"""Master class for Jaseci."""
from jaseci.core.element import Element


class Master(Element):
    """Master class for Jaseci."""

    def __init__(self: "Master", *args: list, **kwargs: dict) -> None:
        """Initialize master."""
        super().__init__(*args, **kwargs)
