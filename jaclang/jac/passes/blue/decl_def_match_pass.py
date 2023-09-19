"""Connect Decls and Defs in AST."""
import jaclang.jac.absyntree as ast
from jaclang.jac.passes import Pass
from jaclang.jac.passes.blue import SubNodeTabPass
from jaclang.jac.symtable import SymbolHitType


class DeclDefMatchPass(Pass):
    """Decls and Def matching pass."""

    def after_pass(self) -> None:
        """Rebuild sub node table."""
        self.ir = SubNodeTabPass(mod_path=self.mod_path, input_ir=self.ir).ir

    def exit_ability(self, node: ast.Ability) -> None:
        """Sub objects.

        name_ref: Name | SpecialVarRef | ArchRef,
        is_func: bool,
        is_async: bool,
        is_static: bool,
        doc: Optional[Token],
        decorators: Optional[Decorators],
        access: Optional[Token],
        signature: Optional[FuncSignature | TypeSpec | EventSignature],
        body: Optional[CodeBlock],
        sym_tab: Optional[SymbolTable],
        arch_attached: Optional[ArchBlock],
        """
        if not node.body:
            name = node.resolve_ability_symtab_name()
            if not node.sym_tab:
                return self.ice("Expected symbol table on node.")
            adef = node.sym_tab.lookup(name, sym_hit=SymbolHitType.DEFN)
            if node.is_abstract:
                if adef:
                    self.error(f"Abstract ability {name} should not have a definition.")
                return
            if (
                not adef
                or not len(adef.defn)
                or not isinstance(adef.defn[-1], ast.AbilityDef)
            ):
                return self.error(
                    f"Unable to match ability declaration {name} to an implementation."
                )
            adef.decl = node
            ast.append_node(adef.decl, adef.defn[-1])
            adef.decl.body = adef.defn[-1].body
            adef.decl.sym_tab = adef.defn[-1].sym_tab

    def exit_enum(self, node: ast.Enum) -> None:
        """Sub objects.

        name: Name,
        doc: Optional[DocString],
        decorators: Optional[Decorators],
        access: Optional[Token],
        base_classes: BaseClasses,
        body: Optional[EnumBlock],
        """
        if not node.body:
            name = node.name.value
            if not node.sym_tab:
                return self.ice("Expected symbol table on node.")
            print(node.sym_tab)
            adef = node.sym_tab.lookup(name, sym_hit=SymbolHitType.DEFN)
            if (
                not adef
                or not len(adef.defn)
                or not isinstance(adef.defn[-1], ast.EnumDef)
            ):
                return self.error(
                    f"Unable to match enum declaration {name} to an implementation."
                )
            adef.decl = node
            ast.append_node(adef.decl, adef.defn[-1])
            adef.decl.body = adef.defn[-1].body
            adef.decl.sym_tab = adef.defn[-1].sym_tab

    def exit_enum_def(self, node: ast.EnumDef) -> None:
        """Sub objects.

        doc: Optional[Token],
        enum: ArchRef,
        mod: Optional[DottedNameList],
        body: EnumBlock,
        sym_tab: Optional[SymbolTable],
        """
        print(node.sym_tab)
