"""JType collect pass.

This pass is resbponsible for annotating jtype object
using type annotations in the code.
"""

from typing import Any, Optional

import jaclang.compiler.passes.typecheck.jtype as jtype
import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import UniPass
from jaclang.compiler.passes.typecheck.semantic_msgs import JacSemanticMessages
from jaclang.settings import settings


class JTypeAnnotatePass(UniPass):
    """Populate type annotations to symbols."""

    def report_error(
        self,
        msg: JacSemanticMessages,
        node_override: Optional[uni.UniNode] = None,
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
        node_override: Optional[uni.UniNode] = None,
        **fmt_args: Any,  # noqa ANN401
    ) -> None:
        """Generate Semantic warning message."""
        node = self.cur_node if node_override is None else node_override
        self.prog.semantic_warnnings_had.append(
            (msg, node, {k: str(fmt_args[k]) for k in fmt_args})
        )
        formatted_msg = msg.value.format(**fmt_args)
        return self.log_warning(f"[JAC] {formatted_msg}", node_override)

    def before_pass(self) -> None:
        """Do setup pass vars."""  # noqa D403, D401
        if not settings.enable_jac_semantics:
            self.terminate()

    def enter_assignment(self, node: uni.Assignment) -> None:
        """Propagate type annotations for variable declarations."""
        # Resolve the declared type from the annotation, or default to no type
        type_annotation = (
            self.prog.expr_type_handler.get_type(node.type_tag.tag)
            if node.type_tag
            else jtype.JNoType()
        )

        # if the annotation is a JClass type then we need to convert it to a JClassInstance
        if isinstance(type_annotation, jtype.JClassType):
            type_annotation = jtype.JClassInstanceType(type_annotation)

        # Iterate over each target in the assignment (e.g., `x` in `x: int = 5`)
        for target in node.target.items:
            if isinstance(target, uni.Name):
                assert target.sym is not None

                # If the current type is unknown or compatible with the declared one, set it
                if isinstance(target.sym.jtype, (type(type_annotation), jtype.JNoType)):
                    self.prog.expr_type_handler.set_type(target, type_annotation)

                # If there’s a type mismatch, issue a redefinition warning
                elif not isinstance(type_annotation, jtype.JNoType):
                    self.report_warning(
                        JacSemanticMessages.VAR_REDEFINITION,
                        var_name=target.sym_name,
                        new_type=type_annotation,
                    )

            # If the target is not a simple name and a type annotation is present, error
            elif not isinstance(type_annotation, jtype.JNoType):
                self.report_error(
                    JacSemanticMessages.UNSUPPORTED_TYPE_ANNOTATION,
                    expr=target.unparse(),
                )

    def enter_ability(self, node: uni.Ability) -> None:
        """Process a function/ability definition.

        - Sets the return type
            - convert JClassType return type to JClassInstanceType
            - TODO: Need to check how to support returning the actual class
        - Validates presence of return statements when required
        - Sets parameter types based on annotations
        """
        # Get and set the declared return type of the ability
        ret_type = self.prog.expr_type_handler.get_type(node.signature.return_type)

        # if the ret_type is a JClass type then we need to convert it to a JClassInstance
        if isinstance(ret_type, jtype.JClassType):
            ret_type = jtype.JClassInstanceType(ret_type)

        # If the function has a non-None return type but no return statements, report error
        has_return_stmts = len(node.get_all_sub_nodes(uni.ReturnStmt)) > 0
        if (
            not has_return_stmts
            and not isinstance(ret_type, jtype.JNoneType)
            and not node.is_abstract
        ):
            self.report_error(JacSemanticMessages.MISSING_RETURN_STATEMENT)

        # Set types for parameters (if any)
        params: dict[str, jtype.JType] = {}
        assert isinstance(node.signature, uni.FuncSignature)
        if node.signature.params:
            for param in node.signature.params.items:
                if param.type_tag:
                    type_annotation = self.prog.expr_type_handler.get_type(
                        param.type_tag.tag
                    )
                else:
                    type_annotation = jtype.JNoType()
                self.prog.expr_type_handler.set_type(param.name, type_annotation)
                params[param.name.sym_name] = type_annotation

        # set ability type to be JCallableType
        self.prog.expr_type_handler.set_type(
            node.name_spec,
            jtype.JCallableType(
                param_types=params, return_type=ret_type, is_assignable=False
            ),
        )

    def enter_architype(self, node: uni.Architype) -> None:
        """Register the type of an architype type annotation pass.

        This assigns a JClassType to the architype's name based on its symbol table,
        enabling type checking for later references to the architype.
        """
        self.prog.expr_type_handler.set_type(
            node.name_spec, jtype.JClassType(node.sym_tab)
        )

    def enter_has_var(self, node: uni.HasVar) -> None:
        """Analyze a `has` variable declaration and populates its type.

        Ensures that each declared variable has an associated type, and checks for redefinitions.
        Raises an error if a variable is declared more than once.
        """

        assert node.type_tag is not None  # QA: why type_tag is optional?
        type_annotation = self.prog.expr_type_handler.get_type(node.type_tag.tag)

        assert node.name_spec.sym is not None
        if isinstance(node.name_spec.sym.jtype, jtype.JNoType):
            self.prog.expr_type_handler.set_type(node.name_spec, type_annotation)
        else:
            self.report_error(
                JacSemanticMessages.CLASS_VAR_REDEFINITION,
                var_name=node.name_spec.sym_name,
            )
