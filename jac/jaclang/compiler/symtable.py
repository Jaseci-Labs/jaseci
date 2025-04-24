"""Jac Symbol Table."""

from __future__ import annotations

import ast as ast3
from typing import Optional, Sequence

import jaclang.compiler.unitree as uni
from jaclang.compiler.constant import SymbolAccess, SymbolType
from jaclang.utils.treeprinter import dotgen_symtab_tree, print_symtab_tree


# Symbols can have mulitple definitions but resolves decl to be the
# first such definition in a given scope.
class Symbol:
    """Symbol."""

    def __init__(
        self,
        defn: uni.NameAtom,
        access: SymbolAccess,
        parent_tab: UniScopeNode,
    ) -> None:
        """Initialize."""
        self.defn: list[uni.NameAtom] = [defn]
        self.uses: list[uni.NameAtom] = []
        defn.sym = self
        self.access: SymbolAccess = access
        self.parent_tab = parent_tab

    @property
    def decl(self) -> uni.NameAtom:
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
        current_tab: UniScopeNode | None = self.parent_tab
        while current_tab is not None:
            out.append(current_tab.nix_name)
            current_tab = current_tab.parent_scope
        out.reverse()
        return ".".join(out)

    @property
    def fetch_sym_tab(self) -> Optional[UniScopeNode]:
        """Get symbol table."""
        return self.parent_tab.find_scope(self.sym_name)

    def add_defn(self, node: uni.NameAtom) -> None:
        """Add defn."""
        self.defn.append(node)
        node.sym = self

    def add_use(self, node: uni.NameAtom) -> None:
        """Add use."""
        self.uses.append(node)
        node.sym = self

    def __repr__(self) -> str:
        """Repr."""
        return f"Symbol({self.sym_name}, {self.sym_type}, {self.access}, {self.defn})"


class UniScopeNode:
    """Symbol Table."""

    def __init__(
        self, name: str, owner: uni.UniNode, parent: Optional[UniScopeNode] = None
    ) -> None:
        """Initialize."""
        self.nix_name = name
        self.nix_owner = owner
        self.parent_scope = parent
        self.kid_scope: list[UniScopeNode] = []
        self.names_in_scope: dict[str, Symbol] = {}
        self.inherited_scope: list[InheritedSymbolTable] = []

    def get_type(self) -> SymbolType:
        """Get type."""
        if isinstance(self.nix_owner, uni.AstSymbolNode):
            return self.nix_owner.sym_category
        return SymbolType.VAR

    def get_parent(self) -> Optional[UniScopeNode]:
        """Get parent."""
        return self.parent_scope

    def lookup(self, name: str, deep: bool = True) -> Optional[Symbol]:
        """Lookup a variable in the symbol table."""
        if name in self.names_in_scope:
            return self.names_in_scope[name]
        for i in self.inherited_scope:
            found = i.lookup(name, deep=False)
            if found:
                return found
        if deep and self.parent_scope:
            return self.parent_scope.lookup(name, deep)
        return None

    def insert(
        self,
        node: uni.AstSymbolNode,
        access_spec: Optional[uni.AstAccessNode] | SymbolAccess = None,
        single: bool = False,
        force_overwrite: bool = False,
    ) -> Optional[uni.UniNode]:
        """Set a variable in the symbol table.

        Returns original symbol as collision if single check fails, none otherwise.
        Also updates node.sym to create pointer to symbol.
        """
        collision = (
            self.names_in_scope[node.sym_name].defn[-1]
            if single and node.sym_name in self.names_in_scope
            else None
        )
        if force_overwrite or node.sym_name not in self.names_in_scope:
            self.names_in_scope[node.sym_name] = Symbol(
                defn=node.name_spec,
                access=(
                    access_spec
                    if isinstance(access_spec, SymbolAccess)
                    else access_spec.access_type if access_spec else SymbolAccess.PUBLIC
                ),
                parent_tab=self,
            )
        else:
            self.names_in_scope[node.sym_name].add_defn(node.name_spec)
        node.name_spec.sym = self.names_in_scope[node.sym_name]
        return collision

    def find_scope(self, name: str) -> Optional[UniScopeNode]:
        """Find a scope in the symbol table."""
        for k in self.kid_scope:
            if k.nix_name == name:
                return k
        for k2 in self.inherited_scope:
            if k2.base_symbol_table.nix_name == name:
                return k2.base_symbol_table
        return None

    def push_kid_scope(self, name: str, key_node: uni.UniNode) -> UniScopeNode:
        """Push a new scope onto the symbol table."""
        self.kid_scope.append(UniScopeNode(name, key_node, self))
        return self.kid_scope[-1]

    def inherit_sym_tab(self, target_sym_tab: UniScopeNode) -> None:
        """Inherit symbol table."""
        for i in target_sym_tab.names_in_scope.values():
            self.def_insert(i.decl, access_spec=i.access)

    def def_insert(
        self,
        node: uni.AstSymbolNode,
        access_spec: Optional[uni.AstAccessNode] | SymbolAccess = None,
        single_decl: Optional[str] = None,
        force_overwrite: bool = False,
    ) -> Optional[Symbol]:
        """Insert into symbol table."""
        if node.sym and self == node.sym.parent_tab:
            return node.sym
        self.insert(
            node=node,
            single=single_decl is not None,
            access_spec=access_spec,
            force_overwrite=force_overwrite,
        )
        self.update_py_ctx_for_def(node)
        return node.sym

    def chain_def_insert(self, node_list: list[uni.AstSymbolNode]) -> None:
        """Link chain of containing names to symbol."""
        if not node_list:
            return
        cur_sym_tab: UniScopeNode | None = node_list[0].sym_tab
        node_list[-1].name_spec.py_ctx_func = ast3.Store
        if isinstance(node_list[-1].name_spec, uni.AstSymbolNode):
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
        node: uni.AstSymbolNode,
        sym_table: Optional[UniScopeNode] = None,
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

    def chain_use_lookup(self, node_list: Sequence[uni.AstSymbolNode]) -> None:
        """Link chain of containing names to symbol."""
        if not node_list:
            return
        cur_sym_tab: UniScopeNode | None = node_list[0].sym_tab
        for i in node_list:
            if cur_sym_tab is None:
                break
            lookup = self.use_lookup(i, sym_table=cur_sym_tab)
            if lookup:
                cur_sym_tab = lookup.decl.sym_tab

                # check if the symbol table name is not the same as symbol name
                # then try to find a child scope with the same name
                # This is used to get the scope in case of
                #      import:py math;
                #      b = math.floor(1.7);
                if cur_sym_tab.nix_name != i.sym_name:
                    t = cur_sym_tab.find_scope(i.sym_name)
                    if t:
                        cur_sym_tab = t
            else:
                cur_sym_tab = None

    def update_py_ctx_for_def(self, node: uni.AstSymbolNode) -> None:
        """Update python context for definition."""
        node.name_spec.py_ctx_func = ast3.Store
        if isinstance(node, (uni.TupleVal, uni.ListVal)) and node.values:
            # Handling of UnaryExpr case for item is only necessary for
            # the generation of Starred nodes in the AST for examples
            # like `(a, *b) = (1, 2, 3, 4)`.
            def fix(item: uni.TupleVal | uni.ListVal | uni.UnaryExpr) -> None:
                if isinstance(item, uni.UnaryExpr):
                    if isinstance(item.operand, uni.AstSymbolNode):
                        item.operand.name_spec.py_ctx_func = ast3.Store
                elif isinstance(item, (uni.TupleVal, uni.ListVal)):
                    for i in item.values.items if item.values else []:
                        if isinstance(i, uni.AstSymbolNode):
                            i.name_spec.py_ctx_func = ast3.Store
                        elif isinstance(i, uni.AtomTrailer):
                            self.chain_def_insert(i.as_attr_list)
                        if isinstance(i, (uni.TupleVal, uni.ListVal, uni.UnaryExpr)):
                            fix(i)

            fix(node)

    def inherit_baseclasses_sym(self, node: uni.Architype | uni.Enum) -> None:
        """Inherit base classes symbol tables."""
        if node.base_classes:
            for base_cls in node.base_classes.items:
                if (
                    isinstance(base_cls, uni.AstSymbolNode)
                    and (found := self.use_lookup(base_cls))
                    and found
                ):
                    found_tab = found.decl.sym_tab
                    inher_sym_tab = InheritedSymbolTable(
                        base_symbol_table=found_tab, load_all_symbols=True, symbols=[]
                    )
                    self.inherited_scope.append(inher_sym_tab)
                    base_cls.name_spec.name_of = found.decl.name_of

    def pp(self, depth: Optional[int] = None) -> str:
        """Pretty print."""
        return print_symtab_tree(root=self, depth=depth)

    def dotgen(self) -> str:
        """Generate dot graph for sym table."""
        return dotgen_symtab_tree(self)

    def __repr__(self) -> str:
        """Repr."""
        out = f"{self.nix_name} {super().__repr__()}:\n"
        for k, v in self.names_in_scope.items():
            out += f"    {k}: {v}\n"
        return out


__all__ = [
    "Symbol",
    "UniScopeNode",
    "SymbolType",
    "SymbolAccess",
]


class InheritedSymbolTable:

    def __init__(
        self,
        base_symbol_table: UniScopeNode,
        load_all_symbols: bool = False,  # This is needed for python imports
        symbols: Optional[list[str]] = None,
    ) -> None:
        """Initialize."""
        self.base_symbol_table: UniScopeNode = base_symbol_table
        self.load_all_symbols: bool = load_all_symbols
        self.symbols: list[str] = symbols if symbols else []

    def lookup(self, name: str, deep: bool = False) -> Optional[Symbol]:
        """Lookup a variable in the symbol table."""
        if self.load_all_symbols:
            return self.base_symbol_table.lookup(name, deep)
        else:
            if name in self.symbols:
                return self.base_symbol_table.lookup(name, deep)
            else:
                return None
