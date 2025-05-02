"""Semantic analysis for Jac language."""

from typing import Any, Optional

import jaclang.compiler.passes.typecheck.jtype as jtype
import jaclang.compiler.unitree as ast
from jaclang.compiler.passes import UniPass
from jaclang.compiler.passes.typecheck.semantic_msgs import JacSemanticMessages
from jaclang.settings import settings


SemanticErrorObject = tuple[JacSemanticMessages, ast.UniNode, dict[str, str]]


class SemanticAnalysisPass(UniPass):
    """Jac pass for semantic analysis."""

    def before_pass(self) -> None:
        """Do setup pass vars."""  # noqa D403, D401
        # TODO: Change this to use the errors_had infrastructure
        if not settings.enable_jac_semantics:
            self.terminate()
        return super().before_pass()

    def report_error(
        self,
        msg: JacSemanticMessages,
        node_override: Optional[ast.UniNode] = None,
        **fmt_args: Any,  # noqa ANN401
    ) -> None:
        """Generate Semantic error message."""
        node = self.cur_node if node_override is None else node_override
        self.prog.semantic_errors_had.append(
            (msg, node, {k: str(fmt_args[k]) for k in fmt_args})
        )
        formatted_msg = msg.value.format(**fmt_args)
        return self.log_error(f"[JAC] {formatted_msg}", node_override)

    def report_warning(
        self,
        msg: JacSemanticMessages,
        node_override: Optional[ast.UniNode] = None,
        **fmt_args: Any,  # noqa ANN401
    ) -> None:
        """Generate Semantic warning message."""
        node = self.cur_node if node_override is None else node_override
        self.prog.semantic_warnnings_had.append(
            (msg, node, {k: str(fmt_args[k]) for k in fmt_args})
        )
        formatted_msg = msg.value.format(**fmt_args)
        return self.log_warning(f"[JAC] {formatted_msg}", node_override)

    def __debug_print(self, msg: str) -> None:
        if settings.debug_jac_semantics:
            print("[SemanticAnalysisPass]", msg)

    #############
    # Abilities #
    #############
    def enter_return_stmt(self, node: ast.ReturnStmt) -> None:
        """Check the return var type across the annotated return type."""
        return_type = self.prog.expr_type_handler.get_type(node.expr)

        # if the ret_type is a JClass type then we need to convert it to a JClassInstance
        if isinstance(return_type, jtype.JClassType):
            return_type = jtype.JClassInstanceType(return_type)

        func_decl = node.parent_of_type(ast.Ability)
        sig_ret_type = self.prog.expr_type_handler.get_type(func_decl.name_spec)
        assert isinstance(sig_ret_type, jtype.JCallableType)
        sig_ret_type = sig_ret_type.return_type

        if return_type and isinstance(sig_ret_type, jtype.JNoneType):
            self.report_warning(JacSemanticMessages.RETURN_FOR_NONE_ABILITY)
        elif not sig_ret_type.is_assignable_from(return_type):
            self.report_error(
                JacSemanticMessages.CONFLICTING_RETURN_TYPE,
                actual_return_type=sig_ret_type,
                formal_return_type=return_type,
            )

    #################
    # Ability calls #
    #################
    def enter_func_call(self, node: ast.FuncCall) -> None:
        """Check the vars used as actual parameters across the formal parameters."""
        if not isinstance(node.target, ast.NameAtom):
            self.report_error(
                JacSemanticMessages.EXPR_NOT_CALLABLE, expr=node.unparse()
            )
            return

        if not isinstance(node.target, ast.Name):
            self.__debug_print(
                "func call target not in form of Name is not supported yet"
            )
            return

        current_symbol_table: Optional[ast.UniNode | ast.UniScopeNode] = node.sym_tab
        while current_symbol_table is not None and not isinstance(
            current_symbol_table, ast.ProgramModule
        ):
            assert isinstance(current_symbol_table, ast.UniScopeNode)
            func_symbol = current_symbol_table.find_scope(
                node.target.name_spec.sym_name
            )
            if func_symbol:
                break
            else:
                assert current_symbol_table.parent is not None
                current_symbol_table = current_symbol_table.parent

        if not func_symbol:
            self.report_error(
                JacSemanticMessages.UNDEFINED_FUNCTION_NAME,
                func_name=node.target.name_spec.sym_name,
            )
            return

        # Check if this is actually an ability or a class constructor
        if isinstance(func_symbol, ast.Architype):
            # Try to get the constructor
            symbol = func_symbol.sym_tab.lookup("__init__")
            func_symbol = symbol.fetch_sym_tab if symbol else None
            # if no constructor found then just check for number of params
            if not func_symbol:
                actual_items = node.params.items if node.params else []
                if len(actual_items) > 0:
                    self.report_error(
                        JacSemanticMessages.PARAM_NUMBER_MISMATCH,
                        actual_number=0,
                        passed_number=len(actual_items),
                    )
                return

        assert isinstance(func_symbol, ast.Ability)
        assert isinstance(func_symbol.signature, ast.FuncSignature)

        func_params = (
            {a.sym_name: a for a in func_symbol.signature.params.items}
            if func_symbol.signature.params
            else {}
        )

        actual_params = node.params
        formal_keys = list(func_params.keys())
        actual_items = actual_params.items if actual_params else []

        if len(formal_keys) != len(actual_items):
            self.report_error(
                JacSemanticMessages.PARAM_NUMBER_MISMATCH,
                actual_number=len(formal_keys),
                passed_number=len(actual_items),
            )
            return

        if not formal_keys:
            return  # No parameters expected or passed

        params_connected = []
        kw_items_seen = False

        for actual, formal in zip(actual_items, func_params.values()):
            if isinstance(actual, ast.KWPair):
                kw_items_seen = True

            if not kw_items_seen:
                if isinstance(actual, ast.KWPair):
                    self.report_error(JacSemanticMessages.POSITIONAL_ARG_AFTER_KWARG)
                    continue

                param_name = formal.name.sym_name
                actual_type = self.prog.expr_type_handler.get_type(actual)
                formal_type = self.prog.expr_type_handler.get_type(formal.name)

            else:
                if not isinstance(actual, ast.KWPair):
                    self.report_error(JacSemanticMessages.POSITIONAL_ARG_AFTER_KWARG)
                    continue

                assert actual.key is not None
                param_name = actual.key.sym_name
                if param_name not in func_params:
                    self.report_error(
                        JacSemanticMessages.ARG_NAME_NOT_FOUND,
                        param_name=param_name,
                        arg_name=func_symbol.name_spec.sym_name,
                    )
                    continue

                if func_params[param_name].name in params_connected:
                    self.report_error(
                        JacSemanticMessages.REPEATED_ARG,
                        param_name=param_name,
                    )
                    continue

                actual_type = self.prog.expr_type_handler.get_type(actual.value)
                formal_type = self.prog.expr_type_handler.get_type(
                    func_params[param_name].name
                )

            params_connected.append(
                func_params[param_name].name if kw_items_seen else formal.name
            )

            if not formal_type.is_assignable_from(actual_type):
                self.report_error(
                    JacSemanticMessages.CONFLICTING_ARG_TYPE,
                    param_name=param_name,
                    formal_type=formal_type,
                    actual_type=actual_type,
                )

    ##################################
    # Assignments & Var delcarations #
    ##################################
    def enter_assignment(self, node: ast.Assignment) -> None:
        """Set var type & check the value type across the var annotated type."""
        value = node.value
        value_type = self.prog.expr_type_handler.get_type(value) if value else None

        # handle multiple assignment targets
        for target in node.target.items:
            # check target expression types
            if isinstance(target, ast.FuncCall):
                self.report_error(
                    JacSemanticMessages.ASSIGN_TO_RTYPE, expr=target.unparse()
                )
                continue

            sym_type = self.prog.expr_type_handler.get_type(target)

            # A value exists to the assignment
            if value_type:
                # symbol doesn't have type, assign the value type to be the symbol type
                if isinstance(sym_type, jtype.JNoType):
                    self.prog.expr_type_handler.set_type(target, value_type)
                # symbol has a type, check the type compatability
                elif not sym_type.is_assignable_from(value_type):
                    self.report_error(
                        JacSemanticMessages.CONFLICTING_VAR_TYPE,
                        val_type=value_type,
                        var_type=sym_type,
                    )
