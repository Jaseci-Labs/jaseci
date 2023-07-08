"""First Jac pass bootstrapped in Jac"""
import:py jaclang.jac.absyntree as ast;
import:py from jaclang.jac.passes.blue_pygen_pass, BluePygenPass;
import:py from jaclang.core, Object, Node, Edge, Walker, Ability;

object PurplePygenPass:BluePygenPass {
    """Sub objects.

    name: Name,
    arch_type: Token,
    doc: Optional[DocString],
    decorators: Optional["Decorators"],
    access: Optional[Token],
    base_classes: "BaseClasses",
    body: Optional["ArchBlock"],
    """
    can exit_architype(node: ast.Architype) -> None {
        if node.decorators {
            {node, node.decorators.meta["py_code"]} |> emit_ln .> <self>;
        }
        if not node.base_classes.base_classes |> len {
            {node, f"class {node.name.meta['py_code']}:"} |> emit_ln .> <self>;
        }
        else {
            self.emit_ln(
                node,
                f"class {node.name.meta['py_code']}({node.base_classes.meta['py_code']}):",
            );
        }
        if node.doc:
            self.emit_ln(node, node.doc.meta["py_code"], indent_delta=1)
        if node.body:
            self.emit_ln(node, node.body.meta["py_code"], indent_delta=1)
        else:
            self.decl_def_missing(node.name.meta["py_code"])
    }
}
