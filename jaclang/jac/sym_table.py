"""Jac Symbol Table."""
from typing import Optional

import jaclang.jac.absyntree as ast


class Symbol:
    """Symbol."""

    def __init__(
        self,
        name: str,
        typ: type,
        def_node: ast.AstNode,
        access: Optional[str] = None,
    ) -> None:
        """Initialize."""
        self.name = name
        self.typ = typ
        self.def_node = def_node
        self.def_line = def_node.line
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

    def set(self, name: str, symbol: Symbol, fresh_only: bool = False) -> bool:
        """Set a variable in the symbol table."""
        if fresh_only and name in self.tab:
            return False
        self.tab[name] = symbol
        return True

    def update(
        self,
        name: str,
        typ: Optional[type] = None,
        def_line: Optional[int] = None,
        def_node: Optional[ast.AstNode] = None,
        access: Optional[str] = None,
        deep: bool = False,
    ) -> bool:
        """Set a variable in the symbol table."""
        if name in self.tab:
            self.tab[name].typ = typ if typ else self.tab[name].typ
            self.tab[name].def_line = def_line if def_line else self.tab[name].def_line
            self.tab[name].def_node = def_node if def_node else self.tab[name].def_node
            self.tab[name].access = access if access else self.tab[name].access
            return True
        elif deep and self.parent:
            return self.parent.update(name, typ, def_line, def_node, access, deep)
        return False
