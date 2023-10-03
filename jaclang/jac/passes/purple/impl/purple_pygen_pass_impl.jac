"""First Jac pass bootstrapped in Jac"""
import:py from jaclang.jac.constant, Constants as C, EdgeDir, Tokens as Tok;

:object:PurplePygenPass:ability:add_element_import
(arch: str) {
    (<self>.preamble, f"from jaclang.core import {arch} as _jac_{arch}_")
        |> <self>.emit_ln_unique;
    (<self>.preamble, f"from jaclang.core import make_architype as _jac_make_architype_")
        |> <self>.emit_ln_unique;
}

:object:PurplePygenPass:ability:add_exec_context {
    (<self>.preamble, f"from jaclang.core import exec_ctx as {C.EXEC_CONTEXT}")
        |> <self>.emit_ln_unique;
}

:object:PurplePygenPass:ability:add_edge_directions {
    (<self>.preamble, f"from jaclang.jac.constant import EdgeDir as {C.EDGE_DIR}")
        |> <self>.emit_ln_unique;
}

:object:PurplePygenPass:ability:needs_jac_import {
    (<self>.preamble, "from jaclang import jac_purple_import as __jac_import__")
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
        (nd, f"@_jac_make_architype_({arch_insert})") |> <self>.emit_ln;
    }
    elif arch_type == Tok.KW_NODE {
        "Node" |> <self>.add_element_import;
        arch_insert = C.NODE_CLASS;
        (nd, f"@_jac_make_architype_({arch_insert})") |> <self>.emit_ln;
    }
    elif arch_type == Tok.KW_EDGE {
        "Edge" |> <self>.add_element_import;
        arch_insert = C.EDGE_CLASS;
        (nd, f"@_jac_make_architype_({arch_insert})") |> <self>.emit_ln;
    }
    elif arch_type == Tok.KW_WALKER {
        "Walker" |> <self>.add_element_import;
        arch_insert = C.WALKER_CLASS;
        (nd, f"@_jac_make_architype_({arch_insert})") |> <self>.emit_ln;
    }
    if nd.base_classes.base_classes |> len {
        (nd, f"class {nd.name.meta['py_code']}"
             f"({nd.base_classes.meta['py_code']}):")
            |> <self>.emit_ln;
    } else {
        (nd, f"class {nd.name.meta['py_code']}:") |> <self>.emit_ln;
    }
    <self>.indent_level += 1;
    if nd.doc {
        (nd, nd.doc.meta["py_code"]) |> <self>.emit_ln; }
    if nd.body {
        (nd, nd.body.meta["py_code"]) |> <self>.emit_ln; }
    else {
        nd.name.meta["py_code"] |> <self>.decl_def_missing; }
    <self>.indent_level -= 1;
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
    ability_name = nd.py_resolve_name();
    if nd.arch_attached and ability_name == "__init__" {
        return;
    }
    if nd.signature:>type == ast.EventSignature and nd.arch_attached and
        nd.signature.event.name == Tok.KW_ENTRY {
        "Object" |> <self>.add_element_import;
        type_list = nd.signature.arch_tag_info?.meta?["py_code"] ?: "";
        (nd, f"@{C.OBJECT_CLASS}.{C.ON_ENTRY}([{type_list.replace('|', ', ')}])") |> <self>.emit_ln;
    }
    elif nd.signature:>type == ast.EventSignature and nd.arch_attached and
        nd.signature.event.name == Tok.KW_EXIT {
        "Object" |> <self>.add_element_import;
        type_list = nd.signature.arch_tag_info?.meta?["py_code"] ?: "";
        (nd, f"@{C.OBJECT_CLASS}.{C.ON_EXIT}([{type_list.replace('|', ', ')}])") |> <self>.emit_ln;
    }
    (nd) |> <super>.exit_ability;
}


"""Sub objects.

event: Token,
arch_tag_info: Optional["TypeList | TypeSpec"],
return_type: Optional["TypeSpec"],
"""
:object:PurplePygenPass:ability:exit_event_signature
(nd: ast.EventSignature) {
    if nd.arch_tag_info {
        (nd, f"{C.HERE}: {nd.arch_tag_info.meta['py_code']}")
            |> <self>.emit;
    } else {
        (nd, f"{C.HERE}") |> <self>.emit;
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
    if nd.ctrl.name == Tok.KW_SKIP {
        (nd, "return") |> <self>.emit_ln;
    } else {
        <super>.exit_ctrl_stmt(nd);
    }
}


"""Sub objects.

ctrl: Token,
from_walker: bool = False,
"""
:object:PurplePygenPass:ability:exit_ignore_stmt
(nd: ast.IgnoreStmt) {
    loc = 'self' if nd.from_walker else C.HERE;
    (nd, f"{loc}.{C.WALKER_IGNORE}({nd.target.meta['py_code']})" )
        |> <self>.emit_ln;
}


"""Sub objects.

vis_type: Optional[Token],
target: ExprType,
else_body: Optional["ElseStmt"],
from_walker: bool = False,
"""
:object:PurplePygenPass:ability:exit_visit_stmt
(nd: ast.VisitStmt) {
    vis_type = nd.vis_type?.value ?: "";
    loc = 'self' if nd.from_walker else C.HERE;
    (nd, f"if not {loc}.{C.WALKER_VISIT}({nd.target.meta['py_code']}): " )
        |> <self>.emit_ln;
    <self>.indent_level += 1;
    if nd.else_body {
        (nd, nd.else_body.body.meta["py_code"]) |> <self>.emit;
    } else {
        (nd, 'pass') |> <self>.emit_ln;
    }
    <self>.indent_level -= 1;
}


"""Sub objects.
from_walker: bool = False,
"""
:object:PurplePygenPass:ability:exit_disengage_stmt
(nd: ast.VisitStmt) {
    loc = 'self' if nd.from_walker else C.HERE;
    (nd, f"return {loc}.{C.DISENGAGE}()") |> <self>.emit_ln;
}


"""Sub objects.

left: ExprType,
right: ExprType,
op: Token,
"""
:object:PurplePygenPass:ability:exit_binary_expr
(nd: ast.BinaryExpr) {
    if (nd.op:>type) == ast.ConnectOp {
        (nd, f"{nd.left.meta['py_code']}.{C.CONNECT_NODE}({nd.right.meta['py_code']}, {nd.op.meta['py_code']})")
            |> <self>.emit;
    } elif (nd.op:>type) == ast.DisconnectOp {
        <self>.ds_feature_warn(); # TODO: Implement
    } elif nd.op.name == Tok.PIPE_FWD and isinstance(nd.right, ast.TupleVal) {
        <self>.ds_feature_warn(); # TODO: Implement
    }
    else {
        <super>.exit_binary_expr(nd);
    }
}


"""Sub objects.

filter_type: Optional[ExprType],
filter_cond: Optional[FilterCompr],
edge_dir: EdgeDir,
from_walker: bool = False,
"""
:object:PurplePygenPass:ability:exit_edge_op_ref
(nd: ast.EdgeOpRef) {
    loc = C.HERE if nd.from_walker else 'self';
    edge_dir = f"{C.EDGE_DIR}.IN" if nd.edge_dir == EdgeDir.IN
               else f"{C.EDGE_DIR}.OUT" if nd.edge_dir == EdgeDir.OUT
               else f"{C.EDGE_DIR}.ANY";
    if nd.filter_type and nd.filter_cond {
        (nd, f"[{C.JAC_TMP} for {C.JAC_TMP} in {loc}.{C.EDGES_TO_NODE}({edge_dir})"
            f" if isinstance({C.JAC_TMP}, {nd.filter_type.meta['py_code']})"
            f" and {nd.filter_cond.meta['py_code'].replace(C.PATCH, C.JAC_TMP)}]")
            |> <self>.emit;
    }
    elif nd.filter_type {
        (nd, f"[{C.JAC_TMP} for {C.JAC_TMP} in {loc}.{C.EDGES_TO_NODE}({edge_dir})"
            f" if isinstance({C.JAC_TMP}, {nd.filter_type.meta['py_code']})]")
            |> <self>.emit;
    }
    else {
        (nd, f"{loc}.{C.EDGES_TO_NODE}({edge_dir})")
            |> <self>.emit;
    }
}


"""Sub objects.

conn_type: Optional[ExprType],
conn_assign: Optional[AssignmentList],
edge_dir: EdgeDir,
"""
:object:PurplePygenPass:ability:exit_connect_op
(nd: ast.ConnectOp) {
    "Edge" |> <self>.add_element_import;
    |> <self>.add_edge_directions;

    if nd.conn_type {
        (nd, f"{nd.conn_type.meta['py_code']}.{C.WITH_DIR}({C.EDGE_DIR}.{nd.edge_dir.name}") |> <self>.emit;
    } else {
        (nd, f"{C.EDGE_CLASS}().{C.WITH_DIR}({C.EDGE_DIR}.{nd.edge_dir.name}") |> <self>.emit;
    }
    if nd.conn_assign {
        (nd, f", {nd.conn_assign.meta['py_code']})") |> <self>.emit;
    } else {
        (nd, ")") |> <self>.emit;
    }
}

"""Sub objects.

conn_type: Optional[ExprType],
conn_assign: Optional[AssignmentList],
edge_dir: EdgeDir,
"""
:object:PurplePygenPass:ability:exit_disconnect_op
(nd: ast.DisconnectOp) {

}