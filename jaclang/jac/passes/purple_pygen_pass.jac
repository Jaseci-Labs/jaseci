"""First Jac pass bootstrapped in Jac"""
import:py jaclang.jac.absyntree as ast;
import:py from jaclang.jac.passes.blue_pygen_pass, BluePygenPass;
import:py from jaclang.core, Object, Node, Edge, Walker, Ability;

object PurplePygenPass:BluePygenPass {

    can exit_architype(node: ast.Architype);
}

"""Sub objects.

name: Name,
arch_type: Token,
doc: Optional[DocString],
decorators: Optional["Decorators"],
access: Optional[Token],
base_classes: "BaseClasses",
body: Optional["ArchBlock"],
"""
:object:PurplePygenPass:a:exit_architype
(node: ast.Architype) {
    if node.decorators { {node, node.decorators.meta["py_code"]} |> <self>.emit_ln; }
    if not node.base_classes.base_classes |> len {
        (node, f"class {node.name.meta['py_code']}:") |> <self>.emit_ln;
    } else {
        {node, f"class {node.name.meta['py_code']}({node.base_classes.meta['py_code']}):"}
        |> <self>.emit_ln;
    }
    if node.doc {
        {node, node.doc.meta["py_code"], indent_delta=1} |> <self>.emit_ln; }
    if node.body {
        {node, node.body.meta["py_code"], indent_delta=1} |> <self>.emit_ln; }
    else {
        {node.name.meta["py_code"]} |> <self>.decl_def_missing; }
}

