"""Jac Symbol Table."""
from typing import Optional


class Symbol:
    """Symbol."""

    def __init__(self) -> None:
        """Initialize."""
        self.name = None
        self.access = None
        self.typ = None


class SymbolTable:
    """Symbol Table."""

    def __init__(
        self, scope_name: str = "", parent: Optional["SymbolTable"] = None
    ) -> None:
        """Initialize."""
        self.parent = parent
        self.table: dict[str, Symbol] = {}
