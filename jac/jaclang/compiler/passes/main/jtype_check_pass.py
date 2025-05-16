"""Semantic analysis for Jac language."""

from typing import Any, Optional

import jaclang.compiler.jtyping as jtype
import jaclang.compiler.unitree as ast
from jaclang.compiler.passes import UniPass
from jaclang.settings import settings


class JTypeCheckPass(UniPass):
    """Jac pass for semantic analysis."""

    def before_pass(self) -> None:
        """Do setup pass vars."""  # noqa D403, D401
        # TODO: Change this to use the errors_had infrastructure
        if not settings.enable_jac_semantics:
            self.terminate()
        if self.ir_in.name == "builtins":
            self.terminate()
        return super().before_pass()

    def __debug_print(self, msg: str) -> None:
        if settings.debug_jac_typing:
            print("[JTypeCheckPass]", msg)

    #############
    # Abilities #
    #############
    def exit_return_stmt(self, node: ast.ReturnStmt) -> None:
        """Check the return var type across the annotated return type."""
        return_type = self.prog.type_resolver.get_type(node.expr)

        # if the ret_type is a JClass type then we need to convert it to a JClassInstance
        if isinstance(return_type, jtype.JClassType):
            return_type = jtype.JClassInstanceType(return_type)

        func_decl = node.parent_of_type(ast.Ability)
        sig_ret_type = self.prog.type_resolver.get_type(func_decl.name_spec)
        assert isinstance(sig_ret_type, jtype.JFunctionType)
        sig_ret_type = sig_ret_type.return_type

        if return_type and isinstance(sig_ret_type, jtype.JNoneType):
            self.log_warning("Ability has a return type however it's defined as None type")
        
        elif not sig_ret_type.can_assign_from(return_type):
            self.log_error(f"Ability have a return type {sig_ret_type} but got assigned a type {return_type}")

    #################
    # Ability calls #
    #################
    def exit_func_call(self, node: ast.FuncCall) -> None:
        """Check the vars used as actual parameters across the formal parameters."""
        
        assert isinstance(node.target, ast.NameAtom)
        assert node.target.name_spec.sym is not None
        assert isinstance(node.target.name_spec.sym.jtype, jtype.JFunctionType)

        callable_type = node.target.name_spec.sym.jtype
        func_params = {a.name: a.type for a in callable_type.parameters}

        actual_params = node.params
        actual_items = actual_params.items if actual_params else []

        kw_args_seen = False
        arg_count = 0
        
        for actual, formal in zip(actual_items, func_params.values()):
            arg_name = ""       
            
            if isinstance(actual, ast.Expr):
                assert kw_args_seen == False
                actual_type = self.prog.type_resolver.get_type(actual)
                arg_name = list(func_params.keys())[arg_count]
                arg_count += 1
            
            elif isinstance(actual, ast.KWPair):
                kw_args_seen = True
                actual_type = self.prog.type_resolver.get_type(actual.value)
                assert actual.key is not None
                arg_name = actual.key.sym_name
                formal = func_params[arg_name]
            
            if not formal.can_assign_from(actual_type):
                self.log_error(f"Error: Can't assign a value {actual_type} to a parameter '{arg_name}' of type {formal}")


    ##################################
    # Assignments & Var delcarations #
    ##################################
    def exit_assignment(self, node: ast.Assignment) -> None:
        """Set var type & check the value type across the var annotated type."""
        value = node.value

        # if no value is assigned then no need to do type check
        if not value:
            return
        
        value_type = self.prog.type_resolver.get_type(value)
        # handle multiple assignment targets
        for target in node.target.items:

            # check target expression types
            if isinstance(target, ast.FuncCall):
                self.log_error(f"Expression '{target.unparse()}' can't be assigned (not a valid ltype)")
                continue

            sym_type = self.prog.type_resolver.get_type(target)
            if not sym_type.can_assign_from(value_type):
                self.log_error(f"Error: Can't assign a value {value_type} to a {sym_type} object")

    # # The goal here is to fix the AtomTrailer symbols after the type annotations
    # # of first nodes in the atom trailers
    # def enter_atom_trailer(self, node: ast.AtomTrailer) -> None:
    #     """Fix missing symbols."""
    #     self.prune()
    #     # Get the symbol table where the node exists
    #     node_href = self.prog.mod.main.get_href_path(node).split(("."))[1:]
    #     current_symtab = self.prog.mod.main.sym_tab
    #     for i in node_href:
    #         current_symtab = current_symtab.find_scope(i)
    #         assert current_symtab is not None

    #     # Get the symbol table of the object that contains the needed field
    #     last_node: Optional[ast.AstSymbolNode] = None
    #     for atom_t_node in node.as_attr_list[:-1]:
    #         assert atom_t_node.sym is not None
    #         atom_t_node_jtype = self.prog.expr_type_handler.get_type(atom_t_node)
    #         if not isinstance(
    #             atom_t_node_jtype, (jtype.JClassInstanceType, jtype.JClassType)
    #         ):
    #             self.report_error(
    #                 JacSemanticMessages.FIELD_ACCESS_FROM_INVALID_TYPE,
    #                 expr=atom_t_node.unparse(),
    #                 expr_type=atom_t_node_jtype,
    #             )
    #             return

    #         atom_t_node_jtype_name = atom_t_node_jtype.name
    #         current_symtab = current_symtab.find_scope(atom_t_node_jtype_name)
    #         if current_symtab is None and last_node is not None:
    #             self.report_error(
    #                 JacSemanticMessages.FIELD_NOT_FOUND,
    #                 field_name=atom_t_node.sym_name,
    #                 expr=last_node.unparse(),
    #                 expr_type=last_node.sym.jtype,
    #             )
    #             return
    #         last_node = atom_t_node

    #     needed_sym = current_symtab.lookup(node.as_attr_list[-1].sym_name)
    #     if needed_sym is None:
    #         self.report_error(
    #             JacSemanticMessages.FIELD_NOT_FOUND,
    #             field_name=node.as_attr_list[-1].sym_name,
    #             expr=node.as_attr_list[-2].unparse(),
    #             expr_type=self.prog.expr_type_handler.get_type(node.as_attr_list[-2]),
    #         )
    #         return
    #     else:
    #         node.as_attr_list[-1].sym = needed_sym