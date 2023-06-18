"""Import Pass written in Jac bootstrapped with Python strategy."""

import:py jaclang.jac.ast;
import:py from jaclang.jac.ast, AstNode;
import:py from jaclang.jac.passes.ir_pass, Pass;
import:py from


object ImportPass:Pass {
    has symbol_table: dict[str, any];

    can exit_import(node:AstNode) {
        return node.type == "Import";
    }
}