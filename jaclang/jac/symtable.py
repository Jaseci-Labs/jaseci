"""Jac Symbol Table."""
from __future__ import annotations

from enum import Enum
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    import jaclang.jac.absyntree as ast


class SymbolType(Enum):
    """Symbol types."""

    MODULE = "module"
    MOD_VAR = "mod_var"
    VAR = "var"
    IMM_VAR = "immutable"
    ABILITY = "ability"
    OBJECT_ARCH = "object"
    NODE_ARCH = "node"
    EDGE_ARCH = "edge"
    WALKER_ARCH = "walker"
    ENUM_ARCH = "enum"
    TEST = "test"
    TYPE = "type"
    IMPL = "impl"
    HAS_VAR = "field"
    METHOD = "method"
    CONSTRUCTOR = "constructor"
    ENUM_MEMBER = "enum_member"

    def __str__(self) -> str:
        """Stringify."""
        return self.value


class SymbolAccess(Enum):
    """Symbol types."""

    PRIVATE = "private"
    PUBLIC = "public"
    PROTECTED = "protected"

    def __str__(self) -> str:
        """Stringify."""
        return self.value


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
        access: SymbolAccess,
        typ: Optional[type] = None,
        decl: Optional[ast.AstSymbolNode] = None,
        defn: Optional[list[ast.AstSymbolNode]] = None,
        uses: Optional[list[ast.AstSymbolNode]] = None,
    ) -> None:
        """Initialize."""
        self.name = name
        self.sym_type = sym_type
        self.typ = typ
        self.decl = decl
        self.defn: list[ast.AstSymbolNode] = defn if defn else []
        self.uses: list[ast.AstSymbolNode] = uses if uses else []
        self.access = access

    def __repr__(self) -> str:
        """Repr."""
        return (
            f"Symbol({self.name}, {self.sym_type}, {self.typ}, "
            f"{self.decl}, {self.defn}, {self.uses})"
        )


class SymbolTable:
    """Symbol Table."""

    def __init__(
        self, name: str, owner: ast.AstNode, parent: Optional[SymbolTable] = None
    ) -> None:
        """Initialize."""
        self.name = name
        self.owner = owner
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
        sym_hit: SymbolHitType,
        node: ast.AstSymbolNode,
        access_spec: Optional[ast.AstAccessNode] = None,
        single: bool = False,
    ) -> Optional[ast.AstNode]:
        """Set a variable in the symbol table.

        Returns original symbol as collision if single check fails, none otherwise.
        Also updates node.sym to create pointer to symbol.
        """
        if single:
            if (
                sym_hit in [SymbolHitType.DECL, SymbolHitType.DECL_DEFN]
                and node.sym_name in self.tab
                and self.tab[node.sym_name].decl
            ):
                return self.tab[node.sym_name].decl
            elif (
                sym_hit in [SymbolHitType.DEFN, SymbolHitType.DECL_DEFN]
                and node.sym_name in self.tab
                and len(self.tab[node.sym_name].defn)
            ):
                return self.tab[node.sym_name].defn[-1]
            elif (
                sym_hit == SymbolHitType.USE
                and node.sym_name in self.tab
                and len(self.tab[node.sym_name].uses)
            ):
                return self.tab[node.sym_name].uses[-1]
        if node.sym_name not in self.tab:
            sym = Symbol(
                name=node.sym_name,
                sym_type=node.sym_type,
                access=access_spec.access_type if access_spec else SymbolAccess.PUBLIC,
            )
            node.sym_link = sym
            self.tab[node.sym_name] = sym
        if sym_hit == SymbolHitType.DECL:
            self.tab[node.sym_name].decl = node
        elif sym_hit == SymbolHitType.DEFN:
            self.tab[node.sym_name].defn.append(node)
        elif sym_hit == SymbolHitType.DECL_DEFN:
            self.tab[node.sym_name].defn.append(node)
            if not self.tab[node.sym_name].decl:
                self.tab[node.sym_name].decl = node
        elif sym_hit == SymbolHitType.USE:
            self.tab[node.sym_name].uses.append(node)

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


__all__ = [
    "Symbol",
    "SymbolTable",
    "SymbolType",
    "SymbolAccess",
    "SymbolHitType",
]
