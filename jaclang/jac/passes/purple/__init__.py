"""Collection of purple passes for Jac IR."""
from jaclang import jac_blue_import
from jaclang.jac.passes.blue import pass_schedule


purple = jac_blue_import("purple_pygen_pass")
analyze = jac_blue_import("analyze_pass")
AnalyzePass = analyze.AnalyzePass  # type: ignore
PurplePygenPass = purple.PurplePygenPass  # type: ignore


pass_schedule = [
    *pass_schedule[:-1],
    AnalyzePass,
    PurplePygenPass,
]

__all__ = [
    "pass_schedule",
    "AnalyzePass",
    "PurplePygenPass",
]
