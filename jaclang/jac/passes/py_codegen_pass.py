"""Transpilation pass for Jaseci Ast."""
from typing import List

import jaclang.jac.jac_ast as ast
from jaclang.jac.jac_ast import AstNode
from jaclang.jac.passes.ir_pass import Pass
from jaclang.utils.log import logging


logger = logging.getLogger(__name__)


class PyCodeGenPass(Pass):
    """Jac transpilation to python pass."""

    marked_incomplete: List[str] = []

    def __init__(self: "PyCodeGenPass") -> None:
        """Initialize pass."""
        self.indent_size = 4
        self.indent_level = 0
        self.cur_arch = None  # tracks current architype during transpilation
        super().__init__()

    def enter_node(self: Pass, node: AstNode) -> None:
        """Enter node."""
        if node:
            node.meta["py_code"] = ""
        return Pass.enter_node(self, node)

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
        """Sub objects.

        name: str,
        value: str,
        """
        self.emit(node, node.value)

    def exit_parse(self: "PyCodeGenPass", node: ast.Parse) -> None:
        """Sub objects.

        name: str,
        """
        logger.critical("Parse node should not be in this AST!!")
        raise ValueError("Parse node should not be in AST after being Built!!")

    def exit_module(self: "PyCodeGenPass", node: ast.Module) -> None:
        """Sub objects.

        name: str,
        doc: Token,
        body: "Elements",
        """
        self.emit_ln(node, node.doc.value)
        self.emit(node, node.body.meta["py_code"])
        self.ir = node

    def exit_elements(self: "PyCodeGenPass", node: ast.Elements) -> None:
        """Sub objects.

         elements: List[
            "GlobalVars | Test | ModuleCode | Import | Architype | Ability | AbilitySpec"
        ],
        """
        for i in node.elements:
            self.emit(node, i.meta["py_code"])

    @Pass.incomplete
    def exit_global_vars(self: "PyCodeGenPass", node: ast.GlobalVars) -> None:
        """Sub objects.

        doc: "DocString",
        access: Optional[Token],
        assignments: "AssignmentList",
        """
        self.emit_ln(node, node.assignments.meta["py_code"])

    @Pass.incomplete
    def exit_test(self: "PyCodeGenPass", node: ast.Test) -> None:
        """Sub objects.

        name: Token,
        doc: "DocString",
        description: Token,
        body: "CodeBlock",
        """

    def exit_module_code(self: "PyCodeGenPass", node: ast.ModuleCode) -> None:
        """Sub objects.

        doc: "DocString",
        body: "CodeBlock",
        """
        self.emit(node, node.doc.meta["py_code"])
        self.emit(node, node.body.meta["py_code"])

    def exit_doc_string(self: "PyCodeGenPass", node: ast.DocString) -> None:
        """Sub objects.

        value: Optional[Token],
        """
        if type(node.value) == ast.Token:
            self.emit_ln(node, node.value.value)

    @Pass.incomplete
    def exit_import(self: "PyCodeGenPass", node: ast.Import) -> None:
        """Sub objects.

        lang: Token,
        path: "ModulePath",
        alias: Optional[Token],
        items: Optional["ModuleItems"],
        is_absorb: bool,  # For includes
        """
        if not node.items:
            if not node.alias:
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
        """Sub objects.

        path: List[Token],
        """
        self.emit(node, "".join([i.value for i in node.path]))

    def exit_module_items(self: "PyCodeGenPass", node: ast.ModuleItems) -> None:
        """Sub objects.

        items: List["ModuleItem"],
        """
        self.emit(node, ", ".join([i.meta["py_code"] for i in node.items]))

    def exit_module_item(self: "PyCodeGenPass", node: ast.ModuleItem) -> None:
        """Sub objects.

        name: Token,
        alias: Optional[Token],
        """
        if type(node.alias) == ast.Token:
            self.emit(node, node.name.value + " as " + node.alias.value)
        else:
            self.emit(node, node.name.value)

    @Pass.incomplete
    def exit_architype(self: "PyCodeGenPass", node: ast.Architype) -> None:
        """Sub objects.

        name: Token,
        typ: Token,
        doc: DocString,
        access: Token,
        base_classes: "BaseClasses",
        body: "ArchBlock",
        """
        if not node.base_classes:
            self.emit_ln(node, f"class {node.name.meta['py_code']}:")
        else:
            self.emit_ln(
                node,
                f"class {node.name.meta['py_code']}({node.base_classes.meta['py_code']}):",
            )
        self.emit_ln(node, node.doc.meta["py_code"], indent_delta=1)
        self.emit(node, node.body.meta["py_code"])

    @Pass.incomplete
    def exit_arch_decl(self: "PyCodeGenPass", node: ast.ArchDecl) -> None:
        """Sub objects.

        doc: DocString,
        access: Token,
        typ: Token,
        name: Token,
        base_classes: "BaseClasses",
        self.def_link: Optional["ArchDef"] = None
        """

    @Pass.incomplete
    def exit_arch_def(self: "PyCodeGenPass", node: ast.ArchDef) -> None:
        """Sub objects.

        doc: DocString,
        mod: Token,
        arch: "ObjectRef | NodeRef | EdgeRef | WalkerRef",
        body: "ArchBlock",
        """

    def exit_base_classes(self: "PyCodeGenPass", node: ast.BaseClasses) -> None:
        """Sub objects.

        base_classes: List[Token],
        """
        self.emit(node, ", ".join([i.value for i in node.base_classes]))

    @Pass.incomplete
    def exit_ability(self: "PyCodeGenPass", node: ast.Ability) -> None:
        """Sub objects.

        name: Token,
        is_func: bool,
        doc: DocString,
        access: Token,
        signature: "FuncSignature | TypeSpec",
        body: "CodeBlock",
        """
        self.emit_ln(node, f"def {node.name.value}{node.signature.meta['py_code']}:")
        self.emit_ln(node, node.doc.meta["py_code"], indent_delta=1)
        self.emit(node, node.body.meta["py_code"])
