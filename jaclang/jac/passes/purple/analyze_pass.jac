"""Code analysis pass.

This pass is used to analyze the code and add some extra information to the
AST. For example, it will mark all the walker relevent statement nodes that
are within a walker so the purple codegen can statically recognize here and
visitor.
"""
import:py jaclang.jac.absyntree as ast;

import:py from jaclang.jac.passes, Pass;
import:py from jaclang.jac.constant, Tokens as Tok;


object AnalyzePass:Pass: {
    can <init>(*args: list, **kwargs: dict) {
        <super>.<init>(*args, **kwargs);
    }
    can enter_architype(nd: ast.Architype);
}


:object:AnalyzePass:ability:enter_architype(nd:ast.Architype) {
    if (
        nd.arch_type.name == Tok.KW_WALKER
    ) {
        for i in <self>.get_all_sub_nodes(nd, ast.VisitStmt, brute_force=False){
            i.from_walker = True;
        }
        for i in <self>.get_all_sub_nodes(nd, ast.IgnoreStmt, brute_force=False){
            i.from_walker = True;
        }
        for i in <self>.get_all_sub_nodes(nd, ast.DisengageStmt, brute_force=False){
            i.from_walker = True;
        }
        for i in <self>.get_all_sub_nodes(nd, ast.EdgeOpRef, brute_force=False){
            i.from_walker = True;
        }
    }
}