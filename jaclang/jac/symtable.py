"""Jac Symbol Table."""
from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import jaclang.jac.absyntree as ast


class Symbol:
    """Symbol."""

    def __init__(
        self,
        name: str,
        decl: ast.AstNode,
        typ: Optional[type] = None,
        defn: Optional[list[ast.AstNode]] = None,
        uses: Optional[list[ast.AstNode]] = None,
    ) -> None:
        """Initialize."""
        self.name = name
        self.typ = typ
        self.decl = decl
        self.defn: list[ast.AstNode] = defn if defn else []
        self.uses: list[ast.AstNode] = uses if uses else []


class SymbolTable:
    """Symbol Table."""

    def __init__(self, parent: Optional[SymbolTable] = None) -> None:
        """Initialize."""
        self.parent = parent
        self.tab: dict[str, Symbol] = {}

    def lookup(self, name: str, deep: bool = True) -> Optional[Symbol]:
        """Lookup a variable in the symbol table."""
        if name in self.tab:
            return self.tab[name]
        if deep and self.parent:
            return self.parent.lookup(name, deep)
        return None

    def insert(self, sym: Symbol, fresh_only: bool = False) -> bool:
        """Set a variable in the symbol table."""
        if fresh_only and sym.name in self.tab:
            return False
        self.tab[sym.name] = sym
        return True

    def push_scope(self) -> SymbolTable:
        """Push a new scope onto the symbol table."""
        return SymbolTable(self)
