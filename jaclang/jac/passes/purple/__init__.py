"""Collection of purple passes for Jac IR."""
from jaclang import jac_blue_import
from jaclang.jac.passes.main import pass_schedule
from jaclang.jac.passes.purple.purple_pyast_gen_pass import PurplePyastGenPass


purple = jac_blue_import("purple_pygen_pass")
analyze = jac_blue_import("analyze_pass")
AnalyzePass = analyze.AnalyzePass  # type: ignore
PurplePygenPass = purple.PurplePygenPass  # type: ignore


pass_schedule = [
    *pass_schedule[:-2],
    PurplePyastGenPass,
    PurplePygenPass,
]

__all__ = [
    "pass_schedule",
    "AnalyzePass",
    "PurplePygenPass",
]
