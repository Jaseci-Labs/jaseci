"""Jac Registry Pass.

This pass is responsible for creating object containing the senstring, scope,
type of different important nodes in the AST as we loose access to the
semstrings after PyASTGen pass. So we create those as a pickled file for
each module
"""

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.semtable import SemInfo, SemRegistry
from jaclang.runtimelib.utils import get_sem_scope
from jaclang.settings import settings


class RegistryPass(Pass):
    """Creates a registry for each module."""

    modules_visited: list[ast.Module] = []

    def enter_module(self, node: ast.Module) -> None:
        """Create registry for each module."""
        if settings.disable_mtllm:
            self.terminate()
            return None
        node.registry = SemRegistry()
        self.modules_visited.append(node)

    def exit_module(self, node: ast.Module) -> None:
        """Save registry for each module."""
        module_name = node.name
        try:
            from jaclang.runtimelib.machine import JacMachine

            JacMachine.get().get_sem_ir(node.registry)
        except Exception as e:
            self.warning(f"Can't save registry for {module_name}: {e}")
        self.modules_visited.pop()

    def exit_architype(self, node: ast.Architype) -> None:
        """Save architype information."""
        scope = get_sem_scope(node)
        seminfo = SemInfo(
            node,
            node.name.value,
            node.arch_type.value,
            node.semstr.lit_value if node.semstr else "",
        )
        if (
            len(self.modules_visited)
            and self.modules_visited[-1].registry
            and scope.parent
        ):
            self.modules_visited[-1].registry.add(scope.parent, seminfo)

    def exit_enum(self, node: ast.Enum) -> None:
        """Save enum information."""
        scope = get_sem_scope(node)
        seminfo = SemInfo(
            node, node.name.value, "Enum", node.semstr.lit_value if node.semstr else ""
        )
        if (
            len(self.modules_visited)
            and self.modules_visited[-1].registry
            and scope.parent
        ):
            self.modules_visited[-1].registry.add(scope.parent, seminfo)

    def exit_has_var(self, node: ast.HasVar) -> None:
        """Save variable information."""
        extracted_type = (
            "".join(self.extract_type(node.type_tag.tag)) if node.type_tag else None
        )
        scope = get_sem_scope(node)
        seminfo = SemInfo(
            node,
            node.name.value,
            extracted_type,
            node.semstr.lit_value if node.semstr else "",
        )
        if len(self.modules_visited) and self.modules_visited[-1].registry:
            self.modules_visited[-1].registry.add(scope, seminfo)

    def exit_ability(self, node: ast.Ability) -> None:
        """Save ability information."""
        scope = get_sem_scope(node)
        seminfo = SemInfo(
            node,
            node.name_ref.sym_name,
            "Ability",
            node.semstr.lit_value if node.semstr else "",
        )
        if len(self.modules_visited) and self.modules_visited[-1].registry:
            (
                self.modules_visited[-1].registry.add(scope.parent, seminfo)
                if scope.parent
                else None
            )

    def exit_param_var(self, node: ast.ParamVar) -> None:
        """Save param information."""
        scope = get_sem_scope(node)
        extracted_type = (
            "".join(self.extract_type(node.type_tag.tag)) if node.type_tag else None
        )
        seminfo = SemInfo(
            node,
            node.name.value,
            extracted_type,
            node.semstr.lit_value if node.semstr else "",
        )
        if len(self.modules_visited) and self.modules_visited[-1].registry:
            self.modules_visited[-1].registry.add(scope, seminfo)

    def exit_assignment(self, node: ast.Assignment) -> None:
        """Save assignment information."""
        if node.aug_op:
            return

        extracted_type = (
            "".join(self.extract_type(node.type_tag.tag)) if node.type_tag else None
        )
        scope = get_sem_scope(node)
        seminfo = SemInfo(
            node,
            (
                node.target.items[0].value
                if isinstance(node.target.items[0], ast.Name)
                else ""
            ),
            extracted_type,
            node.semstr.lit_value if node.semstr else "",
        )
        if len(self.modules_visited) and self.modules_visited[-1].registry:
            self.modules_visited[-1].registry.add(scope, seminfo)

    def exit_name(self, node: ast.Name) -> None:
        """Save name information. for enum stmts."""
        if (
            node.parent
            and node.parent.parent
            and node.parent.parent.__class__.__name__ == "Enum"
        ):
            scope = get_sem_scope(node)
            seminfo = SemInfo(node, node.value, None, "")
            if len(self.modules_visited) and self.modules_visited[-1].registry:
                self.modules_visited[-1].registry.add(scope, seminfo)

    def extract_type(self, node: ast.AstNode) -> list[str]:
        """Collect type information in assignment using bfs."""
        extracted_type = []
        if isinstance(node, (ast.BuiltinType, ast.Token)):
            extracted_type.append(node.value)
        for child in node.kid:
            extracted_type.extend(self.extract_type(child))
        return extracted_type
