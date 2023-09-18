"""Connect Decls and Defs in AST."""
import jaclang.jac.absyntree as ast
from jaclang.jac.passes import Pass
from jaclang.jac.passes.blue import SubNodeTabPass


class DeclDefMatchPass(Pass):
    """Decls and Def matching pass."""

    def after_pass(self) -> None:
        """Rebuild sub node table."""
        self.ir = SubNodeTabPass(mod_path=self.mod_path, input_ir=self.ir).ir

    def exit_ability_def(self, node: ast.AbilityDef) -> None:
        """Sub objects.

        doc: Optional[DocString],
        target: Optional["DottedNameList"],
        ability: "ArchRef",
        signature: "FuncSignature | EventSignature",
        body: "CodeBlock",
        """
        name = node.py_resolve_name()
        if not node.sym_tab:
            return self.ice("Expected symbol table on node.")
        adef = node.sym_tab.lookup(name)
        if (
            not adef
            or not isinstance(adef.decl, ast.Ability)
            or not len(adef.defn)
            or not isinstance(adef.defn[-1], ast.AbilityDef)
        ):
            return self.ice(
                f"Expected ability def symbol {name} in symbol table, got {adef}."
            )
        ast.append_node(adef.decl, adef.defn[-1])
        adef.decl.body = adef.defn[-1].body
        adef.decl.sym_tab = adef.defn[-1].sym_tab

    def enter_arch_block(self, node: ast.ArchBlock) -> None:
        """Sub objects.

        members: list['ArchHas | Ability'],
        """
        # Tags all function signatures whether method style or not
        for i in self.get_all_sub_nodes(node, ast.Ability):
            i.arch_attached = node

    # def exit_enum(self, node: ast.Enum) -> None:
    #     """Sub objects.

    #     name: Name,
    #     doc: Optional[DocString],
    #     decorators: Optional[Decorators],
    #     access: Optional[Token],
    #     base_classes: BaseClasses,
    #     body: Optional[EnumBlock],
    #     """
    #     name = node.name.value
    #     decl = self.sym_tab.lookup(name)
    #     if decl and decl.has_decl:
    #         self.error(
    #             f"Enum bound with name {name} already defined on Line {decl.node.line}."
    #         )
    #     elif decl and decl.has_def:
    #         decl.has_decl = True
    #         decl.node = node
    #         decl.node.body = (
    #             decl.other_node.body
    #             if isinstance(decl.other_node, ast.EnumDef)
    #             else self.ice("Expected node of type EnumDef in symbol table.")
    #         )
    #         ast.append_node(decl.node, decl.other_node)
    #         self.sym_tab.set(decl)
    #     else:
    #         decl = DefDeclSymbol(name=name, node=node, has_decl=True)
    #         if node.body:
    #             decl.has_def = True
    #             decl.other_node = node
    #         self.sym_tab.set(decl)

    # def exit_enum_def(self, node: ast.EnumDef) -> None:
    #     """Sub objects.

    #     doc: Optional[Token],
    #     enum: ArchRef,
    #     mod: Optional[DottedNameList],
    #     body: EnumBlock,
    #     """
    #     name = node.enum.py_resolve_name()
    #     decl = self.sym_tab.lookup(name)
    #     if decl and decl.has_def:
    #         self.error(
    #             f"Enum bound with name {name} already defined on Line {decl.other_node.line}."
    #         )
    #     elif decl and decl.has_decl:
    #         decl.has_def = True
    #         decl.other_node = node
    #         decl.node.body = decl.other_node.body
    #         ast.append_node(decl.node, decl.other_node)
    #         self.sym_tab.set(decl)
    #     else:
    #         self.sym_tab.set(DefDeclSymbol(name=name, other_node=node, has_def=True))
