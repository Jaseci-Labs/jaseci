"""Jac Symbol Table."""
import pprint
from typing import Optional, TypeVar


import jaclang.jac.absyntree as ast


class Symbol:
    """Symbol."""

    def __init__(
        self,
        name: str,
        node: Optional[ast.AstNode] = None,
    ) -> None:
        """Initialize."""
        self.name = name
        self.node = node

    def pretty_print(self) -> str:
        """Pretty print the symbol."""
        return pprint.pformat(vars(self), indent=2)

    def __repr__(self) -> str:
        """Representation for printing Symbols."""
        return f"{self.pretty_print()}"


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
        node: Optional[ast.AstNode] = None,
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

    def pop(self) -> "SymbolTable":
        """Pop the current scope off the symbol table."""
        return self.parent if self.parent else self

    def pretty_print(self) -> str:
        """Pretty print the symbol table and return the result as a string."""
        output = f"Scope: {self.scope_name}\n"
        output += pprint.pformat(self.tab)
        if self.parent:
            output += f"\nParent Scope: {self.parent.scope_name}\n"
            output += self.parent.pretty_print()
        return output

    def __repr__(self) -> str:
        """Return the symbol table as a string."""
        return self.pretty_print()
