"""Jac to python ast link pass.

This pass is needed so cases where there are multiple Jac nodes relevant to a
single python node can be linked. For example FuncDef doesn't have a Name node
however Ability does.
"""

import ast as ast3

import jaclang.compiler.unitree as uni
from jaclang.compiler.passes import UniPass


class PyJacAstLinkPass(UniPass):
    """Link jac ast to python ast nodes."""

    def link_jac_py_nodes(
        self, jac_node: uni.UniNode, py_nodes: list[ast3.AST]
    ) -> None:
        """Link jac name ast to py ast nodes."""
        jac_node.gen.py_ast = py_nodes
        for i in py_nodes:
            if isinstance(i.jac_link, list):  # type: ignore
                i.jac_link.append(jac_node)  # type: ignore

    def exit_module_path(self, node: uni.ModulePath) -> None:
        if node.alias:
            self.link_jac_py_nodes(jac_node=node.alias, py_nodes=node.gen.py_ast)

    def exit_architype(self, node: uni.Architype) -> None:
        self.link_jac_py_nodes(jac_node=node.name, py_nodes=node.gen.py_ast)
        if isinstance(node.body, uni.ArchDef):
            self.link_jac_py_nodes(jac_node=node.body, py_nodes=node.gen.py_ast)

    def exit_arch_def(self, node: uni.ArchDef) -> None:
        for i in node.target.archs:
            if i.name_spec.name_of.sym:
                self.link_jac_py_nodes(
                    jac_node=i, py_nodes=i.name_spec.name_of.sym.decl.gen.py_ast
                )
                self.link_jac_py_nodes(
                    jac_node=i.name_spec,
                    py_nodes=i.name_spec.name_of.sym.decl.gen.py_ast,
                )

    def exit_enum(self, node: uni.Enum) -> None:
        if isinstance(node.body, uni.EnumDef):
            self.link_jac_py_nodes(jac_node=node.body, py_nodes=node.gen.py_ast)

    def exit_enum_def(self, node: uni.EnumDef) -> None:
        for i in node.target.archs:
            if i.name_spec.name_of.sym:
                self.link_jac_py_nodes(
                    jac_node=i, py_nodes=i.name_spec.name_of.sym.decl.gen.py_ast
                )
                self.link_jac_py_nodes(
                    jac_node=i.name_spec,
                    py_nodes=i.name_spec.name_of.sym.decl.gen.py_ast,
                )

    def exit_ability(self, node: uni.Ability) -> None:
        self.link_jac_py_nodes(jac_node=node.name_ref, py_nodes=node.gen.py_ast)
        if isinstance(node.body, uni.AbilityDef):
            self.link_jac_py_nodes(jac_node=node.body, py_nodes=node.gen.py_ast)

    def exit_ability_def(self, node: uni.AbilityDef) -> None:
        for i in node.target.archs:
            if i.name_spec.name_of.sym:
                self.link_jac_py_nodes(
                    jac_node=i, py_nodes=i.name_spec.name_of.sym.decl.gen.py_ast
                )
                self.link_jac_py_nodes(
                    jac_node=i.name_spec,
                    py_nodes=i.name_spec.name_of.sym.decl.gen.py_ast,
                )

        if isinstance(node.decl_link, uni.Ability) and node.decl_link.signature:
            if isinstance(node.signature, uni.FuncSignature) and node.signature.params:
                for src_prm in node.signature.params.items:
                    if (
                        isinstance(node.decl_link.signature, uni.FuncSignature)
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
                isinstance(node.signature, uni.FuncSignature)
                and node.signature.return_type
            ) and (
                isinstance(node.decl_link.signature, uni.FuncSignature)
                and node.decl_link.signature.return_type
            ):
                self.link_jac_py_nodes(
                    jac_node=node.signature.return_type,
                    py_nodes=node.decl_link.signature.return_type.gen.py_ast,
                )

        if isinstance(node.decl_link, uni.Ability) and isinstance(
            node.target, uni.ArchRefChain
        ):
            for arch in node.target.archs:
                if arch.arch_name.sym:
                    arch.arch_name.sym.add_use(arch.arch_name)

    def exit_param_var(self, node: uni.ParamVar) -> None:
        self.link_jac_py_nodes(jac_node=node.name, py_nodes=node.gen.py_ast)

    def exit_except(self, node: uni.Except) -> None:
        if node.name:
            self.link_jac_py_nodes(jac_node=node.name, py_nodes=node.gen.py_ast)

    def exit_expr_as_item(self, node: uni.ExprAsItem) -> None:
        self.link_jac_py_nodes(jac_node=node.expr, py_nodes=node.gen.py_ast)
        if node.alias:
            self.link_jac_py_nodes(jac_node=node.alias, py_nodes=node.gen.py_ast)

    def exit_global_stmt(self, node: uni.GlobalStmt) -> None:
        for x, y in enumerate(node.target.items):
            self.link_jac_py_nodes(jac_node=y, py_nodes=[node.gen.py_ast[x]])

    def exit_non_local_stmt(self, node: uni.NonLocalStmt) -> None:
        for x, y in enumerate(node.target.items):
            self.link_jac_py_nodes(jac_node=y, py_nodes=[node.gen.py_ast[x]])

    def exit_k_w_pair(self, node: uni.KWPair) -> None:
        if node.key:
            self.link_jac_py_nodes(jac_node=node.key, py_nodes=node.gen.py_ast)

    def exit_atom_trailer(self, node: uni.AtomTrailer) -> None:
        if node.is_attr and isinstance(node.right, uni.AstSymbolNode):
            self.link_jac_py_nodes(
                jac_node=node.right.name_spec, py_nodes=node.gen.py_ast
            )
