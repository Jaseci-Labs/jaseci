 """Type Analyze Pass."""
import:py jaclang.jac.absyntree as ast;

import:py from jaclang.jac.passes, Pass;
import:py from jaclang.jac.constant, Tokens as Tok;


object AnalyzePass:Pass{
    can enter_arch_block(nd:ast.ArchBlock);
}


:object:AnalyzePass:ability:enter_arch_block(nd:ast.ArchBlock) {
    if (
        isinstance(nd.parent, ast.Architype)
        and nd.parent.arch_type.name == Tok.KW_WALKER
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