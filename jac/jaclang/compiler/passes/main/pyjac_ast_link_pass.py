"""Jac to python ast link pass.

This pass is needed so cases where there are multiple Jac nodes relevant to a
single python node can be linked. For example FuncDef doesn't have a Name node
however Ability does.
"""

import ast as ast3

import jaclang.compiler.absyntree as ast
from jaclang.compiler.passes import Pass


class PyJacAstLinkPass(Pass):
    """Link jac ast to python ast nodes."""

    def link_jac_py_nodes(
        self, jac_node: ast.AstNode, py_nodes: list[ast3.AST]
    ) -> None:
        """Link jac name ast to py ast nodes."""
        jac_node.gen.py_ast = py_nodes
        for i in py_nodes:
            if isinstance(i.jac_link, list):  # type: ignore
                i.jac_link.append(jac_node)  # type: ignore

    def exit_module_path(self, node: ast.ModulePath) -> None:
        if node.alias:
            self.link_jac_py_nodes(jac_node=node.alias, py_nodes=node.gen.py_ast)

    def exit_architype(self, node: ast.Architype) -> None:
        self.link_jac_py_nodes(jac_node=node.name, py_nodes=node.gen.py_ast)
        if isinstance(node.body, ast.ArchDef):
            self.link_jac_py_nodes(jac_node=node.body, py_nodes=node.gen.py_ast)

    def exit_arch_def(self, node: ast.ArchDef) -> None:
        for i in node.target.archs:
            if i.name_spec.name_of.sym:
                self.link_jac_py_nodes(
                    jac_node=i, py_nodes=i.name_spec.name_of.sym.decl.gen.py_ast
                )
                self.link_jac_py_nodes(
                    jac_node=i.name_spec,
                    py_nodes=i.name_spec.name_of.sym.decl.gen.py_ast,
                )

    def exit_enum(self, node: ast.Enum) -> None:
        if isinstance(node.body, ast.EnumDef):
            self.link_jac_py_nodes(jac_node=node.body, py_nodes=node.gen.py_ast)

    def exit_enum_def(self, node: ast.EnumDef) -> None:
        for i in node.target.archs:
            if i.name_spec.name_of.sym:
                self.link_jac_py_nodes(
                    jac_node=i, py_nodes=i.name_spec.name_of.sym.decl.gen.py_ast
                )
                self.link_jac_py_nodes(
                    jac_node=i.name_spec,
                    py_nodes=i.name_spec.name_of.sym.decl.gen.py_ast,
                )

    def exit_ability(self, node: ast.Ability) -> None:
        self.link_jac_py_nodes(jac_node=node.name_ref, py_nodes=node.gen.py_ast)
        if isinstance(node.body, ast.AbilityDef):
            self.link_jac_py_nodes(jac_node=node.body, py_nodes=node.gen.py_ast)

    def exit_ability_def(self, node: ast.AbilityDef) -> None:
        for i in node.target.archs:
            if i.name_spec.name_of.sym:
                self.link_jac_py_nodes(
                    jac_node=i, py_nodes=i.name_spec.name_of.sym.decl.gen.py_ast
                )
                self.link_jac_py_nodes(
                    jac_node=i.name_spec,
                    py_nodes=i.name_spec.name_of.sym.decl.gen.py_ast,
                )

        if isinstance(node.decl_link, ast.Ability) and node.decl_link.signature:
            if isinstance(node.signature, ast.FuncSignature) and node.signature.params:
                for src_prm in node.signature.params.items:
                    if (
                        isinstance(node.decl_link.signature, ast.FuncSignature)
                        and node.decl_link.signature.params
                    ):
                        for trg_prm in node.decl_link.signature.params.items:
                            if src_prm.name.sym_name == trg_prm.name.sym_name:
                                self.link_jac_py_nodes(
                                    jac_node=src_prm, py_nodes=trg_prm.gen.py_ast
                                )
                                self.link_jac_py_nodes(
                                    jac_node=src_prm.name,
                                    py_nodes=trg_prm.name.gen.py_ast,
                                )
            if (
                isinstance(node.signature, ast.FuncSignature)
                and node.signature.return_type
            ) and (
                isinstance(node.decl_link.signature, ast.FuncSignature)
                and node.decl_link.signature.return_type
            ):
                self.link_jac_py_nodes(
                    jac_node=node.signature.return_type,
                    py_nodes=node.decl_link.signature.return_type.gen.py_ast,
                )

        if isinstance(node.decl_link, ast.Ability) and isinstance(
            node.target, ast.ArchRefChain
        ):
            for arch in node.target.archs:
                if arch.arch_name.sym:
                    arch.arch_name.sym.add_use(arch.arch_name)

    def exit_param_var(self, node: ast.ParamVar) -> None:
        self.link_jac_py_nodes(jac_node=node.name, py_nodes=node.gen.py_ast)

    def exit_except(self, node: ast.Except) -> None:
        if node.name:
            self.link_jac_py_nodes(jac_node=node.name, py_nodes=node.gen.py_ast)

    def exit_expr_as_item(self, node: ast.ExprAsItem) -> None:
        self.link_jac_py_nodes(jac_node=node.expr, py_nodes=node.gen.py_ast)
        if node.alias:
            self.link_jac_py_nodes(jac_node=node.alias, py_nodes=node.gen.py_ast)

    def exit_global_stmt(self, node: ast.GlobalStmt) -> None:
        for x, y in enumerate(node.target.items):
            self.link_jac_py_nodes(jac_node=y, py_nodes=[node.gen.py_ast[x]])

    def exit_non_local_stmt(self, node: ast.NonLocalStmt) -> None:
        for x, y in enumerate(node.target.items):
            self.link_jac_py_nodes(jac_node=y, py_nodes=[node.gen.py_ast[x]])

    def exit_k_w_pair(self, node: ast.KWPair) -> None:
        if node.key:
            self.link_jac_py_nodes(jac_node=node.key, py_nodes=node.gen.py_ast)

    def exit_atom_trailer(self, node: ast.AtomTrailer) -> None:
        if node.is_attr and isinstance(node.right, ast.AstSymbolNode):
            self.link_jac_py_nodes(
                jac_node=node.right.name_spec, py_nodes=node.gen.py_ast
            )
