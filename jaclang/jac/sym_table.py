"""Jac Symbol Table."""
from typing import Optional

import jaclang.jac.absyntree as ast


class Symbol:
    """Symbol."""

    def __init__(
        self,
        name: str,
        typ: type,
        def_line: int,
        def_node: ast.AstNode,
        access: Optional[str] = None,
    ) -> None:
        """Initialize."""
        self.name = name
        self.typ = typ
        self.def_line = def_line
        self.def_node = def_node
        self.access = access


class SymbolTable:
    """Symbol Table."""

    def __init__(
        self,
        scope_name: str = "",
        parent: Optional["SymbolTable"] = None,
    ) -> None:
        """Initialize."""
        self.scope_name = scope_name
        self.parent = parent
        self.tab: dict[str, Symbol] = {}

    def lookup(self, name: str, deep: bool = True) -> Optional[Symbol]:
        """Lookup a variable in the symbol table."""
        if name in self.tab:
            return self.tab[name]
        if deep and self.parent:
            return self.parent.lookup(name, deep)
        return None

    def set(self, name: str, symbol: Symbol) -> None:
        """Set a variable in the symbol table."""
        self.tab[name] = symbol
