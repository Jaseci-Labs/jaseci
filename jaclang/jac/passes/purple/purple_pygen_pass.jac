"""First Jac pass bootstrapped in Jac"""
import:py jaclang.jac.absyntree as ast;
import:py from jaclang.jac.passes.blue, BluePygenPass;
import:py from jaclang.core, Object, Node, Edge, Walker;
import:py from jaclang.jac.lexer, Tokens as Tok;
import:py from jaclang.jac.constant, Constants as C;

include:jac impl.purple_pygen_pass_impl;

object PurplePygenPass:BluePygenPass {

    """ Addd arch import to the preamble """
    can add_element_import(arch: str);
    """ Addd exec context import to the preamble """
    can add_exec_context();

    can exit_architype(nd: ast.Architype);
    can exit_ability(nd: ast.Ability);
    can exit_event_signature(nd: ast.EventSignature);
    can exit_ctrl_stmt(nd: ast.CtrlStmt);
    can exit_visit_stmt(nd: ast.VisitStmt);
    can exit_binary_expr(nd: ast.BinaryExpr);
    can exit_connect_op(nd: ast.ConnectOp);
}
