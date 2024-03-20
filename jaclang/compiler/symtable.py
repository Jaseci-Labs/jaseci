"""Jac Symbol Table."""

from __future__ import annotations

from enum import Enum
from typing import Optional, TYPE_CHECKING

from jaclang.utils.treeprinter import dotgen_symtab_tree, print_symtab_tree


if TYPE_CHECKING:
    import jaclang.compiler.absyntree as ast


class SymbolType(Enum):
    """Symbol types."""

    MODULE = "module"  # LSP: Module
    MOD_VAR = "mod_var"  # LSP: Variable
    VAR = "var"  # LSP: Variable
    IMM_VAR = "immutable"  # LSP: Constant
    ABILITY = "ability"  # LSP: Function
    OBJECT_ARCH = "object"  # LSP: Class
    NODE_ARCH = "node"  # LSP: Class
    EDGE_ARCH = "edge"  # LSP: Class
    WALKER_ARCH = "walker"  # LSP: Class
    ENUM_ARCH = "enum"  # LSP: Enum
    TEST = "test"  # LSP: Function
    TYPE = "type"  # LSP: TypeParameter
    IMPL = "impl"  # LSP: Interface or Property
    HAS_VAR = "field"  # LSP: Field
    METHOD = "method"  # LSP: Method
    CONSTRUCTOR = "constructor"  # LSP: Constructor
    ENUM_MEMBER = "enum_member"  # LSP: EnumMember
    NUMBER = "number"  # LSP: Number
    STRING = "string"  # LSP: String
    BOOL = "bool"  # LSP: Boolean
    SEQUENCE = "sequence"  # LSP: Array
    NULL = "null"  # LSP: Null

    def __str__(self) -> str:
        """Stringify."""
        return self.value


class SymbolInfo:
    """Symbol Info."""

    def __init__(self, typ: str = "NoType") -> None:  # noqa: ANN401
        """Initialize."""
        self.typ = typ
        self.typ_sym_table: Optional[SymbolTable] = None


class SymbolAccess(Enum):
    """Symbol types."""

    PRIVATE = "private"
    PUBLIC = "public"
    PROTECTED = "protected"

    def __str__(self) -> str:
        """Stringify."""
        return self.value


# Symbols can have mulitple definitions but resolves decl to be the
# first such definition in a given scope.
class Symbol:
    """Symbol."""

    def __init__(
        self,
        defn: ast.AstSymbolNode,
        access: SymbolAccess,
        parent_tab: SymbolTable,
        typ: Optional[type] = None,
    ) -> None:
        """Initialize."""
        self.typ = typ
        self.defn: list[ast.AstSymbolNode] = [defn]
        defn.sym_link = self
        self.access = access
        self.parent_tab = parent_tab

    @property
    def decl(self) -> ast.AstSymbolNode:
        """Get decl."""
        return self.defn[0]

    @property
    def sym_name(self) -> str:
        """Get name."""
        return self.decl.sym_name

    @property
    def sym_type(self) -> SymbolType:
        """Get sym_type."""
        return self.decl.sym_type

    def add_defn(self, node: ast.AstSymbolNode) -> None:
        """Add defn."""
        self.defn.append(node)
        node.sym_link = self

    def __repr__(self) -> str:
        """Repr."""
        return (
            f"Symbol({self.sym_name}, {self.sym_type}, {self.access}, "
            f"{self.typ}, {self.defn})"
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
        self.uses: list[ast.AstSymbolNode] = []

    def has_parent(self) -> bool:
        """Check if has parent."""
        return self.parent != self

    def get_parent(self) -> SymbolTable:
        """Get parent."""
        if self.parent == self:
            raise Exception("No parent")
        return self.parent

    def lookup(self, name: str, deep: bool = True) -> Optional[Symbol]:
        """Lookup a variable in the symbol table."""
        if name in self.tab:
            return self.tab[name]
        if deep and self.has_parent():
            return self.get_parent().lookup(name, deep)
        return None

    def insert(
        self,
        node: ast.AstSymbolNode,
        access_spec: Optional[ast.AstAccessNode] = None,
        single: bool = False,
    ) -> Optional[ast.AstNode]:
        """Set a variable in the symbol table.

        Returns original symbol as collision if single check fails, none otherwise.
        Also updates node.sym to create pointer to symbol.
        """
        collision = (
            self.tab[node.sym_name].defn[-1]
            if single and node.sym_name in self.tab
            else None
        )
        if node.sym_name not in self.tab:
            self.tab[node.sym_name] = Symbol(
                defn=node,
                access=access_spec.access_type if access_spec else SymbolAccess.PUBLIC,
                parent_tab=self,
            )
        else:
            self.tab[node.sym_name].add_defn(node)
        node.sym_link = self.tab[node.sym_name]
        return collision

    def find_scope(self, name: str) -> Optional[SymbolTable]:
        """Find a scope in the symbol table."""
        for k in self.kid:
            if k.name == name:
                return k
        return None

    def push_scope(self, name: str, key_node: ast.AstNode) -> SymbolTable:
        """Push a new scope onto the symbol table."""
        self.kid.append(SymbolTable(name, key_node, self))
        return self.kid[-1]

    def pp(self, depth: Optional[int] = None) -> str:
        """Pretty print."""
        return print_symtab_tree(root=self, depth=depth)

    def dotgen(self) -> str:
        """Generate dot graph for sym table."""
        return dotgen_symtab_tree(self)

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
]
