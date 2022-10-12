from jaseci.jac.ir.passes.prune_pass import PrunePass
from jaseci.jac.ir.passes.printer_pass import PrinterPass
from jaseci.jac.ir.passes.stats_pass import StatsPass
from jaseci.jac.ir.ast_builder import JacAstBuilder


def multi_pass_optimizer(jac_ast: JacAstBuilder, debug_out: bool = True, print_walk: bool = True):
    if debug_out:
        if print_walk:
            PrinterPass(jac_ast).run()
        StatsPass(jac_ast).run()
    PrunePass(jac_ast).run()
    if debug_out:
        StatsPass(jac_ast).run()
