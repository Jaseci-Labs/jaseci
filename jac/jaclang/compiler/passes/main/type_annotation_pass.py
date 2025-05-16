"""JType collect pass.

This pass is resbponsible for annotating jtype object
using type annotations in the code.
"""

import jaclang.compiler.jtyping as jtype
import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import UniPass
from jaclang.settings import settings


class JTypeAnnotatePass(UniPass):
    """Populate type annotations to symbols."""

    def __debug_print(self, msg: str) -> None:
        if settings.debug_jac_typing:
            print("[JTypeAnnotatePass]", msg)

    def before_pass(self) -> None:
        """Do setup pass vars."""  # noqa D403, D401
        if not settings.enable_jac_semantics:
            self.terminate()
        if self.ir_in.name == "builtins":
            self.terminate()

    def enter_assignment(self, node: uni.Assignment) -> None:
        """Propagate type annotations for variable declarations."""
        # Resolve the declared type from the annotation
        if not node.type_tag:
            return

        type_annotation = self.prog.type_resolver.get_type(node.type_tag.tag)

        # Iterate over each target in the assignment (e.g., `x` in `x: int = 5`)
        for target in node.target.items:
            if isinstance(target, uni.Name):
                assert target.sym is not None

                # If the current type is unknown or compatible with the declared one, set it
                if isinstance(
                    target.sym.jtype, (type(type_annotation), jtype.JAnyType)
                ):
                    self.prog.type_resolver.set_type(target, type_annotation)

                # If there’s a type mismatch, issue a redefinition warning
                elif not isinstance(type_annotation, jtype.JAnyType):
                    self.log_warning(
                        f"Can't redefine {target.sym_name} to be {type_annotation}"
                    )

            # If the target is not a simple name and a type annotation is present, error
            elif not isinstance(type_annotation, jtype.JAnyType):
                self.log_error(
                    f"Type annotations is not supported for '{target.unparse()}' expression"
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
        if node.signature is None:
            self.prog.type_resolver.set_type(
                node.name_spec,
                jtype.JFunctionType(parameters=[], return_type=jtype.JNoneType()),
            )
            return
        ret_type = self.prog.type_resolver.get_type(node.signature.return_type)

        # If the function has a non-None return type but no return statements, report error
        has_return_stmts = len(node.get_all_sub_nodes(uni.ReturnStmt)) > 0
        if (
            not has_return_stmts
            and not isinstance(ret_type, jtype.JNoneType)
            and not node.is_abstract
        ):
            self.log_error("Missing return statement")

        # Set types for parameters (if any)
        params: list[jtype.JFuncArgument] = []
        assert isinstance(node.signature, uni.FuncSignature)
        if node.signature.params:
            for param in node.signature.params.items:
                if param.type_tag:
                    type_annotation = self.prog.type_resolver.get_type(
                        param.type_tag.tag
                    )
                else:
                    type_annotation = jtype.JAnyType()

                self.prog.type_resolver.set_type(param.name, type_annotation)
                params.append(
                    jtype.JFuncArgument(name=param.name.sym_name, type=type_annotation)
                )

        # set ability type to be JCallableType
        self.prog.type_resolver.set_type(
            node.name_spec, jtype.JFunctionType(parameters=params, return_type=ret_type)
        )

    def enter_architype(self, node: uni.Architype) -> None:
        """Register the type of an architype type annotation pass.

        This assigns a JClassType to the architype's name based on its symbol table,
        enabling type checking for later references to the architype.
        """
        self.prog.type_resolver.set_type(
            node.name_spec,
            jtype.JClassType(
                name=node.sym_name,
                full_name=f"{self.prog.mod.main.get_href_path(node)}.{node.sym_name}",
                module=node.parent_of_type(uni.Module),
                is_abstract=node.is_abstract,
                instance_members={},  # TODO: Pass this correctly
                class_members={},  # TODO: Pass this correctly
            ),
        )

    def enter_has_var(self, node: uni.HasVar) -> None:
        """Analyze a `has` variable declaration and populates its type.

        Ensures that each declared variable has an associated type, and checks for redefinitions.
        Raises an error if a variable is declared more than once.
        """
        assert node.type_tag is not None  # QA: why type_tag is optional?
        type_annotation = self.prog.type_resolver.get_type(node.type_tag.tag)

        assert node.name_spec.sym is not None
        if isinstance(node.name_spec.sym.jtype, jtype.JAnyType):
            self.prog.type_resolver.set_type(node.name_spec, type_annotation)
        else:
            self.log_error(f"'{node.name_spec.sym_name}' was defined before")
