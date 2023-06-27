"""Jac Symbol Table."""
from typing import Optional, TypeVar


import jaclang.jac.absyntree as ast


class Symbol:
    """Symbol."""

    def __init__(
        self,
        name: str,
        node: ast.AstNode,
    ) -> None:
        """Initialize."""
        self.name = name
        self.node = node
        self.def_line = node.line


T = TypeVar("T", bound=Symbol)


class TypedSymbol(Symbol):
    """Typed Symbol."""

    def __init__(
        self,
        name: str,
        typ: type,
        node: ast.AstNode,
        access: Optional[str] = None,
    ) -> None:
        """Initialize."""
        self.typ = typ
        self.access = access
        super().__init__(name, node)


class DefDeclSymbol(Symbol):
    """DefDecl Symbol."""

    def __init__(
        self,
        name: str,
        node: ast.AstNode,
        other_node: Optional[ast.AstNode] = None,
        has_def: bool = False,
        has_decl: bool = False,
    ) -> None:
        """Initialize."""
        self.other_node = other_node
        self.has_def = has_def
        self.has_decl = has_decl
        super().__init__(name, node)


class SymbolTable:
    """Symbol Table.

    Functions as a stack by default, can create a separate table in pass
    if keeping track of multiple scopes is necessary.
    """

    def __init__(
        self,
        scope_name: str = "",
        parent: Optional["SymbolTable"] = None,
    ) -> None:
        """Initialize."""
        self.scope_name = scope_name
        self.parent = parent
        self.tab: dict = {}

    def lookup(self, name: str, deep: bool = True) -> Optional[T]:
        """Lookup a variable in the symbol table."""
        if name in self.tab:
            return self.tab[name]
        if deep and self.parent:
            return self.parent.lookup(name, deep)
        return None

    def set(self, sym: T, fresh_only: bool = False) -> bool:
        """Set a variable in the symbol table."""
        if fresh_only and sym.name in self.tab:
            return False
        self.tab[sym.name] = sym
        return True

    def update(self, sym: T, deep: bool = False) -> bool:
        """Set a variable in the symbol table."""
        if sym.name in self.tab:
            self.tab[sym.name] = T
            return True
        elif deep and self.parent:
            return self.parent.update(sym)
        return False

    def push(self, scope_name: str = "") -> "SymbolTable":
        """Push a new scope onto the symbol table."""
        return SymbolTable(scope_name, self)
