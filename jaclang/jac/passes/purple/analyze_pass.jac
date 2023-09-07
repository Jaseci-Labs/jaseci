 """Type Analyze Pass."""
import:py jaclang.jac.absyntree as ast;

import:py jaclang.jac.passes, Pass;

object AnalyzePass:Pass{
    can exit_arch_block(node:ast.ArchBlock){
        if (
            isinstance(node.parent, ast.Architype)
            and node.parent.arch_type.name == Tok.KW_WALKER
        ){
            for i in <self>.get_all_sub_nodes(node, ast.VisitStmt, brute_force=True){
                i.from_walker = True;
            }
            for i in <self>.get_all_sub_nodes(node, ast.DisengageStmt, brute_force=True){
                i.from_walker = True;
            }
            for i in <self>.get_all_sub_nodes(node, ast.EdgeOpRef, brute_force=True){
                i.from_walker = True;
            }
    }
}
}