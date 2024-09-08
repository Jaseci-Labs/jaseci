"""Access check pass for the Jac compiler.

This pass checks for access to attributes in the Jac language.
"""

from typing import Optional

import jaclang.compiler.absyntree as ast
from jaclang.compiler.constant import SymbolAccess
from jaclang.compiler.passes import Pass
from jaclang.compiler.symtable import Symbol
from jaclang.settings import settings


class AccessCheckPass(Pass):
    """Jac Ast Access Check pass."""

    # NOTE: This method is a hacky way to detect if the drivied class is inherit from base class, it
    # doesn't work if the base class was provided as an expression (ex. obj Dri :module.Base: {...}).
    def is_class_inherited_from(
        self, dri_class: ast.Architype, base_class: ast.Architype
    ) -> bool:
        """Return true if the dri_class inherited from base_class."""
        if dri_class.base_classes is None:
            return False
        for expr in dri_class.base_classes.items:
            if not isinstance(expr, ast.Name):
                continue
            if not isinstance(expr.name_of, ast.Architype):
                continue  # Unlikely.
            if expr.name_of == base_class:
                return True
            if self.is_class_inherited_from(expr.name_of, base_class):
                return True
        return False

    def report_error(self, message: str, node: Optional[ast.AstNode] = None) -> None:
        """Report error message related to illegal access of attributes and objects."""
        self.error(message, node)

    def exit_node(self, node: ast.AstNode) -> None:  # TODO: Move to debug pass
        """Exit node."""
        super().exit_node(node)
        if (
            settings.lsp_debug
            and isinstance(node, ast.NameAtom)
            and not node.sym
            and not node.parent_of_type(ast.Module).is_raised_from_py
            and not (
                node.sym_name == "py"
                and node.parent
                and isinstance(node.parent.parent, ast.Import)
            )
        ):
            self.warning(f"Name {node.sym_name} not present in symbol table")

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
        if isinstance(node.name_of, (ast.Ability, ast.Architype, ast.Enum)):
            return

        # Get the context to check the access.
        curr_class: Optional[ast.Architype] = Pass.find_parent_of_type(
            node, ast.Architype
        )
        curr_module: Optional[ast.Module] = Pass.find_parent_of_type(node, ast.Module)
        if curr_module is None:
            return

        # Note that currently we can only check for name + symbols, because expressions are not associated with the
        # typeinfo thus they don't have a symbol. In the future the name nodes will become expression nodes.
        if not isinstance(node.sym, Symbol):
            return

        # Public symbols are fine.
        if node.sym.access == SymbolAccess.PUBLIC:
            return

        # Note that from bellow the access is either private or protected.
        is_portect = node.sym.access == SymbolAccess.PROTECTED
        access_type = "protected" if is_portect else "private"

        # The class we're currently in (None if we're not inside any).
        sym_owner: ast.AstNode = node.sym.parent_tab.owner

        # If the symbol belongs to a class, we need to check if the access used properly
        # within the class and in it's inherited classes.
        if isinstance(sym_owner, ast.Architype):

            # Accessing a private/protected member within the top level scope illegal.
            if curr_class is None:
                return self.report_error(
                    f'Error: Invalid access of {access_type} member "{node.sym_name}".',
                    node,
                )

            if curr_class != node.sym.parent_tab.owner:
                if not is_portect:  # private member accessed in a different class.
                    return self.report_error(
                        f'Error: Invalid access of {access_type} member "{node.sym_name}".',
                        node,
                    )
                else:  # Accessing a protected member, check we're in an inherited class.
                    if not self.is_class_inherited_from(curr_class, sym_owner):
                        return self.report_error(
                            f'Error: Invalid access of {access_type} member "{node.sym_name}".',
                            node,
                        )

        elif isinstance(sym_owner, ast.Module) and sym_owner != curr_module:
            # Accessing a private/public member in a different module.
            return self.report_error(
                f'Error: Invalid access of {access_type} member "{node.sym_name}".',
                node,
            )
