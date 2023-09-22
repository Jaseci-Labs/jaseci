"""Jac Symbol Table."""
from __future__ import annotations

from enum import Enum
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import jaclang.jac.absyntree as ast


class SymbolType(Enum):
    """Symbol types."""

    VAR = "var"
    ABILITY = "ability"
    ARCH = "arch"
    IMPL = "impl"
    HAS = "field"


class SymbolHitType(Enum):
    """Symbol types."""

    DECL = "decl"
    DEFN = "defn"
    DECL_DEFN = "decl_defn"
    USE = "use"


class Symbol:
    """Symbol."""

    def __init__(
        self,
        name: str,
        sym_type: SymbolType,
        typ: Optional[type] = None,
        decl: Optional[ast.AstNode] = None,
        defn: Optional[list[ast.AstNode]] = None,
        uses: Optional[list[ast.AstNode]] = None,
    ) -> None:
        """Initialize."""
        self.name = name
        self.sym_type = sym_type
        self.typ = typ
        self.decl = decl
        self.defn: list[ast.AstNode] = defn if defn else []
        self.uses: list[ast.AstNode] = uses if uses else []

    def __repr__(self) -> str:
        """Repr."""
        return (
            f"Symbol({self.name}, {self.sym_type}, {self.typ}, "
            f"{self.decl}, {self.defn}, {self.uses})"
        )


class SymbolTable:
    """Symbol Table."""

    def __init__(
        self, name: str, key_node: ast.AstNode, parent: Optional[SymbolTable] = None
    ) -> None:
        """Initialize."""
        self.name = name
        self.key_node = key_node
        self.parent = parent if parent else self
        self.kid: list[SymbolTable] = []
        self.tab: dict[str, Symbol] = {}

    def has_parent(self) -> bool:
        """Check if has parent."""
        return self.parent != self

    def get_parent(self) -> SymbolTable:
        """Get parent."""
        if self.parent == self:
            raise Exception("No parent")
        return self.parent

    def lookup(
        self, name: str, sym_hit: Optional[SymbolHitType] = None, deep: bool = True
    ) -> Optional[Symbol]:
        """Lookup a variable in the symbol table."""
        if name in self.tab and (
            not sym_hit
            or (sym_hit == SymbolHitType.DECL and self.tab[name].decl)
            or (sym_hit == SymbolHitType.DEFN and len(self.tab[name].defn))
            or (
                sym_hit == SymbolHitType.DECL_DEFN
                and (self.tab[name].decl or len(self.tab[name].defn))
            )
            or (sym_hit == SymbolHitType.USE and len(self.tab[name].uses))
        ):
            return self.tab[name]
        if deep and self.has_parent():
            return self.get_parent().lookup(name, sym_hit, deep)
        return None

    def insert(
        self,
        name: str,
        sym_type: SymbolType,
        sym_hit: SymbolHitType,
        node: ast.AstNode,
        single: bool = False,
    ) -> Optional[ast.AstNode]:
        """Set a variable in the symbol table.

        Returns original symbol single check fails.
        """
        if single:
            if (
                sym_hit in [SymbolHitType.DECL, SymbolHitType.DECL_DEFN]
                and name in self.tab
                and self.tab[name].decl
            ):
                return self.tab[name].decl
            elif (
                sym_hit in [SymbolHitType.DEFN, SymbolHitType.DECL_DEFN]
                and name in self.tab
                and len(self.tab[name].defn)
            ):
                return self.tab[name].defn[-1]
            elif (
                sym_hit == SymbolHitType.USE
                and name in self.tab
                and len(self.tab[name].uses)
            ):
                return self.tab[name].uses[-1]
        if name not in self.tab:
            self.tab[name] = Symbol(name=name, sym_type=sym_type)
        if sym_hit == SymbolHitType.DECL:
            self.tab[name].decl = node
        elif sym_hit == SymbolHitType.DEFN:
            self.tab[name].defn.append(node)
        elif sym_hit == SymbolHitType.DECL_DEFN:
            self.tab[name].defn.append(node)
            if not self.tab[name].decl:
                self.tab[name].decl = node
        elif sym_hit == SymbolHitType.USE:
            self.tab[name].uses.append(node)

    def push_scope(self, name: str, key_node: ast.AstNode) -> SymbolTable:
        """Push a new scope onto the symbol table."""
        self.kid.append(SymbolTable(name, key_node, self))
        return self.kid[-1]

    def __repr__(self) -> str:
        """Repr."""
        out = f"{self.name} {super().__repr__()}:\n"
        for k, v in self.tab.items():
            out += f"    {k}: {v}\n"
        return out
