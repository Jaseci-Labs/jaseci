"""Symbol table tree build pass for Jaseci Ast.

This pass builds the symbol table tree for the Jaseci Ast. It also adds symbols
for globals, imports, architypes, and abilities declarations and definitions.
"""

import ast as ast3
import builtins
from typing import Optional, Sequence

import jaclang.compiler.absyntree as ast
from jaclang.compiler.constant import Tokens as Tok
from jaclang.compiler.passes import Pass
from jaclang.compiler.symtable import Symbol, SymbolTable


class SymTabPass(Pass):
    """Jac Ast build pass."""

    def before_pass(self) -> None:
        """Before pass."""
        self.unlinked: set[ast.AstSymbolNode] = set()  # Failed use lookups
        self.linked: set[ast.AstSymbolNode] = set()  # Successful use lookups

    def seen(self, node: ast.AstSymbolNode) -> bool:
        """Check if seen."""
        result = node in self.linked or node in self.unlinked
        if node.sym_link and not result:
            self.linked.add(node)
            return True
        return result

    def def_insert(
        self,
        node: ast.AstSymbolNode,
        access_spec: Optional[ast.AstAccessNode] = None,
        single_decl: Optional[str] = None,
        table_override: Optional[SymbolTable] = None,
    ) -> Optional[Symbol]:
        """Insert into symbol table."""
        table = table_override if table_override else node.sym_tab
        if self.seen(node) and node.sym_link and table == node.sym_link.parent_tab:
            return node.sym_link
        if (
            table
            and (
                table.insert(
                    node=node, single=single_decl is not None, access_spec=access_spec
                )
            )
            and single_decl
        ):
            # self.already_declared_err(
            #     name=node.sym_name,
            #     typ=single_decl if single_decl else "ICE",
            #     original=collide,
            # )
            pass  # TODO: Sort this out at some point
        node.py_ctx_func = ast3.Store
        if isinstance(node.sym_name_node, ast.AstSymbolNode):
            node.sym_name_node.py_ctx_func = ast3.Store
        if isinstance(node, (ast.TupleVal, ast.ListVal)) and node.values:

            # Handling of UnaryExpr case for item is only necessary for
            # the generation of Starred nodes in the AST for examples
            # like `(a, *b) = (1, 2, 3, 4)`.
            def fix(item: ast.TupleVal | ast.ListVal | ast.UnaryExpr) -> None:
                if isinstance(item, ast.UnaryExpr):
                    if isinstance(item.operand, ast.AstSymbolNode):
                        item.operand.py_ctx_func = ast3.Store
                elif isinstance(item, (ast.TupleVal, ast.ListVal)):
                    for i in item.values.items if item.values else []:
                        if isinstance(i, ast.AstSymbolNode):
                            i.py_ctx_func = ast3.Store
                        elif isinstance(i, ast.AtomTrailer):
                            self.chain_def_insert(self.unwind_atom_trailer(i))
                        if isinstance(i, (ast.TupleVal, ast.ListVal, ast.UnaryExpr)):
                            fix(i)

            fix(node)
        self.handle_hit_outcome(node)
        return node.sym_link

    def use_lookup(
        self,
        node: ast.AstSymbolNode,
        sym_table: Optional[SymbolTable] = None,
    ) -> Optional[Symbol]:
        """Link to symbol."""
        if self.seen(node):
            return node.sym_link
        if not sym_table:
            sym_table = node.sym_tab
        if sym_table:
            node.sym_link = (
                sym_table.lookup(name=node.sym_name, deep=True) if sym_table else None
            )
            # If successful lookup mark linked, add to table uses, and link others
            if node.sym_link:
                sym_table.uses.append(node)
        self.handle_hit_outcome(node)
        return node.sym_link

    def chain_def_insert(self, node_list: Sequence[ast.AstSymbolNode]) -> None:
        """Link chain of containing names to symbol."""
        if not node_list:
            return
        cur_sym_tab = node_list[0].sym_tab
        node_list[-1].py_ctx_func = ast3.Store
        if isinstance(node_list[-1].sym_name_node, ast.AstSymbolNode):
            node_list[-1].sym_name_node.py_ctx_func = ast3.Store

        node_list = node_list[:-1]  # Just performs lookup mappings of pre assign chain
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

    def chain_use_lookup(self, node_list: Sequence[ast.AstSymbolNode]) -> None:
        """Link chain of containing names to symbol."""
        if not node_list:
            return
        cur_sym_tab = node_list[0].sym_tab
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

    def unwind_atom_trailer(self, node: ast.AtomTrailer) -> list[ast.AstSymbolNode]:
        """Sub objects.

        target: ExprType,
        right: AtomType,
        is_scope_contained: bool,
        """
        left = node.right if isinstance(node.right, ast.AtomTrailer) else node.target
        right = node.target if isinstance(node.right, ast.AtomTrailer) else node.right
        trag_list: list[ast.AstSymbolNode] = (
            [right] if isinstance(right, ast.AstSymbolNode) else []
        )
        if not trag_list:
            self.ice("Something went very wrong with atom trailer not valid")
        while isinstance(left, ast.AtomTrailer) and left.is_attr:
            if isinstance(left.right, ast.AstSymbolNode):
                trag_list.insert(0, left.right)
            else:
                raise self.ice("Something went very wrong with atom trailer not valid")
            left = left.target
        if isinstance(left, ast.AstSymbolNode):
            trag_list.insert(0, left)
        return trag_list

    def handle_hit_outcome(
        self,
        node: ast.AstSymbolNode,
    ) -> None:
        """Handle outcome of lookup or insert."""
        # If successful lookup mark linked, add to table uses, and link others
        if node.sym_link:
            self.linked.add(node)
            if isinstance(node.sym_name_node, ast.AstSymbolNode):
                node.sym_name_node.sym_link = node.sym_link
        if not node.sym_link:
            # Mark nodes that were not successfully linked
            self.unlinked.add(node)
            if (
                isinstance(node.sym_name_node, ast.AstSymbolNode)
                and not node.sym_name_node.sym_link
            ):
                self.unlinked.add(node.sym_name_node)

    def already_declared_err(
        self,
        name: str,
        typ: str,
        original: ast.AstNode,
        other_nodes: Optional[list[ast.AstNode]] = None,
    ) -> None:
        """Already declared error."""
        err_msg = (
            f"Name used for {typ} '{name}' already declared at "
            f"{original.loc.mod_path}, line {original.loc.first_line}"
        )
        if other_nodes:
            for i in other_nodes:
                err_msg += f", also see {i.loc.mod_path}, line {i.loc.first_line}"
        self.warning(err_msg)


class SymTabBuildPass(SymTabPass):
    """Jac Symbol table build pass."""

    def before_pass(self) -> None:
        """Before pass."""
        super().before_pass()
        self.cur_sym_tab: list[SymbolTable] = []

    def push_scope(self, name: str, key_node: ast.AstNode, fresh: bool = False) -> None:
        """Push scope."""
        if fresh:
            self.cur_sym_tab.append(SymbolTable(name, key_node))
        else:
            self.cur_sym_tab.append(self.cur_scope().push_scope(name, key_node))

    def pop_scope(self) -> None:
        """Pop scope."""
        self.cur_sym_tab.pop()

    def cur_scope(self) -> SymbolTable:
        """Return current scope."""
        return self.cur_sym_tab[-1]

    def sync_node_to_scope(self, node: ast.AstNode) -> None:
        """Sync node to scope."""
        node.sym_tab = self.cur_scope()

    def enter_module(self, node: ast.Module) -> None:
        """Sub objects.

        name: str,
        doc: Token,
        body: Optional['Elements'],
        mod_path: str,
        is_imported: bool,
        """
        self.push_scope(node.name, node, fresh=True)
        self.sync_node_to_scope(node)
        for obj in dir(builtins):
            builtin = ast.Name(
                file_path=node.loc.mod_path,
                name=Tok.NAME,
                value=str(obj),
                line=0,
                col_start=0,
                col_end=0,
                pos_start=0,
                pos_end=0,
            )
            self.sync_node_to_scope(builtin)
            self.def_insert(builtin)

    def exit_module(self, node: ast.Module) -> None:
        """Sub objects.

        name: str,
        doc: Token,
        body: Optional['Elements'],
        mod_path: str,
        is_imported: bool,
        """
        self.pop_scope()
        if (
            isinstance(node.parent, ast.Module)
            and node
            in [
                node.parent.impl_mod,
                node.parent.test_mod,
            ]
            and node.sym_tab
        ):
            for v in node.sym_tab.tab.values():
                self.def_insert(v.decl, table_override=self.cur_scope())

    def enter_global_vars(self, node: ast.GlobalVars) -> None:
        """Sub objects.

        access: Optional[SubTag[Token]],
        assignments: SubNodeList[Assignment],
        is_frozen: bool,
        doc: Optional[Constant] = None,
        """
        self.sync_node_to_scope(node)

    def exit_global_vars(self, node: ast.GlobalVars) -> None:
        """Sub objects.

        access: Optional[SubTag[Token]],
        assignments: SubNodeList[Assignment],
        is_frozen: bool,
        doc: Optional[Constant] = None,
        """
        for i in self.get_all_sub_nodes(node, ast.Assignment):
            for j in i.target.items:
                if isinstance(j, ast.AstSymbolNode):
                    self.def_insert(j, access_spec=node, single_decl="global var")
                else:
                    self.ice("Expected name type for globabl vars")

    def enter_sub_tag(self, node: ast.SubTag) -> None:
        """Sub objects.

        tag: T,
        """
        self.sync_node_to_scope(node)

    def enter_sub_node_list(self, node: ast.SubNodeList) -> None:
        """Sub objects.

        items: list[T],
        """
        self.sync_node_to_scope(node)

    def enter_test(self, node: ast.Test) -> None:
        """Sub objects.

        name: Name,
        doc: Optional[Token],
        description: Token,
        body: CodeBlock,
        """
        self.sync_node_to_scope(node)

    def exit_test(self, node: ast.Test) -> None:
        """Sub objects.

        name: Name,
        doc: Optional[Token],
        description: Token,
        body: CodeBlock,
        """
        self.def_insert(node, single_decl="test")
        self.push_scope(node.name.value, node)
        self.sync_node_to_scope(node)
        self.pop_scope()

    def enter_module_code(self, node: ast.ModuleCode) -> None:
        """Sub objects.

        doc: Optional[Token],
        name: Optional[Name],
        body: CodeBlock,
        """
        # self.push_scope("module_code", node)
        self.sync_node_to_scope(node)

    def exit_module_code(self, node: ast.ModuleCode) -> None:
        """Sub objects.

        doc: Optional[Token],
        body: 'CodeBlock',
        """
        # self.pop_scope()

    def enter_py_inline_code(self, node: ast.PyInlineCode) -> None:
        """Sub objects.

        code: Token,
        """
        self.sync_node_to_scope(node)

    def enter_import(self, node: ast.Import) -> None:
        """Sub objects.

        lang: Name,
        path: ModulePath,
        alias: Optional[Name],
        items: Optional[ModuleItems],
        is_absorb: bool,
        sub_module: Optional[Module],
        """
        self.sync_node_to_scope(node)

    def exit_import(self, node: ast.Import) -> None:
        """Sub objects.

        lang: Name,
        path: ModulePath,
        alias: Optional[Name],
        items: Optional[ModuleItems],
        is_absorb: bool,
        sub_module: Optional[Module],
        """
        if not node.is_absorb:
            for i in node.items.items:
                self.def_insert(i, single_decl="import item")
        elif node.is_absorb and node.hint.tag.value == "jac":
            source = node.items.items[0]
            if (
                not isinstance(source, ast.ModulePath)
                or not source.sub_module
                or not source.sub_module.sym_tab
            ):
                self.error(
                    f"Module {node.from_loc.path_str if node.from_loc else 'from location'}"
                    f" not found to include *, or ICE occurred!"
                )
            else:
                for v in source.sub_module.sym_tab.tab.values():
                    self.def_insert(v.decl, table_override=self.cur_scope())

    def enter_module_path(self, node: ast.ModulePath) -> None:
        """Sub objects.

        path: Sequence[Token],
        alias: Optional[Name],
        sub_module: Optional[Module] = None,
        """
        self.sync_node_to_scope(node)

    def exit_module_path(self, node: ast.ModulePath) -> None:
        """Sub objects.

        path: Sequence[Token],
        alias: Optional[Name],
        sub_module: Optional[Module] = None,
        """
        if node.alias:
            self.def_insert(node.alias, single_decl="import")
        elif node.path and isinstance(node.path[0], ast.Name):
            self.def_insert(node.path[0])
        else:
            pass  # Need to support pythonic import symbols with dots in it

    def enter_module_item(self, node: ast.ModuleItem) -> None:
        """Sub objects.

        name: Name,
        alias: Optional[Token],
        body: Optional[AstNode],
        """
        self.sync_node_to_scope(node)

    def enter_architype(self, node: ast.Architype) -> None:
        """Sub objects.

        name: Name,
        arch_type: Token,
        doc: Optional[Token],
        decorators: Optional[Decorators],
        access: Optional[Token],
        base_classes: BaseClasses,
        body: Optional[ArchBlock],
        """
        self.sync_node_to_scope(node)
        self.def_insert(node, single_decl="architype")
        self.push_scope(node.name.value, node)
        self.sync_node_to_scope(node)

    def exit_architype(self, node: ast.Architype) -> None:
        """Sub objects.

        name: Name,
        arch_type: Token,
        doc: Optional[Token],
        decorators: Optional[Decorators],
        access: Optional[Token],
        base_classes: BaseClasses,
        body: Optional[ArchBlock],
        """
        self.pop_scope()

    def enter_arch_def(self, node: ast.ArchDef) -> None:
        """Sub objects.

        doc: Optional[Token],
        mod: Optional[DottedNameList],
        arch: ArchRef,
        body: ArchBlock,
        """
        self.sync_node_to_scope(node)
        self.def_insert(node, single_decl="arch def")
        self.push_scope(node.sym_name, node)
        self.sync_node_to_scope(node)

    def exit_arch_def(self, node: ast.ArchDef) -> None:
        """Sub objects.

        doc: Optional[Token],
        mod: Optional[DottedNameList],
        arch: ArchRef,
        body: ArchBlock,
        """
        self.pop_scope()

    def enter_ability(self, node: ast.Ability) -> None:
        """Sub objects.

        name_ref: Name | SpecialVarRef | ArchRef,
        is_func: bool,
        is_async: bool,
        is_static: bool,
        doc: Optional[Token],
        decorators: Optional[Decorators],
        access: Optional[Token],
        signature: Optional[FuncSignature | TypeSpec | EventSignature],
        body: Optional[CodeBlock],
        """
        self.sync_node_to_scope(node)
        self.def_insert(node, single_decl="ability")
        self.push_scope(node.sym_name, node)
        self.sync_node_to_scope(node)

    def exit_ability(self, node: ast.Ability) -> None:
        """Sub objects.

        name_ref: Name | SpecialVarRef | ArchRef,
        is_func: bool,
        is_async: bool,
        is_static: bool,
        doc: Optional[Token],
        decorators: Optional[Decorators],
        access: Optional[Token],
        signature: Optional[FuncSignature | TypeSpec | EventSignature],
        body: Optional[CodeBlock],
        """
        self.pop_scope()

    def enter_ability_def(self, node: ast.AbilityDef) -> None:
        """Sub objects.

        doc: Optional[Token],
        target: ArchRefChain,
        signature: FuncSignature | EventSignature,
        body: CodeBlock,
        """
        self.sync_node_to_scope(node)
        self.def_insert(node, single_decl="ability def")
        self.push_scope(node.sym_name, node)
        self.sync_node_to_scope(node)

    def exit_ability_def(self, node: ast.AbilityDef) -> None:
        """Sub objects.

        doc: Optional[Token],
        target: Optional[DottedNameList],
        ability: ArchRef,
        signature: FuncSignature | EventSignature,
        body: CodeBlock,
        """
        self.pop_scope()

    def enter_event_signature(self, node: ast.EventSignature) -> None:
        """Sub objects.

        event: Token,
        arch_tag_info: Optional[SubNodeList[TypeSpec]],
        return_type: Optional[SubTag[SubNodeList[TypeSpec]]],
        """
        self.sync_node_to_scope(node)

    def enter_arch_ref_chain(self, node: ast.ArchRefChain) -> None:
        """Sub objects.

        archs: list[ArchRef],
        """
        self.sync_node_to_scope(node)

    def enter_func_signature(self, node: ast.FuncSignature) -> None:
        """Sub objects.

        params: Optional['FuncParams'],
        return_type: Optional['TypeSpec'],
        """
        self.sync_node_to_scope(node)

    def enter_param_var(self, node: ast.ParamVar) -> None:
        """Sub objects.

        name: Name,
        unpack: Optional[Token],
        type_tag: 'TypeSpec',
        value: Optional[ExprType],
        """
        self.sync_node_to_scope(node)

    def enter_enum(self, node: ast.Enum) -> None:
        """Sub objects.

        name: Name,
        doc: Optional[Token],
        decorators: Optional['Decorators'],
        access: Optional[Token],
        base_classes: 'BaseClasses',
        body: Optional['EnumBlock'],
        """
        self.sync_node_to_scope(node)
        self.def_insert(node, single_decl="enum")
        self.push_scope(node.sym_name, node)
        self.sync_node_to_scope(node)

    def exit_enum(self, node: ast.Enum) -> None:
        """Sub objects.

        name: Name,
        doc: Optional[Token],
        decorators: Optional['Decorators'],
        access: Optional[Token],
        base_classes: 'BaseClasses',
        body: Optional['EnumBlock'],
        """
        self.pop_scope()

    def enter_enum_def(self, node: ast.EnumDef) -> None:
        """Sub objects.

        doc: Optional[Token],
        target: list[ArchRef],
        body: EnumBlock,
        """
        self.sync_node_to_scope(node)
        self.def_insert(node, single_decl="enum def")
        self.push_scope(node.sym_name, node)
        self.sync_node_to_scope(node)

    def exit_enum_def(self, node: ast.EnumDef) -> None:
        """Sub objects.

        doc: Optional[Token],
        enum: ArchRef,
        mod: Optional[DottedNameList],
        body: EnumBlock,
        """
        self.pop_scope()

    def enter_arch_has(self, node: ast.ArchHas) -> None:
        """Sub objects.

        doc: Optional[Token],
        is_static: bool,
        access: Optional[Token],
        vars: 'HasVarList',
        is_frozen: bool,
        """
        self.sync_node_to_scope(node)

    def enter_has_var(self, node: ast.HasVar) -> None:
        """Sub objects.

        name: Name,
        type_tag: 'TypeSpec',
        value: Optional[ExprType],
        """
        self.sync_node_to_scope(node)

    def enter_typed_ctx_block(self, node: ast.TypedCtxBlock) -> None:
        """Sub objects.

        type_ctx: TypeSpecList,
        body: CodeBlock,
        """
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_typed_ctx_block(self, node: ast.TypedCtxBlock) -> None:
        """Sub objects.

        type_ctx: TypeSpecList,
        body: CodeBlock,
        """
        self.pop_scope()

    def enter_if_stmt(self, node: ast.IfStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: 'CodeBlock',
        elseifs: Optional['ElseIfs'],
        else_body: Optional['ElseStmt'],
        """
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_if_stmt(self, node: ast.IfStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: 'CodeBlock',
        elseifs: Optional['ElseIfs'],
        else_body: Optional['ElseStmt'],
        """
        self.pop_scope()

    def enter_else_if(self, node: ast.ElseIf) -> None:
        """Sub objects.

        elseifs: list['IfStmt'],
        """
        self.push_scope("elif_stmt", node)
        self.sync_node_to_scope(node)

    def exit_else_if(self, node: ast.ElseIf) -> None:
        """Sub objects.

        elseifs: list['IfStmt'],
        """
        self.pop_scope()

    def enter_else_stmt(self, node: ast.ElseStmt) -> None:
        """Sub objects.

        body: 'CodeBlock',
        """
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_else_stmt(self, node: ast.ElseStmt) -> None:
        """Sub objects.

        body: 'CodeBlock',
        """
        self.pop_scope()

    def enter_expr_stmt(self, node: ast.ExprStmt) -> None:
        """Sub objects.

        expr: ExprType,
        """
        self.sync_node_to_scope(node)

    def enter_try_stmt(self, node: ast.TryStmt) -> None:
        """Sub objects.

        body: 'CodeBlock',
        excepts: Optional['ExceptList'],
        finally_body: Optional['FinallyStmt'],
        """
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_try_stmt(self, node: ast.TryStmt) -> None:
        """Sub objects.

        body: 'CodeBlock',
        excepts: Optional['ExceptList'],
        finally_body: Optional['FinallyStmt'],
        """
        self.pop_scope()

    def enter_except(self, node: ast.Except) -> None:
        """Sub objects.

        ex_type: ExprType,
        name: Optional[Token],
        body: 'CodeBlock',
        """
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_except(self, node: ast.Except) -> None:
        """Sub objects.

        ex_type: ExprType,
        name: Optional[Token],
        body: 'CodeBlock',
        """
        self.pop_scope()

    def enter_finally_stmt(self, node: ast.FinallyStmt) -> None:
        """Sub objects.

        body: 'CodeBlock',
        """
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_finally_stmt(self, node: ast.FinallyStmt) -> None:
        """Sub objects.

        body: 'CodeBlock',
        """
        self.pop_scope()

    def enter_iter_for_stmt(self, node: ast.IterForStmt) -> None:
        """Sub objects.

        iter: 'Assignment',
        condition: ExprType,
        count_by: ExprType,
        body: 'CodeBlock',
        """
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_iter_for_stmt(self, node: ast.IterForStmt) -> None:
        """Sub objects.

        iter: 'Assignment',
        condition: ExprType,
        count_by: ExprType,
        body: 'CodeBlock',
        """
        self.pop_scope()

    def enter_in_for_stmt(self, node: ast.InForStmt) -> None:
        """Sub objects.

        target: ExprType,
        is_async: bool,
        collection: ExprType,
        body: SubNodeList[CodeBlockStmt],
        else_body: Optional[ElseStmt],
        """
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_in_for_stmt(self, node: ast.InForStmt) -> None:
        """Sub objects.

        target: ExprType,
        is_async: bool,
        collection: ExprType,
        body: SubNodeList[CodeBlockStmt],
        else_body: Optional[ElseStmt],
        """
        self.pop_scope()

    def enter_name(self, node: ast.Name) -> None:
        """Sub objects.

        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        already_declared: bool,
        """
        self.sync_node_to_scope(node)

    def enter_while_stmt(self, node: ast.WhileStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: 'CodeBlock',
        """
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_while_stmt(self, node: ast.WhileStmt) -> None:
        """Sub objects.

        condition: ExprType,
        body: 'CodeBlock',
        """
        self.pop_scope()

    def enter_with_stmt(self, node: ast.WithStmt) -> None:
        """Sub objects.

        exprs: 'ExprAsItemList',
        body: 'CodeBlock',
        """
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_with_stmt(self, node: ast.WithStmt) -> None:
        """Sub objects.

        exprs: 'ExprAsItemList',
        body: 'CodeBlock',
        """
        self.pop_scope()

    def enter_expr_as_item(self, node: ast.ExprAsItem) -> None:
        """Sub objects.

        expr: ExprType,
        alias: Optional[ExprType],
        """
        self.sync_node_to_scope(node)

    def enter_raise_stmt(self, node: ast.RaiseStmt) -> None:
        """Sub objects.

        cause: Optional[ExprType],
        """
        self.sync_node_to_scope(node)

    def enter_assert_stmt(self, node: ast.AssertStmt) -> None:
        """Sub objects.

        condition: ExprType,
        error_msg: Optional[ExprType],
        """
        self.sync_node_to_scope(node)

    def enter_ctrl_stmt(self, node: ast.CtrlStmt) -> None:
        """Sub objects.

        ctrl: Token,
        """
        self.sync_node_to_scope(node)

    def enter_delete_stmt(self, node: ast.DeleteStmt) -> None:
        """Sub objects.

        target: ExprType,
        """
        self.sync_node_to_scope(node)

    def enter_report_stmt(self, node: ast.ReportStmt) -> None:
        """Sub objects.

        expr: ExprType,
        """
        self.sync_node_to_scope(node)

    def enter_return_stmt(self, node: ast.ReturnStmt) -> None:
        """Sub objects.

        expr: Optional[ExprType],
        """
        self.sync_node_to_scope(node)

    def enter_yield_expr(self, node: ast.YieldExpr) -> None:
        """Sub objects.

        expr: Optional[ExprType],
        """
        self.sync_node_to_scope(node)

    def enter_ignore_stmt(self, node: ast.IgnoreStmt) -> None:
        """Sub objects.

        target: ExprType,
        """
        self.sync_node_to_scope(node)

    def enter_visit_stmt(self, node: ast.VisitStmt) -> None:
        """Sub objects.

        vis_type: Optional[Token],
        target: ExprType,
        else_body: Optional['ElseStmt'],
        from_walker: bool,
        """
        self.sync_node_to_scope(node)

    def enter_revisit_stmt(self, node: ast.RevisitStmt) -> None:
        """Sub objects.

        hops: Optional[ExprType],
        else_body: Optional['ElseStmt'],
        from_walker: bool,
        """
        self.sync_node_to_scope(node)

    def enter_disengage_stmt(self, node: ast.DisengageStmt) -> None:
        """Sub objects.

        from_walker: bool,
        """
        self.sync_node_to_scope(node)

    def enter_await_expr(self, node: ast.AwaitExpr) -> None:
        """Sub objects.

        target: ExprType,
        """
        self.sync_node_to_scope(node)

    def enter_global_stmt(self, node: ast.GlobalStmt) -> None:
        """Sub objects.

        names: NameList,
        """
        self.sync_node_to_scope(node)

    def enter_non_local_stmt(self, node: ast.NonLocalStmt) -> None:
        """Sub objects.

        names: NameList,
        """
        self.sync_node_to_scope(node)

    def enter_assignment(self, node: ast.Assignment) -> None:
        """Sub objects.

        is_static: bool,
        target: 'AtomType',
        value: ExprType,
        mutable: bool,
        """
        self.sync_node_to_scope(node)

    def enter_binary_expr(self, node: ast.BinaryExpr) -> None:
        """Sub objects.

        left: ExprType,
        right: ExprType,
        op: Token | DisconnectOp | ConnectOp,
        """
        self.sync_node_to_scope(node)

    def enter_compare_expr(self, node: ast.CompareExpr) -> None:
        """Sub objects.

        left: Expr,
        rights: list[Expr],
        ops: list[Token],
        """
        self.sync_node_to_scope(node)

    def enter_if_else_expr(self, node: ast.IfElseExpr) -> None:
        """Sub objects.

        condition: 'BinaryExpr | IfElseExpr',
        value: ExprType,
        else_value: ExprType,
        """
        self.sync_node_to_scope(node)

    def enter_unary_expr(self, node: ast.UnaryExpr) -> None:
        """Sub objects.

        operand: ExprType,
        op: Token,
        """
        self.sync_node_to_scope(node)

    def enter_bool_expr(self, node: ast.BoolExpr) -> None:
        """Sub objects.

        value: Token,
        """
        self.sync_node_to_scope(node)

    def enter_lambda_expr(self, node: ast.LambdaExpr) -> None:
        """Sub objects.

        params: Optional['FuncParams'],
        return_type: Optional['TypeSpec'],
        body: ExprType,
        """
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_lambda_expr(self, node: ast.LambdaExpr) -> None:
        """Sub objects.

        params: Optional['FuncParams'],
        return_type: Optional['TypeSpec'],
        body: ExprType,
        """
        self.pop_scope()

    def enter_multi_string(self, node: ast.MultiString) -> None:
        """Sub objects.

        strings: list['Token | FString'],
        """
        self.sync_node_to_scope(node)

    def enter_list_val(self, node: ast.ListVal) -> None:
        """Sub objects.

        values: list[ExprType],
        """
        self.sync_node_to_scope(node)

    def enter_set_val(self, node: ast.SetVal) -> None:
        """Sub objects.

        values: list[ExprType],
        """
        self.sync_node_to_scope(node)

    def enter_tuple_val(self, node: ast.TupleVal) -> None:
        """Sub objects.

        first_expr: Optional[ExprType],
        exprs: Optional[ExprList],
        assigns: Optional[AssignmentList],
        """
        self.sync_node_to_scope(node)

    def enter_dict_val(self, node: ast.DictVal) -> None:
        """Sub objects.

        kv_pairs: list['KVPair'],
        """
        self.sync_node_to_scope(node)

    def enter_k_v_pair(self, node: ast.KVPair) -> None:
        """Sub objects.

        key: ExprType,
        value: ExprType,
        """
        self.sync_node_to_scope(node)

    def enter_k_w_pair(self, node: ast.KWPair) -> None:
        """Sub objects.

        key: ExprType,
        value: ExprType,
        """
        self.sync_node_to_scope(node)

    def enter_list_compr(self, node: ast.ListCompr) -> None:
        """Sub objects.

        compr: InnerCompr,
        """
        self.sync_node_to_scope(node)

    def enter_gen_compr(self, node: ast.GenCompr) -> None:
        """Sub objects.

        compr: InnerCompr,
        """
        self.sync_node_to_scope(node)

    def enter_set_compr(self, node: ast.SetCompr) -> None:
        """Sub objects.

        compr: InnerCompr,
        """
        self.sync_node_to_scope(node)

    def enter_inner_compr(self, node: ast.InnerCompr) -> None:
        """Sub objects.

        out_expr: ExprType,
        names: SubNodeList[Name],
        collection: ExprType,
        conditional: Optional[ExprType],
        """
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_inner_compr(self, node: ast.InnerCompr) -> None:
        """Sub objects.

        out_expr: ExprType,
        names: SubNodeList[Name],
        collection: ExprType,
        conditional: Optional[ExprType],
        """
        self.pop_scope()

    def enter_dict_compr(self, node: ast.DictCompr) -> None:
        """Sub objects.

        kv_pair: KVPair,
        names: SubNodeList[Name],
        collection: ExprType,
        conditional: Optional[ExprType],
        """
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_dict_compr(self, node: ast.DictCompr) -> None:
        """Sub objects.

        kv_pair: KVPair,
        names: SubNodeList[Name],
        collection: ExprType,
        conditional: Optional[ExprType],
        """
        self.pop_scope()

    def enter_atom_trailer(self, node: ast.AtomTrailer) -> None:
        """Sub objects.

        target: 'AtomType',
        right: 'IndexSlice | ArchRef | Token',
        null_ok: bool,
        """
        self.sync_node_to_scope(node)

    def enter_atom_unit(self, node: ast.AtomUnit) -> None:
        """Sub objects.

        value: AtomType | ExprType,
        is_paren: bool,
        is_null_ok: bool,
        """
        self.sync_node_to_scope(node)

    def enter_func_call(self, node: ast.FuncCall) -> None:
        """Sub objects.

        target: 'AtomType',
        params: Optional['ParamList'],
        """
        self.sync_node_to_scope(node)

    def enter_index_slice(self, node: ast.IndexSlice) -> None:
        """Sub objects.

        start: Optional[ExprType],
        stop: Optional[ExprType],
        is_range: bool,
        """
        self.sync_node_to_scope(node)

    def enter_arch_ref(self, node: ast.ArchRef) -> None:
        """Sub objects.

        name_ref: Name | SpecialVarRef,
        arch: Token,
        """
        self.sync_node_to_scope(node)

    def enter_special_var_ref(self, node: ast.SpecialVarRef) -> None:
        """Sub objects.

        var: Token,
        """
        self.sync_node_to_scope(node)

    def enter_edge_ref_trailer(self, node: ast.EdgeRefTrailer) -> None:
        """Sub objects.

        chain: list[Expr],
        edges_only: bool,
        """
        self.sync_node_to_scope(node)

    def enter_edge_op_ref(self, node: ast.EdgeOpRef) -> None:
        """Sub objects.

        filter_type: Optional[ExprType],
        filter_cond: Optional[FilterCompr],
        edge_dir: EdgeDir,
        from_walker: bool,
        """
        self.sync_node_to_scope(node)

    def enter_disconnect_op(self, node: ast.DisconnectOp) -> None:
        """Sub objects.

        filter_type: Optional[ExprType],
        filter_cond: Optional[FilterCompr],
        edge_dir: EdgeDir,
        from_walker: bool,
        """
        self.sync_node_to_scope(node)

    def enter_connect_op(self, node: ast.ConnectOp) -> None:
        """Sub objects.

        conn_type: Optional[ExprType],
        conn_assign: Optional[AssignmentList],
        edge_dir: EdgeDir,
        """
        self.sync_node_to_scope(node)

    def enter_filter_compr(self, node: ast.FilterCompr) -> None:
        """Sub objects.

        compares: list[BinaryExpr],
        """
        self.sync_node_to_scope(node)

    def enter_assign_compr(self, node: ast.AssignCompr) -> None:
        """Sub objects.

        assigns: list[KVPair],
        """
        self.sync_node_to_scope(node)

    def enter_f_string(self, node: ast.FString) -> None:
        """Sub objects.

        parts: list['Token | ExprType'],
        """
        self.sync_node_to_scope(node)

    def enter_match_stmt(self, node: ast.MatchStmt) -> None:
        """Sub objects.

        target: SubNodeList[ExprType],
        cases: list[MatchCase],
        """
        self.sync_node_to_scope(node)

    def enter_match_case(self, node: ast.MatchCase) -> None:
        """Sub objects.

        pattern: ExprType,
        guard: Optional[ExprType],
        body: SubNodeList[CodeBlockStmt],
        """
        self.push_scope(f"{node.__class__.__name__}", node)
        self.sync_node_to_scope(node)

    def exit_match_case(self, node: ast.MatchCase) -> None:
        """Sub objects.

        pattern: ExprType,
        guard: Optional[ExprType],
        body: SubNodeList[CodeBlockStmt],
        """
        self.pop_scope()

    def enter_match_or(self, node: ast.MatchOr) -> None:
        """Sub objects.

        list[MatchPattern],
        """
        self.sync_node_to_scope(node)

    def enter_match_as(self, node: ast.MatchAs) -> None:
        """Sub objects.

        name: NameType,
        pattern: MatchPattern,
        """
        self.sync_node_to_scope(node)

    def enter_match_wild(self, node: ast.MatchWild) -> None:
        """Sub objects."""
        self.sync_node_to_scope(node)

    def enter_match_value(self, node: ast.MatchValue) -> None:
        """Sub objects.

        value: ExprType,
        """
        self.sync_node_to_scope(node)

    def enter_match_singleton(self, node: ast.MatchSingleton) -> None:
        """Sub objects.

        value: Bool | Null,
        """
        self.sync_node_to_scope(node)

    def enter_match_sequence(self, node: ast.MatchSequence) -> None:
        """Sub objects.

        values: list[MatchPattern],
        """
        self.sync_node_to_scope(node)

    def enter_match_mapping(self, node: ast.MatchMapping) -> None:
        """Sub objects.

        values: list[MatchKVPair | MatchStar],
        """
        self.sync_node_to_scope(node)

    def enter_match_k_v_pair(self, node: ast.MatchKVPair) -> None:
        """Sub objects.

        key: MatchPattern | NameType,
        value: MatchPattern,
        """
        self.sync_node_to_scope(node)

    def enter_match_star(self, node: ast.MatchStar) -> None:
        """Sub objects.

        name: NameType,
        is_list: bool,
        """
        self.sync_node_to_scope(node)

    def enter_match_arch(self, node: ast.MatchArch) -> None:
        """Sub objects.

        name: NameType,
        arg_patterns: Optional[SubNodeList[MatchPattern]],
        kw_patterns: Optional[SubNodeList[MatchKVPair]],
        """
        self.sync_node_to_scope(node)

    def enter_token(self, node: ast.Token) -> None:
        """Sub objects.

        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        self.sync_node_to_scope(node)

    def enter_float(self, node: ast.Float) -> None:
        """Sub objects.

        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        self.sync_node_to_scope(node)

    def enter_int(self, node: ast.Int) -> None:
        """Sub objects.

        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        self.sync_node_to_scope(node)

    def enter_string(self, node: ast.String) -> None:
        """Sub objects.

        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        self.sync_node_to_scope(node)

    def enter_bool(self, node: ast.Bool) -> None:
        """Sub objects.

        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        self.sync_node_to_scope(node)

    def enter_null(self, node: ast.Null) -> None:
        """Sub objects.

        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        self.sync_node_to_scope(node)

    def enter_ellipsis(self, node: ast.Ellipsis) -> None:
        """Sub objects.

        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        self.sync_node_to_scope(node)

    def enter_builtin_type(self, node: ast.BuiltinType) -> None:
        """Sub objects.

        name: str,
        value: str,
        line: int,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        typ: type,
        """
        self.sync_node_to_scope(node)

    def enter_semi(self, node: ast.Semi) -> None:
        """Sub objects."""
        self.sync_node_to_scope(node)

    def enter_comment_token(self, node: ast.CommentToken) -> None:
        """Sub objects."""
        self.sync_node_to_scope(node)
