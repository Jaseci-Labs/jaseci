 """Type Analyze Pass."""
import:py jaclang.jac.absyntree as ast;

import:py from jaclang.jac.passes, Pass;

object AnalyzePass:Pass{
    can exit_arch_block(nd:ast.ArchBlock){
        if (
            isinstance(nd.parent, ast.Architype)
            and nd.parent.arch_type.name == Tok.KW_WALKER
        ){
            for i in <self>.get_all_sub_nodes(nd, ast.VisitStmt, brute_force=True){
                i.from_walker = True;
            }
            for i in <self>.get_all_sub_nodes(nd, ast.DisengageStmt, brute_force=True){
                i.from_walker = True;
            }
            for i in <self>.get_all_sub_nodes(nd, ast.EdgeOpRef, brute_force=True){
                i.from_walker = True;
            }
    }
}
}