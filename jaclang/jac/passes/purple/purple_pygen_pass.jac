"""First Jac pass bootstrapped in Jac"""
import:py jaclang.jac.absyntree as ast;
import:py from jaclang.jac.passes.blue, BluePygenPass;
import:py from jaclang.core, Object, Node, Edge, Walker;


include:jac impl.purple_pygen_pass_impl;

"""
This pass leverages data spacial lib to provide code
gen for full Jac language. It is bootstrapped in Jac blue.
"""
object PurplePygenPass:BluePygenPass {

    #*
    These add functions generate necessary imports
    given code being generated.
    *#
    can add_element_import(arch: str);
    can add_exec_context;
    can add_edge_directions;
    can needs_jac_import;

    can exit_architype(nd: ast.Architype);
    can exit_ability(nd: ast.Ability);
    can exit_event_signature(nd: ast.EventSignature);
    can exit_ctrl_stmt(nd: ast.CtrlStmt);
    can exit_report_stmt(nd: ast.ReportStmt) {} # TODO: Implement
    can exit_ignore_stmt(nd: ast.IgnoreStmt);
    can exit_visit_stmt(nd: ast.VisitStmt);
    can exit_revisit_stmt(nd: ast.RevisitStmt) {} # TODO: Implement
    can exit_await_stmt(nd: ast.AwaitStmt) {} # TODO: Implement
    can exit_disengage_stmt(nd: ast.DisengageStmt);
    can exit_binary_expr(nd: ast.BinaryExpr); # TODO: Unfinished
    can exit_edge_op_ref(nd: ast.EdgeOpRef);
    can exit_connect_op(nd: ast.ConnectOp);
    can exit_disconnect_op(nd: ast.DisconnectOp);
}
