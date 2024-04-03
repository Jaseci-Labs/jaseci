"""Jac Registry Pass.

This pass is responsible for creating object containing the senstring, scope,
type of different important nodes in the AST as we loose access to the
semstrings after PyASTGen pass. So we create those as a pickled file for
each module
"""

import os
import pickle

import jaclang.compiler.absyntree as ast
from jaclang.compiler.constant import Constants as Con
from jaclang.compiler.passes import Pass
from jaclang.core.registry import Registry, Scope, SemInfo


class RegistryPass(Pass):
    """Creates a registry for each module."""

    modules_visited: list[ast.Module] = []

    def enter_module(self, node: ast.Module) -> None:
        """Create registry for each module."""
        node.registry = Registry()
        self.modules_visited.append(node)

    def exit_module(self, node: ast.Module) -> None:
        """Save registry for each module."""
        module_dir = os.path.join(
            os.path.abspath(os.path.dirname(node.source.file_path)), Con.JAC_GEN_DIR
        )
        module_name = node.name
        os.makedirs(module_dir, exist_ok=True)
        with open(os.path.join(module_dir, f"{module_name}.registry.pkl"), "wb") as f:
            pickle.dump(node.registry, f)
        self.modules_visited.pop()

    def exit_architype(self, node: ast.Architype) -> None:
        """Save architype information."""
        scope = self.get_scope(node)
        seminfo = SemInfo(
            node.name.value,
            node.arch_type.value,
            node.semstr.lit_value if node.semstr else None,
        )
        if (
            len(self.modules_visited)
            and self.modules_visited[-1].registry
            and scope.parent
        ):
            self.modules_visited[-1].registry.add(scope.parent, seminfo)

    def exit_enum(self, node: ast.Enum) -> None:
        """Save enum information."""
        scope = self.get_scope(node)
        seminfo = SemInfo(
            node.name.value, "Enum", node.semstr.lit_value if node.semstr else None
        )
        if (
            len(self.modules_visited)
            and self.modules_visited[-1].registry
            and scope.parent
        ):
            self.modules_visited[-1].registry.add(scope.parent, seminfo)

    def exit_has_var(self, node: ast.HasVar) -> None:
        """Save variable information."""
        scope = self.get_scope(node)
        seminfo = SemInfo(
            node.name.value,
            (
                node.type_tag.tag.value
                if node.type_tag and isinstance(node.type_tag.tag, ast.Name)
                else None
            ),
            node.semstr.lit_value if node.semstr else None,
        )
        if len(self.modules_visited) and self.modules_visited[-1].registry:
            self.modules_visited[-1].registry.add(scope, seminfo)

    def exit_assignment(self, node: ast.Assignment) -> None:
        """Save assignment information."""
        if node.aug_op:
            return

        extracted_type = (
            "".join(self.extract_type(node.type_tag.kid[1:][0]))
            if node.type_tag
            else None
        )
        scope = self.get_scope(node)
        seminfo = SemInfo(
            (
                node.target.items[0].value
                if isinstance(node.target.items[0], ast.Name)
                else ""
            ),
            extracted_type,
            node.semstr.lit_value if node.semstr else None,
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
            scope = self.get_scope(node)
            seminfo = SemInfo(node.value, None, None)
            if len(self.modules_visited) and self.modules_visited[-1].registry:
                self.modules_visited[-1].registry.add(scope, seminfo)

    def get_scope(self, node: ast.AstNode) -> Scope:
        """Get scope of the node."""
        a = (
            node.name
            if isinstance(node, ast.Module)
            else node.name.value if isinstance(node, (ast.Enum, ast.Architype)) else ""
        )
        if isinstance(node, ast.Module):
            return Scope(a, "Module", None)
        elif isinstance(node, (ast.Enum, ast.Architype)):
            node_type = (
                node.__class__.__name__
                if isinstance(node, ast.Enum)
                else node.arch_type.value
            )
            if node.parent:
                return Scope(a, node_type, self.get_scope(node.parent))
        else:
            if node.parent:
                return self.get_scope(node.parent)
        return Scope("", "", None)

    def extract_type(self, node: ast.AstNode) -> list[str]:
        """Collect type information in assignment using bfs."""
        extracted_type = []
        if isinstance(node, (ast.BuiltinType, ast.Token)):
            extracted_type.append(node.value)
        for child in node.kid:
            extracted_type.extend(self.extract_type(child))
        return extracted_type
