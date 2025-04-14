"""Jac SemIR Build Pass.

This pass is responsible for creating object containing the senstring, scope,
type of different important nodes in the AST as we loose access to the
semstrings after PyASTGen pass.
"""

from jaclang.compiler.symtable import SymbolTable
import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass
from jaclang.compiler.semir import SemIR, SemNode
from jaclang.settings import settings
from jaclang.utils.log import logging
from typing import Optional


logger = logging.getLogger(__name__)


class SemIRBuildPass(Pass):
    """Builds the semantic IR for Jaclang."""

    semir: Optional[SemIR] = None
    modules_visited: list[ast.Module] = []
    sym_table: Optional[SymbolTable] = None

    def __debug_print(self, msg: str) -> None:
        logger.info("[SemIRBuildPass] " + str(msg))

    def before_pass(self):
        """Initialize the semantic IR."""
        try:
            from jaclang.runtimelib.machine import JacMachine

            if JacMachine.get().jac_program.sem_ir:
                self.semir = JacMachine.get().jac_program.sem_ir
            else:
                self.semir = SemIR()
                JacMachine.get().jac_program.sem_ir = self.semir
        except ImportError:
            self.warning("JacMachine is not available. Skipping SemIR build pass.")
            return None

    def enter_module(self, node: ast.Module) -> None:
        """Create registry for each module."""
        self.modules_visited.append(node)
        self.sym_table = node._sym_tab
        if not self.sym_table:
            self.sym_table = node._sym_tab
        sem_node = SemNode(
            name=node.name, node_type=str(type(node)).split(".")[-1][0:-2]
        )
        self.semir.tree.add_child(sem_node)

    def exit_module(self, node: ast.Module) -> None:
        """Save semir for each module."""
        module_name = node.name
        try:
            from jaclang.runtimelib.machine import JacMachine

            JacMachine.get().get_sem_ir(self.semir)
        except Exception as e:
            self.warning(f"Can't save semir for {module_name}: {e}")
        self.modules_visited.pop()
        print("SemIR: \n",self.semir.pp())

    def exit_architype(self, node: ast.Architype) -> None:
        semnode = SemNode(name=node.name.value, node_type=node.arch_type.value)
        semnode.semstr = node.semstr.lit_value if node.semstr else ""
        self.semir.add_node(node, semnode)

    def exit_has_var(self, node: ast.HasVar) -> None:
        extracted_type = (
            "".join(self.extract_type(node.type_tag.tag)) if node.type_tag else None
        )
        semnode = SemNode(
            name=node.name.value,
            node_type=extracted_type,
        )
        semnode.semstr = node.semstr.lit_value if node.semstr else ""
        self.semir.add_node(node, semnode)

    def exit_ability(self, node: ast.Ability) -> None:
        pass

    def exit_param_var(self, node: ast.ParamVar) -> None:
        pass

    def exit_assignment(self, node: ast.Assignment) -> None:
        pass

    def exit_name(self, node: ast.Name) -> None:
        pass

    def exit_enum(self, node: ast.Enum) -> None:
        pass

    def extract_type(self, node: ast.AstNode) -> list[str]:
        """Collect type information in assignment using bfs."""
        extracted_type = []
        if isinstance(node, (ast.BuiltinType, ast.Token)):
            extracted_type.append(node.value)
        for child in node.kid:
            extracted_type.extend(self.extract_type(child))
        print(f"Extracted type: {extracted_type}")
        return extracted_type