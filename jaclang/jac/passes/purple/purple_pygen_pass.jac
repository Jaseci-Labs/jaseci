"""First Jac pass bootstrapped in Jac"""
import:py jaclang.jac.absyntree as ast;
import:py from jaclang.jac.passes.blue, BluePygenPass;
import:py from jaclang.core, Object, Node, Edge, Walker, Ability;
import:py from jaclang.jac.lexer, Tokens as Tok;

object PurplePygenPass:BluePygenPass {

    can exit_architype(nd: ast.Architype);
}

"""
Sub objects.

name: Name,
arch_type: Token,
doc: Optional[DocString],
decorators: Optional["Decorators"],
access: Optional[Token],
base_classes: "BaseClasses",
body: Optional["ArchBlock"],
"""
:object:PurplePygenPass:a:exit_architype
(nd: ast.Architype) {
    if nd.decorators {
        (nd, nd.decorators.meta["py_code"]) |> <self>.emit_ln;
    }
    arch_type=nd.arch_type.name;
    if arch_type == Tok.KW_OBJECT {}
    if arch_type == Tok.KW_NODE {}
    if arch_type == Tok.KW_EDGE {}
    if arch_type == Tok.KW_WALKER {}
    if nd.base_classes.base_classes |> len {
        (nd, f"class {nd.name.meta['py_code']}({nd.base_classes.meta['py_code']}):")
        |> <self>.emit_ln;
    } else {
        (nd, f"class {nd.name.meta['py_code']}:") |> <self>.emit_ln;
    }
    if nd.doc {
        (nd, nd.doc.meta["py_code"], indent_delta=1) |> <self>.emit_ln; }
    if nd.body {
        (nd, nd.body.meta["py_code"], indent_delta=1) |> <self>.emit_ln; }
    else {
        nd.name.meta["py_code"] |> <self>.decl_def_missing; }
}

