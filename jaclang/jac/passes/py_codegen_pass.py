"""Transpilation pass for Jaseci Ast."""
import jaclang.jac.ast as ast
from jaclang.jac.ast import AstNode
from jaclang.jac.passes.ir_pass import Pass


class PyCodeGenPass(Pass):
    """Jac transpilation to python pass."""

    def __init__(self: "PyCodeGenPass") -> None:
        """Initialize pass."""
        self.indent_size = 4
        self.indent_level = 0
        self.cur_arch = None  # tracks current architype during transpilation
        super().__init__()

    def indent_str(self: "PyCodeGenPass", indent_delta: int) -> str:
        """Return string for indent."""
        return " " * self.indent_size * (self.indent_level + indent_delta)

    def emit_ln(
        self: "PyCodeGenPass", node: AstNode, s: str, indent_delta: int = 0
    ) -> None:
        """Emit code to node."""
        node.meta["py_code"] += (
            self.indent_str(indent_delta)
            + s.replace("\n", "\n" + self.indent_str(indent_delta))
            + "\n"
        )

    def emit(self: "PyCodeGenPass", node: AstNode, s: str) -> None:
        """Emit code to node."""
        node.meta["py_code"] += s

    def exit_token(self: "PyCodeGenPass", node: ast.Token) -> None:
        """Convert token to python code."""
        self.emit(node, node.value)

    def exit_module(self: "PyCodeGenPass", node: ast.Module) -> None:
        """Convert module to python code."""
        if not node.doc.is_blank():
            self.emit_ln(node, node.doc.value)
        self.emit(node, node.body.meta["py_code"])
        self.ir = node

    def exit_elements(self: "PyCodeGenPass", node: ast.Elements) -> None:
        """Convert module to python code."""
        for i in node.elements:
            self.emit(node, i.meta["py_code"])

    def exit_doc_string(self: "PyCodeGenPass", node: ast.DocString) -> None:
        """Convert doc_string to python code."""
        if not node.value.is_blank():
            self.emit_ln(node, node.value.value)

    def exit_global_vars(self: "PyCodeGenPass", node: ast.GlobalVars) -> None:
        """Convert global vars to python code."""
        self.emit_ln(node, node.assignments.meta["py_code"])

    def exit_module_code(self: "PyCodeGenPass", node: ast.ModuleCode) -> None:
        """Convert module code to python code."""
        self.emit(node, node.doc.meta["py_code"])
        self.emit(node, node.body.meta["py_code"])

    def exit_import(self: "PyCodeGenPass", node: ast.Import) -> None:
        """Convert import to python code."""
        if node.items.is_blank():
            if node.alias.is_blank():
                self.emit_ln(node, f"import {node.path.meta['py_code']}")
            else:
                self.emit_ln(
                    node,
                    f"import {node.path.meta['py_code']} as {node.alias.meta['py_code']}",
                )
        else:
            self.emit_ln(
                node,
                f"from {node.path.meta['py_code']} import {node.items.meta['py_code']}",
            )

    def exit_module_path(self: "PyCodeGenPass", node: ast.ModulePath) -> None:
        """Convert module path to python code."""
        self.emit(node, "".join([i.value for i in node.path]))

    def exit_module_items(self: "PyCodeGenPass", node: ast.ModuleItems) -> None:
        """Convert module items to python code."""
        self.emit(node, ", ".join([i.meta["py_code"] for i in node.items]))

    def exit_module_item(self: "PyCodeGenPass", node: ast.ModuleItem) -> None:
        """Convert module item to python code."""
        if node.alias.is_blank():
            self.emit(node, node.name.value)
        else:
            self.emit(node, node.name.value + " as " + node.alias.value)

    def enter_architype(self: "PyCodeGenPass", node: AstNode) -> None:
        """Enter architype."""
        if not node.doc.value.is_blank():
            self.emit(node, node.doc.value.value)

    def exit_architype(self: "PyCodeGenPass", node: AstNode) -> None:
        """Convert object arch to python code."""
        if node.base_classes.is_blank():
            self.emit_ln(node, f"class {node.name.meta['py_code']}:")
        else:
            self.emit_ln(
                node,
                f"class {node.name.meta['py_code']}({node.base_classes.meta['py_code']}):",
            )
        self.emit(node, node.body.meta["py_code"])

    def exit_func_arch(self: "PyCodeGenPass", node: AstNode) -> None:
        """Convert func arch to python code."""
        self.emit_ln(
            node, f"def {node.name.meta['py_code']}({node.signature.meta['py_code']}):"
        )
        self.emit(node, node.body.meta["py_code"])
        self.indent_level -= 1

    def exit_base_classes(self: "PyCodeGenPass", node: AstNode) -> None:
        """Convert base classes to python code."""
        self.emit(node, ", ".join([i.value for i in node.base_classes]))

    def enter_arch_block(self: "PyCodeGenPass", node: AstNode) -> None:
        """Enter arch block."""
        self.indent_level += 1

    def exit_arch_block(self: "PyCodeGenPass", node: AstNode) -> None:
        """Exit arch block."""
        self.indent_level -= 1

    def enter_node(self: Pass, node: AstNode) -> None:
        """Enter node."""
        node.meta["py_code"] = ""
        return super().enter_node(node)
