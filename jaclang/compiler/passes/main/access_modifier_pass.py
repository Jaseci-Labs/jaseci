"""Access check pass for the Jac compiler.

This pass checks for access to attributes in the Jac language.
"""

from typing import Optional

import jaclang.compiler.absyntree as ast
from jaclang.compiler.constant import SymbolAccess, SymbolType
from jaclang.compiler.passes import Pass
from jaclang.compiler.symtable import Symbol
from jaclang.settings import settings


class AccessCheckPass(Pass):
    """Jac Ast Access Check pass."""

    def report_error(self, message: str, node: Optional[ast.AstNode] = None) -> None:
        """Report error message related to illegal access of attributes and objects."""
        self.error(message, node)

    def after_pass(self) -> None:
        """After pass."""
        pass

    def exit_node(self, node: ast.AstNode) -> None:
        """Exit node."""
        super().exit_node(node)
        if settings.lsp_debug and isinstance(node, ast.NameAtom) and not node.sym:
            self.warning(f"Name {node.sym_name} not present in symbol table")

    def access_register(
        self, node: ast.AstSymbolNode, acc_tag: Optional[SymbolAccess] = None
    ) -> None:
        """Access register."""

    def enter_global_vars(self, node: ast.GlobalVars) -> None:
        """Sub objects.

        access: Optional[SubTag[Token]],
        assignments: SubNodeList[Assignment],
        is_frozen: bool,
        """
        pass

    def enter_module(self, node: ast.Module) -> None:
        """Sub objects.

        name: str,
        doc: Token,
        body: Optional['Elements'],
        mod_path: str,
        is_imported: bool,
        """

    def enter_architype(self, node: ast.Architype) -> None:
        """Sub objects.

        name: Name,
        arch_type: Token,
        access: Optional[SubTag[Token]],
        base_classes: Optional[SubNodeList[Expr]],
        body: Optional[SubNodeList[ArchBlockStmt] | ArchDef],
        decorators: Optional[SubNodeList[Expr]] = None,
        """
        pass

    def enter_enum(self, node: ast.Enum) -> None:
        """Sub objects.

        name: Name,
        access: Optional[SubTag[Token]],
        base_classes: Optional[SubNodeList[Expr]],
        body: Optional[SubNodeList[EnumBlockStmt] | EnumDef],
        decorators: Optional[SubNodeList[Expr]] = None,
        """
        pass

    def enter_ability(self, node: ast.Ability) -> None:
        """Sub objects.

        name_ref: NameSpec,
        is_func: bool,
        is_async: bool,
        is_override: bool,
        is_static: bool,
        is_abstract: bool,
        access: Optional[SubTag[Token]],
        signature: Optional[FuncSignature | EventSignature],
        body: Optional[SubNodeList[CodeBlockStmt] | AbilityDef],
        decorators: Optional[SubNodeList[Expr]] = None,
        """
        pass

    def enter_sub_node_list(self, node: ast.SubNodeList) -> None:
        """Sub objects.

        items: list[T]
        """

    def enter_arch_has(self, node: ast.ArchHas) -> None:
        """Sub objects.

        is_static: bool,
        access: Optional[SubTag[Token]],
        vars: SubNodeList[HasVar],
        is_frozen: bool,
        """
        pass

    def enter_atom_trailer(self, node: ast.AtomTrailer) -> None:
        """Sub objects.

        access: Optional[SubTag[Token]],
        """
        pass

    def enter_func_call(self, node: ast.FuncCall) -> None:
        """Sub objects.

        target: Expr,
        params: Optional[SubNodeList[Expr | KWPair]],
        genai_call: Optional[FuncCall],
        kid: Sequence[AstNode],
        """
        pass

    def enter_name(self, node: ast.Name) -> None:
        """Sub objects.

        name: str,
        value: str,
        col_start: int,
        col_end: int,
        pos_start: int,
        pos_end: int,
        """
        # TODO: Enums are not considered at the moment, I'll need to test and add them bellow.

        # If the current node is a global variable's name there is no access, it's just the declaration.
        if Pass.find_parent_of_type(node, ast.GlobalVars) is not None:
            return

        # Class name, and ability name are declarations and there is no access here as well.
        if isinstance(node.name_of, (ast.Ability, ast.Architype)):
            return

        # Note that currently we can only check for name + symbols, because expressions are not associated with the
        # typeinfo thus they don't have a symbol. In the future the name nodes will become expression nodes.
        if not isinstance(node.sym, Symbol):
            # In an expression 'foo.bar', the name bar doesn't contains any symbols if 'foo' is a module.
            # In that case we'll manually get the module and check the access. This is one hacky way
            # and needs to be done properly in the future.
            if not (isinstance(node.parent, ast.AtomTrailer) and node.parent.is_attr):
                return

            access_obj = node.parent.target
            if not isinstance(access_obj, ast.Name) or access_obj.sym is None:
                return

            if access_obj.sym.sym_type == SymbolType.MODULE:
                curr_module: Optional[ast.Module] = Pass.find_parent_of_type(
                    node=node, typ=ast.Module
                )
                if curr_module is None:
                    return
                accessed_module: Optional[ast.Module] = None
                for mod_dep in curr_module.mod_deps.values():
                    if mod_dep.name == access_obj.sym.sym_name:
                        accessed_module = mod_dep
                        break
                else:
                    return

                symbol: Optional[Symbol] = accessed_module.sym_tab.lookup(node.value)
                if symbol is None:
                    # TODO: This is a symantic error, assuming that a non
                    # existing member access was reported by some other
                    # semantic analysis pass, as it's not the responsibility
                    # of the current pass.
                    return

                # Assuming toplevel things (class, vars, ability) cannot be protected.
                if symbol.access == SymbolAccess.PRIVATE:
                    self.report_error(
                        f"Error: Invalid access of private member of module '{accessed_module.name}'.",
                        node,
                    )

            # Not sure what else (except for module.member) can have a name
            # node without symbol, we're just returning here for now.
            return

        # Public symbols are fine.
        if node.sym.access == SymbolAccess.PUBLIC:
            return

        # Note that from bellow the access is either private or protected.
        is_portect = node.sym.access == SymbolAccess.PROTECTED
        access_type = "protected" if is_portect else "private"

        # Check if private member variable / ability is accessed outside of the class.
        if node.sym.sym_type in (SymbolType.HAS_VAR, SymbolType.ABILITY):

            curr_class: Optional[ast.Architype] = Pass.find_parent_of_type(
                node=node, typ=ast.Architype
            )
            member_type: str = (
                "variable" if node.sym.sym_type == SymbolType.HAS_VAR else "ability"
            )

            # Accessing a private member outside of a class.
            if curr_class is None:
                return self.report_error(
                    f"Error: Invalid access of {access_type} member {member_type} variable.",
                    node,
                )

            # Accessing a private member variable from a different or even inherited class.
            assert isinstance(node.sym.parent_tab.owner, ast.Architype)
            if curr_class != node.sym.parent_tab.owner:
                if is_portect:

                    # NOTE: This method is a hacky way to detect if the drivied class is inherit from base class, it
                    # doesn't work if the base class was provided as an expression (ex. obj Dri :module.Base: {...}).
                    # TODO: This function may be exists somewhere else (I cannot find) or else moved to somewhere
                    # common.
                    def is_class_inherited_from(
                        dri_class: ast.Architype, base_class: ast.Architype
                    ) -> bool:
                        if dri_class.base_classes is None:
                            return False
                        for expr in dri_class.base_classes.items:
                            if not isinstance(expr, ast.Name):
                                continue
                            if not isinstance(expr.name_of, ast.Architype):
                                continue  # Unlikely.
                            if expr.name_of == base_class:
                                return True
                            if is_class_inherited_from(expr.name_of, base_class):
                                return True
                        return False

                    if not is_class_inherited_from(
                        curr_class, node.sym.parent_tab.owner
                    ):
                        return self.report_error(
                            f"Error: Invalid access of {access_type} member {member_type}.",
                            node,
                        )
                else:
                    return self.report_error(
                        f"Error: Invalid access of {access_type} member {member_type}.",
                        node,
                    )
