from jaseci.jac.ir.passes.prune_pass import PrunePass
from jaseci.jac.ir.passes.printer_pass import PrinterPass
from jaseci.jac.ir.passes.stats_pass import StatsPass


def multi_pass_optimizer(jac_ast, debug_out=False):
    if debug_out:
        PrinterPass(jac_ast).run()
        StatsPass(jac_ast).run()
    PrunePass(jac_ast).run()
    if debug_out:
        StatsPass(jac_ast).run()
