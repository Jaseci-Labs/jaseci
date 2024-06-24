"""Jac Symbol Table."""

from __future__ import annotations

import ast as ast3
from typing import Optional, Sequence

import jaclang.compiler.absyntree as ast
from jaclang.compiler.constant import SymbolAccess, SymbolType
from jaclang.utils.treeprinter import dotgen_symtab_tree, print_symtab_tree


# Symbols can have mulitple definitions but resolves decl to be the
# first such definition in a given scope.
class Symbol:
    """Symbol."""

    def __init__(
        self,
        defn: ast.NameAtom,
        access: SymbolAccess,
        parent_tab: SymbolTable,
    ) -> None:
        """Initialize."""
        self.defn: list[ast.NameAtom] = [defn]
        self.uses: list[ast.NameAtom] = []
        defn.sym = self
        self.access: SymbolAccess = access
        self.parent_tab = parent_tab

    @property
    def decl(self) -> ast.NameAtom:
        """Get decl."""
        return self.defn[0]

    @property
    def sym_name(self) -> str:
        """Get name."""
        return self.decl.sym_name

    @property
    def sym_type(self) -> SymbolType:
        """Get sym_type."""
        return self.decl.sym_category

    @property
    def sym_dotted_name(self) -> str:
        """Return a full path of the symbol."""
        out = [self.defn[0].sym_name]
        current_tab: SymbolTable | None = self.parent_tab
        while current_tab is not None:
            out.append(current_tab.name)
            current_tab = current_tab.parent
        out.reverse()
        return ".".join(out)

    def add_defn(self, node: ast.NameAtom) -> None:
        """Add defn."""
        self.defn.append(node)
        node.sym = self

    def add_use(self, node: ast.NameAtom) -> None:
        """Add use."""
        self.uses.append(node)
        node.sym = self

    def __repr__(self) -> str:
        """Repr."""
        return f"Symbol({self.sym_name}, {self.sym_type}, {self.access}, {self.defn})"


class SymbolTable:
    """Symbol Table."""

    def __init__(
        self, name: str, owner: ast.AstNode, parent: Optional[SymbolTable] = None
    ) -> None:
        """Initialize."""
        self.name = name
        self.owner = owner
        self.parent = parent
        self.kid: list[SymbolTable] = []
        self.tab: dict[str, Symbol] = {}
        self.inherit: list[SymbolTable] = []

    def get_parent(self) -> Optional[SymbolTable]:
        """Get parent."""
        return self.parent

    def lookup(self, name: str, deep: bool = True) -> Optional[Symbol]:
        """Lookup a variable in the symbol table."""
        if name in self.tab:
            return self.tab[name]
        for i in self.inherit:
            found = i.lookup(name, deep=False)
            if found:
                return found
        if deep and self.parent:
            return self.parent.lookup(name, deep)
        return None

    def insert(
        self,
        node: ast.AstSymbolNode,
        access_spec: Optional[ast.AstAccessNode] | SymbolAccess = None,
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
                defn=node.name_spec,
                access=(
                    access_spec
                    if isinstance(access_spec, SymbolAccess)
                    else access_spec.access_type if access_spec else SymbolAccess.PUBLIC
                ),
                parent_tab=self,
            )
        else:
            self.tab[node.sym_name].add_defn(node.name_spec)
        node.name_spec.sym = self.tab[node.sym_name]
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

    def inherit_sym_tab(self, target_sym_tab: SymbolTable) -> None:
        """Inherit symbol table."""
        for i in target_sym_tab.tab.values():
            self.def_insert(i.decl, access_spec=i.access)

    def def_insert(
        self,
        node: ast.AstSymbolNode,
        access_spec: Optional[ast.AstAccessNode] | SymbolAccess = None,
        single_decl: Optional[str] = None,
    ) -> Optional[Symbol]:
        """Insert into symbol table."""
        if node.sym and self == node.sym.parent_tab:
            return node.sym
        self.insert(node=node, single=single_decl is not None, access_spec=access_spec)
        self.update_py_ctx_for_def(node)
        return node.sym

    def chain_def_insert(self, node_list: list[ast.AstSymbolNode]) -> None:
        """Link chain of containing names to symbol."""
        if not node_list:
            return
        cur_sym_tab: SymbolTable | None = node_list[0].sym_tab
        node_list[-1].name_spec.py_ctx_func = ast3.Store
        if isinstance(node_list[-1].name_spec, ast.AstSymbolNode):
            node_list[-1].name_spec.py_ctx_func = ast3.Store

        node_list = node_list[:-1]  # Just performs lookup mappings of pre assign chain
        for i in node_list:
            cur_sym_tab = (
                lookup.decl.sym_tab
                if (
                    lookup := self.use_lookup(
                        i,
                        sym_table=cur_sym_tab,
                    )
                )
                else None
            )

    def use_lookup(
        self,
        node: ast.AstSymbolNode,
        sym_table: Optional[SymbolTable] = None,
    ) -> Optional[Symbol]:
        """Link to symbol."""
        if node.sym:
            return node.sym
        if not sym_table:
            sym_table = node.sym_tab
        if sym_table:
            lookup = sym_table.lookup(name=node.sym_name, deep=True)
            lookup.add_use(node.name_spec) if lookup else None
        return node.sym

    def chain_use_lookup(self, node_list: Sequence[ast.AstSymbolNode]) -> None:
        """Link chain of containing names to symbol."""
        if not node_list:
            return
        cur_sym_tab: SymbolTable | None = node_list[0].sym_tab
        for i in node_list:
            if cur_sym_tab is None:
                break
            cur_sym_tab = (
                lookup.decl.sym_tab
                if (
                    lookup := self.use_lookup(
                        i,
                        sym_table=cur_sym_tab,
                    )
                )
                else None
            )

    def update_py_ctx_for_def(self, node: ast.AstSymbolNode) -> None:
        """Update python context for definition."""
        node.name_spec.py_ctx_func = ast3.Store
        if isinstance(node, (ast.TupleVal, ast.ListVal)) and node.values:
            # Handling of UnaryExpr case for item is only necessary for
            # the generation of Starred nodes in the AST for examples
            # like `(a, *b) = (1, 2, 3, 4)`.
            def fix(item: ast.TupleVal | ast.ListVal | ast.UnaryExpr) -> None:
                if isinstance(item, ast.UnaryExpr):
                    if isinstance(item.operand, ast.AstSymbolNode):
                        item.operand.name_spec.py_ctx_func = ast3.Store
                elif isinstance(item, (ast.TupleVal, ast.ListVal)):
                    for i in item.values.items if item.values else []:
                        if isinstance(i, ast.AstSymbolNode):
                            i.name_spec.py_ctx_func = ast3.Store
                        elif isinstance(i, ast.AtomTrailer):
                            self.chain_def_insert(i.as_attr_list)
                        if isinstance(i, (ast.TupleVal, ast.ListVal, ast.UnaryExpr)):
                            fix(i)

            fix(node)

    def inherit_baseclasses_sym(self, node: ast.Architype | ast.Enum) -> None:
        """Inherit base classes symbol tables."""
        if node.base_classes:
            for base_cls in node.base_classes.items:
                if (
                    isinstance(base_cls, ast.AstSymbolNode)
                    and (found := self.use_lookup(base_cls))
                    and found
                ):
                    self.inherit.append(found.decl.sym_tab)
                    base_cls.name_spec.name_of = found.decl.name_of

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
