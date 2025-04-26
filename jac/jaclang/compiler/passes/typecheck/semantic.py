from typing import Any, Optional

import jaclang.compiler.absyntree as ast
import jaclang.compiler.passes.typecheck.type as jtype
from jaclang.compiler.passes import Pass
from jaclang.compiler.passes.typecheck.expr_type import JacExpressionType
from jaclang.compiler.passes.typecheck.semantic_msgs import JacSemanticMessages
from jaclang.settings import settings


class SemanticAnalysisPass(Pass):

    def before_pass(self) -> None:
        # TODO: Change this to use the errors_had infrastructure
        self.expr_check = JacExpressionType()
        self.semantic_errors: list[
            tuple[JacSemanticMessages, ast.AstNode, dict[str, str]]
        ] = []
        self.semantic_warning: list[
            tuple[JacSemanticMessages, ast.AstNode, dict[str, str]]
        ] = []
        return super().before_pass()

    def report_error(
        self,
        msg: JacSemanticMessages,
        node_override: Optional[ast.AstNode] = None,
        **fmt_args: Any,  # noqa ANN401
    ) -> None:
        """Generate Semantic error message."""
        node = self.cur_node if node_override is None else node_override
        self.semantic_errors.append((msg, node, fmt_args))
        formatted_msg = msg.value.format(**fmt_args)
        return self.error(f"[JAC] {formatted_msg}", node_override)

    def report_warning(
        self,
        msg: JacSemanticMessages,
        node_override: Optional[ast.AstNode] = None,
        **fmt_args: Any,  # noqa ANN401
    ) -> None:
        """Generate Semantic warning message."""
        node = self.cur_node if node_override is None else node_override
        self.semantic_warning.append((msg, node, fmt_args))
        formatted_msg = msg.value.format(**fmt_args)
        return self.warning(f"[JAC] {formatted_msg}", node_override)

    def __debug_print(self, msg: str) -> None:
        if settings.jac_semantics:
            print("[SemanticAnalysisPass]", msg)

    #############
    # Abilities #
    #############
    def enter_ability(self, node: ast.Ability) -> None:
        """Set ability return type based on the type annotation."""
        # Check for return statements in case of functions with no return annotation
        ret_type = self.expr_check.get_type(node.signature.return_type)
        self.expr_check.set_type(node.name_spec, ret_type)
        if len(node.get_all_sub_nodes(ast.ReturnStmt)) == 0 and not isinstance(
            ret_type, jtype.JNoneType
        ):
            self.report_error(JacSemanticMessages.MISSING_RETURN_STATEMENT)
        # Assign the type of func params
        assert isinstance(node.signature, ast.FuncSignature)
        if node.signature.params:
            for param in node.signature.params.items:
                type_annotation = self.expr_check.get_type(
                    param.type_tag.tag if param.type_tag else None
                )
                self.expr_check.set_type(param.name, type_annotation)

    def enter_return_stmt(self, node: ast.ReturnStmt) -> None:
        """Check the return var type across the annotated return type."""
        return_type = self.expr_check.get_type(node.expr)
        func_decl = node.parent_of_type(ast.Ability)
        sig_ret_type = self.expr_check.get_type(func_decl.signature.return_type)

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
                assert isinstance(func_symbol.owner, ast.Ability)
                assert isinstance(func_symbol.owner.signature, ast.FuncSignature)
                func_params = (
                    {a.sym_name: a for a in func_symbol.owner.signature.params.items}
                    if func_symbol.owner.signature.params
                    else {}
                )
                actual_params = node.params
                params_connected = []
                if actual_params and len(func_params.keys()) == len(
                    actual_params.items
                ):
                    kw_items: bool = False
                    # TODO: check if a redefinition of a var is done using kwargs
                    for actual, formal in zip(
                        actual_params.items, func_params.values()
                    ):
                        if isinstance(actual, ast.KWPair):
                            kw_items = True

                        formal_type: jtype.JType
                        actual_type: jtype.JType

                        # No kw args parameter is seen till now
                        # Parameter is a positional argument parameter
                        if not kw_items:
                            assert not isinstance(actual, ast.KWPair)
                            actual_type = self.expr_check.get_type(actual)
                            formal_type = self.expr_check.get_type(formal.name)
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
                                        arg_name=func_symbol.name,
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
                                    actual_type = self.expr_check.get_type(actual.value)
                                    formal_type = self.expr_check.get_type(
                                        func_params[param_name].name
                                    )

                        if not formal_type.is_assignable_from(actual_type):
                            self.report_error(
                                JacSemanticMessages.CONFLICTING_ARG_TYPE,
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
        value_type = self.expr_check.get_type(value) if value else None
        type_annotation = node.type_tag.tag if node.type_tag else None

        # handle multiple assignment targets
        for target in node.target.items:
            sym_type = self.expr_check.get_type(target)

            # type annotation exists
            if type_annotation:
                # symbol doesn't have a type, assign its' type
                if sym_type is None:
                    sym_type = self.expr_check.get_type(type_annotation)
                    self.expr_check.set_type(target, sym_type)

                # symbol already has a type, need to check if the annotated type is the
                # same as current type
                else:
                    annotation_type = self.expr_check.get_type(type_annotation)
                    if type(sym_type) is not type(annotation_type):
                        self.report_error(
                            JacSemanticMessages.VAR_REDEFINITION,
                            var_name=target.unparse(),
                            new_type=annotation_type,
                        )

            # A value exists to the assignment
            if value_type:
                # symbol doesn't have type, assign the value type to be the symbol type
                if sym_type is None:
                    self.expr_check.set_type(target, value_type)
                # symbol has a type, check the type compatability
                elif not sym_type.is_assignable_from(value_type):
                    self.report_error(
                        JacSemanticMessages.CONFLICTING_VAR_TYPE,
                        val_type=value_type,
                        var_type=sym_type,
                    )
