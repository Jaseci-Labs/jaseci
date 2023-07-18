"""First Jac pass bootstrapped in Jac"""
import:py jaclang.jac.absyntree as ast;
import:py from jaclang.jac.passes.blue, BluePygenPass;
import:py from jaclang.core, Object, Node, Edge, Walker;
import:py from jaclang.jac.lexer, Tokens as Tok;
import:py from jaclang.jac.constant, Constants as C;

object PurplePygenPass:BluePygenPass {

    """ Addd arch import to the preamble """
    can add_element_import(arch: str);
    """ Addd exec context import to the preamble """
    can add_exec_context();

    can exit_architype(nd: ast.Architype);
    can exit_ability(nd: ast.Ability);
    can exit_event_signature(nd: ast.EventSignature);
    can exit_ctrl_stmt(nd: ast.CtrlStmt);
    can exit_binary_expr(nd: ast.BinaryExpr);
    # can exit_connect_op(nd: ast.ConnectOp);
}

:object:PurplePygenPass:ability:add_element_import
(arch: str) {
    (self.preamble, f"from jaclang.core import {arch} as __jac_{arch}__")
    |> <self>.emit_ln_unique;
}

:object:PurplePygenPass:ability:add_exec_context {
    (self.preamble, f"from jaclang.core import exec_ctx as {C.EXEC_CONTEXT}")
    |> <self>.emit_ln_unique;
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
:object:PurplePygenPass:ability:exit_architype
(nd: ast.Architype) {
    |> <self>.add_exec_context;
    if nd.decorators {
        (nd, nd.decorators.meta["py_code"]) |> <self>.emit_ln;
    }
    arch_type=nd.arch_type.name;
    arch_insert = "";
    if arch_type == Tok.KW_OBJECT {
        "Object" |> <self>.add_element_import;
        arch_insert = C.OBJECT_CLASS;
    }
    elif arch_type == Tok.KW_NODE {
        "Node" |> <self>.add_element_import;
        arch_insert = C.NODE_CLASS;
    }
    elif arch_type == Tok.KW_EDGE {
        "Edge" |> <self>.add_element_import;
        arch_insert = C.EDGE_CLASS;
    }
    elif arch_type == Tok.KW_WALKER {
        "Walker" |> <self>.add_element_import;
        arch_insert = C.WALKER_CLASS;
    }
    if nd.base_classes.base_classes |> len {
        (nd, f"class {nd.name.meta['py_code']}"
             f"({nd.base_classes.meta['py_code']}, {arch_insert}):")
            |> <self>.emit_ln;
    } else {
        (nd, f"class {nd.name.meta['py_code']}({arch_insert}):") |> <self>.emit_ln;
    }
    if nd.doc {
        (nd, nd.doc.meta["py_code"], indent_delta=1) |> <self>.emit_ln; }
    if nd.body {
        (nd, nd.body.meta["py_code"], indent_delta=1) |> <self>.emit_ln; }
    else {
        nd.name.meta["py_code"] |> <self>.decl_def_missing; }
}


"""Sub objects.

name: Name,
is_func: bool,
is_async: bool,
doc: Optional[DocString],
decorators: Optional["Decorators"],
access: Optional[Token],
signature: Optional["FuncSignature | TypeSpec | EventSignature"],
body: Optional["CodeBlock"],
arch_attached: Optional["ArchBlock"] = None,
"""
:object:PurplePygenPass:ability:exit_ability
(nd: ast.Ability) {
    if nd.decorators {
        (nd, nd.decorators.meta["py_code"]) |> <self>.emit_ln;
    }
    if (nd.signature|>type) in [ast.FuncSignature, ast.EventSignature] {
        if nd.arch_attached {
            (nd, f"def {nd.name.meta['py_code']}(self{nd.signature.meta['py_code']}:")
                |> <self>.emit_ln;
            # (nd, "1/0", indent_delta=1) |> <self>.emit_ln;
        } else {
            (nd, f"def {nd.name.meta['py_code']}({nd.signature.meta['py_code']}:")
                |> <self>.emit_ln;
        }
    } else {
        if nd.arch_attached {
            (nd, f"def {nd.name.meta['py_code']}(self):") |> <self>.emit_ln;
        } else {
            (nd, f"def {nd.name.meta['py_code']}():") |> <self>.emit_ln;
        }
    }
    if nd.doc {
        (nd, nd.doc.meta["py_code"], indent_delta=1) |> <self>.emit_ln;
    }
    if nd.body {
        (nd, nd.body.meta["py_code"], indent_delta=1) |> <self>.emit_ln;
    } else {
        nd.name.meta["py_code"] |> <self>.decl_def_missing;
    }
}


"""Sub objects.

event: Token,
arch_tag_info: Optional["TypeList | TypeSpec"],
return_type: Optional["TypeSpec"],
"""
:object:PurplePygenPass:ability:exit_event_signature
(nd: ast.EventSignature) {
    if nd.arch_tag_info {
        (nd, f"{C.HERE}: {nd.arch_tag_info.meta['py_code']})")
            |> <self>.emit;
    } else {
        (nd, f"{C.HERE})") |> <self>.emit;
    }
    if nd.return_type {
        (nd, f" -> {nd.return_type.meta['py_code']}") |> <self>.emit;
    }
}


"""Sub objects.

ctrl: Token,
"""
:object:PurplePygenPass:ability:exit_ctrl_stmt
(nd: ast.CtrlStmt) {

}


"""Sub objects.

left: ExprType,
right: ExprType,
op: Token,
"""
:object:PurplePygenPass:ability:exit_binary_expr
(nd: ast.BinaryExpr) {
    if (nd.op.name|>type) == ast.ConnectOp {
        if(nd.op.spwn) {
            (nd, f"{nd.left.meta['py_code']}.{C.CONNECT_NODE}({nd.right.meta['py_code']}, {nd.op.meta['py_code']})")
                |> <self>.emit;
        } else {
            (nd, f"{nd.left.meta['py_code']}.{C.CONNECT_NODE}({nd.right.meta['py_code']})")
                |> <self>.emit;
        }
    } else {
        <super>.exit_binary_expr(nd);
    }
}


"""Sub objects.

spawn: Optional[ExprType],
edge_dir: EdgeDir,
"""
:object:PurplePygenPass:ability:exit_connect_op
(nd: ast.ConnectOp) {
    "Edge" |> <self>.add_element_import;

    if nd.spwn {
        (nd, f"{nd.spwn.meta['py_code']}.{C.WITH_DIR}(ast.EdgeDir.{nd.edge_dir.name})") |> <self>.emit;
    } else {
        (nd, f"Edge().{C.WITH_DIR}(ast.EdgeDir.{nd.edge_dir.name})") |> <self>.emit;
    }
    (nd, f" {nd.meta['py_code']}") |> <self>.emit_ln;
}