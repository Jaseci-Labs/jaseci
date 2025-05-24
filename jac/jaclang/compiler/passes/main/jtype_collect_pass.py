"""
JType Collect Pass.

This pass is responsible for collecting and registering type definitions
(e.g., classes, structs, interfaces) found in the source code. It creates
`JType` objects (typically `JClassType`) and stores them in the global
type registry for later use by the type annotation and checking passes.

This pass **does not** resolve members, inheritance, or annotations. It only
registers top-level type shells to support forward references and multi-pass analysis.
"""

import jaclang.compiler.jtyping as jtype
import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import UniPass
from jaclang.settings import settings


class JTypeCollectPass(UniPass):
    """
    Type collection pass for Jac.

    This pass walks the IR and registers all user-defined types (archetypes)
    into the global type registry using their fully qualified names. This
    enables later passes (like annotation and type checking) to resolve
    references to these types even before their definitions are fully processed.
    """

    def __debug_print(self, msg: str) -> None:
        """
        Print debug messages if JAC typing debug mode is enabled.

        Args:
            msg (str): The message to print.
        """
        if settings.debug_jac_typing:
            print("[JTypeCollect]", msg)

    def before_pass(self) -> None:
        """
        Perform initial setup and determine whether to run this pass.

        Terminates early if:
            - Jac semantics are disabled in the global settings.
            - The current module is the built-in module (built-ins are preloaded).
        """
        if not settings.enable_jac_semantics:
            self.terminate()
        if self.ir_in.name == "builtins":
            self.terminate()

    def enter_archetype(self, node: uni.Archetype) -> None:
        """
        Register the JClassType for a user-defined archetype (class-like type).

        This creates a `JClassType` shell and registers it in the type registry
        with its fully qualified name. Member population and inheritance
        resolution are handled in later passes.

        Args:
            node (uni.Archetype): The AST node representing the archetype definition.
        """
        type_full_name = self.prog.mod.main.get_href_path(node)
        class_type = jtype.JClassType(
            name=node.sym_name,
            full_name=type_full_name,
            module=node.parent_of_type(uni.Module),
            is_abstract=node.is_abstract,
            instance_members={},
            class_members={},
        )
        self.prog.type_registry.register(class_type)
        self.__debug_print(f"Registered type: {type_full_name}")
