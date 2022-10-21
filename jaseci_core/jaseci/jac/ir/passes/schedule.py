from jaseci.jac.ir.passes import (
    ParseTreePrunePass,
    PrinterPass,
    StatsPass,
    CodeGenPass,
    AstPrunePass,
)
from jaseci.jac.ir.ast import Ast


def multi_pass_optimizer(jac_ast: Ast, opt_level: int):
    ParseTreePrunePass(ir=jac_ast).run() if opt_level > 0 else None
    CodeGenPass(ir=jac_ast).run() if opt_level > 2 else None
    AstPrunePass(ir=jac_ast).run() if opt_level > 2 else None


def debug_pass(
    jac_ast: Ast,
    print_walk: bool = False,
    stats_out: bool = False,
):
    PrinterPass(jac_ast).run() if print_walk else None
    StatsPass(jac_ast).run() if stats_out else None
