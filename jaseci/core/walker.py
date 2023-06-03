"""Walker class for Jaseci."""
from jaseci.core.object import Object


class Walker(Object):
    """Walker class for Jaseci."""

    def __init__(self: "Walker", *args: list, **kwargs: dict) -> None:
        """Initialize walker."""
        super().__init__(*args, **kwargs)
