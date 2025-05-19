"""Semantic analysis for Jac language."""

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

        func_decl = node.parent_of_type(ast.Ability)
        sig_ret_type = self.prog.type_resolver.get_type(func_decl.name_spec)

        assert isinstance(sig_ret_type, jtype.JFunctionType)
        sig_ret_type = sig_ret_type.return_type

        if return_type and isinstance(sig_ret_type, jtype.JNoneType):
            self.log_warning(
                "Ability has a return type however it's defined as None type"
            )

        elif not sig_ret_type.can_assign_from(return_type):
            self.log_error(
                f"Ability have a return type {sig_ret_type} but got assigned a type {return_type}"
            )

    #################
    # Ability calls #
    #################
    def exit_func_call(self, node: ast.FuncCall) -> None:
        """Check the vars used as actual parameters across the formal parameters."""
        assert isinstance(node.target, (ast.NameAtom, ast.AtomTrailer))

        if isinstance(node.target, ast.NameAtom) and node.target.name_spec.sym is None:
            self.__debug_print(
                f"Ignoring function call {node.unparse()}, no symbol linked to it"
            )
            return

        callable_type = self.prog.type_resolver.get_type(node.target)

        assert isinstance(callable_type, (jtype.JFunctionType, jtype.JClassType))

        if isinstance(callable_type, jtype.JClassType):
            callable_type = callable_type.get_constrcutor()

        func_params = {a.name: a.type for a in callable_type.parameters}

        actual_params = node.params
        actual_items = actual_params.items if actual_params else []

        kw_args_seen = False
        arg_count = 0

        for actual, formal in zip(actual_items, func_params.values()):
            arg_name = ""

            if isinstance(actual, ast.Expr):
                assert kw_args_seen is False
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
                self.log_error(
                    f"Error: Can't assign a value {actual_type} to a parameter '{arg_name}' of type {formal}"
                )

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
                self.log_error(
                    f"Expression '{target.unparse()}' can't be assigned (not a valid ltype)"
                )
                continue

            sym_type = self.prog.type_resolver.get_type(target)
            if not sym_type.can_assign_from(value_type):
                self.log_error(
                    f"Error: Can't assign a value {value_type} to a {sym_type} object"
                )

    #####################
    ### Atom Trailers ###
    #####################
    def enter_atom_trailer(self, node: ast.AtomTrailer) -> None:
        """
        Resolve and validates chaine attribute accesses (e.g., a.b.c) in the AST.

        This method performs static analysis on a sequence of attribute accesses by:
        1. Resolving the type of the base expression.
        2. Walking through each attribute in the chain.
        3. Verifying that each attribute exists on the current type.
        4. Updating the AST with the resolved symbol information for each attribute.

        Args:
            node (ast.AtomTrailer): The AST node representing a chain of attribute accesses.

        Logs errors if:
            - Any intermediate type in the chain is not a class or instance type.
            - A requested attribute does not exist on the current type.
        """
        self.prune()  # prune the traversal into the atom trailer.

        nodes = node.as_attr_list
        first_item_type = self.prog.type_resolver.get_type(
            nodes[0]
        )  # Resolve type of base object.

        last_node_type: jtype.JClassInstanceType | jtype.JClassType
        next_type: jtype.JType = first_item_type

        # Iterate through each attribute in the chain (excluding the first base object).
        for n in nodes[1:]:
            # Ensure the current type can have members.
            if not isinstance(next_type, (jtype.JClassInstanceType, jtype.JClassType)):
                self.log_error(
                    f"Can't access a field from an object of type {first_item_type}"
                )
                return
            else:
                last_node_type = next_type

            node_name = n.sym_name
            member = last_node_type.get_member(
                node_name
            )  # Try to fetch the member from the current type.

            if member is None:
                # Attribute doesn't exist; log an error with context.
                self.log_error(
                    f"No member called '{node_name}' in {last_node_type} object",
                    node_override=n,
                )
                break
            else:
                # Update type for the next iteration and store the resolved symbol.
                next_type = member.type
                n.name_spec.sym = member.decl
