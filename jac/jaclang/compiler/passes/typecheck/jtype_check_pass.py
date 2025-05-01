"""Semantic analysis for Jac language."""

from typing import Any, Optional

import jaclang.compiler.passes.typecheck.jtype as jtype
import jaclang.compiler.unitree as ast
from jaclang.compiler.passes import AstPass
from jaclang.compiler.passes.typecheck.semantic_msgs import JacSemanticMessages
from jaclang.settings import settings


SemanticErrorObject = tuple[JacSemanticMessages, ast.UniNode, dict[str, str]]


class SemanticAnalysisPass(AstPass):
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
        func_decl = node.parent_of_type(ast.Ability)
        sig_ret_type = self.prog.expr_type_handler.get_type(
            func_decl.signature.return_type
        )

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
        if isinstance(node.target, ast.Name):
            func_symbol = node.sym_tab.find_scope(node.target.name_spec.sym_name)
            if func_symbol:
                assert isinstance(func_symbol, ast.Ability)
                assert isinstance(func_symbol.signature, ast.FuncSignature)
                func_params = (
                    {a.sym_name: a for a in func_symbol.signature.params.items}
                    if func_symbol.signature.params
                    else {}
                )
                actual_params = node.params
                params_connected = []
                if (
                    actual_params
                    and len(func_params.keys()) == len(actual_params.items)
                ) or (len(func_params.keys()) == 0 and actual_params is None):
                    if len(func_params.keys()) == 0:
                        return

                    kw_items: bool = False
                    assert actual_params is not None
                    # TODO: check if a redefinition of a var is done using kwargs
                    for actual, formal in zip(
                        actual_params.items, func_params.values()
                    ):
                        if isinstance(actual, ast.KWPair):
                            kw_items = True

                        formal_type: jtype.JType
                        actual_type: jtype.JType
                        param_name: str

                        # No kw args parameter is seen till now
                        # Parameter is a positional argument parameter
                        if not kw_items:
                            assert not isinstance(actual, ast.KWPair)
                            actual_type = self.prog.expr_type_handler.get_type(actual)
                            formal_type = self.prog.expr_type_handler.get_type(
                                formal.name
                            )
                            param_name = formal.name.sym_name
                            params_connected.append(formal.name)

                        # KW Args parameter is seen before
                        # Parameter should be a kw args and if not then generate an error
                        # QA: Do we need to pop a syntax error here?
                        else:
                            if not isinstance(actual, ast.KWPair):
                                self.report_error(
                                    JacSemanticMessages.POSITIONAL_ARG_AFTER_KWARG
                                )
                                continue
                            else:
                                assert actual.key is not None
                                param_name = actual.key.sym_name
                                if param_name not in func_params:
                                    self.report_error(
                                        JacSemanticMessages.ARG_NAME_NOT_FOUND,
                                        param_name=param_name,
                                        arg_name=func_symbol.name_spec.sym_name,
                                    )
                                    continue
                                else:
                                    if func_params[param_name].name in params_connected:
                                        self.report_error(
                                            JacSemanticMessages.REPEATED_ARG,
                                            param_name=param_name,
                                        )
                                        continue
                                    params_connected.append(
                                        func_params[param_name].name
                                    )
                                    actual_type = self.prog.expr_type_handler.get_type(
                                        actual.value
                                    )
                                    formal_type = self.prog.expr_type_handler.get_type(
                                        func_params[param_name].name
                                    )

                        if not formal_type.is_assignable_from(actual_type):
                            self.report_error(
                                JacSemanticMessages.CONFLICTING_ARG_TYPE,
                                param_name=param_name,
                                formal_type=formal_type,
                                actual_type=actual_type,
                            )

                else:
                    passed_number = len(actual_params.items) if actual_params else 0
                    self.report_error(
                        JacSemanticMessages.PARAM_NUMBER_MISMATCH,
                        actual_number=len(func_params.items()),
                        passed_number=passed_number,
                    )
            else:
                # TODO: Here I depend on the AST matching, Is this correct?
                self.report_error(
                    JacSemanticMessages.UNDEFINED_FUNCTION_NAME,
                    func_name=node.target.name_spec.sym_name,
                )
        else:
            self.__debug_print(
                "func call target not in form of Name is not supported yet"
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
                if sym_type is None:
                    self.prog.expr_type_handler.set_type(target, value_type)
                # symbol has a type, check the type compatability
                elif not sym_type.is_assignable_from(value_type):
                    self.report_error(
                        JacSemanticMessages.CONFLICTING_VAR_TYPE,
                        val_type=value_type,
                        var_type=sym_type,
                    )
